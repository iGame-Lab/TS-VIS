# -*- coding: UTF-8 -*-
# MIT License
#
# Copyright (c) 2019 Vadim Velicodnii
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from collections import namedtuple
from collections.abc import Iterable
from typing import Union, Optional
import numpy as np
import struct
from io import BytesIO
# Compatible tensorboard calculation graph
from tensorboard.compat.proto.graph_pb2 import GraphDef
from oneflow.customized.utils import HParamsPluginData
# from tensorboard.plugins.hparams.plugin_data_pb2 import HParamsPluginData
from tbparser.events_reader import EventReadingError, EventsFileReader

SummaryItem = namedtuple(
    'SummaryItem', ['tag', 'step', 'wall_time', 'value', 'type']
)
GraphItem = namedtuple(
    'GraphItem', ['wall_time', 'value', 'type']
)

# tensor data type
_data_type = {1: 'float',
              2: 'double',
              3: 'int32',
              # DT_UINT8 = 4;
              # DT_INT16 = 5;
              # DT_INT8 = 6;
              # DT_STRING = 7;
              # DT_COMPLEX64 = 8;  // Single-precision complex
              9: 'int64',
              10: 'bool',
              # DT_QINT8 = 11;     // Quantized int8
              # DT_QUINT8 = 12;    // Quantized uint8
              # DT_QINT32 = 13;    // Quantized int32
              # DT_BFLOAT16 = 14;  // Float32 truncated to 16 bits.  Only for cast ops.
              # DT_QINT16 = 15;    // Quantized int16
              # DT_QUINT16 = 16;   // Quantized uint16
              17: 'uint16',
              # DT_COMPLEX128 = 18;  // Double-precision complex
              # DT_HALF = 19;
              # DT_RESOURCE = 20;
              # DT_VARIANT = 21;  // Arbitrary C++ data types
              22: 'uint32',
              23: 'uint64'}


def _decode_byte(tensor):
    # 若tensor是float类型
    if tensor.dtype == 1:
        return struct.unpack('f', tensor.tensor_content)[0]


