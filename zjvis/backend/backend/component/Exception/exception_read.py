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
import numpy as np
import math
from .histogram import Histogram


class Exception_read:
    def __init__(self, data=None, step=None):
        self.data = data
        self.step = step

    def get_histogram(self):
        for _data in self.data:
            if _data['step'] == self.step:
                # [min,max,buckets]
                res = [Histogram(_data['value']).get_data()]
                return res

    def get_flatten_shape(self, k):
        n = math.floor(pow(k / 2, 0.5))
        if n == 0:
            return 1, k

        while k % n != 0:
            n = n - 1
        m = k // n
        return n, m

    def flatten(self, data):
        shapes = data.shape
        l = len(shapes)
        if l == 1 or l == 2:
            return data
        else:
            if l == 3:
                n, m = self.get_flatten_shape(shapes[0])  # [B,W,H]
            else:
                data = data.transpose(0, 3, 1, 2)  # [B,C,W,H]
                shapes = data.shape
                n, m = self.get_flatten_shape(shapes[0] * shapes[1])
            data = data.reshape(n, m, shapes[-2], shapes[-1])  # [n,m,w,h]
            data = data.transpose(0, 2, 1, 3)  # [n,w,m,h]
            data = data.reshape(n * shapes[-2], m * shapes[-1])  # [n*w,m*h]
            return data

    def box_exception(self, data, limit=None):
        # 异常点
        data = self.flatten(data)
        up = max(limit)
        down = min(limit)
        if (up == np.nanmax(data)) and (down == np.nanmin(data)):
            return [], []

        ep = np.argwhere((data > up) | (data < down) | (np.isnan(data)))
        exception = data[ep[:, 0]].tolist() if len(data.shape) == 1 \
            else data[ep[:, 0], ep[:, 1]].tolist()
        return exception, ep.tolist()

    def box_line(self, data):
        x = data.ravel()
        # 四分位数
        p = (0, 5, 10, 25, 50, 75, 90, 95, 100)
        p_val = np.nanpercentile(x, p, interpolation='midpoint', overwrite_input=True).tolist()
        q1 = p_val[3]
        q2 = p_val[4]
        q3 = p_val[5]
        iqr = q3 - q1
        up = min(q3 + 1.5 * iqr, float(np.nanmax(x)))
        down = max(q1 - 1.5 * iqr, float(np.nanmin(x)))
        box_info = [up, q3, q2, q1, down]
        del p_val[3:6]
        return box_info, p_val

    def get_meta_data(self):
        if self.data:
            _data = self.data
        else:
            return None
        steps = []
        box_infos = []
        for i, items in enumerate(_data):
            steps.append(items['step'])
            box_info = self.box_line(items['value'])
            box_infos.append(box_info)
        res = {
            'step': steps,
            'box': box_infos
        }
        return res

    def get_data(self):
        for _data in self.data:
            if _data['step'] == self.step:
                data = _data['value']
                _shape = data.shape
                _min = data.min().tolist()
                _max = data.max().tolist()
                _mean = data.mean().tolist()
                # 变换数据数组大小到n*m
                flatten_data = self.flatten(data)
                res = [_shape, _min, _max, _mean, flatten_data.tolist()]
                return res

    def get_outlier(self, limit):
        for _data in self.data:
            if _data['step'] == self.step:
                data = _data['value']
                res = self.box_exception(data, limit)
                return res