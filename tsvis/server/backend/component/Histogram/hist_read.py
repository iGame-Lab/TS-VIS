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
import random
import numpy as np

class histogram_read:
    def __init__(self, data=None, samples=None):
        self.samples = samples
        self.data = data  # 原始数据

    def hist_bucket(self, item):
        """
        Construct buckets of histogram based on the parsed data for each step
        Args:
              item: Histogram data for each step
        Returns:
              bucket: Histogram data with buckets for each step
        """
        bucket_min = item['value']['min']
        bucket_max = item['value']['max']
        bucket_limit = item['value']['bucket_limit']
        bucket_num = item['value']['bucket']
        bucket = []
        L = len(bucket_limit)
        for i in range(L):
            if i == 0:
                bucket.append([bucket_min, bucket_limit[i], bucket_num[i]])
            elif i == L - 1:
                bucket.append([bucket_limit[i - 1], bucket_max, bucket_num[i]])
            else:
                bucket.append([bucket_limit[i - 1], bucket_limit[i], bucket_num[i]])

        return bucket

    def frontend_data(self, item):
        """
        Construct a histogram data format delivered to the front for each step
        Args:
              item: Histogram data for each step
        Returns:
              hist_data: Histogram data with front-end delivery format for each step
        """
        step = item['step']
        wall_time = item['wall_time']
        value_min = item['value']['min']
        value_max = item['value']['max']
        value = self.hist_bucket(item)
        hist_data = [wall_time, step, value_min, value_max, value]
        return hist_data

    def downsample(self, hist_value, k):
        """
        Downsampling data according to parameter k
        Args:
              hist_value: Histogram data with all steps
              k: Number of downsampling
        Returns:
              sample: Downsampled data
        """
        L = len(hist_value)
        if k >= L:
            return hist_value

        rng = random.Random(0)
        index = rng.sample(range(L), k)
        index = sorted(index)
        sample = [hist_value[i] for i in index]

        return sample

    def get_data(self):
        """
        Return the corresponding data according to the tag name, which can be directly interacted with the front
        Returns:
            hist_value: Histogram data
        """
        if self.data:
            steps = len(self.data)
            if steps > 50:
                idx = np.linspace(0, steps-1, 50, dtype=np.int)
                _data = [self.data[i] for i in idx]
            else:
                _data = self.data
        else:
            return None

        hist_value = []
        for items in _data:
            if type(items['value']) == dict:  # tensorflow summary
                hist_value.append(self.frontend_data(items))
            else:  # tendorboard summary
                value_min = items['value'][0, 0]
                value_max = items['value'][-1, 1]
                hist_value.append([items['wall_time'], items['step'], value_min, value_max, items['value'].tolist()])
        if self.samples is not None:
            hist_value = self.downsample(hist_value, self.samples)

        return hist_value
