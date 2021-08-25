# -*- coding: utf-8 -*-
# @Time    : 2021/7/17 16:57
# @Author  : MSH
# @FileName: test_media_request.py
# @Software: PyCharm
from django.test import TestCase
import json
import random

class TestMediaRequest(TestCase):
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

    def test_get_text(self):
        self.init_test()
        _run = ""
        _tag = ""
        for k in self.category.keys():
            if "media" in self.category[k].keys() and "text" in self.category[k]['media'].keys():
                _run = k
                _components = self.category[k]['media']
                _tag = random.choice(_components['text'])
                break
        try:
            assert _run != "" and _tag != "", "There is no text data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return

        res = self.client.get("/api/text", {'run': _run, 'tag': _tag})
        _json = json.loads(res.content)
        self.assertEqual(_json["code"], 200)

    def test_get_audio(self):
        self.init_test()
        _run = ""
        _tag = ""
        for k in self.category.keys():
            if "media" in self.category[k].keys() and "audio" in self.category[k]['media'].keys():
                _run = k
                _components = self.category[k]['media']
                _tag = random.choice(_components['audio'])
                break
        try:
            assert _run != "" and _tag != "", "There is no audio data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return

        _audio_meta = self.client.get("/api/audio", {'run': _run, 'tag': _tag})
        _am_json = json.loads(_audio_meta.content)
        self.assertEqual(_am_json["code"], 200)

        _step = random.choice(_am_json["data"][_tag])["step"]
        _audio_raw = self.client.get("/api/audio_raw", {'run': _run, 'tag': _tag, "step": _step})
        _ia_json = json.loads(_audio_raw.content)
        self.assertEqual(_ia_json["code"], 200)

    def test_get_image(self):
        self.init_test()
        _run = ""
        _tag = ""
        for k in self.category.keys():
            if "media" in self.category[k].keys() and "image" in self.category[k]['media'].keys():
                _run = k
                _components = self.category[k]['media']
                _tag = random.choice(_components['image'])
                break
        try:
            assert _run != "" and _tag != "", "There is no image data in test logs."
        except AssertionError as e:
            import logging
            logging.error(str(e))
            return

        _image_meta = self.client.get("/api/image", {'run': _run, 'tag': _tag})
        _im_json = json.loads(_image_meta.content)
        self.assertEqual(_im_json["code"], 200)

        _step = random.choice(_im_json["data"][_tag])["step"]
        _image_raw = self.client.get("/api/image_raw", {'run': _run, 'tag': _tag, "step": _step})
        _ir_json = json.loads(_image_raw.content)
        self.assertEqual(_ir_json["code"], 200)
