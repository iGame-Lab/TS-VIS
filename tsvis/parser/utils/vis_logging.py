# -*- coding: utf-8 -*-
# @Time    : 2021/7/7 21:33
# @Author  : MSH
# @FileName: vis_logging.py
# @Software: PyCharm
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
