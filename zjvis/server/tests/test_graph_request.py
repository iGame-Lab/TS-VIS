# -*- coding: utf-8 -*-
# @Time    : 2021/7/18 23:22
# @Author  : MSH
# @FileName: test_graph_request.py
# @Software: PyCharm
from django.test import TestCase
import json

class TestGraphRequest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def init_test(self):
        if getattr(self, "category", None) is None:
            _init_res = self.client.get("/api/init", format="json")
            self.assertEqual(_init_res.status_code, 200)
            _init_json = json.loads(_init_res.content)
            self.assertEqual(_init_json["code"], 200)

            _cate_res = self.client.get("/api/getCategory", format="json")
            self.category = json.loads(_cate_res.content)["data"]

    def test_get_c_graph(self):
        self.init_test()
        _run = ""
        _tag = ""
        for k in self.category.keys():
            if "graph" in self.category[k].keys():
                _run = k
                _tag = "c_graph"
                break

        try:
            assert _run != "" and _tag != "", "There is no calculation graph data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return

        res = self.client.get("/api/graph", {'run': _run, 'tag': _tag})
        _json = json.loads(res.content)
        self.assertEqual(_json["code"], 200)

    def test_get_s_graph(self):
        self.init_test()
        _run = ""
        _tag = ""
        for k in self.category.keys():
            if "graph" in self.category[k].keys() and "s_graph" in self.category[k]["graph"]:
                _run = k
                _tag = "s_graph"
                break

        try:
            assert _run != "" and _tag != "", "There is no structure graph data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return

        res = self.client.get("/api/graph", {'run': _run, 'tag': _tag})
        _json = json.loads(res.content)
        self.assertEqual(_json["code"], 200)