class SummaryReader(Iterable):
    """
    Iterates over events in all the files in the current logdir.
    """

    def _get_scalar(self, value):
        """
        Decode an scalar event
        :param value: A value field of an event
        :return: Decoded scalar
        """
        if value.HasField('simple_value'):
            return value.simple_value
        elif value.HasField('metadata'):
            if value.metadata.plugin_data.plugin_name == 'scalars':
                tensor = value.tensor
                return _decode_byte(tensor)
        return None

    def _get_image(self, value) -> Optional[dict]:
        """
        Decode an image event
        :param value: A value field of an event
        :return: Decoded image
        """
        if value.HasField('image'):
            dic = {
                'width': value.image.width,
                'height': value.image.height,
                'colorspace': value.image.colorspace,
                'encoded_image_string': value.image.encoded_image_string
            }
            return dic
        return None

    def _get_text(self, value) -> Optional[np.ndarray]:
        """
            Return text data
            :param value: A value field of an event
            :return: text data
            TODO: Tensorflow API
        """
        if value.HasField('metadata'):
            if value.metadata.plugin_data.plugin_name == 'text':
                return np.array([v.decode() for v in value.tensor.string_val])
        return None

    def _get_audio(self, value):
        if value.HasField('audio'):
            dic = {
                'sample_rate': value.audio.sample_rate,
                'num_channels': value.audio.num_channels,
                'length_frames': value.audio.length_frames,
                'encoded_audio_string': value.audio.encoded_audio_string
            }
            return dic
        # if Tensorboard API, use tensor decoder
        elif value.HasField('metadata'):
            if value.metadata.plugin_data.plugin_name == 'audio':
                dic = {
                    'tensor_shape': tuple([i.size for i in value.tensor.tensor_shape.dim]),
                    'string_val': [v for v in value.tensor.string_val]
                }
                if value.tag not in self.audio_exit_tag:
                    # record the tag
                    self.audio_exit_tag.append(value.tag)
                return dic
        elif value.tag in self.audio_exit_tag:
            dic = {
                'tensor_shape': tuple([i.size for i in value.tensor.tensor_shape.dim]),
                'string_val': [v for v in value.tensor.string_val]
            }
            return dic
        return None

    def _get_hist(self, value):
        if value.HasField('histo'):
            dic = {
                'min': value.histo.min,
                'max': value.histo.max,
                'num': value.histo.num,
                'sum': value.histo.sum,
                'sum_squares': value.histo.sum_squares,
                'bucket_limit': np.array(value.histo.bucket_limit),
                'bucket': np.array(value.histo.bucket),
            }
            return dic
        # if Tensorboard API, use tensor decoder
        elif value.HasField('metadata'):
            if value.metadata.plugin_data.plugin_name == 'histograms':
                tensor = value.tensor
                dtype = _data_type[tensor.dtype]
                tensor_shape = tuple([i.size for i in tensor.tensor_shape.dim])
                tensor_content = tensor.tensor_content
                tensor_content = np.frombuffer(tensor_content, dtype=dtype)
                if value.tag not in self.hist_exit_tag:
                    # record the tag
                    self.hist_exit_tag.append(value.tag)
                return tensor_content.reshape(tensor_shape)
        elif value.tag in self.hist_exit_tag:
            tensor = value.tensor
            dtype = _data_type[tensor.dtype]
            tensor_shape = tuple([i.size for i in tensor.tensor_shape.dim])
            tensor_content = tensor.tensor_content
            tensor_content = np.frombuffer(tensor_content, dtype=dtype)
            return tensor_content.reshape(tensor_shape)
        return None

    def _get_hparams(self, value):
        if value.HasField('metadata'):
            if value.metadata.plugin_data.plugin_name == 'hparams':
                metadata = value.metadata
                plugin_data = HParamsPluginData()
                plugin_data.ParseFromString(metadata.plugin_data.content)
                return plugin_data

    _DECODERS = {
        'scalar': _get_scalar,
        'image': _get_image,
        'text': _get_text,
        'audio': _get_audio,
        'hist': _get_hist,
        'hparams': _get_hparams,
    }

    def __init__(
            self,
            fileblock: BytesIO,
            tag_filter: Optional[Iterable] = None,
            types: Iterable = ('scalar',),
            stop_on_error: bool = False
    ):
        """
        Initalize new summary reader
        :param fileblock: Event file block of Tensorboard
        :param tag_filter: A list of tags to leave (`None` for all)
        :param types: A list of types to get.
        :param stop_on_error: Whether stop on a broken file
        """
        self._fileblock = fileblock

        self._tag_filter = set(tag_filter) if tag_filter is not None else None
        self._types = set(types)
        self._check_type_names()
        self._stop_on_error = stop_on_error
        # Record the tag, that has been read by the parser.
        # If the tag, in this list appears next,
        # the type is automatically identified.
        self.scalar_exit_tag = []
        self.image_exit_tag = []
        self.text_exit_tag = []
        self.audio_exit_tag = []
        self.hist_exit_tag = []

    def _check_type_names(self):
        if self._types is None:
            return
        if not all(
                type_name in self._DECODERS.keys() or type_name == "graph" for type_name in self._types
        ):
            raise ValueError('Invalid type name')

    # def _decode_events(self, events: Iterable) -> Optional[Union[SummaryItem, GraphDef]]:
    def _decode_events(self, events: Iterable) \
            -> Optional[Union[SummaryItem]]:
        """
        Convert events to `SummaryItem` instances
        :param events: An iterable with events objects
        :return: A generator with decoded events
            or `None`s if an event can't be decoded
        """
        for event in events:
            #     yield None
            step = event.step
            wall_time = event.wall_time
            if event.HasField('summary'):
                for value in event.summary.value:
                    tag = value.tag
                    # if value.HasField('metadata'):
                    #     continue
                    for value_type in self._types:
                        if value_type == "graph":
                            continue
                        decoder = self._DECODERS[value_type]
                        data = decoder(self, value)
                        if data is not None:
                            yield SummaryItem(
                                tag=tag,
                                step=step,
                                wall_time=wall_time,
                                value=data,
                                type=value_type
                            )
                    else:
                        yield None
            elif event.HasField('graph_def'):
                graph = GraphDef()
                graph.ParseFromString(event.graph_def)
                yield GraphItem(
                    wall_time=wall_time,
                    value=graph,
                    type='graph'
                )

    def _check_tag(self, tag: str) -> bool:
        """
        Check if a tag matches the current tag filter
        :param tag: A string with tag
        :return: A boolean value.
        """
        return self._tag_filter is None or tag in self._tag_filter

    def __iter__(self) -> SummaryItem:
        """
        Iterate over events in all the files in the current logdir
        :return: A generator with `SummaryItem` objects
        """
        reader = EventsFileReader(self._fileblock)
        try:
            yield from (
                item for item in self._decode_events(reader)
                if item is not None and all([
                    self._check_tag(None if type(item) == GraphItem else item.tag),
                    item.type in self._types
                ])
            )
        except EventReadingError:
            if self._stop_on_error:
                raise
            else:
                yield
