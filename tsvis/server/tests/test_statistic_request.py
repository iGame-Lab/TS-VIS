# -*- coding: utf-8 -*-
# @Time    : 2021/7/17 16:40
# @Author  : MSH
# @FileName: test_statistic_request.py
# @Software: PyCharm
from django.test import TestCase
import json
import random

class TestStatisticRequest(TestCase):
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

    def test_get_histogram(self):
        self.init_test()
        _run = ""
        _tag = ""
        for k in self.category.keys():
            if "statistic" in self.category[k].keys():
                _run = k
                _tag = random.choice(self.category[k]['statistic']['histogram'])
                break
        try:
            assert _run != "" and _tag != "", "There is no statistic data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return

        res = self.client.get("/api/histogram", {'run': _run, 'tag': _tag})
        _json = json.loads(res.content)
        self.assertEqual(_json["code"], 200)

    def test_get_distribution(self):
        self.init_test()
        _run = ""
        _tag = ""
        for k in self.category.keys():
            if "statistic" in self.category[k].keys():
                _run = k
                _tag = random.choice(self.category[k]['statistic']['histogram'])
                break
        try:
            assert _run != "" and _tag != "", "There is no statistic data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return

        res = self.client.get("/api/distribution", {'run': _run, 'tag': _tag})
        _json = json.loads(res.content)
        self.assertEqual(_json["code"], 200)
