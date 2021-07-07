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
from utils.cache_io import CacheIO
from utils.vis_logging import get_logger
from utils.logfile_utils import path_parser
from .audio_read import audio_read
from backend.api.utils import get_api_params
import base64


def audio_meta_provider(file_path):
    # read from cache
    res = CacheIO(file_path).get_cache()
    if res:
        audio_meta_data = audio_read(data=res) \
            .get_meta_data()
        return audio_meta_data
    else:
        raise ValueError('Parameter error, no data found')


def audio_provider(file_path, step):
    res = CacheIO(file_path).get_cache()
    if res:
        return audio_read(data=res, step=step).get_data()
    else:
        raise ValueError('Parameter error, no data found')


def get_audio_meta_data(request):
    params = ['run', 'tag']
    run, tag = get_api_params(request, params)

    file_path = path_parser(get_logger().cachedir, run, 'audio', tag)
    data = audio_meta_provider(file_path)
    return {tag: data}


def get_audio_data(request):
    params = ['run', 'tag', 'step']
    run, tag, step = get_api_params(request, params)

    file_path = path_parser(get_logger().cachedir, run, 'audio', tag)
    data = base64.b64encode(audio_provider(file_path, step=int(step)))
    res = "data:audio/wav;base64,%s" % data.decode()
    if data:
        return res
    else:
        raise ValueError('No such data')
