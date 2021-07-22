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
from queue import Queue

from loader.logfile_loader import Trace_Thread
from utils.logfile_utils import is_available_flie

class LazyLoad:
    def __init__(self, run: str, rundir: Union[str, Path], comm = None):
        self.run = run
        self.rundir = rundir
        self.comm = comm

    # 惰性加载，在初始化的时候加载目前日志中的所有数据
    def init_load(self, cache_path, is_init=False):

        files = [f for f in self.rundir.glob("*") if is_available_flie(f)]

        # 构建线程间通信的队列
        comm_queue = Queue()
        finished = set()
        for file in files:
            _thread = Trace_Thread(self.run, file, cache_path, comm_queue, is_init, daemon=False)
            _thread.start()

            finished.add(file.name)

        # 判断是否完成初始化加载
        if is_init:
            assert len(finished) == len(files)
            while len(finished) >0 :
                _signal = comm_queue.get()
                finished.remove(_signal)
            comm_queue.queue.clear()

            # 通知解析服务主进程，该run文件夹已完成加载
            assert self.comm is not None, f'{self.__name__}.comm must be a Queue in init stage.'
            self.comm.put(self.run)
