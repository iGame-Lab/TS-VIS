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
import json
from io import BytesIO
from pathlib import Path
from queue import Queue
from tbparser import SummaryReader
from tbparser import Projector_Reader
from utils.cache_io import CacheIO
from utils.logfile_utils import path_parser
import pickle


class Trace_Thread(threading.Thread):
    def __init__(self, runname, filename, current_size, cache_path, comm: Queue):
        threading.Thread.__init__(self, name=filename.name)
        self.runname = runname
        self.cache_path = cache_path
        self.filename = filename
        self.current_size = current_size
        self.comm = comm
        # 该日志中是否有超参数
        self.has_hparams = False
        self.first_write = False
        self.metrics = []

    def run(self):
        print('监听文件 %s' % self.filename)
        self.trace(self.current_size)

    def trace(self, current_size):
        filename = Path(self.filename)
        if filename.suffix == ".json":
            self.load_model_file(filename)
            # 已完成graph文件解析，将完成标志放入队列
            self.comm.put({self.name: True})
            return
        f = open(filename, "rb")
        # for event file
        if "event" in filename.name:
            _io = BytesIO(f.read(current_size))
            self.load_event_file(_io)
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
        # for projector file
        elif "projector" in filename.name:
            self.load_projector_file(f)
            # 已完成projector文件解析，将完成标志放入队列
            self.comm.put({self.name: True})

    def set_cache(self, file_name, data):
        if not file_name.parent.exists():
            file_name.parent.mkdir(parents=True, exist_ok=True)
        with open(file_name, 'ab') as f:
            pickle.dump(data, f)
            f.close()

    def load_event_file(self, fileIO):
        reader = SummaryReader(fileIO, types=[
            'scalar',
            'graph',
            'hist',
            'text',
            'image',
            'audio',
            'hparams'
        ])
        for items in reader:
            if items.type == "graph":
                file_path = path_parser(self.cache_path, self.runname, items.type, tag='c_graph')
                CacheIO(file_path).set_cache(data=items.value)
                continue
            elif items.type == "hparams":
                file_path = path_parser(self.cache_path, self.runname,
                                        type='hyperparm', tag='hparams')
                self.set_cache(file_name=file_path, data=items.value)
                continue

            item_data = {
                'step': items.step,
                'wall_time': items.wall_time,
                'value': items.value,
                'type': items.type
            }
            file_path = path_parser(self.cache_path, self.runname,
                                    type=items.type,
                                    tag=items.tag)
            CacheIO(file_path).set_cache(data=item_data)

    def load_projector_file(self, fileIO):
        p_reader = Projector_Reader(fileIO).read()
        for items in p_reader.projectors:
            item_data = {
                'step': items.step,
                'wall_time': items.wall_time,
                'value': items.value.reshape(items.value.shape[0], -1)
                if items.value.ndim > 2 else items.value,
                'label': items.label,
            }
            file_path = path_parser(self.cache_path, self.runname,
                                    type=p_reader.metadata.type,
                                    tag=items.tag)
            CacheIO(file_path).set_cache(data=item_data)
        if p_reader.sample:
            file_path = path_parser(self.cache_path, self.runname,
                                    type="embedding",
                                    tag="sample_" + items.tag)
            CacheIO(file_path).set_cache(data=p_reader.sample)

    def filter_graph(self, file):
        variable_names = {}
        graph = json.loads(file)
        for sub_graph in graph:
            cfg = sub_graph["config"]
            # 拷贝一份，用于循环
            cfg_copy = cfg["layers"].copy()
            for layer in cfg_copy:
                if layer["class_name"] == "variable":
                    _name = layer["name"]
                    variable_names[_name] = layer
                    cfg["layers"].remove(layer)
        # 第二遍循环，删除`variable_names`出现在`inbound_nodes`中的名字
        for sub_graph in graph:
            cfg = sub_graph["config"]
            for layer in cfg["layers"]:
                in_nodes = layer["inbound_nodes"]
                in_nodes_copy = in_nodes.copy()
                for node in in_nodes_copy:
                    # 在里面则删除
                    if node in variable_names.keys():
                        in_nodes.remove(node)
        graph_str = json.dumps(graph)
        return graph_str

    def load_model_file(self, file):
        with open(file, "r") as f:
            # 结构图内容
            _cg_content = f.read()
            _sg_content = self.filter_graph(_cg_content)
            # caclulate_graph.json
            sg_file_path = path_parser(self.cache_path, self.runname,
                                       type="graph",
                                       tag="s_graph")
            cg_file_path = path_parser(self.cache_path, self.runname,
                                       type="graph",
                                       tag="c_graph")
            CacheIO(sg_file_path).set_cache(data=_sg_content)
            CacheIO(cg_file_path).set_cache(data=_cg_content)
