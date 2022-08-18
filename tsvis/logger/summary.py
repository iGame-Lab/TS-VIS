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
import time
import numpy as np
import torch
import math
from six import string_types
from torch.nn import functional as F
from .x2num import make_np
from collections import defaultdict
from tsvis.proto import projector_pb2
from tsvis.proto.projector_pb2 import Projector
from tsvis.proto.summary_pb2 import Summary, SummaryMetadata, HistogramProto
from tsvis.proto.tensor_pb2 import TensorProto, TensorShapeProto
from tsvis.proto.plugin_hparams_pb2 import HParamsPluginData, SessionStartInfo
from .utils import make_image, make_histogram, check_image, make_audio, get_embedding, pfv, get_activation, \
    get_name_test, get_gray, Guided_backprop, filters


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
    check_image(tensor)

    if tensor.ndim == 2:
        tensor = np.expand_dims(tensor, -1)

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


def featuremap_PFV(model, input_batch):
    embeddings = []
    name = []
    clean = []
    model_list = get_name_test(model)

    get_embedding(model, embeddings, name, model_list, clean)
    model(input_batch)
    for need_clean in clean:
        need_clean.remove()

    vis = pfv(embeddings, image_shape=input_batch.shape[-2:])
    normalize = lambda x: (x - x.min()) / (x.max() - x.min())
    imgs = input_batch.detach().cpu().numpy()

    orig_imgs = filters(imgs, normalize)
    vis_imgs = filters(vis)
    out = []
    for orig, vis in zip(orig_imgs, vis_imgs):
        out.append(orig * 0.2 + 0.8 * vis)
    out = np.array(out)
    out = out * 255
    featuremap = make_tensor2(out)
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='featuremap'))
    return Summary(value=[Summary.Value(tag=name[-1] + "-PFV", tensor=featuremap, metadata=metadata)])


def featuremap_GradCam(model, input_batch):
    out = []
    model_list = get_name_test(model)
    name = []
    tip = 0
    for img_tensor in input_batch:
        img_tensor = img_tensor.unsqueeze(0)

        all_vis = get_activation(model, img_tensor, name, model_list)
        if len(out) == 0:
            for need_name in name:
                out.append([])
        for index, vis in enumerate(all_vis):
            feature_image = vis * 255
            feature_image[:, :, [0, 1, 2]] = feature_image[:, :, [2, 1, 0]]
            out[index].append(feature_image)

    return out, name


def featuremap_Gray(model, input_batch):
    model_list = get_name_test(model)
    name = []
    all_vis = get_gray(model, input_batch, name, model_list)
    return all_vis, name


def featuremap_guidebp(model, input_batch):
    model_list = get_name_test(model)
    name = []
    input_batch.requires_grad_()
    guided_bp = Guided_backprop(model, model_list, name, input_batch)
    out = guided_bp.find_layer()
    new_name = []
    for kid in name:
        new_name.append(list(kid.keys())[0])
    return out, new_name


def featuremap_result(model, input_batch, task):
    put_sorce = model(input_batch)
    put_sorce = F.softmax(put_sorce, dim=1).detach().numpy()
    put_sorce = make_tensor2(put_sorce)
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='featuremap'))
    return Summary(value=[Summary.Value(tag=task + "-sorce",
                                        tensor=put_sorce,
                                        metadata=metadata)])


def featuremap_label(label, task):
    label = make_tensor2(label.numpy())
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='featuremap'))
    return Summary(value=[Summary.Value(tag=task + "-label",
                                        tensor=label,
                                        metadata=metadata)])


