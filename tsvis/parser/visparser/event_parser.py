# -*- coding: UTF-8 -*-
"""
 Copyright 2021 Tianshu AI Platform. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 =============================================================
"""
import struct
import numpy as np
import json
from tsvis.proto.plugin_hparams_pb2 import HParamsPluginData
from tsvis.proto.graph_pb2 import GraphDef

def get_parser(value, step, wall_time):
    """
    :param event:
    :return:
        dict = {tag, step, wall_time, value, type}
    """
    data = dict(step=step, wall_time=wall_time)
    if value.HasField('simple_value'):
        value = _get_scalar(value)

    elif value.HasField('image'):
        value = _get_image(value)

    elif value.HasField('audio'):
        value = _get_audio(value)

    elif value.HasField('histo'):
        value = _get_hist(value)

    elif value.HasField('projector'):
        value = _get_projector(value)

    elif value.HasField('metadata'):
        if value.metadata.plugin_data.plugin_name == 'hparams':
            value = _get_hparams(value)
        elif value.metadata.plugin_data.plugin_name == 'text':
            value = _get_text(value)
        else:
            raise Exception(f'cannot parse {value.metadata.plugin_data.plugin_name} data.')

    else:
        raise Exception(f'cannot parse this data: {value}')

    data.update(value)
    return data

def _decode_byte(tensor):
    # 若tensor是float类型
    if tensor.dtype == 1:
        return struct.unpack('f', tensor.tensor_content)[0]

def _decoder_tensor(tensor):
    # tensor 为字节流
    tensor_shape = tuple([i.size for i in tensor.tensor_shape.dim])
    tensor_content = np.frombuffer(tensor.tensor_content, dtype=tensor.dtype)
    return tensor_content.reshape(tensor_shape)

def get_graph(event):
    graph = GraphDef()
    graph.ParseFromString(event.graph_def)
    return dict(wall_time=event.wall_time,
                value=graph,
                type='graph')

def _get_scalar(value):
    """
    Decode an scalar event
    :param value: A value field of an event
    :return: Decoded scalar
    """
    return dict(tag=value.tag,
                value=value.simple_value,
                type='scalar')

def _get_image(value):
    """
    Decode an image event
    :param value: A value field of an event
    :return: Decoded image
    """
    dic = {
        'width': value.image.width,
        'height': value.image.height,
        'colorspace': value.image.colorspace,
        'encoded_image_string': value.image.encoded_image_string
    }

    return dict(tag=value.tag,
                value=dic,
                type='image')

def _get_text(value):
    """
        Return text data
        :param value: A value field of an event
        :return: text data
    """
    return dict(tag=value.tag,
                value=np.array([v.decode() for v in value.tensor.string_val]),
                type='text')

def _get_audio(value):
    dic = {'sample_rate': value.audio.sample_rate,
           'num_channels': value.audio.num_channels,
           'length_frames': value.audio.length_frames,
           'encoded_audio_string': value.audio.encoded_audio_string}

    return dict(tag=value.tag,
                value=dic,
                type='audio')

def _get_hist(value):
    dic = { 'min': value.histo.min,
            'max': value.histo.max,
            'num': value.histo.num,
            'sum': value.histo.sum,
            'sum_squares': value.histo.sum_squares,
            'bucket_limit': np.array(value.histo.bucket_limit),
            'bucket': np.array(value.histo.bucket)}

    return dict(tag=value.tag,
                value=dic,
                type='hist')

def _get_hparams(value):
    metadata = value.metadata
    plugin_data = HParamsPluginData()
    plugin_data.ParseFromString(metadata.plugin_data.content)

    return dict(tag=value.tag,
                value=plugin_data,
                type='hparams')

def _get_embedding(value):
    projector = value.projector
    if projector.embedding.HasField('sample'):
        sample_type = {1:'audio', 2:'text', 3:'image'}
        sample = projector.embedding.sample
        data =dict(type = sample_type[sample.type],
                    X = _decoder_tensor(sample.X))
        return dict(tag = 'sample_' + value.tag,
                    value = data,
                    type = 'embedding'
                    )

    else:
        embedding = projector.embedding
        return dict(tag = value.tag,
                    value = _decoder_tensor(embedding.value),
                    label = _decoder_tensor(embedding.label) if embedding.HasField('label') else np.array([]),
                    type = 'embedding')

def _get_exception(value):

    return dict(tag=value.tag,
                value=_decoder_tensor(value.projector.exception.value),
                type='exception')

def _get_projector(value):
    projector = value.projector
    if projector.HasField('embedding'):
        return _get_embedding(value)
    else:
        return _get_exception(value)

def filter_graph(file):
    variable_names = {}
    graph = json.loads(file)
    for sub_graph in graph:
        cfg = sub_graph["config"]
        # 拷贝一份，用于循环
        cfg_copy = cfg["layers"].copy()
        for layer in cfg_copy:
            if layer["class_name"] == "variable":
                _name = layer["name"]
                variable_names[_name] = layer
                cfg["layers"].remove(layer)
    # 第二遍循环，删除`variable_names`出现在`inbound_nodes`中的名字
    for sub_graph in graph:
        cfg = sub_graph["config"]
        for layer in cfg["layers"]:
            in_nodes = layer["inbound_nodes"]
            in_nodes_copy = in_nodes.copy()
            for node in in_nodes_copy:
                # 在里面则删除
                if node in variable_names.keys():
                    in_nodes.remove(node)
    graph_str = json.dumps(graph)
    return graph_str
