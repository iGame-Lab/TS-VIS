# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 19:52
# @Author  : MSH
# @FileName: test_hyperparm_request.py
# @Software: PyCharm
from django.test import TestCase
import json

class TestHyperparmRequest(TestCase):
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

    def test_get_hparams(self):
        self.init_test()
        _run = ""
        for k in self.category.keys():
            if "hyperparm" in self.category[k].keys():
                _run = k
                break

        try:
            assert _run != "", "There is no hyperparm data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return

        res = self.client.get("/api/hyperparm", {'run': _run})
        _json = json.loads(res.content)
        self.assertEqual(_json["code"], 200)