def attention(text, tokenizer_tokens, attention_data):
    # 判断是否是句子对类型
    is_sentence_pair = False
    if type(text[0]) == list:
        is_sentence_pair = True

    # 存放所有句子的attention及相关信息，每个元素为一个包装好的对象
    attn_dict_list = []

    for i in range(len(text)):
        attn_dict = defaultdict(list)

        if is_sentence_pair:
            slice_a = slice(0, len(tokenizer_tokens[i][0]))
            slice_b = slice(len(tokenizer_tokens[i][0]), len(tokenizer_tokens[i][0]) + len(tokenizer_tokens[i][1]))

        for j in range(len(attention_data[i])):
            attn_dict["all"].append(attention_data[i][j][0].tolist())

            if is_sentence_pair:
                attn_dict["aa"].append(attention_data[i][0][0][:, slice_a, slice_a].tolist())
                attn_dict["bb"].append(attention_data[i][0][0][:, slice_b, slice_b].tolist())
                attn_dict["ab"].append(attention_data[i][0][0][:, slice_a, slice_b].tolist())
                attn_dict["ba"].append(attention_data[i][0][0][:, slice_b, slice_a].tolist())

        if is_sentence_pair:
            results = {
                'all': {
                    'attn': attn_dict['all'],
                    'left_text': tokenizer_tokens[i][0] + tokenizer_tokens[i][1],
                    'right_text': tokenizer_tokens[i][0] + tokenizer_tokens[i][1]
                }
            }
        else:
            results = {
                'all': {
                    'attn': attn_dict['all'],
                    'left_text': tokenizer_tokens[i],
                    'right_text': tokenizer_tokens[i]
                }
            }

        if is_sentence_pair:
            results.update({
                'aa': {
                    'attn': attn_dict['aa'],
                    'left_text': tokenizer_tokens[i][0],
                    'right_text': tokenizer_tokens[i][0]
                },
                'bb': {
                    'attn': attn_dict['bb'],
                    'left_text': tokenizer_tokens[i][1],
                    'right_text': tokenizer_tokens[i][1]
                },
                'ab': {
                    'attn': attn_dict['ab'],
                    'left_text': tokenizer_tokens[i][0],
                    'right_text': tokenizer_tokens[i][1]
                },
                'ba': {
                    'attn': attn_dict['ba'],
                    'left_text': tokenizer_tokens[i][1],
                    'right_text': tokenizer_tokens[i][1]
                }
            })
        bidirectional = True
        params = {
            'attention': results,
            'default_filter': "all",
            'bidirectional': bidirectional,
            'display_mode': "light",
            'layer': 0,
            'head': 0
        }

        attn_dict_list.append(params)

    return attn_dict_list


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
    tensor = make_np(audio_data)
    length_frames, num_channels, audio_string = make_audio(tensor, sample_rate)
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


def make_tensor2(tensor):
    """ 转换numpy数组到potobuf格式 """
    shape = TensorShapeProto(dim=[TensorShapeProto.Dim(size=d) for d in tensor.shape])

    return TensorProto(dtype=str(tensor.dtype),
                       tensor_shape=shape,
                       tensor_content=tensor.tobytes())


def make_tensor(tensor):
    """ 转换numpy数组到potobuf格式 """
    shape = projector_pb2.Tensor.TensorShape(dim=[projector_pb2.Tensor.TensorShape.Dim(size=d)
                                                  for d in tensor.shape])

    return projector_pb2.Tensor(dtype=str(tensor.dtype),
                                tensor_shape=shape,
                                tensor_content=tensor.tobytes())


