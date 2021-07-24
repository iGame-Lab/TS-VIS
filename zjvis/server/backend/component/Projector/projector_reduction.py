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
from sklearn.decomposition import PCA
import numpy as np
from tsne import bh_sne


class projector_reduction:
    def __init__(self, data, method, dimension=None):
        self.data = self.data_preprocess(data)
        self.method = method
        if dimension is None:
            self.dimension = 2
        else:
            self.dimension = dimension

    def data_preprocess(self, data):
        data = np.array(data)
        _ndim = data.ndim
        if _ndim == 2:
            pass
        elif _ndim > 3:
            data = data.reshape(data.shape[0], -1)
        else:
            raise ValueError('The processed data dimension should be >=2, '
                             'but the dimension given is {}'.format(_ndim))
        return data

    def Pca(self):
        pca = PCA(n_components=self.dimension)  # 确定想要的维度 PCA
        return pca.fit_transform(self.data).tolist()  # 得到处理的结果

    def Tsne(self):
        if self.dimension > 3:
            raise ValueError('The dimension of the tsne method must be 2 or 3')
        _data = np.array(self.data)
        seed = np.random.RandomState(0)

        perplexity = _data.shape[0] // 4 if _data.shape[0] < 100 else 30
        data = bh_sne(_data, pca_d=True, d=self.dimension, perplexity=perplexity, random_state=seed)
        return data.tolist()

    def get_data(self):
        if self.method == 'pca':
            return self.Pca()
        elif self.method == 'tsne':
            return self.Tsne()
        else:
            return
