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
from django.http import JsonResponse


def session_middleware(get_response):
    def middleware(request):
        _sid = request.session.session_key
        _session = request.session.get(_sid, '')
        if request.path != '/api/init' and request.path != '/':
            if not _session:
                return JsonResponse({
                    'code': 500,
                    'msg': "session已过期或未登录，请刷新页面重试",
                    'data': ""
                }, json_dumps_params={'ensure_ascii': False})
        response = get_response(request)
        return response
    return middleware
