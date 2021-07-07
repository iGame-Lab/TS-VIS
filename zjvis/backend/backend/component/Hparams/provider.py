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
from .hparams_read import hparams_read
from utils.vis_logging import get_logger
from utils.logfile_utils import path_parser
from backend.api.utils import get_api_params


def hparams_provider(run):
    file_path1 = path_parser(get_logger().cachedir, run, 'hyperparm', 'hparams')
    _data = CacheIO(file_path1).get_cache()
    return hparams_read(_data, None).get_data()


def get_hparams_data(request):
    params = ['run']
    run = get_api_params(request, params)
    return hparams_provider(run=run)
