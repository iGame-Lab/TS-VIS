# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 21:11
# @Author  : MSH
# @FileName: test_exception_request.py
# @Software: PyCharm
from django.test import TestCase
import json
import random


class TestExceptionRequest(TestCase):
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

    def test_exception_all_request(self):
        self.init_test()
        _run = ""
        _tag = ""
        for k in self.category.keys():
            if "exception" in self.category[k].keys():
                _run = k
                _tag = random.choice(self.category[k]['exception'])
                break

        try:
            assert _run != "" and _tag != "", "There is no exception data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return
        # 请求元数据
        res = self.client.get("/api/exception", {'run': _run, 'tag': _tag})
        _json = json.loads(res.content)
        self.assertEqual(_json["code"], 200)

        _step_list = _json["data"][_tag]["step"]
        _step_idx = random.randint(0, len(_step_list) - 1)
        _step = _step_list[_step_idx]
        # 请求异常检测热力图数据
        data_res = self.client.get("/api/exception_data", {'run': _run, 'tag': _tag, "step": _step})
        _data_json = json.loads(data_res.content)
        self.assertEqual(_data_json["code"], 200)
        # 请求异常检测直方图数据
        hist_res = self.client.get("/api/exception_hist", {'run': _run, 'tag': _tag, "step": _step})
        _hist_json = json.loads(hist_res.content)
        self.assertEqual(_hist_json["code"], 200)
        # 请求异常检测盒须图数据
        _box_info = _json["data"][_tag]["box"][_step_idx][0]
        _up_boundary = _box_info[0]
        _box_up_boundary = _box_info[1]
        _box_down_boundary = _box_info[-2]
        _down_boundary = _box_info[-1]
        _up = random.uniform(_box_up_boundary, _up_boundary)
        _down = random.uniform(_down_boundary, _box_down_boundary)
        box_res = self.client.get("/api/exception_box",
                                  {'run': _run, 'tag': _tag, "step": _step,
                                   "up": _up, "down": _down})
        _box_json = json.loads(box_res.content)
        self.assertEqual(_box_json["code"], 200)
