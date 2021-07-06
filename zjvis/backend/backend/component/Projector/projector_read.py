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


class projector_read:
    def __init__(self, data=None, step=None, index=None):
        self.data = data
        self.step = step
        self.index = index

    def get_meta_data(self):
        if self.data:
            _data = self.data
        else:
            return None
        result = []
        for items in _data:
            result.append(items['step'])
        shape = _data[0]['value'].shape
        return [result, shape]

    def get_data(self):
        # 请求指定step的原始数据
        if self.index is None:
            for _data in self.data:
                if _data['step'] == self.step:
                    return [_data['value'].tolist(), _data['label'].tolist()]
        # 请求样本索引，返回样本图像
        else:
            _data = self.data[0]
            # 获取指定step
            return {
                'val': _data['X'][self.index].squeeze(),
                'type': _data['type']
            }
