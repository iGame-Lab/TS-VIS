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
import time
import threading
from pathlib import Path
from tsvis.parser.visparser import SummaryReader
from tsvis.parser.utils.cache_io import CacheIO
from tsvis.parser.utils.logfile_utils import path_parser
from tsvis.parser.visparser.event_parser import filter_graph


class Trace_Thread(threading.Thread):
    def __init__(self, runname, filename, cache_path, comm=None,
                 is_init=False, event=None, daemon=True):
        threading.Thread.__init__(self, name=filename.name)
        self.daemon = daemon
        self.runname = runname
        self.cache_path = cache_path
        self.filename = filename
        self.comm = comm
        self.is_init = is_init
        self.event = event

    def run(self):
        print('监听文件 %s' % self.filename)
        self.trace()

    def trace(self):
        filename = Path(self.filename)
        if filename.suffix == ".json":
            with open(filename, "r") as f:
                # 结构图内容
                _cg_content = f.read()
                _sg_content = filter_graph(_cg_content)
                # caclulate_graph.json
                sg_file_path = path_parser(self.cache_path, self.runname,
                                           category="graph", tag="s_graph")
                # cg_file_path = path_parser(self.cache_path, self.runname,
                #                            category="graph", tag="c_graph")

                CacheIO(sg_file_path).set_cache(data=_sg_content)
                # CacheIO(cg_file_path).set_cache(data=_cg_content)
            # 已完成graph文件解析，将完成标志放入队列
            if self.comm:
                self.comm.put(self.name)
            return

        # for event file
        if "event" in filename.name:
            fd = open(filename, "rb")
            while True:
                reader = SummaryReader(fd)
                for items in reader:
                    if items['type'] == "graph":
                        file_path = path_parser(self.cache_path, self.runname,
                                                items['type'], tag='c_graph')
                        CacheIO(file_path).set_cache(data=items['value'])
                    elif items['type'] == "hparams":
                        file_path = path_parser(self.cache_path, self.runname,
                                                'hyperparm', tag='hparams')
                        CacheIO(file_path, mod='ab').set_cache(data=items['value'])
                    else:
                        file_path = path_parser(self.cache_path, self.runname,
                                                items['type'], tag=items['tag'])
                        CacheIO(file_path).set_cache(data=items)

                # print(self.name + " is finish parsing")
                # 已完成event文件解析，将完成标志放入队列
                if self.is_init and self.comm:
                    self.comm.put(self.name)
                    self.is_init = False

                # 线程是否结束
                if isinstance(self.event, threading.Event) and self.event.is_set():
                    break
                else:
                    time.sleep(1)
