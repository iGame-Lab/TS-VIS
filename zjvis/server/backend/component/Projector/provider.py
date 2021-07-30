# -*- coding: UTF-8 -*-
"""
 Copyright 2020 Tianshu AI Platform. All Rights Reserved.

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
from PIL import Image
import io
from zjvis.parser.utils.cache_io import CacheIO
from zjvis.parser.utils.logfile_utils import path_parser
from .projector_read import projector_read
from .projector_reduction import projector_reduction
from zjvis.server.backend.api.utils import get_api_params
import base64
import numpy as np

def projector_meta_provider(file_path, sample_file_path):
    # read from cache
    res = CacheIO(file_path).get_cache()
    if res:
        projector_meta_data = projector_read(data=res) \
            .get_meta_data()
        if sample_file_path.exists():
            projector_meta_data.append(True)
            sample = projector_sample_provider(sample_file_path, index=0)
            projector_meta_data.append(sample['type'])
        else:
            projector_meta_data.append(False)
            projector_meta_data.append('')

        return projector_meta_data
    else:
        raise ValueError('Parameter error, no data found')


# 返回样本数据
def projector_sample_provider(file_path, index=None):
    res = CacheIO(file_path).get_cache()
    if res:
        sample = projector_read(data=res, index=index).\
            get_data()
        return sample
    else:
        raise ValueError('Parameter error, no data found')


# 返回Tensor数据
def projector_raw_provider(file_path, step):
    res = CacheIO(file_path).get_cache()
    if res:
        xy = projector_read(data=res, step=step) \
            .get_data()
        return xy
    else:
        raise ValueError('Parameter error, no data found')


def projector_provider(file_path, step, method, dims, samples=1000):
    res = CacheIO(file_path).get_cache()
    if res:
        xy = projector_read(data=res, step=step) \
            .get_data()
        x = xy[0]
        samples = min(samples, len(x))
        y = xy[1][0:samples]
        res = projector_reduction(x[0:samples], method, dimension=dims)\
            .get_data()
        return [res, y]
    else:
        raise ValueError('Parameter error, no data found')


def get_projector_meta_data(request):
    params = ['run', 'tag']
    run, tag = get_api_params(request, params)

    from zjvis.parser.utils.vis_logging import get_logger
    file_path = path_parser(get_logger().cachedir, run, 'embedding', tag)
    sample_tag = 'sample_' + tag.replace('/', '#').replace(':', '$')
    sample_file_path = path_parser(get_logger().cachedir, run, 'embedding', sample_tag)
    data = projector_meta_provider(file_path, sample_file_path)
    return {
        tag: data[0],
        'shape': data[1],
        'sample': data[2],
        'sample_type': data[3]
    }


def get_projector_raw_data(request):
    params = ['run', 'tag', 'step']
    run, tag, step = get_api_params(request, params)

    from zjvis.parser.utils.vis_logging import get_logger
    file_path = path_parser(get_logger().cachedir, run, 'embedding', tag)
    data = projector_raw_provider(file_path, step=int(step))

    if data:
        return {step: data}
    else:
        raise ValueError('No such data')


def get_projector_sample_data(request):
    params = ['run', 'tag', 'index']
    run, tag, index = get_api_params(request, params)

    from zjvis.parser.utils.vis_logging import get_logger
    sample_tag = 'sample_' + tag.replace('/', '#').replace(':', '$')
    file_path = path_parser(get_logger().cachedir, run, 'embedding', sample_tag)
    sample = projector_sample_provider(file_path, index=int(index))

    if sample:
        _io = io.BytesIO()
        if sample['type'] == 'image':
            _img = Image.fromarray((sample['val']*255).astype(np.uint8))
            _img.save(_io, "png")
            _content = _io.getvalue()
            _data = base64.b64encode(_content)
            res = "data:image/png;base64,%s" % _data.decode()
        elif sample['type'] == 'audio':
            _content = sample['val']
            _data = base64.b64encode(_content)
            res = "data:audio/wav;base64,%s" % _data.decode()
        elif sample['type'] == 'text':
            _content = sample['val']
            res = _content
        else:
            res = None
        return res
        # return HttpResponse(content=_content, content_type=_content_type)
    else:
        raise ValueError('No such data')


def get_projector_data(request):
    params = ['run', 'tag', 'step', 'method']
    run, tag, step, method = get_api_params(request, params)
    # 可选参数
    if request.GET.get('dims'):
        dims = int(request.GET.get('dims'))
    else:
        dims = None

    from zjvis.parser.utils.vis_logging import get_logger
    file_path = path_parser(get_logger().cachedir, run, 'embedding', tag)
    data = projector_provider(file_path, step=int(step), method=method, dims=dims)

    if data:
        return {step: data}
    else:
        raise ValueError('No such data')
