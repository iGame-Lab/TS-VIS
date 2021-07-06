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


class image_read:
    def __init__(self, data=None, step=None):
        self.data = data
        self.step = step

    def get_meta_data(self):
        if self.data:
            _data = self.data
        else:
            return None
        result = []
        for items in _data:
            values = {'wall_time': items['wall_time'],
                      'step': items['step'],
                      'width': items['value']['width'],
                      'height': items['value']['height']
                      }
            result.append(values)
        return result

    def get_data(self):
        for _data in self.data:
            if _data['step'] == self.step:
                return _data['value']['encoded_image_string']
