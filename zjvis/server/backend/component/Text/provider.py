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
from zjvis.parser.utils.cache_io import CacheIO
from zjvis.parser.utils.logfile_utils import path_parser
from .text_read import text_read
from zjvis.server.backend.api.utils import get_api_params


def text_provider(file_path):
    # read from cache
    res = CacheIO(file_path).get_cache()
    if res:
        text_data = text_read(data=res)\
            .get_data()
        return text_data
    else:
        raise ValueError('Parameter error, no data found')


def get_text_data(request):
    params = ['run', 'tag']
    run, tag = get_api_params(request, params)

    from zjvis.parser.utils.vis_logging import get_logger
    file_path = path_parser(get_logger().cachedir, run, 'text', tag)
    data = text_provider(file_path)
    return {tag: data}
