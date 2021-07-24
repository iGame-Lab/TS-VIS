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

from backend.component.Histogram.hist_read import histogram_read

DISTRIBUTION_BPS = (0, 668, 1587, 3085, 5000, 6915, 8413, 9332, 10000)


class distribution_read:
    def __init__(self, samples=None, data=None):
        self.samples = samples
        self.data = data  # 原始数据

    def hist_to_dist(self, buckets, bps=DISTRIBUTION_BPS):
        """
        直方图数据转换为分布图数据
        args:
            buckets:直方图区间
            bps:分步数
        """
        if not len(buckets):
            return [[k, 0.0] for k in bps]

        buckets = np.array(buckets)
        edges_min = buckets[0][0]
        edges_max = buckets[-1][1]
        counts = buckets[:, 2]
        edges = list(buckets[:, 1])
        if counts.sum:
            weights = counts.cumsum()  # 区间散落从小到大的数值累加
            rate = bps[-1] / weights[-1]  # 加权比率(映射到bps)
            weights = weights * rate

        dist_data = []
        for i in range(len(bps)):
            index = np.searchsorted(weights, bps[i], side='right')  # 计算bps分布对应的加权区间索引,最后一个符合条件的下标
            if index < len(weights):  # 判断加权区间索引是否存在
                weights_cumsum = weights[index]
                right_edge = min(edges[index], edges_max)
            else:  # index =len(weights)时，对应的bps是10000
                break
            # 获取前一个累积权值和区间左端点
            if index == 0:
                weights_cumsum_pre = 0.0
                left_edge = max(edges[0], edges_min)
            else:
                while (index - 2) >= 0 and weights[index - 2] == weights[index - 1]:
                    index = index - 1
                weights_cumsum_pre = weights[index - 1]
                left_edge = max(edges[index - 1], edges_min)

            # 根据权重得到bps对应的区间坐标
            weight = self.compress(bps[i], weights_cumsum_pre, weights_cumsum, left_edge, right_edge)
            dist_data.append([bps[i], weight])

        while i < len(bps):
            dist_data.append([bps[i], edges_max])
            i += 1

        return dist_data

    def compress(self, x, weights_cumsum_pre, weights_cumsum, left_edge, right_edge):
        """
        区间合并，返回当前点x所在的刻度
        """
        weight_width = weights_cumsum - weights_cumsum_pre
        bucket_width = float(right_edge - left_edge)
        bucket = left_edge + (x - weights_cumsum_pre) * bucket_width / weight_width
        return bucket

    def get_data(self):
        """
        返回distribution数据
        return:
            dist数组
        """
        global _data
        if self.data:
            _data = histogram_read(samples=self.samples, data=self.data).get_data()
        else:
            return None

        result = []
        for hist in _data:
            (wall_time, step, value_min, value_max, buckets) = hist
            dist_data = self.hist_to_dist(buckets)
            result.append([wall_time, step, dist_data])
        return result
