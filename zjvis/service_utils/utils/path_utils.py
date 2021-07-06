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
from pathlib import Path
from .redis_utils import RedisInstance
from .config_utils import ConfigInstance


def id2logdir(uid, trainJobName):
    _base = Path(ConfigInstance.conf_logdir_base()).absolute()
    log_dir = _base / uid / trainJobName / "visualizedlog"
    try:
        int(uid)
    except ValueError:
        _base = Path("../demo_logs").absolute()
        log_dir = _base / uid / "logs"

    cache_dir = Path("../__cache__").absolute() / uid / trainJobName
    return log_dir, cache_dir


def get_file_path(uid, run, type, tag):
    _key = uid + '_' + run + '_' + type + '_' + tag
    try:
        _res = RedisInstance.get(_key)
        _path = Path(RedisInstance.get(_res))
    except TypeError:
        raise OSError('Redis key {} not found according to request '
                      'parameters, please check the parameters\n _path={}'
                      .format(_key, _res))
    return _path


def path_parser(cache_path, run, type, tag):
    run = run if not (run == '.') else 'root'
    tag = tag.replace('/', '#').replace(':', '$')
    file_path = cache_path / run / type / tag
    return file_path
