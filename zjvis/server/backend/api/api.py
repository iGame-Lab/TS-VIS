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
from .utils import *
from backend.component import *
from django.views.decorators.gzip import gzip_page


@response_wrapper
def init_process(request):
    return validate_get_request(request, get_init_data)


@gzip_page
@response_wrapper
def get_category(request):
    return validate_get_request(request, get_category_data)


@gzip_page
@response_wrapper
def get_scalar(request):
    return validate_get_request(request, get_scalar_data)


@gzip_page
@response_wrapper
def get_histogram(request):
    return validate_get_request(request, get_histogram_data)


@gzip_page
@response_wrapper
def get_distribution(request):
    return validate_get_request(request, get_distribution_data)


@gzip_page
@response_wrapper
def get_text(request):
    return validate_get_request(request, get_text_data)


@gzip_page
@response_wrapper
def get_audio_meta(request):
    return validate_get_request(request, get_audio_meta_data)


@gzip_page
@response_wrapper
def get_audio(request):
    return validate_get_request(request, get_audio_data)


@gzip_page
@response_wrapper
def get_image_meta(request):
    return validate_get_request(request, get_image_meta_data)


@gzip_page
@response_wrapper
def get_image(request):
    return validate_get_request(request, get_image_data)


@gzip_page
@response_wrapper
def get_graph(request):
    return validate_get_request(request, get_graph_data)


@gzip_page
@response_wrapper
def get_hparams(request):
    return validate_get_request(request, get_hparams_data)


@gzip_page
@response_wrapper
def get_projector_meta(request):
    return validate_get_request(request, get_projector_meta_data)


@gzip_page
@response_wrapper
def get_projector_raw(request):
    return validate_get_request(request, get_projector_raw_data)


@gzip_page
@response_wrapper
def get_projector_sample(request):
    return validate_get_request(request, get_projector_sample_data)


@gzip_page
@response_wrapper
def get_projector(request):
    return validate_get_request(request, get_projector_data)


@gzip_page
@response_wrapper
def get_exception_meta(request):
    return validate_get_request(request, get_exception_meta_data)


@gzip_page
@response_wrapper
def get_exception(request):
    return validate_get_request(request, get_exception_data)


@gzip_page
@response_wrapper
def get_exception_hist(request):
    return validate_get_request(request, get_exception_hist_data)


@gzip_page
@response_wrapper
def get_exception_box(request):
    return validate_get_request(request, get_exception_box_data)
