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
import io
import numpy as np
from PIL import Image
import torch.nn as nn
import torch
import torch.nn.functional as F
import logging
import functools


from torchvision import transforms


def check_image(tensor):
    ndim = tensor.ndim
    if ndim == 2:
        pass
    elif ndim == 3:
        if tensor.shape[2] > 4:
            raise Exception(f'the expected image type is (LA), (RGB), (RGBA), and the third dimension is less than 4, '
                            f'but get shape {tensor.shape}')
    else:
        raise Exception(f'the shape of image must be (H,W) or (H,W,C), but get shape {tensor.shape}')


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

    # If start == 0, we need to add an empty one left, otherwise we can just include
    # the bin left to the first nonzero-count bin:
    counts = counts[start - 1:end] if start > 0 else np.concatenate([[0], counts[:end]])
    limits = limits[start:end + 1]

    if counts.size == 0 or limits.size == 0:
        raise ValueError('The histogram is empty, please file a bug report.')

    sum_sq = values.dot(values)
    return sum_sq, limits.tolist(), counts.tolist()


def make_audio(tensor, sample_rate=44100):
    import soundfile
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
    return length_frames, num_channels, audio_string


def get_embedding(model, embeddings, name, model_list, clean):
    def feature_map_hook(module, input, output):
        embeddings.append(input[0])

    try:
        for i in model._modules.keys():
            module = model._modules[i]
            if isinstance(module, nn.MaxPool2d) or (isinstance(module, nn.Conv2d) and module.stride > (1, 1)):
                x = module.register_forward_hook(feature_map_hook)
                clean.append(x)
                for j in model_list:
                    if j[list(j.keys())[0]] == module:
                        name.append(list(j.keys())[0])
            get_embedding(module, embeddings, name, model_list, clean)
        # for i, module in enumerate(model.children()):
        #     if list(module.children()):
        #         get_embedding(module, embeddings)
        #     elif isinstance(module, nn.MaxPool2d) or (isinstance(module, nn.Conv2d) and module.stride > (1,1)):
        #         module.register_forward_hook(feature_map_hook)

    except:
        logging.error('请下载pytorch')


def get_activation(model, input_batch, name, model_list):
    vis = None
    all_vis = []
    fmap_block = []
    grad_block = []
    clean = []
    model.zero_grad()
    input_batch.requires_grad_()

    def forward_hook(module, input, output):
        # activation = output
        fmap_block.append(output)

    def backward_hook(module, input, output):
        # activation_grad = output[0]
        grad_block.insert(0, output[0])

    torch.set_grad_enabled(True)
    layers_hook(model, name, model_list, forward_hook, backward_hook, clean)
    model.zero_grad()
    output = model(input_batch)
    #
    # classes = F.softmax(output)
    #
    # print(classes)
    # one_hot, _ = output.max(dim=-1)
    # one_hot.requires_grad_()
    # model.zero_grad()
    one_hot = output.max()
    # if 1 - one_hot < 0.00001:
    #     # one_hot_, _ = classes.min(dim=-1)
    #     one_hot = 1 - one_hot_ * 10000
    # print(one_hot)
    one_hot.backward()
    for need_clean in clean:
        need_clean.remove()
    for activation, activation_grad in zip(fmap_block, grad_block):
        vis = GradCam(activation, activation_grad, input_batch)
        all_vis.append(vis)
    return all_vis


def pca_decomposition(x, n_components=3):
    feats = x.permute(0, 2, 3, 1).reshape(-1, x.shape[1])
    feats = feats - torch.mean(feats, 0)
    u, s, v = torch.svd(feats, compute_uv=True)
    pc = torch.matmul(u[:, :n_components], torch.diag(s[:n_components]))
    pc = pc.view(x.shape[0], x.shape[2], x.shape[3], 3).permute(0, 3, 1, 2)
    return pc


def normalize_and_scale_features(features, n_sigma=1):
    scaled_features = (features - np.mean(features)) / (np.std(features))
    scaled_features = np.clip(scaled_features, -n_sigma, n_sigma)
    scaled_features = (scaled_features - scaled_features.min()) / (scaled_features.max() - scaled_features.min())
    return scaled_features


