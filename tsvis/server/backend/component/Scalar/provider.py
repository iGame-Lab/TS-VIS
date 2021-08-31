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
from tsvis.parser.utils.cache_io import CacheIO
from .scalar_read import scalar_read
from tsvis.parser.utils.logfile_utils import path_parser
from tsvis.server.backend.api.utils import get_api_params


def scalar_provider(file_path):
    # read from cache
    res = CacheIO(file_path).get_cache()
    if res:
        scalar_data = scalar_read(data=res).get_data()
        return scalar_data
    else:
        raise ValueError('Parameter error, no data found')


def get_scalar_data(request):
    params = ['run', 'tag']
    run, tag = get_api_params(request, params)

    from tsvis.parser.utils.vis_logging import get_logger
    file_path = path_parser(get_logger().cachedir, run, 'scalar', tag)
    return { tag: scalar_provider(file_path) }
