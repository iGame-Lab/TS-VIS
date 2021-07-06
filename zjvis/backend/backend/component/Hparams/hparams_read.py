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
def get_proto_value(value):
    _data = None
    if value.HasField("number_value"):
        _data = value.number_value
    elif value.HasField("string_value"):
        _data = value.string_value
    elif value.HasField("bool_value"):
        _data = value.bool_value
    return _data


class hparams_read:
    """
    返回hparams数据
    args:
        data:内存中的超参数数据
    """

    def __init__(self, data=None, scalar_data=None):
        self.data = data
        self.scalar_data = scalar_data
        self.res = {"hparamsInfo": [], "metrics": []}

    def get_data(self):
        _data = self.data
        if not _data:
            return None
        self.parse_hparams()
        return self.res

    def parse_hparams(self):
        # 先添加metrics的tag
        for i in range(len(self.data[0].session_start_info.metrics)):
            self.res['metrics'].append({'tag': '', 'value': []})
        # 再添加metrics的数据
        for hp in self.data:
            group_name = hp.session_start_info.group_name
            current_hparams_info = {
                group_name: {"hparams": [], "start_time_secs": None}
            }
            session_start_info = hp.session_start_info
            for name in session_start_info.hparams:
                value = session_start_info.hparams[name]
                _data = get_proto_value(value)
                current_hparams_info[group_name]["hparams"].append({
                    "name": name,
                    "data": _data
                })
            current_hparams_info[group_name]["start_time_secs"] = \
                hp.session_start_info.start_time_secs
            for i, metric in enumerate(session_start_info.metrics):
                self.res['metrics'][i]['tag'] = metric
                value = session_start_info.metrics[metric]
                _data = get_proto_value(value)
                self.res['metrics'][i]['value'].append(_data)
            self.res["hparamsInfo"].append(current_hparams_info)
