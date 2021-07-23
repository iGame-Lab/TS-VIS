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
__all__ = [
    "get_scalar_data", "get_histogram_data", "get_distribution_data",
    "get_text_data", "get_audio_meta_data", "get_audio_data",
    "get_image_meta_data", "get_image_data", "get_graph_data",
    "get_hparams_data", "get_projector_meta_data", "get_projector_raw_data",
    "get_projector_sample_data", "get_projector_data", "get_exception_meta_data",
    "get_exception_data", "get_exception_hist_data", "get_exception_box_data"
           ]

from backend.component.Audio.provider import get_audio_meta_data, \
    get_audio_data
from backend.component.Distribution.provider import get_distribution_data
from backend.component.Exception.provider import get_exception_meta_data, \
    get_exception_data, get_exception_hist_data, get_exception_box_data
from backend.component.Graph.provider import get_graph_data
from backend.component.Histogram.provider import get_histogram_data
from backend.component.Hparams.provider import get_hparams_data
from backend.component.Image.provider import get_image_meta_data,\
    get_image_data
from backend.component.Projector.provider import get_projector_meta_data, \
    get_projector_raw_data, get_projector_sample_data, get_projector_data
from backend.component.Scalar.provider import get_scalar_data
from backend.component.Text.provider import get_text_data
