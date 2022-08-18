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
import json
from tsvis.parser.utils.cache_io import CacheIO
from tsvis.parser.utils.logfile_utils import path_parser
from .graph_read import get_data as graph_get_data
from .s_graph_read import get_s_graph_data
from .graph import graph_op
from tsvis.server.backend.api.utils import get_api_params
from .graph_read import filter

def graph_provider(file_path, tag):
    res = CacheIO(file_path).get_cache()
    if res:
        if tag == "c_graph":
            # if isinstance(res, str):
            #     data = get_s_graph_data(res)
            # else:
            data, _ = graph_get_data(res)
            return {
                'net': data,
                'operator': graph_op
            }
        else:
            g, graph = graph_get_data(res)
            return {
                'net': [filter(g, graph)],
                'operator': graph_op
            }
    else:
        raise ValueError('Parameter error, no data found')


def get_graph_data(request):
    params = ['run', 'tag']  #type = "c_graph":获取计算图数据 type = "s_graph" :获取结构图数据
    run, tag = get_api_params(request, params)

    from tsvis.parser.utils.vis_logging import get_logger
    file_path = path_parser(get_logger().cachedir, run, 'graph', "c_graph")
    return json.dumps(graph_provider(file_path, tag))
