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
# DO NOT alter/distruct/free input object !
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import numpy as np
import six


def check_nan(array):
    tmp = np.sum(array)
    if np.isnan(tmp) or np.isinf(tmp):
        logging.warning('NaN or Inf found in input tensor.')
    return array


def make_np(x):
    if isinstance(x, list):
        return check_nan(np.array(x))
    if isinstance(x, np.ndarray):
        return check_nan(x)

    if np.isscalar(x):
        return check_nan(np.array([x]))

    if 'torch' in str(type(x)):
        return check_nan(prepare_pytorch(x))

    if 'tensorflow' in str(type(x)):
        return check_nan(prepare_tensorflow(x))

    raise NotImplementedError(
        'Got {}, but expected numpy array or torch tensor.'.format(type(x)))


def prepare_pytorch(x):
    import torch
    if isinstance(x, torch.autograd.Variable):
        x = x.data
    x = x.cpu().numpy()
    return x


def prepare_tensorflow(x):
    from caffe2.python import workspace
    x = workspace.FetchBlob(x)
    return x

