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
import time
import atexit
from tsvis.parser.utils import logfile_utils
from tsvis.parser.loader.lazy_load import LazyLoad
from multiprocessing import Process, Queue
from pathlib import Path
from shutil import rmtree
from tsvis.parser.loader.dictionary_watcher import start_run_watcher
from tsvis.parser.utils.cache_io import CacheIO
import threading

class LogParser:
    def __init__(self, logdir, cachedir):
        self._logdir = logdir
        self._cachedir = cachedir
        self._event = threading.Event()

    def start_parse(self):
        if Path(self._logdir).exists():
            cache_path = set_cache_path(self._cachedir)
            run_dirs = logfile_utils.get_runinfo(self._logdir)
            # 开启文件监听
            start_run_watcher('.', self._logdir, cache_path, self._event)

            # 如果有相关日志，加载日志
            process_pool = load_logs(run_dirs, cache_path)

            # 程序退出时，关闭所有进程，进程和文件IO
            atexit.register(cleanup, process_pool, cache_path, self._event)
        else:
            raise FileExistsError("No such dictionary {}".format(self._logdir))


def load_logs(run_dirs, cache_path):
    msg = '({}) starts successfully'.format(run_dirs)
    print(msg)
    comm_queue = Queue()
    start_time = time.time()

    # 给每一个run开一个进程
    process_pool = {}
    for _run, _dir in run_dirs.items():
        _ll = LazyLoad(_run, _dir, comm_queue)
        p = Process(target=_ll.init_load, args=(cache_path, True), name=_run, daemon=True)
        p.start()
        process_pool[_run] = p

    # 判断初始化加载是否完成
    finished = set(run_dirs.keys())
    assert len(finished) == len(run_dirs)
    while len(finished) > 0:
        _signal = comm_queue.get()
        finished.remove(_signal)
        if time.time() - start_time >= 30:
            break
    comm_queue.close()
    return process_pool

def set_cache_path(cache_dir):
    cache_dir = Path(cache_dir).absolute()
    if cache_dir.exists():
        rmtree(cache_dir)
    return cache_dir.absolute()

def cleanup(process_pool, cache_path, event):
    # 关闭所有run进程
    for run, p in process_pool.items():
        if p.is_alive():
            p.terminate()
            p.join()

    # 设置threading.Evnet, 关闭所有监听线程
    event.set()

    # 关闭所有已打开的文件io
    for name, f in CacheIO(None).file_io.items():
        f.close()

    # 清除缓存文件
    if cache_path.exists():
        rmtree(cache_path)
