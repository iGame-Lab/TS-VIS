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
    def __init__(self,
                 log_dir: str='logs/',
                 max_queue: int = 10,
                 flush_secs: int = 120,
                 filename_suffix:str = ''):
        """
            创建一个日志写入器，添加event
        Args:
            log_dir: 字符串，event文件写入的目录
            max_queue: 整数，文件每次flush前可追加event的队列大小，默认为10
            flush_secs: 整数，写入文件的时间间隔，默认为120s
            filename_suffix: 字符串，event文件的后缀
        """
        self.log_dir = log_dir
        self.event_file_writer = EventFileWriter(log_dir, max_queue, flush_secs, filename_suffix=filename_suffix)
        self._file_writer = {'event':self.event_file_writer}

    def get_writer(self,
                   name: str) -> EventFileWriter:
        """
            返回指定名称的event文件写入器,若不存在，则新建一个文件写入器并返回
        Args:
            name: event文件写入器的名称
        Returns:
            返回name对应的event文件写入器
        """
        if name not in self._file_writer:
            self._file_writer[name] = EventFileWriter(self.log_dir, name = name)

        return self._file_writer[name]

    def add_scalar(self,
                   tag: str,
                   scalar_value: Union[float, numpy_compatible],
                   step: Optional[int] = None):
        """
            添加标量数据到日志
        Args:
            tag: 数据标识
            scalar_value: 标量的值
            step: 可选参数，记录数据的step
        """
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
        """
            添加图像数据到日志
        Args:
            tag: 图像的标识
            tensor: 图像数据，'uint8' 或 'float' 类型的数据，大小为(H,W,C), 其中C为1,3,4
            step: 可选参数，记录数据的step
        """

        self.event_file_writer.add_summary(image(tag, tensor), global_step=step)

    def add_figure(self, tag, figure, step=None, close=True):
        pass

    def add_video(self,
                  tag: str,
                  video_tensor: numpy_compatible,
                  step: Optional[int] = None,
                  fps: Optional[Union[int, float]] = 4):
        """
            添加视频数据到日志
        Args:
            tag: 视频的标识
            video_tensor: 视频数据 ，数组类型
            step: 可选参数，记录数据的step
            fps: 可选参数，视频的帧率， 默认为4
        """
        self.event_file_writer.add_summary(video(tag, video_tensor, fps), global_step=step)

    def add_audio(self,
                  tag: str,
                  audio_tensor: numpy_compatible,
                  step: Optional[int],
                  sample_rate: Optional[int] = 44100):
        """
            添加音频数据到日志
        Args:
            tag: 音频的标识
            audio_tensor: 音频数据，数组类型，大小为(L, C), 其中L为音频帧的长度，C为通道，通常C=1，2
            step: 可选参数，记录数据的step
            sample_rate: 采样率 Hz
        """
        self.event_file_writer.add_summary(audio(tag, audio_tensor, sample_rate), global_step=step)

    def add_text(self,
                 tag: str,
                 text_string: str,
                 step: Optional[int] = None):
        """
            添加文本数据到日志
        Args:
            tag: 文本的标识
            text_string: 文本字符串
            step: 可选参数，记录数据的step
        """
        self.event_file_writer.add_summary(text(tag, text_string), global_step=step)

    def add_histogram(self,
                      tag: str,
                      tensor: numpy_compatible,
                      step: Optional[int] = None,
                      max_bins: Optional[int] = None):
        """
            添加直方图数据到日志
        Args:
            tag: 直方图的标识
            tensor: 直方图数据，数组类型
            step: 可选参数，记录数据的step
            max_bins: 可选参数，直方图划分的区间个数
        """
        self.event_file_writer.add_summary(histogram(tag, tensor, max_bins), global_step=step)

    def add_onnx_graph(self,
                       onnx_model_file):
        """
            添加onnx模型到日志
        Args:
            onnx_model_file: onnx模型对应的文件
        """
        from .onnx_graph import load_onnx_graph
        self.event_file_writer.add_onnx_graph(load_onnx_graph(onnx_model_file))

    def add_graph(self,
                  model,
                  input_to_model=None,
                  model_type='pytorch',
                  verbose=False):
        """
            添加神经网络的图结构到日志，支持tensorflow，pytorch
        Args:
            model: 神经网络模型, torch.nn.Module 或 tf.Session().graph
            input_to_model: 一个模型的测试输入
            model_type: 模型的类型，‘pytorch’ 或 'tensorflow'
            verbose: pytorch模型是否输出到控制台
        """
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
        """
            添加要监测的异常数据到日志
        Args:
            tag: 待监测的异常数据的标识
            tensor: 待监测的异常数据
            step: 可选参数，记录数据的step
        """

        self.get_writer('projector').add_summary(summary=exception(tag, tensor),
                                                 global_step=step)

    def add_embedding_sample(self,
                            tag: str,
                            tensor: numpy_compatible,
                            sample_type: str):
        """
            添加降维处理的高维数据对应的样本到日志，以便查看降维后数据点对应的原始样本
        Args:
            tag: 高维数据样本的标识，应与高维数据保持一致
            tensor: 高维数据的样本，数据类型，大小为[N,*]
            sample_type: 样本数据的类型，支持‘image’,'text','audio'
        """
        self.get_writer('projector').add_summary(summary=embedding_sample(name = tag,
                                                                          tensor = tensor,
                                                                          sample_type =sample_type))

    def add_embedding(self,
                      tag: str,
                      tensor: numpy_compatible,
                      label: Optional[numpy_compatible] =None,
                      step: Optional[int] = None):
        """
            添加降维处理的高维数据到日志
        Args:
            tag: 降维处理的高维数据的标识，应与高维数据的样本标识相同
            tensor: 高维数据的样本，数据类型，大小为[N,*]
            label: 可选参数，高维数据对应的类别标签，大小为[N]
            step: 可选参数，记录数据的step
        """
        self.get_writer('projector').add_summary(summary=embedding(tag, tensor, label=label),
                                                 global_step=step)

    def add_hparams(self,
                    hparam_dict: Dict[str, Union[bool, str, float, int]],
                    metric_dict: Optional[Dict[str, float]] =None,
                    tag: Optional[str] = None):
        """
            添加一组数据到日志
        Args:
            hparam_dict: 模型的超参数
            metric_dict: 可选参数， 模型的度量数据
            tag: 该组超参数的标识
        """
        self.get_writer('hparams').add_summary(summary=hparams(hparam_dict, metric_dict, tag))
        self.get_writer('hparams').close()

    def close(self):
        """
            关闭所有event文件写入器
        """
        for writer in self._file_writer.values():
            writer.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()