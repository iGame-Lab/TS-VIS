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
from utils.path_utils import get_file_path
from .exception_read import Exception_read
from backend.api.utils import get_api_params


def exception_meta_provider(file_path):
    # read from cache
    res = CacheIO(file_path).get_cache()
    if res:
        exception_meta_data = Exception_read(data=res) \
            .get_meta_data()
        return exception_meta_data
    else:
        raise ValueError('Parameter error, no data found')


def exception_provider(file_path, step):
    res = CacheIO(file_path).get_cache()
    if res:
        # raw_data
        data = Exception_read(data=res, step=step) \
            .get_data()
        return data
    else:
        raise ValueError('Parameter error, no data found')


def exception_box_provider(file_path, step, limit):
    res = CacheIO(file_path).get_cache()
    if res:
        # raw_data
        data = Exception_read(data=res, step=step) \
            .get_outlier(limit)
        return data
    else:
        raise ValueError('Parameter error, no data found')


def exception_hist_provider(file_path, step):
    res = CacheIO(file_path).get_cache()
    if res:
        # raw_data
        data = Exception_read(data=res, step=step) \
            .get_histogram()
        return data
    else:
        raise ValueError('Parameter error, no data found')


def get_exception_meta_data(request):
    params = ['uid', 'trainJobName', 'run', 'tag']
    uid, trainJobName, run, tag = get_api_params(request, params)

    file_path = get_file_path(uid, run, 'exception', tag)
    data = exception_meta_provider(file_path)
    return {tag: data}


def get_exception_data(request):
    params = ['uid', 'trainJobName', 'run', 'tag', 'step']
    uid, trainJobName, run, tag, step = get_api_params(request, params)

    file_path = get_file_path(uid, run, 'exception', tag)
    data = exception_provider(file_path, step=int(step))

    if data:
        return {step: data}
    else:
        raise ValueError('No such data')


def get_exception_hist_data(request):
    params = ['uid', 'trainJobName', 'run', 'tag', 'step']
    uid, trainJobName, run, tag, step = get_api_params(request, params)

    file_path = get_file_path(uid, run, 'exception', tag)
    data = exception_hist_provider(file_path, step=int(step))

    if data:
        return {step: data}
    else:
        raise ValueError('No such data')


def get_exception_box_data(request):
    params = ['uid', 'trainJobName', 'run', 'tag', 'step', 'up', 'down']
    uid, trainJobName, run, tag, step, up, down = get_api_params(request, params)

    file_path = get_file_path(uid, run, 'exception', tag)
    data = exception_box_provider(file_path, step=int(step), limit=[float(up), float(down)])

    if data:
        return {step: data}
    else:
        raise ValueError('No such data')
