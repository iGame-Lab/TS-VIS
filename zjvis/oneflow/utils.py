import io
import numpy as np
from PIL import Image
import os
import logging

def make_image(tensor):
    # Do not assume that user passes in values in [0, 255], use data type to detect
    if tensor.dtype != np.uint8:
        tensor = (tensor * 255.0).astype(np.uint8)

    image = Image.fromarray(tensor.squeeze())

    output = io.BytesIO()
    image.save(output, format='PNG')
    image_string = output.getvalue()
    output.close()

    return image_string

def make_histogram(values, max_bins=None):
    """Convert values into a histogram proto using logic from histogram.cc."""
    # Create default bins for histograms, see generate_testdata.py in tensorflow/tensorboard
    v = 1E-12
    buckets = []
    neg_buckets = []
    while v < 1E20:
        buckets.append(v)
        neg_buckets.append(-v)
        v *= 1.1
    bins = neg_buckets[::-1] + [0] + buckets

    if values.size == 0:
        raise ValueError('The input has no element.')
    values = values.reshape(-1)
    counts, limits = np.histogram(values, bins=bins)
    num_bins = len(counts)
    if max_bins is not None and num_bins > max_bins:
        subsampling = num_bins // max_bins
        subsampling_remainder = num_bins % subsampling
        if subsampling_remainder != 0:
            counts = np.pad(counts, pad_width=[[0, subsampling - subsampling_remainder]],
                            mode="constant", constant_values=0)
        counts = counts.reshape(-1, subsampling).sum(axis=-1)
        new_limits = np.empty((counts.size + 1,), limits.dtype)
        new_limits[:-1] = limits[:-1:subsampling]
        new_limits[-1] = limits[-1]
        limits = new_limits

    # Find the first and the last bin defining the support of the histogram:
    cum_counts = np.cumsum(np.greater(counts, 0, dtype=np.int32))
    start, end = np.searchsorted(cum_counts, [0, cum_counts[-1] - 1], side="right")
    start = int(start)
    end = int(end) + 1
    del cum_counts

    # TensorBoard only includes the right bin limits. To still have the leftmost limit
    # included, we include an empty bin left.
    # If start == 0, we need to add an empty one left, otherwise we can just include the bin left to the
    # first nonzero-count bin:
    counts = counts[start - 1:end] if start > 0 else np.concatenate([[0], counts[:end]])
    limits = limits[start:end + 1]

    if counts.size == 0 or limits.size == 0:
        raise ValueError('The histogram is empty, please file a bug report.')

    sum_sq = values.dot(values)
    return sum_sq, limits.tolist(), counts.tolist()

def _prepare_video(V):
    import numpy as np
    b, t, c, h, w = V.shape

    if V.dtype == np.uint8:
        V = np.float32(V) / 255.

    def is_power2(num):
        return num != 0 and ((num & (num - 1)) == 0)

    # pad to nearest power of 2, all at once
    if not is_power2(V.shape[0]):
        len_addition = int(2**V.shape[0].bit_length() - V.shape[0])
        V = np.concatenate(
            (V, np.zeros(shape=(len_addition, t, c, h, w))), axis=0)

    n_rows = 2**((b.bit_length() - 1) // 2)
    n_cols = V.shape[0] // n_rows

    V = np.reshape(V, newshape=(n_rows, n_cols, t, c, h, w))
    V = np.transpose(V, axes=(2, 0, 4, 1, 5, 3))
    V = np.reshape(V, newshape=(t, n_rows * h, n_cols * w, c))

    return V

def make_video(tensor, fps):
    try:
        import moviepy  # noqa: F401
    except ImportError:
        print('add_video needs package moviepy')
        return
    try:
        from moviepy import editor as mpy
    except ImportError:
        print("moviepy is installed, but can't import moviepy.editor.",
              "Some packages could be missing [imageio, requests]")
        return
    import tempfile

    t, h, w, c = tensor.shape

    # encode sequence of images into gif string
    clip = mpy.ImageSequenceClip(list(tensor), fps=fps)

    filename = tempfile.NamedTemporaryFile(suffix='.gif', delete=False).name

    # moviepy >= 1.0.0 use logger=None to suppress output.
    try:
        clip.write_gif(filename, verbose=False, logger=None)
    except TypeError:
        logging.warning('Upgrade to moviepy >= 1.0.0 to supress the progress bar.')
        clip.write_gif(filename, verbose=False)

    with open(filename, 'rb') as f:
        tensor_string = f.read()

    try:
        os.remove(filename)
    except OSError:
        logging.warning('The temporary file used by moviepy cannot be deleted.')

    return [h,w,c], tensor_string