def pfv(embeddings, image_shape=None, idx_layer=None, interp_mode='bilinear'):
    if image_shape is None: image_shape = embeddings[0].shape[-2:]
    if idx_layer is None: idx_layer = len(embeddings) - 1
    with torch.no_grad():
        layer_to_visualize = pca_decomposition(embeddings[idx_layer], 3)
        amap = [F.interpolate(torch.sum(x, dim=1).unsqueeze(1), size=image_shape, mode=interp_mode) for x in
                embeddings[:idx_layer]]
        amap = torch.cat(amap, dim=1)
        layer_to_visualize = F.interpolate(layer_to_visualize, size=image_shape, mode=interp_mode) * torch.sum(amap,
                                                                                                               dim=1).unsqueeze(
            1)
        layer_to_visualize = layer_to_visualize.detach().cpu().numpy()
        rgb = normalize_and_scale_features(layer_to_visualize)
        return rgb

def filters(imgs, f=lambda x: x):
    imgs = np.transpose(imgs, (0, 2, 3, 1))
    l = [f(imgs[i, :, :, :]) for i in range(imgs.shape[0])]
    # return np.concatenate(l, axis=1)
    return l

def layers_hook(model, name, model_list, forward_hook, backward_hook, clean):
    for need_layer in model_list:
        module = list(need_layer.values())[0]
        if isinstance(module, nn.Conv2d) or isinstance(module, nn.MaxPool2d):
            x = module.register_forward_hook(forward_hook)
            y = module.register_backward_hook(backward_hook)
            clean.append(x)
            clean.append(y)
            name.append(list(need_layer.keys())[0])

    # for i, module in enumerate(model.children()):
    #     if list(module.children()) and isinstance(module, nn.Module):
    #         layers_hook(module, name, model_list, forward_hook, backward_hook, clean)
    #     elif isinstance(module, nn.Conv2d) or isinstance(module, nn.MaxPool2d):
    #         x = module.register_forward_hook(forward_hook)
    #         y = module.register_backward_hook(backward_hook)
    #         clean.append(x)
    #         clean.append(y)
    #         for j in model_list:
    #             if j[list(j.keys())[0]] == module:
    #                 name.append(list(j.keys())[0])


def GradCam(data_, data_grad_, img_data):
    image_size = (img_data.shape[-1], img_data.shape[-2])
    for i in range(img_data.shape[0]):
        img = img_data[i].detach().numpy()
        img = img - np.min(img)
        if np.max(img) != 0:
            img = img / np.max(img)
        data = data_[i, :, :, :]
        data_grad = data_grad_[i, :, :, :]  # !维度扩充
        weight = data_grad.mean(dim=-1, keepdim=True).mean(dim=-2, keepdim=True)
        mask = F.relu((weight * data).sum(dim=0))
        mask = F.interpolate(mask.unsqueeze(0).unsqueeze(0), image_size, mode='bilinear').squeeze(0).squeeze(0)
        mask = mask.detach().numpy()
        if np.max(mask) != 0:
            mask = mask / np.max(mask)
        else:
            mask = mask
        heat_map = np.float32(map_JET(255 * mask))  # 自定义映射规则
        # heat_map = np.float32(cv2.applyColorMap(np.uint8(255 * mask), cv2.COLORMAP_JET))   #opencv映射规则
        cam = heat_map + np.float32((np.uint8(img.transpose((1, 2, 0)) * 255)))
        cam = cam - np.min(cam)
        if np.max(cam) != 0:
            cam = cam / np.max(cam)
    return cam


def get_gray(model, input_batch, name, model_list):
    out = []
    clean = []

    def forward_hook(module, input, output):
        output = output.detach().numpy()[:, 0, :, :]
        out.append(nol(output))

    def backward_hook(module, input, output):
        pass

    layers_hook(model, name, model_list, forward_hook, backward_hook, clean)
    model(input_batch)
    for need_clean in clean:
        need_clean.remove()
    return out


