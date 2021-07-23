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


def histogram(data, buckets_count=None):
    def auto_ranges(_min, _max):
        _range = [_min]
        temp = _min * 1.1
        while temp < _max:
            _range.append(temp)
            temp = temp * 1.1
        _range.append(_max)
        return np.array(_range)

    def merge_zero(counts, buckets_limit):
        # 合并相邻统计值为0的区间，减少写入日志大小
        delete_index = []
        for index, x in enumerate(counts[1:], start=1):
            if x == 0 and counts[index - 1] == 0:
                delete_index.append(index)
        counts = np.delete(counts, delete_index)
        buckets_limit = np.delete(buckets_limit, delete_index)

        return buckets_limit, counts

    def auto_buckets(data):
        # 根据数据分布自动设置区间大小
        _min = data.min()
        _max = data.max()
        abs_min = np.min(np.abs(data))

        if _min < 0 and _max > 0:
            _range = auto_ranges(abs_min, _max)
            neg_range = 0 - auto_ranges(abs_min, -_min)[::-1]  # reverse
            ranges = np.append(neg_range, _range)
        elif _min >= 0:
            ranges = auto_ranges(_min, _max)
        elif _max <= 0:
            ranges = 0 - auto_ranges(0 - _max, 0 - _min)[::-1]

        if len(ranges) == 1:  # 统计数据都为一个常数
            ranges.append(ranges[0])
        counts, buckets_limit = np.histogram(data, bins=ranges)
        buckets_limit, counts = merge_zero(counts, buckets_limit)

        return _min, _max, buckets_limit[1:], counts

    def specified_buckets(data, buckets_count):
        counts, buckets_limit = np.histogram(data, bins=buckets_count)
        buckets_limit, counts = merge_zero(counts, buckets_limit)
        _min = buckets_limit[0]
        _max = buckets_limit[-1]
        return _min, _max, buckets_limit[1:], counts

    data = np.array(data).ravel()  # flatten
    if data.size == 0:
        return [0], [0]

    if buckets_count is None:
        # 自动设置区间
        return auto_buckets(data)
    else:
        return specified_buckets(data, buckets_count)
