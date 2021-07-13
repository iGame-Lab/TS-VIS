# -*- coding: utf-8 -*-
# @Time    : 2021/7/7 21:33
# @Author  : MSH
# @FileName: vis_logging.py
# @Software: PyCharm
from absl import flags
from pathlib import Path

class VisLogging:
    _instance = None

    # 保证只有一个单例
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, path):
        self._logging_path = Path(path)
        self._cache_path = self._logging_path.parent / "__viscache__"

    @property
    def logdir(self):
        return self._logging_path

    @property
    def cachedir(self):
        return self._cache_path


_logging = VisLogging(flags.FLAGS.logdir)

def get_logger():
    return _logging