class Guided_backprop():
    def __init__(self, model, model_list, name, img_tensor):
        self.model = model
        self.image_reconstruction = []
        self.activation_maps = []
        self.need_change_relu = []
        self.model_list = model_list
        self.name = name
        self.input = img_tensor
        self.clean = []
        self.find_db_layer()
        self.temp = 0
        self.need_change_relu_activation = []
        self.data_activation_maps = []



    def find_db_layer(self):
        def forward_hook_fn(module, input, output):
            # 在全局变量中保存 ReLU 层的前向传播输出
            # 用于将来做 guided backpropagation
            self.activation_maps.append(output)
        def get_activation_maps():
            for layer in self.model_list:
                if isinstance(list(layer.values())[0], nn.ReLU) or isinstance(list(layer.values())[0], nn.Conv2d):
                    y = list(layer.values())[0].register_forward_hook(forward_hook_fn)
                    self.name.append(layer)
                    self.clean.append(y)
        get_activation_maps()
        self.model(self.input)
        for need_clean_hook in self.clean:
            need_clean_hook.remove()



    def register_backward_hooks(self):
        def forward_hook_fn(module, input, output):
            # 在全局变量中保存 ReLU 层的前向传播输出
            # 用于将来做 guided backpropagation
            self.data_activation_maps.append(output)
        def get_activation_maps():
            for layer in self.model_list:
                if isinstance(list(layer.values())[0], nn.ReLU) or isinstance(list(layer.values())[0], nn.Conv2d):
                    y = list(layer.values())[0].register_forward_hook(forward_hook_fn)
                    self.clean.append(y)
        def backward_hook_fn(module, grad_in, grad_out):
            grad = self.need_change_relu_activation[self.temp]
            self.temp += 1
            grad[grad > 0] = 1

            # grad_out[0] 表示 feature 的梯度，只保留大于 0 的部分
            positive_grad_out = torch.clamp(grad_out[0], min=0.0)
            # 创建新的输入端梯度
            new_grad_in = positive_grad_out * grad
            # new_grad_in = grad_out[0] * grad

            # ReLU 不含 parameter，输入端梯度是一个只有一个元素的 tuple
            return (new_grad_in,)


        def back_hook(backward_hook):
            for relu_kid in self.need_change_relu:
                x =relu_kid.register_backward_hook(backward_hook)
                self.clean.append(x)


        get_activation_maps()
        back_hook(backward_hook_fn)

    @staticmethod  ##使得normalize变成静态方法和他model没有关系，Guided_backprop.normalize()调用
    def normalize(I):
        # 归一化梯度map，先归一化到 mean=0 std=1
        norm = (I - I.mean()) / I.std()
        # 把 std 重置为 0.1，让梯度map中的数值尽可能接近 0
        norm = norm * 0.1
        # 均值加 0.5，保证大部分的梯度值为正
        norm = norm + 0.5
        # 把 0，1 以外的梯度值分别设置为 0 和 1
        norm = norm.clip(0, 1)
        return norm

    def find_layer(self):

        # self.model.zero_grad()
        # model_output = self.model(self.input)
        # pred_class = torch.argmax(model_output, dim=1)
        # # 生成目标类 one-hot 向量，作为反向传播的起点
        # grad_target_map = torch.zeros(model_output.shape,
        #                               dtype=torch.float)
        # img_idx = torch.arange(0, model_output.size(0))
        # grad_target_map[img_idx, pred_class] = 1
        # # 反向传播，之前注册的 backward hook 开始起作用
        # model_output.backward(grad_target_map)
        for index, need_get_layer in enumerate(self.name):
            self.data_activation_maps = []
            self.need_change_relu = []
            self.need_change_relu_activation = []
            self.clean = []
            self.temp = 0
            i = index
            while (i >= 0):
                if isinstance(list(self.name[i].values())[0], nn.ReLU):
                    self.need_change_relu.append(list(self.name[i].values())[0])
                    self.need_change_relu_activation.append(self.activation_maps[i])
                i-=1
            self.register_backward_hooks()
            self.model.zero_grad()
            model_output = self.model(self.input)
            output_data = self.data_activation_maps[index]
            torch.mean(output_data).backward(retain_graph=True)
            for clean_kid in self.clean:
                clean_kid.remove()

            import copy
            need_data = copy.deepcopy(self.input.grad)
            need_data = need_data.permute(0, 2, 3, 1)
            need_data = self.normalize(need_data) * 255
            self.image_reconstruction.append(need_data)

        return self.image_reconstruction


# def find_output_sorce(output):
#     datas = []
#     # output = torch.rand(10, 12)
#     sort_index = torch.argsort(output, dim=1, descending=True)
#
#     if output.shape[1] > 10:
#         sort_index = sort_index[:, :10]
#     sort_values = torch.gather(output, 1, sort_index)
#     datas.append(sort_index.detach().numpy())
#     datas.append(sort_values.detach().numpy())
#     return np.array(datas)


def nol(data):
    nb, nn, nf = data.shape
    data = data.reshape(nb, -1)
    min_d, max_d = np.expand_dims(np.min(data, axis=-1), axis=1), np.expand_dims(np.max(data, axis=-1), axis=1)
    np.seterr(divide='ignore', invalid='ignore')
    data = (data - min_d) / (max_d - min_d) * 255
    return data.reshape(nb, nn, nf)


