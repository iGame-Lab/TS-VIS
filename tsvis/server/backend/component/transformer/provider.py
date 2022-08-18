import numpy as np
from tsvis.parser.utils.vis_logging import get_logger
from tsvis.server.backend.api.utils import get_api_params
from tsvis.parser.utils.logfile_utils import path_parser
from tsvis.parser.utils.cache_io import CacheIO
from .attention_map_read import attention_map_read
from .feature_read import transformer_text_read
import base64
import io
from PIL import Image


def attentionmap_provider(file_path, l, x, y, img, g, r=1):
    res = CacheIO(file_path).get_cache()
    if res:
        if g == 1:
            res = deal_attn_map(res[0]['value'], g)
        elif g == 0:
            res = deal_attn_map(res[0]['value'], g, layer=l)
        map_data = attention_map_read(data=res, l=l, x=x, y=y, img=img, r=r).get_data()
        return map_data
    else:
        return []


def deal_attn_map(res, g, layer=None):
    l, num_heads, attn_h, attn_w = res.shape[:4]

    # 全局归一化
    if g == 1:
        attn_map = np.transpose(res, (2, 3, 0, 1, 4, 5))
        for i in range(attn_h):
            for j in range(attn_w):
                temp = attn_map[i, j, :, :, :, :] - np.min(attn_map[i, j, :, :, :, :])
                temp = temp / np.max(temp) * 255
                attn_map[i, j, :, :, :, :] = temp

        attn_map = np.transpose(attn_map, (2, 3, 0, 1, 4, 5))
        return attn_map

    # 局部归一化
    elif g == 0:
        attn_map = res
        for i in range(num_heads):
            for j in range(attn_h):
                for k in range(attn_w):
                    if np.max(attn_map[layer, i, j, k, :, :]) != np.min(attn_map[layer, i, j, k, :, :]):
                        temp = attn_map[layer, i, j, k, :, :] - np.min(attn_map[layer, i, j, k, :, :])
                        temp = (temp / np.max(temp)) * 255
                        attn_map[layer, i, j, k, :, :] = temp
                    else:
                        temp = attn_map[layer, i, j, k, :, :]
                        attn_map[layer, i, j, k, :, :] = np.ones(temp.shape)

        return attn_map


def img_provider(file_path):
    res = CacheIO(file_path).get_cache()
    if res:
        res = res[0]['value']
        return res
    else:
        return []


def transformer_text_data_provider(file_path, tag):
    res = CacheIO(file_path).get_cache()
    if res:
        transformer_data = transformer_text_read(data=res, tag=tag).get_data()
        return transformer_data
    else:
        raise ValueError('No such data')


def encode_base64(data):
    _io = io.BytesIO()
    _img = Image.fromarray(data.astype('uint8'))
    _img.save(_io, "png")
    _content = _io.getvalue()
    _data = base64.b64encode(_content)
    res = "data:image/png;base64,%s" % _data.decode()
    return res


# def get_transformer_data(request):
#     params = ['run', 'tag', 'l', 'x', 'y', 'type', 'g', 'r']
#     run, tag, l, x, y, type, g, r = get_api_params(request, params)
#
#     if type == 'image':
#         attn_file_path = path_parser(get_logger().cachedir, run, 'transformer', tag + f'-am')
#         img_file_path = path_parser(get_logger().cachedir, run, 'transformer', tag)
#
#         img_data = (img_provider(img_file_path) * 255).astype('uint8')
#
#         if x == 'None' and y == 'None':
#             img_data = encode_base64(img_data)
#             res = CacheIO(attn_file_path).get_cache()
#             res = res[0]['value']
#
#             data = {'img': img_data, 'num_layers': res.shape[0]}
#             return data
#         else:
#             resize_img = Image.fromarray(img_data).resize((64, 64))
#             resize_img = np.array(resize_img)
#             if int(g) == 1:
#                 attn_map_data = attentionmap_provider(attn_file_path, int(l), int(x), int(y), resize_img, int(g), float(r))
#
#                 img_data = encode_base64(img_data)
#                 attn_map_datas = []
#                 for i in range(attn_map_data.shape[0]):
#                     attn_map_datas.append(encode_base64(attn_map_data[i]))
#
#                 data = {'img': img_data, 'attn_map': attn_map_datas, 'layer': l}
#
#                 return {tag: data}
#             elif int(g) == 0:
#                 attn_map_data = attentionmap_provider(attn_file_path, int(l), int(x), int(y), resize_img, int(g))
#
#                 img_data = encode_base64(img_data)
#                 attn_map_datas = []
#                 for i in range(attn_map_data.shape[0]):
#                     attn_map_datas.append(encode_base64(attn_map_data[i]))
#                 data = {'img': img_data, 'attn_map': attn_map_datas, 'layer': l}
#
#                 return {tag: data}
#
#     elif type == 'text':
#         file_path = path_parser(get_logger().cachedir, run, 'transformer', tag)
#         data = transformer_text_data_provider(file_path, tag)
#         return {tag: data}
#

def get_transformer_text_data(request):
    params = ['run', 'tag']
    run, tag = get_api_params(request, params)
    file_path = path_parser(get_logger().cachedir, run, 'transformer', tag)
    data = transformer_text_data_provider(file_path, tag)
    return {tag: data}

def get_transformer_image_data(request):
    params = ['run', 'tag', 'l', 'x', 'y', 'g', 'r']
    run, tag, l, x, y, g, r = get_api_params(request, params)
    attn_file_path = path_parser(get_logger().cachedir, run, 'transformer', tag + f'-am')
    img_file_path = path_parser(get_logger().cachedir, run, 'transformer', tag)

    img_data = (img_provider(img_file_path) * 255).astype('uint8')

    if x == 'None' and y == 'None':
        img_data = encode_base64(img_data)
        res = CacheIO(attn_file_path).get_cache()
        res = res[0]['value']

        data = {'img': img_data, 'num_layers': res.shape[0]}
        return data
    else:
        resize_img = Image.fromarray(img_data).resize((64, 64))
        resize_img = np.array(resize_img)
        if int(g) == 1:
            attn_map_data = attentionmap_provider(attn_file_path, int(l), int(x), int(y), resize_img, int(g),
                                                  float(r))

            img_data = encode_base64(img_data)
            attn_map_datas = []
            for i in range(attn_map_data.shape[0]):
                attn_map_datas.append(encode_base64(attn_map_data[i]))

            data = {'img': img_data, 'attn_map': attn_map_datas, 'layer': l}

            return {tag: data}
        elif int(g) == 0:
            attn_map_data = attentionmap_provider(attn_file_path, int(l), int(x), int(y), resize_img, int(g))

            img_data = encode_base64(img_data)
            attn_map_datas = []
            for i in range(attn_map_data.shape[0]):
                attn_map_datas.append(encode_base64(attn_map_data[i]))
            data = {'img': img_data, 'attn_map': attn_map_datas, 'layer': l}

            return {tag: data}