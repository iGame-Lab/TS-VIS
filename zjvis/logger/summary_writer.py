import os
import numpy as np
from typing import Union, Optional, Dict, List
from .writer import EventFileWriter
from .summary import scalar, image, audio, text, histogram, hparams, exception, embedding, embedding_sample
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
        self._max_queue = max_queue
        self._flush_secs = flush_secs
        self._filename_suffix = filename_suffix
        self.event_file_writer = EventFileWriter(log_dir, max_queue, flush_secs, filename_suffix=filename_suffix)
        self._file_writer = {'event':self.event_file_writer}

    def get_writer(self,
                   name: str) -> EventFileWriter:
        """
            返回指定名称的event文件写入器,若不存在，则新建一个文件写入器并返回
        Args:
            name: 字符串，event文件写入器的名称
        Returns:
            返回name对应的event文件写入器
        """
        if name not in self._file_writer:
            self._file_writer[name] = EventFileWriter(self.log_dir, name = name,
                                                      max_queue_size=self._max_queue,
                                                      flush_secs=self._flush_secs,
                                                      filename_suffix=self._filename_suffix)

        return self._file_writer[name]

    def add_scalar(self,
                   tag: str,
                   scalar_value: Union[float, numpy_compatible],
                   step: Optional[int] = None):
        """
            添加标量数据到日志
        Args:
            tag: 字符串，数据标识
            scalar_value: 浮点数，标量的值
            step: 整数，可选参数，记录数据的step
        """
        self.event_file_writer.add_summary(summary= scalar(tag, scalar_value),
                                           global_step=step)

    def add_scalars(self,
                    tag_scalar_dict: Dict[str, Union[float, numpy_compatible]],
                    step: Optional[int] = None):
        """
            添加一组标量数据到日志
        Args:
            tag_scalar_dict: 字典，(标签, 标量值)
            step: 整数，可选参数，记录数据的step
        """
        for tag, val in tag_scalar_dict.items():
            self.event_file_writer.add_summary(summary=scalar(tag, val),
                                               global_step=step)

    def add_image(self,
                  tag: str,
                  tensor: numpy_compatible,
                  step: Optional[int] = None):
        """
            添加图像数据到日志
        Args:
            tag: 字符串，图像的标识
            tensor: 数组，图像数据，'uint8' 或 'float' 类型的数据，大小为(H,W) 或 (H,W,C), 其中C为1,2,3,4
            step: 整数，可选参数，记录数据的step
        """

        self.event_file_writer.add_summary(image(tag, tensor), global_step=step)

    def add_images(self,
                   tag: str,
                   tensors: numpy_compatible,
                   step: Optional[int] = None):
        """
            添加多个图像数据到日志
        Args:
            tag: 字符串，图像的标识, tag_1, tag_2, ... , tag_k
            tensors: 数组，图像数据，'uint8' 或 'float' 类型的数据，大小为(K,H,W) 或 (K,H,W,C), 其中C为1,3,4
            step: 整数，可选参数，记录数据的step
        """
        assert tensors.ndim in [3,4], 'the shape of image tensors must be (K,H,W) or (K,H,W,C)'
        for i, tensor in enumerate(tensors):
            self.event_file_writer.add_summary(image(f'{tag}_{i}', tensor), global_step=step)

    def add_audio(self,
                  tag: str,
                  audio_tensor: numpy_compatible,
                  step: Optional[int],
                  sample_rate: Optional[int] = 44100):
        """
            添加音频数据到日志
        Args:
            tag: 字符串，音频的标识
            audio_tensor: 数组，音频数据，大小为(L, C), 其中L为音频帧的长度，C为通道，通常C=1，2
            step: 整数，可选参数，记录数据的step
            sample_rate: 整数，采样率 Hz
        """
        self.event_file_writer.add_summary(audio(tag, audio_tensor, sample_rate), global_step=step)

    def add_text(self,
                 tag: str,
                 text_string: str,
                 step: Optional[int] = None):
        """
            添加文本数据到日志
        Args:
            tag: 字符串，文本的标识
            text_string: 字符串，文本字符串
            step: 整数，可选参数，记录数据的step
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
            tag: 字符串，直方图的标识
            tensor: 数组，直方图数据
            step: 整数，可选参数，记录数据的step
            max_bins: 整数，可选参数，直方图划分的区间个数
        """
        self.event_file_writer.add_summary(histogram(tag, tensor, max_bins), global_step=step)

    def add_onnx_graph(self,
                       onnx_model_file: str):
        """
            添加onnx模型到日志
        Args:
            onnx_model_file: onnx模型对应的文件
        """
        from .onnx_graph import load_onnx_graph
        self.event_file_writer.add_onnx_graph(load_onnx_graph(onnx_model_file))

    def add_graph(self,
                  model,
                  input_to_model: Union[tuple]=None,
                  model_type: str ='pytorch',
                  verbose: bool =False):
        """
            添加神经网络的图结构到日志，支持tensorflow，pytorch
        Args:
            model: 神经网络模型, torch.nn.Module 或 tf.Session().graph
            input_to_model: 元组， 一组用于模型测试的输入
            model_type: 字符串，模型的类型，‘pytorch’ 或 'tensorflow'
            verbose: 布尔值，pytorch模型是否输出到控制台
        """
        if model_type == 'tensorflow':
            graph_def = model.as_graph_def(add_shapes=True)
            self.event_file_writer.add_graph(graph_def)

        elif model_type == 'pytorch':
            assert (input_to_model is not None), 'Need to feed an input to model'
            from .pytorch_graph import graph
            self.event_file_writer.add_graph(graph(model, input_to_model, verbose))
        else:
            raise Exception('Cannot parse current graph !')

    def add_json_graph(self,
                       model_str: str,
                       name: str = 'model'):
        """
            该功能需要神经网络框架的支持，首先使用内部函数对网络模型的结构进行序列化，然后将序列化的字符串写入到json文件
        Args:
            model_str: 字符串，模型的序列化字符串
            name: 字符串，json文件名
        """
        file = os.path.join(self.log_dir, f'{name}.json')
        with open(file, 'w') as f:
            f.write(str(model_str))

    def add_exception(self,
                      tag: str,
                      tensor: numpy_compatible,
                      step: Optional[int] = None):
        """
            添加监测的异常数据到日志
        Args:
            tag: 字符串，待监测的异常数据的标识
            tensor: 数组，待监测的异常数据
            step: 整数，可选参数，记录数据的step
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
            tag: 字符串，高维数据样本的标识，应与高维数据保持一致
            tensor: 数组，高维数据的样本，数据类型，大小为[N,*]
            sample_type: 字符串，样本数据的类型，支持‘image’,'text','audio'
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
            tag: 字符串，降维处理的高维数据的标识，应与高维数据的样本标识相同
            tensor: 数组，高维数据的样本，数据类型，大小为[N,*]
            label: 数组，可选参数，高维数据对应的类别标签，大小为[N]
            step: 整数，可选参数，记录数据的step
        """
        self.get_writer('projector').add_summary(summary=embedding(tag, tensor, label=label),
                                                 global_step=step)

    def add_hparams(self,
                    hparam_dict: Dict[str, Union[bool, str, float, int]],
                    metrics: Optional[Union[list, tuple]] =None,
                    tag: Optional[str] = None):
        """
            添加一组数据到日志
        Args:
            hparam_dict: 字典，模型的超参数
            metrics: 列表、元组，可选参数， 需要记录的度量指标，该指标必须在scalar中已定义
            tag: 字符串，该组超参数的标识
        """
        self.get_writer('hparams').add_summary(summary=hparams(hparam_dict, metrics, tag))

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