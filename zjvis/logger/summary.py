import io
import time
import numpy as np
from six import string_types
from .x2num import make_np
from zjvis.proto import projector_pb2
from zjvis.proto.projector_pb2 import Projector
from zjvis.proto.summary_pb2 import Summary, SummaryMetadata, HistogramProto
from zjvis.proto.tensor_pb2 import TensorProto, TensorShapeProto
from zjvis.proto.plugin_hparams_pb2 import HParamsPluginData, SessionStartInfo
from .utils import make_image,make_histogram

def scalar(name, scalar_value):
    """ 转换标量数据到potobuf格式 """
    scalar = make_np(scalar_value)
    assert (scalar.squeeze().ndim == 0), 'scalar should be 0D'
    scalar = float(scalar)
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='scalars'))
    return Summary(value=[Summary.Value(tag=name,
                                        simple_value=scalar,
                                        metadata=metadata)])

def image(name, tensor):
    """ 转换图像数据到potobuf格式 """
    tensor = make_np(tensor)
    ndim = tensor.ndim

    if ndim == 2:
        tensor = np.expand_dims(tensor, -1)
    elif ndim == 3:
        if tensor.shape[2]>4:
            raise Exception(f'the expected image type is (LA), (RGB), (RGBA), and the third dimension is less than 4, '
                            f'but get shape {tensor.shape}')
    else:
        raise Exception(f'the shape of image must be (H,W) or (H,W,C), but get shape {tensor.shape}' )

    height, width, channel = tensor.shape
    image_str = make_image(tensor)

    image = Summary.Image(height=height,
                          width=width,
                          colorspace=channel,
                          encoded_image_string=image_str)

    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='images'))
    return Summary(value=[Summary.Value(tag=name,
                                        image=image,
                                        metadata=metadata)])

def text(name, text_string):
    """ 转换文本数据到potobuf格式 """
    tensor = TensorProto(string_val=[text_string.encode(encoding='utf_8')])
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='text'))
    return Summary(value=[Summary.Value(tag=name,
                                        tensor=tensor,
                                        metadata=metadata)])

def histogram(name, tensor, max_bins):
    """ 转换直方图数据到potobuf格式 """
    values = make_np(tensor)
    sum_sq, bucket_limit, bucket = make_histogram(values.astype(float), max_bins)
    hist = HistogramProto(min=values.min(), max=values.max(), num=len(values.reshape(-1)),
                          sum=values.sum(), sum_squares=sum_sq, bucket_limit=bucket_limit, bucket=bucket)

    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='histograms'))
    return Summary(value=[Summary.Value(tag=name,
                                        histo=hist,
                                        metadata=metadata)])

def audio(name, audio_data, sample_rate):
    """ 转换音频数据到potobuf格式 """
    import soundfile
    tensor = make_np(audio_data)
    if abs(tensor).max() > 1:
        print('warning: audio amplitude out of range, auto clipped.')
        tensor = tensor.clip(-1, 1)
    if tensor.ndim == 1:  # old API, which expects single channel audio
        tensor = np.expand_dims(tensor, axis=1)

    assert (tensor.ndim == 2), 'Input tensor should be 2 dimensional.'
    length_frames, num_channels = tensor.shape
    assert num_channels == 1 or num_channels == 2, 'The second dimension should be 1 or 2.'

    with io.BytesIO() as fio:
        soundfile.write(fio, tensor, samplerate=sample_rate, format='wav')
        audio_string = fio.getvalue()

    audio = Summary.Audio(sample_rate=sample_rate,
                          num_channels=num_channels,
                          length_frames=length_frames,
                          encoded_audio_string=audio_string,
                          content_type='audio/wav')
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='audios'))
    return Summary(value=[Summary.Value(tag=name,
                                        audio=audio,
                                        metadata=metadata)])

def set_hparams(k, v):
    if v is None:
        return

    if isinstance(v, string_types):
        k.string_value = v
    elif isinstance(v, bool):
        k.bool_value = v
    elif isinstance(v, int) or isinstance(v, float):
        v = make_np(v)[0]
        k.number_value = v
    else:
        k.string_value = getattr(v, '__name__', str(v))

def hparams(hparam_dict=None, metrics=None, tag=None):
    """ 转换超参数数据到potobuf格式 """
    tag = str(time.time()) if tag is None else tag
    ssi = SessionStartInfo(group_name=tag)
    if not (hparam_dict or metrics):
        raise Exception('hparam_dict or metric_dict must be specified.')

    if hparam_dict:
        for k, v in hparam_dict.items():
            set_hparams(ssi.hparams[k], v)
    if metrics:
        for k in metrics:
            set_hparams(ssi.metrics[k], False)

    content = HParamsPluginData(session_start_info=ssi, version=0)
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='hparams',
                                                                      content=content.SerializeToString()))
    return Summary(value=[Summary.Value(tag='_hparams_/session_start_info',
                                        metadata=metadata)])


def make_tensor(tensor):
    """ 转换numpy数组到potobuf格式 """
    shape = projector_pb2.Tensor.TensorShape(dim=[projector_pb2.Tensor.TensorShape.Dim(size=d)
                                                  for d in tensor.shape])

    return projector_pb2.Tensor(dtype=str(tensor.dtype),
                                tensor_shape=shape,
                                tensor_content=tensor.tobytes())

def embedding_sample(name, tensor, sample_type):
    """ 转换高维数据的样本到potobuf格式 """
    tensor = make_np(tensor)

    Sample = Projector.Embedding.Sample
    types = {
        'text': Sample.SampleType.TEXT,
        'audio': Sample.SampleType.AUDIO,
        'image': Sample.SampleType.IMAGE
    }
    if sample_type not in types:
        raise TypeError('the type of label_img must be one of text, audio, image')

    sample = Sample(type = types[sample_type], X = make_tensor(tensor))
    projector = Projector(embedding=Projector.Embedding(sample = sample))
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='embeddings'))
    return Summary(value=[Summary.Value(tag=name,
                                        projector=projector,
                                        metadata=metadata)])


def embedding(name, tensor, label):
    """ 转换高维数据到potobuf格式 """
    if label is not None:
        assert tensor.shape[0] == label.shape[0], 'the first dimension of tensor and label must be same.'
        assert label.ndim == 1 or (label.ndim == 2 and label.shape[1] == 1), 'label shape must be [N] or [N,1]'

    tensor = make_np(tensor)
    if label is not None:
        embedding = Projector.Embedding(value = make_tensor(tensor), label = make_tensor(label.squeeze()))
    else:
        embedding = Projector.Embedding(value=make_tensor(tensor))

    projector = Projector(embedding=embedding)

    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='embeddings'))
    return Summary(value=[Summary.Value(tag=name,
                                        projector=projector,
                                        metadata=metadata)])


def exception(name, tensor):
    """ 转换异常数据到potobuf格式 """
    tensor = make_np(tensor)
    projector = Projector(exception=Projector.Exception(value = make_tensor(tensor)))
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='exceptions'))
    return Summary(value=[Summary.Value(tag=name,
                                        projector=projector,
                                        metadata=metadata)])