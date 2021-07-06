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
import os
from watchdog.observers.polling import PollingObserver
from watchdog.events import *
from python_io.logfile_loader import Trace_Thread
from .logfile_utils import *


class Watcher_Handler(FileSystemEventHandler):
    def __init__(self, run, uid, cache_path):
        self.runname = run
        self.uid = uid
        self.cache_path = cache_path

    def on_created(self, event):
        print("创建--> %s" % event.src_path)
        filename = Path(event.src_path)
        if filename.is_file():
            if is_available_flie(event.src_path):
                current_size = os.path.getsize(event.src_path)
                Trace_Thread(self.runname, filename, current_size,
                             self.uid, self.cache_path).start()
            else:
                print("非有效日志文件 %s" % filename.name)
        else:
            pass


def start_run_watcher(run, path, uid, cache_path):
    event_handler = Watcher_Handler(run, uid, cache_path)
    observer = PollingObserver()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
