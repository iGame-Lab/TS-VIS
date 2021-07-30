# -*- coding: utf-8 -*-
# @Time    : 2021/7/15 17:07
# @Author  : MSH
# @FileName: test_init_request.py
# @Software: PyCharm
from django.test import TestCase
import json

class TestInitRequest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_get_init_data(self):
        response = self.client.get("/api/init", format="json")
        self.assertEqual(response.status_code, 200)
        _except_res = b'{"code": 200, "msg": "ok", "data": {"msg": "success"}}'
        self.assertEqual(response.content, _except_res)

    def test_get_Category(self):
        # 先请求初始化API
        self.client.get("/api/init", format="json")
        # 再请求测试API
        response = self.client.get("/api/getCategory", format="json")
        self.assertEqual(response.status_code, 200)
        _json_res = json.loads(response.content)
        self.assertEqual(_json_res["code"], 200)
