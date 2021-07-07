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
import sys
sys.path.append('../service_utils')
from utils import logfile_utils
from python_io.lazy_load import LazyLoad
from multiprocessing import Process
from pathlib import Path
from shutil import rmtree
from utils.redis_utils import RedisInstance
import json


def load_logs(run_dirs, cache_path):
    msg = '({}) starts successfully'.format(run_dirs)
    print(msg)
    for key, val in run_dirs.items():
        LazyLoad(key, val).init_load(cache_path=cache_path)


def set_cache_path(cache_dir):
    cache_dir = Path(cache_dir).absolute()
    if cache_dir.exists():
        rmtree(cache_dir)
    return cache_dir.absolute()
#
#
# class Master:
#     def __init__(self):
#         self.file_parsers = {}
#         self.r = RedisInstance
#         self.r.flushdb()
#
#     def set_parser(self, uid, log_dir, cache_dir):
#         if Path(log_dir).exists():
#             run_dirs = logfile_utils.get_runinfo(log_dir)
#             if run_dirs:
#                 if uid in self.file_parsers.keys():
#                     msg = "User {} has already started".format(uid)
#                     RedisInstance.lpush('parser_statu' + uid, json.dumps(
#                         {'code': 200, 'msg': msg}
#                     ))
#                     print(msg)
#                     return
#                 cache_path = set_cache_path(cache_dir)
#                 self.r.set(uid, str(cache_path))
#                 p = Process(target=load_logs, args=(uid, run_dirs, cache_path))
#                 p.start()
#                 self.file_parsers[uid] = p
#             else:
#                 msg = 'No related logs found'
#                 RedisInstance.lpush('parser_statu' + uid, json.dumps(
#                     {'code': 500, 'msg': msg}
#                 ))
#                 print(msg)
#         else:
#             msg = 'User does not exist or log path not found error: {}'\
#                 .format(log_dir)
#             RedisInstance.lpush('parser_statu' + uid, json.dumps(
#                 {'code': 500, 'msg': msg}
#             ))
#             print(msg)
#
#     def kill_parser(self, uid):
#         if uid in self.file_parsers.keys():
#             cache_path = Path(self.r.get(uid))
#             self.file_parsers[uid].terminate()
#             # 清除redis缓存
#             for key in self.r.keys(uid + '*'):
#                 self.r.delete(key)
#             import time
#             time.sleep(2)  # 等待file_parsers线程关闭
#             if not self.file_parsers[uid].is_alive():
#                 self.file_parsers.pop(uid)
#                 if cache_path.exists():
#                     rmtree(cache_path)
#                 print('({}) terminates successfully'.format(uid))
#
#     def run_server(self):
#         while True:
#             _, request = self.r.brpop('sessions')
#             request = json.loads(request)
#             if request['type'] == 'run':
#                 uid = request['uid']
#                 logdir = request['logdir']
#                 cachedir = request['cachedir']
#                 self.set_parser(uid, logdir, cachedir)
#             elif request['type'] == 'kill':
#                 uid = request['uid']
#                 self.kill_parser(uid)
#             else:
#                 print('Unrecognized request')

class LogParser:
    def __init__(self, logdir, cachedir):
        self._logdir = logdir
        self._cachedir = cachedir

    def start_parse(self):
        if Path(self._logdir).exists():
            cache_path = set_cache_path(self._cachedir)
            run_dirs = logfile_utils.get_runinfo(self._logdir)
            # 如果有相关日志
            if run_dirs:
                p = Process(target=load_logs, args=(run_dirs, cache_path))
                p.start()
            else:
                # TODO 引发一个异常
                pass
        else:
            # TODO 引发一个异常
            pass
