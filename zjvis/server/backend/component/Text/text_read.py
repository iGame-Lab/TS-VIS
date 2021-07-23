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


def _warp_values(values):
    mid = "</li><li>".join(list(values))
    return "<ul><li>{}</li></ul>".format(mid)


class text_read:
    """
    根据标签返回指定text数据
    args:
        logdir:文件路径
        tag：标签名
    """

    def __init__(self, data=None):
        self.data = data

    def get_data(self):
        """
        返回一个字典数组，每个字典对应一次迭代。
        """
        if self.data:
            _data = self.data
        else:
            return None

        result = []
        for items in _data:
            values = {'wall_time': items['wall_time'],
                      'step': items['step'],
                      'value': list(items['value'])
                      }
            result.append(values)
        return result

    def get_merge_data(self):
        """
        对所有数据进行合并，返回一个字典。字典的每个属性都是一个包含所有迭代数据的数组
        """
        _wall_time = []
        _step = []
        _value = []
        for items in self.data:
            _wall_time.append(items['wall_time'])
            _step.append(items['step'])
            _value.append(items['value'])

        result = {'wall_time': _wall_time,
                  'step': _step,
                  'value': _value
                  }
        return result
