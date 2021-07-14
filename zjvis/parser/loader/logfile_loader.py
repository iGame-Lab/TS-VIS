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
import threading
from pathlib import Path
from queue import Queue
from visparser import SummaryReader
from utils.cache_io import CacheIO
from utils.logfile_utils import path_parser
from visparser.event_parser import filter_graph


class Trace_Thread(threading.Thread):
    def __init__(self, runname, filename, current_size, cache_path, comm: Queue):
        threading.Thread.__init__(self, name=filename.name)
        self.runname = runname
        self.cache_path = cache_path
        self.filename = filename
        self.current_size = current_size
        self.comm = comm
        self.first_write = False

    def run(self):
        print('监听文件 %s' % self.filename)
        self.trace(self.current_size)

    def trace(self, current_size):
        filename = Path(self.filename)
        if filename.suffix == ".json":
            with open(filename, "r") as f:
                # 结构图内容
                _cg_content = f.read()
                _sg_content = filter_graph(_cg_content)
                # caclulate_graph.json
                sg_file_path = path_parser(self.cache_path, self.runname,
                                           category="graph", tag="s_graph")
                cg_file_path = path_parser(self.cache_path, self.runname,
                                           category="graph", tag="c_graph")

                CacheIO(sg_file_path).set_cache(data=_sg_content)
                CacheIO(cg_file_path).set_cache(data=_cg_content)
            # 已完成graph文件解析，将完成标志放入队列
            self.comm.put({self.name: True})
            return

        # for event file
        elif "event" in filename.name:
            fd = open(filename, "rb")
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
            self.comm.put({self.name: True})

            # TODO 为什么写不进去？只有退出了才可以写进去内容
            # while True:
            #     rest = f.read()
            #     if not rest:
            #         time.sleep(2)
            #         continue
            #     _io = BytesIO(rest)
            #     self.load_event_file(_io)
