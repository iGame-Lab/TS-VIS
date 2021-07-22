# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 20:24
# @Author  : MSH
# @FileName: test_projector_request.py
# @Software: PyCharm
from django.test import TestCase
import json
import random


class TestProjectorRequest(TestCase):
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

    def test_projector_all_request(self):
        self.init_test()
        _run = ""
        _tag = ""
        for k in self.category.keys():
            if "embedding" in self.category[k].keys():
                _run = k
                _tag = random.choice(self.category[k]['embedding'])
                break

        try:
            assert _run != "" and _tag != "", "There is no projector data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return
        # 请求元数据
        res = self.client.get("/api/projector", {'run': _run, 'tag': _tag})
        _json = json.loads(res.content)
        self.assertEqual(_json["code"], 200)

        _step = random.choice(_json["data"][_tag])
        # 请求原始数据
        raw_res = self.client.get("/api/projector_raw", {'run': _run, 'tag': _tag, 'step': _step})
        _raw_json = json.loads(raw_res.content)
        self.assertEqual(_raw_json["code"], 200)
        # 请求降维数据
        _dim = random.randint(2, 6)
        _method = random.choice(["pca", "tsne"])
        data_res = self.client.get("/api/projector_data",
                                   {'run': _run, 'tag': _tag, 'step': _step,
                                    "method": _method, "dim": _dim})
        _data_json = json.loads(data_res.content)
        self.assertEqual(_data_json["code"], 200)
        # 请求样本数据
        _index = random.randint(0, _json["data"]["shape"][0] - 1)
        sample_res = self.client.get("/api/projector_sample",
                                     {'run': _run, 'tag': _tag, 'index': _index})
        _sample_json = json.loads(sample_res.content)
        self.assertEqual(_sample_json["code"], 200)
