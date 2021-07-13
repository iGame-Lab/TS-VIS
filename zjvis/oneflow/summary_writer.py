from typing import Union, Optional, Dict, List
import numpy as np
from .writer import EventFileWriter
from .summary import scalar, image, audio, video, text, histogram, hparams, exception, embedding, embedding_sample
numpy_compatible = np.ndarray
try:
    import torch
    numpy_compatible = torch.Tensor
except ImportError:
    pass

class SummaryWriter(object):
    def __init__(self, log_dir='logs/'):
        self.log_dir = log_dir
        self.event_file_writer = EventFileWriter(log_dir)
        self._file_writer = {'event':self.event_file_writer}

    def get_writer(self,
                   name: str):
        if name not in self._file_writer:
            self._file_writer[name] = EventFileWriter(self.log_dir, name = name)

        return self._file_writer[name]

    def add_scalar(self,
                   tag: str,
                   scalar_value: Union[float, numpy_compatible],
                   step: Optional[int] = None):

        self.event_file_writer.add_summary(summary= scalar(tag, scalar_value),
                                           global_step=step)

    def add_scalars(self,
                    main_tag: str,
                    tag_scalar_dict: Dict[str, float],
                    step: Optional[int] = None):
        pass


    def add_image(self,
                  tag: str,
                  tensor: numpy_compatible,
                  step: Optional[int] = None):

        self.event_file_writer.add_summary(image(tag, tensor), global_step=step)

    def add_figure(self, tag, figure, step=None, close=True):
        pass

    def add_video(self,
                  tag: str,
                  video_tensor: numpy_compatible,
                  step: Optional[int] = None,
                  fps: Optional[Union[int, float]] = 4):

        self.event_file_writer.add_summary(video(tag, video_tensor, fps), global_step=step)

    def add_audio(self,
                  tag: str,
                  audio_tensor: numpy_compatible,
                  step: Optional[int],
                  sample_rate: Optional[int] = 44100):

        self.event_file_writer.add_summary(audio(tag, audio_tensor, sample_rate), global_step=step)

    def add_text(self,
                 tag: str,
                 text_string: str,
                 step: Optional[int] = None):

        self.event_file_writer.add_summary(text(tag, text_string), global_step=step)

    def add_histogram(self,
                      tag: str,
                      tensor: numpy_compatible,
                      step: Optional[int] = None,
                      max_bins: Optional[int] = None):

        self.event_file_writer.add_summary(histogram(tag, tensor, max_bins), global_step=step)

    def add_onnx_graph(self,
                       onnx_model_file):

        from .onnx_graph import load_onnx_graph
        self.event_file_writer.add_onnx_graph(load_onnx_graph(onnx_model_file))

    def add_graph(self,
                  model,
                  input_to_model=None,
                  model_type='pytorch',
                  verbose=False):

        if model_type == 'tensorflow':
            graph_def = model.as_graph_def(add_shapes=True)
            self.event_file_writer.add_graph(graph_def)

        elif model_type == 'pytorch':
            from .pytorch_graph import graph
            self.event_file_writer.add_graph(graph(model, input_to_model, verbose))
        else:
            raise Exception('Cannot parse current graph !')

    def add_exception(self,
                      tag: str,
                      tensor: numpy_compatible,
                      step: Optional[int] = None):

        self.get_writer('projector').add_summary(summary=exception(tag, tensor),
                                                 global_step=step)

    def add_embedding_sample(self,
                            tag: str,
                            tensor: numpy_compatible,
                            sample_type: str):

        self.get_writer('projector').add_summary(summary=embedding_sample(name = tag,
                                                                          tensor = tensor,
                                                                          sample_type =sample_type))

    def add_embedding(self,
                      tag: str,
                      tensor: numpy_compatible,
                      label: Optional[numpy_compatible] =None,
                      step: Optional[int] = None):

        self.get_writer('projector').add_summary(summary=embedding(tag, tensor, label=label),
                                                 global_step=step)

    def add_hparams(self,
                    hparam_dict: Dict[str, Union[bool, str, float, int]],
                    metric_dict: Optional[Dict[str, float]] =None,
                    tag: Optional[str] = None):

        self.get_writer('hparams').add_summary(summary=hparams(hparam_dict, metric_dict, tag))
        self.get_writer('hparams').close()

    def close(self):
        for writer in self._file_writer.values():
            writer.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()