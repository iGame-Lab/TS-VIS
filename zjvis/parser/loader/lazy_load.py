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
from typing import Union
import os
from queue import Queue

from loader.dictionary_watcher import start_run_watcher
from loader.logfile_loader import Trace_Thread
from utils.logfile_utils import is_available_flie


class LazyLoad:
    def __init__(self, run: str, rundir: Union[str, Path], comm):
        self.run = run
        self.rundir = rundir
        self.comm = comm

    # 惰性加载，在初始化的时候加载目前日志中的所有数据
    def init_load(self, cache_path):
        # 开启文件监听
        start_run_watcher(self.run, str(self.rundir), cache_path)
        files = [f for f in self.rundir.glob("*") if is_available_flie(f)]
        thread_pool = {}
        # 线程间通信的队列
        comm_queue = Queue()
        for file in files:
            thread_pool[file.name] = object()
            current_size = os.path.getsize(str(file))
            _thread = Trace_Thread(self.run, file, current_size, cache_path, comm_queue)
            _thread.start()

        assert len(thread_pool) == len(files)
        while len(thread_pool):
            _signal = comm_queue.get()
            thread_pool.pop(_signal)
        comm_queue.queue.clear()
        self.comm.put(self.run)