def embedding_sample(name, tensor, sample_type):
    """ 转换高维数据的样本到potobuf格式 """
    if sample_type == 'text':
        tensor = np.array(tensor)
    elif sample_type == 'image':
        tensor = make_np(tensor)
        assert tensor.ndim in [3, 4], f'the shape of image tensors must be (K,H,W) or (K,H,W,C), ' \
                                      f'but get shape {tensor.shape}'
        check_image(tensor[0])
    elif sample_type == 'audio':
        tensor = np.array([make_audio(t)[-1] for t in make_np(tensor)])
    else:
        raise TypeError('the type of label_img must be one of text, audio, image')

    Sample = Projector.Embedding.Sample
    types = {
        'text': Sample.SampleType.TEXT,
        'audio': Sample.SampleType.AUDIO,
        'image': Sample.SampleType.IMAGE
    }

    sample = Sample(type=types[sample_type], X=make_tensor(tensor))
    projector = Projector(embedding=Projector.Embedding(sample=sample))
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
    assert tensor.ndim >= 2 and \
           np.prod(tensor.shape[1:]) >= 2, 'tensor shape must be (N, *), and * >= 2.'

    if label is not None:
        embedding = Projector.Embedding(value=make_tensor(tensor), label=make_tensor(label.squeeze()))
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
    projector = Projector(exception=Projector.Exception(value=make_tensor(tensor)))
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='exceptions'))
    return Summary(value=[Summary.Value(tag=name,
                                        projector=projector,
                                        metadata=metadata)])


def multi_attention_map(input_tensor, attn_map, cls=True):
    input_h, input_w = input_tensor.shape[-2], input_tensor.shape[-1]
    # imgs_tensor = input_tensor.permute((0, 2, 3, 1))

    attn_map = attn_map.clone().detach()
    # attn_map : bs, l, num_head, h, w 或bs, l, h, w
    if attn_map.ndim == 4:
        attn_map = attn_map.unsqueeze(2).numpy()
    elif attn_map.ndim == 5:
        attn_map = attn_map.numpy()

    if cls:
        attn_map = attn_map[:, :, :, 1:, 1:]

    b, l, num_heads, h, w = attn_map.shape
    if input_h > input_w:
        scale = input_h / input_w
        attn_w = int(math.sqrt(h / scale))
        attn_h = int(attn_w * scale)
    else:
        scale = input_w / input_h
        attn_h = int(math.sqrt(h / scale))
        attn_w = int(attn_h * scale)

    attn_map = attn_map.reshape((b, l, num_heads, attn_h, attn_w, attn_h, attn_w))  # * 255


    attn_map = attn_map.astype('float16')
    return attn_map


def Unnormalize(tensor, mean, std, inplace=False):
    """Unnormalize a tensor image with mean and standard deviation.

    Args:
        tensor (Tensor): Tensor image of size (C, H, W) or (B, C, H, W) to be normalized.
        mean (sequence): Sequence of means for each channel.
        std (sequence): Sequence of standard deviations for each channel.
        inplace(bool,optional): Bool to make this operation inplace.

    Returns:
        Tensor: Normalized Tensor image.
    """
    if not isinstance(tensor, torch.Tensor):
        raise TypeError('Input tensor should be a torch tensor. Got {}.'.format(type(tensor)))

    if tensor.ndim < 3:
        raise ValueError('Expected tensor to be a tensor image of size (..., C, H, W). Got tensor.size() = '
                         '{}.'.format(tensor.size()))

    if not inplace:
        tensor = tensor.clone()

    dtype = tensor.dtype
    mean = torch.as_tensor(mean, dtype=dtype, device=tensor.device)
    std = torch.as_tensor(std, dtype=dtype, device=tensor.device)
    if (std == 0).any():
        raise ValueError('std evaluated to zero after conversion to {}, leading to division by zero.'.format(dtype))
    if mean.ndim == 1:
        mean = mean.view(-1, 1, 1)
    if std.ndim == 1:
        std = std.view(-1, 1, 1)
    tensor.mul_(std).add_(mean)
    return tensor


def state(hidden_state, tag):
    metadata = SummaryMetadata(plugin_data=SummaryMetadata.PluginData(plugin_name='hiddenstate'))
    if isinstance(hidden_state, str):
        hidden_state = make_tensor2(np.array([hidden_state]))
    else:
        hidden_state = make_tensor2(hidden_state.detach().numpy())

    return Summary(value=[Summary.Value(tag=tag, tensor=hidden_state,
                                        metadata=metadata)])
