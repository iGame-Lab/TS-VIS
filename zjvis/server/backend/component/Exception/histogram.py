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


class Histogram:
    def __init__(self, data, buckets_count=None):
        self.data = data
        self.buckets_count = buckets_count

    def auto_ranges(self, _min, _max):
        _range = [_min]
        temp = max(np.finfo(np.float64).eps, _min) * 1.1
        while temp < _max:
            _range.append(temp)
            temp = temp * 1.1
        _range.append(_max)
        return np.array(_range)

    def buckets(self, left, right, counts):
        left = left.reshape(-1, 1)
        right = right.reshape(-1, 1)
        counts = counts.reshape(-1, 1)
        res = np.concatenate((left, right, counts), axis=1)
        return res

    def auto_buckets(self, data):
        # 根据数据分布自动设置区间大小
        _min = data.min().tolist()
        _max = data.max().tolist()
        abs_min = np.abs(data).min().tolist()
        if _min < 0 and _max > 0:
            _range = self.auto_ranges(abs_min, _max)
            neg_range = 0 - self.auto_ranges(abs_min, -_min)[::-1]  # reverse
            ranges = np.append(neg_range, _range)
        elif _min >= 0:
            ranges = self.auto_ranges(_min, _max)
        elif _max <= 0:
            ranges = 0 - self.auto_ranges(0 - _max, 0 - _min)[::-1]
        else:
            ranges = None

        if len(ranges) == 1:  # 统计数据都为一个常数
            ranges.append(ranges[0])
        counts, buckets_limit = np.histogram(data, bins=ranges)
        buckets = self.buckets(buckets_limit[:-1], buckets_limit[1:], counts).tolist()
        return _min, _max, buckets

    def specified_buckets(self, data, buckets_count):
        counts, buckets_limit = np.histogram(data, bins=buckets_count)
        _min = buckets_limit[0].tolist()
        _max = buckets_limit[-1].tolist()
        buckets = self.buckets(buckets_limit[:-1], buckets_limit[1:], counts).tolist()
        return _min, _max, buckets

    def get_data(self):
        data = np.array(self.data).ravel()  # flatten
        if data.size == 0:
            return [0], [0]

        if self.buckets_count is None:
            # 自动设置区间
            return self.auto_buckets(data)
        else:
            return self.specified_buckets(data, self.buckets_count)