def map_JET(img):
    img = np.around(img)
    n, m = img.shape
    out = np.zeros((n, m, 3), dtype=np.uint8)
    # out = np.expand_dims(img, 2).repeat(3, 2)

    indices = np.where((img >= 0) & (img <= 31))
    values = img[indices]
    out[indices[0], indices[1], [0] * len(indices[0])] = 128 + 4 * values

    indices = np.where(img == 32)
    out[indices[0], indices[1], [0] * len(indices[0])] = 255

    indices = np.where((img >= 33) & (img <= 95))
    values = img[indices]
    out[indices[0], indices[1], [1] * len(indices[0])] = 4 + 4 * (values - 33)
    out[indices[0], indices[1], [0] * len(indices[0])] = 255

    indices = np.where(img == 96)
    out[indices[0], indices[1], [2] * len(indices[0])] = 2
    out[indices[0], indices[1], [1] * len(indices[0])] = 255
    out[indices[0], indices[1], [0] * len(indices[0])] = 254

    indices = np.where((img >= 97) & (img <= 158))
    values = img[indices]
    out[indices[0], indices[1], [2] * len(indices[0])] = 6 + 4 * (values - 97)
    out[indices[0], indices[1], [1] * len(indices[0])] = 255
    out[indices[0], indices[1], [0] * len(indices[0])] = 250 - 4 * (values - 97)

    indices = np.where(img == 159)
    out[indices[0], indices[1], [2] * len(indices[0])] = 254
    out[indices[0], indices[1], [1] * len(indices[0])] = 255
    out[indices[0], indices[1], [0] * len(indices[0])] = 1

    indices = np.where((img >= 160) & (img <= 223))
    values = img[indices]
    out[indices[0], indices[1], [2] * len(indices[0])] = 255
    out[indices[0], indices[1], [1] * len(indices[0])] = 252 - 4 * (values - 160)

    indices = np.where((img >= 224) & (img <= 255))
    values = img[indices]
    out[indices[0], indices[1], [2] * len(indices[0])] = 252 - 4 * (values - 224)

    return out


def get_name_test(model):
    model_name = model.__class__.__name__
    model_list = []

    def find_parent_name(model):
        nonlocal model_name
        for i in model._modules.keys():
            module = model._modules[i]

            model_name = model_name + 'to' + module.__class__.__name__ + '[' + str(i) + ']'
            model_list.append({model_name: module})
            find_parent_name(module)
            index = model_name.rfind("to")
            model_name = model_name[:index]

    find_parent_name(model)
    return model_list


def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw, name=text)

        return wrapper

    return decorator


def get_name_test(model):
    model_name = model.__class__.__name__
    model_list = []

    def find_parent_name(model):
        nonlocal model_name
        for i in model._modules.keys():
            module = model._modules[i]

            model_name = model_name + 'to' + module.__class__.__name__ + '[' + str(i) + ']'
            model_list.append({model_name: module})
            find_parent_name(module)
            index = model_name.rfind("to")
            model_name = model_name[:index]

    find_parent_name(model)
    return model_list


def all_layers(model, layers, model_list):
    for i in model._modules.keys():
        module = model._modules[i]
        if list(module.children()) and isinstance(module, nn.Module):
            all_layers(module, layers, model_list)
        else:
            layers['all_layers'].append(module)
            for j in model_list:
                if j[list(j.keys())[0]] == module:
                    layers['all_layers_name'].append(list(j.keys())[0])


def format_special_chars(tokens):
    return [t.replace('Ġ', ' ').replace('▁', ' ') for t in tokens]


def format_delimiters(tokens, tokenizer):
    formatted_tokens = []
    for t in tokens:
        if tokenizer.sep_token:
            t = t.replace(tokenizer.sep_token, '[SEP]')
        if tokenizer.cls_token:
            t = t.replace(tokenizer.cls_token, '[CLS]')
        formatted_tokens.append(t)
    return formatted_tokens


def get_attention_input_embedding(model, embeddings, name, model_list):
    def feature_map_hook(module, input, output):
        embeddings.append(output[0])

    try:
        for i in model._modules.keys():
            module = model._modules[i]
            if isinstance(module, nn.MaxPool2d) or (isinstance(module, nn.Conv2d) and module.stride > (1, 1)):
                module.register_forward_hook(feature_map_hook)
                for j in model_list:
                    if j[list(j.keys())[0]] == module:
                        name.append(list(j.keys())[0])
            get_attention_input_embedding(module, embeddings, name, model_list)
    except:
        print('The model without nn.Conv2d layer or nn.MaxPool2d layer')


def get_attention_embedding(model, embeddings, name, model_list):
    try:
        for i in model._modules.keys():
            module = model._modules[i]
            if isinstance(module, nn.MultiheadAttention):
                module.register_forward_hook(lambda self, input, output: embeddings.append(output[1].detach().numpy()))
                for j in model_list:
                    if j[list(j.keys())[0]] == module:
                        name.append(list(j.keys())[0])
            get_attention_embedding(module, embeddings, name, model_list)
    except:
        print('The model without nn.MultiheadAttention layer')


