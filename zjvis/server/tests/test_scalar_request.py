# -*- coding: utf-8 -*-
# @Time    : 2021/7/17 15:28
# @Author  : MSH
# @FileName: test_scalar_request.py
# @Software: PyCharm
from django.test import TestCase
import json
import random

class TestScalarRequest(TestCase):
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

    def test_get_scalar(self):
        self.init_test()
        _run = ""
        _tag = ""
        for k in self.category.keys():
            if "scalar" in self.category[k].keys():
                _run = k
                _tag = random.choice(list(self.category[k]['scalar'].keys()))
                break

        try:
            assert _run != "" and _tag != "", "There is no scalar data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return

        res = self.client.get("/api/scalar", {'run': _run, 'tag': _tag})
        _json = json.loads(res.content)
        self.assertEqual(_json["code"], 200)
