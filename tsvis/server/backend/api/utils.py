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
import re
import urllib.parse
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, \
    JsonResponse, HttpResponse
from django.core.cache import cache

def validate_get_request(request, func, accept_params=None, args=None):
    """Check if method of request is GET and request params is legal

    Args:
         request: request data given by django
         func: function type, get request and return HTTP response
         accept_params: list type, acceptable parameter list
         args: value of parameters
    Returns:
         HTTP response
    """
    if accept_params is None:
        accept_params = []
    if args is None:
        args = []
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    elif set(accept_params).issubset(set(request.GET)):
        return func(request, *args)
    else:
        return HttpResponseBadRequest('parameter lost!')


def validate_post_request(request, func, accept_params=None, args=None):
    """Check if method of request is POST and request params is legal

    Args:
         request: request data given by django
         func: function type, get request and return HTTP response
         accept_params: list type, acceptable parameter list
         args: value of parameters
    Returns:
         HTTP response
    """
    if accept_params is None:
        accept_params = []
    if args is None:
        args = []
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    elif set(accept_params).issubset(set(request.POST)):
        return func(request, *args)
    else:
        return HttpResponseBadRequest('parameter lost!')


def get_classified_label(tags):
    category = {}
    for tag in tags:
        # 使用斜杠分割类别
        i = tag.find('/')
        _cate_name = tag[0:] if i == -1 else tag[0:i]
        if _cate_name not in category.keys():
            category[_cate_name] = [tag]
        else:
            category[_cate_name].append(tag)
    return category


def process_category(path):
    if not path.exists():
        return {}
    runs = {}
    for run in path.iterdir():
        if run.is_dir():
            key = run.name if not (run.name == 'root') else '.'
            runs[key] = get_component(run)
    return runs


def get_component(path):
    components = {'custom': ['true']}
    for component in path.iterdir():
        if component.is_dir():
            if component.name == 'hist':
                components['statistic'] = {'histogram': get_tags(component)}
            elif component.name == 'graph':
                components['graph'] = get_tags(component)
            elif component.name == 'hyperparm':
                components['hyperparm'] = ['true']
            elif component.name == 'projector':
                components['embedding'] = get_tags(component)
            elif component.name in ['image', 'audio', 'text']:
                key = component.name
                if 'media' in components.keys():
                    components['media'][key] = get_tags(component)
                else:
                    components['media'] = {key: get_tags(component)}
            elif component.name == 'scalar':
                res = get_tags(component)
                components['scalar'] = get_classified_label(res)
            else:
                key = component.name
                components[key] = get_tags(component)
    return components


def get_tags(path):
    files = []
    for file in path.iterdir():
        if file.is_file() and not ('sample' in file.name):
            tag = file.name.replace('#', '/').replace('$', ':')
            files.append(tag)
    return sorted(files, key=lambda x: sort_func(x))


def sort_func(x):
    # 获取字符串中的字母
    res1 = re.findall(r'[A-Za-z]', x)
    # 获取字符串中的数字
    res2 = re.sub("\D", "", x)
    res2 = int(float(res2)) if res2 else 0
    return res1, res2


def get_init_data(request):
    if not cache.get('finished'):
        # 从这里import不会在启动的时候加载很多东西
        from tsvis.parser.log_parser import LogParser
        from tsvis.parser.utils.vis_logging import get_logger

        logdir, cachedir = get_logger().logdir, get_logger().cachedir
        _parser = LogParser(logdir, cachedir)
        _parser.start_parse()
        cache.set('finished', True)
    return { 'msg': 'success' }


def get_category_data(request):
    from tsvis.parser.utils.vis_logging import get_logger
    cache_path = get_logger().cachedir
    res = process_category(cache_path)
    return res


def response_wrapper(fn):
    def inner(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            if not isinstance(res, HttpResponse):
                return JsonResponse({
                    'code': 200,
                    'msg': 'ok',
                    'data': res
                })
            return res
        except Exception as e:
            _tb = e.__traceback__
            _str_tb = ""
            while _tb:
                _st = "in {}, at line {} \n".format(_tb.tb_frame.f_globals["__file__"],
                                                    _tb.tb_lineno)
                _str_tb += _st
                _tb = _tb.tb_next
            msg = "{}: Trace: {}".format(str(e), _str_tb)
            import logging
            logging.error(msg)
            return JsonResponse({
                'code': 500,
                'msg': msg,
                'data': ""
            })

    return inner


def get_api_params(request, params):
    res = {}
    for params_name in params:
        p = request.GET.get(params_name)
        if not p:
            msg = "{} :Parameter request error, parameter '{}' not found" \
                .format(request.path, params_name)
            raise ValueError(msg)
        else:
            res[params_name] = p

    ret = list(res.values())
    # 对url编码的字符串进行解码
    for i, r in enumerate(ret):
        ret[i] = urllib.parse.unquote(r)
        if '%' in ret[i]:
            ret[i] = urllib.parse.unquote(ret[i])
    # 只有一个结果则不返回列表
    ret = ret[0] if len(ret) == 1 else ret
    return ret
