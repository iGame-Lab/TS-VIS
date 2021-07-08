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
import time
sys.path.append('../service_utils')
from utils import logfile_utils
from python_io.lazy_load import LazyLoad
from multiprocessing import Process, Queue
from pathlib import Path
from shutil import rmtree

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
                load_logs(run_dirs, cache_path)
            else:
                # TODO 引发一个异常
                pass
        else:
            # TODO 引发一个异常
            pass


def load_logs(run_dirs, cache_path):
    msg = '({}) starts successfully'.format(run_dirs)
    print(msg)
    comm_queue = Queue()
    start_time = time.time()
    # 给每一个run开一个进程
    for key, val in run_dirs.items():
        _ll = LazyLoad(key, val, comm_queue)
        p = Process(target=_ll.init_load, args=(cache_path, ))
        p.start()
    while comm_queue.qsize() != len(run_dirs):
        if time.time() - start_time >= 30:
            break
        time.sleep(0.5)


def set_cache_path(cache_dir):
    cache_dir = Path(cache_dir).absolute()
    if cache_dir.exists():
        rmtree(cache_dir)
    return cache_dir.absolute()
