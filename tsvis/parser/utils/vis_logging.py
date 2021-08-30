# -*- coding: utf-8 -*-
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
from tsvis.server.command_line import get_cmd_line
from pathlib import Path

class VisLogging:
    _instance = None

    # 保证只有一个单例
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, cmd_line):
        if cmd_line.action != "migrate":
            self._logging_path = Path(cmd_line.args.logdir).absolute()
            self._cache_path = self._logging_path.parent / "__viscache__"

    @property
    def logdir(self):
        return self._logging_path

    @property
    def cachedir(self):
        return self._cache_path


_logging = VisLogging(get_cmd_line())

def get_logger():
    return _logging
