# -*- coding: utf-8 -*-
# @Time    : 2021/7/14 11:25
# @Author  : MSH
# @FileName: test_parser.py
# @Software: PyCharm
import unittest
import sys
sys.path.append("../tsvis")
sys.path.append("../tsvis/parser")

class TestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logdir = "test_logs"
        cls.torch_log = "test_logs/events.out.FX50-PRO"

    def test_log_read(self):
        from tsvis.parser.visparser import SummaryReader
        with open(self.torch_log, "rb") as fd:
            reader = SummaryReader(fd)
            for items in reader:
                self.assertIsNotNone(items['value'])

    def test_path_parser(self):
        from tsvis.parser.utils.logfile_utils import path_parser
        from pathlib import Path
        cache_path = Path("/cache")
        _path = path_parser(cache_path, "test", category="graph", tag="s_graph")
        self.assertEqual(_path, Path("/cache/test/graph/s_graph"))

    def test_get_runinfo(self):
        from tsvis.parser.utils.logfile_utils import get_runinfo
        from pathlib import Path
        _runs = get_runinfo(self.logdir)
        self.assertEqual(_runs["."], Path(self.logdir).absolute())
        self.assertEqual(_runs["run1"], (Path(self.logdir) / "run1").absolute())
        self.assertEqual(_runs["run2"], (Path(self.logdir) / "run2").absolute())
