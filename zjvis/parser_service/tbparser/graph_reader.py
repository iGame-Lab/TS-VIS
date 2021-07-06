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
from tbparser.events_reader import EventReadingError, EventsFileReader
from tensorboard.compat.proto.graph_pb2 import GraphDef
from pathlib import Path
from typing import Union


class GraphReader:
    def __init__(self,
                 logdir: Union[str, Path],
                 stop_on_error: bool = False
    ):
        self._logdir = Path(logdir)
        self._stop_on_error = stop_on_error

    def read(self):
        log_files = sorted(f for f in self._logdir.glob('*') if f.is_file())
        for file_path in log_files:
            with open(file_path, 'rb') as f:
                reader = EventsFileReader(f)
                try:
                    result = self.read_graph_def(reader)
                    if result is not None:
                        return result
                except EventReadingError:
                    if self._stop_on_error:
                        raise
                    else:
                        continue
        return

    def read_graph_def(self, events):
        for event in events:
            if event.HasField('graph_def'):
                # wall_time = event.wall_time
                graph = GraphDef()
                graph.ParseFromString(event.graph_def)
                return graph
        return None