class AttentionVisualizer:
    def __init__(self, model, transform, img, num_attn_layer):
        self.model = model
        self.transform = transform

        self.pil_img = img
        self.tensor_img = None

        self.conv_features = None
        self.embedding = None
        self.enc_attn_weights = []
        self.num_attn_layer = num_attn_layer
        self.out_pro = None
        self.cls = None
        self.bbox = None


    def compute_features(self, img):
        model = self.model
        model.eval()
        # use lists to store the outputs via up-values
        embeddings, enc_attn_weights = [], []
        name, attn_name = [], []

        model_list = get_name_test(model)
        get_attention_input_embedding(model, embeddings, name, model_list)

        attn_model_list = get_name_test(model)
        get_attention_embedding(model, enc_attn_weights, attn_name, attn_model_list)

        # propagate through the model
        outputs = model(img)

        enc_attn_weights = np.array(enc_attn_weights[:self.num_attn_layer])
        enc_attn_weights = torch.from_numpy(enc_attn_weights)

        if enc_attn_weights.ndim == 5:
            enc_attn_weights = enc_attn_weights.permute(1, 0, 2, 3, 4)
            enc_attn_weights = enc_attn_weights.numpy()
        elif enc_attn_weights.ndim == 4:
            enc_attn_weights = enc_attn_weights.permute(1, 0, 2, 3)
            enc_attn_weights = enc_attn_weights.unsqueeze(2)
            enc_attn_weights = enc_attn_weights.numpy()

        # get the HxW shape of the feature maps of the CNN
        shape = embeddings[-1].shape[-2:]

        try:
            if len(enc_attn_weights.shape) == 5:
                b, h = enc_attn_weights.shape[0], enc_attn_weights.shape[2]
                self.enc_attn_weights = enc_attn_weights.reshape((b, self.num_attn_layer, h) + shape + shape)
                # and reshape the self-attention to a more interpretable shape
                for i in range(b):
                    for j in range(self.num_attn_layer):
                        for k in range(h):
                            for m in range(shape[0]):
                                for n in range(shape[1]):
                                    # heat_map = np.float32(map_JET(self.enc_attn_weights[i, j, k, m, n, :, :] / np.max(self.enc_attn_weights[i, j, k, m, n, :, :]) * 255))
                                    # self.enc_attn_weights[i, j, k, m, n, :, :] = heat_map
                                    self.enc_attn_weights[i, j, k, m, n, :, :] = self.enc_attn_weights[i, j, k, m, n, :, :] / np.max(self.enc_attn_weights[i, j, k, m, n, :, :]) * 255
        except:
            print('get wrong dim')

        probas = outputs['pred_logits'].softmax(-1)[:, :, :-1]
        keep = probas.max(-1).values > 0.7

        bboxes = []
        clses = []
        out_pro = [[] for _ in range(outputs['pred_boxes'].shape[0])]
        # convert boxes from [0; 1] to image scales
        for i in range(outputs['pred_boxes'].shape[0]):
            bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][i, keep[i]], (256, 256))
            bboxes.append(bboxes_scaled)
            cls = probas[i, keep[i]].argmax(1)
            clses.append(cls)
            pro = probas[i, keep[i]]
            for j, p in enumerate(pro):
                tem = p[cls[j]].unsqueeze(0)
                # out_pro[i].extend(p[cls[j]].unsqueeze(0))
                out_pro[i].append(p[cls[j]])
            out_pro[i] = torch.stack(out_pro[i])

        # self.bbox = bboxes
        self.bbox = bboxes
        self.cls = clses
        self.out_pro = out_pro

    def compute_on_image(self):
        # mean-std normalize the input image (batch-size: 1)
        input_tensor = []
        for image in self.pil_img:
            input_tensor.append(self.transform(image))
        self.tensor_img = torch.stack(input_tensor)  # 升维
        self.compute_features(self.tensor_img)

        return self.enc_attn_weights, self.bbox, self.out_pro, self.cls



# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)


def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b


def deal_img(image_dir, resize=False):
    import glob
    from PIL import Image


    extensions = ['jpg', 'jpeg', 'png']
    file_list = list()
    for extension in extensions:
        image_files = glob.glob(image_dir + '*.' + extension)
        file_list.extend(image_files)
    input_images = []

    tag = []
    for f in file_list:
        image = Image.open(f)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        f = f.split('\\')[1]
        tag.append(f.split('.')[0])
        if resize:
            t = transforms.Resize((256, 256))
            input_images.append(t(image))
        else:
            input_images.append(image)

    return input_images, tag




