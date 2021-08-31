# -*- coding: utf-8 -*-
"""
 Copyright 2021 Tianshu AI Platform. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 =============================================================
"""
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
