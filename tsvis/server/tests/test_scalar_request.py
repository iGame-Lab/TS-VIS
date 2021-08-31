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
