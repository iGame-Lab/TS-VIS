# -*- coding: UTF-8 -*-
"""
 Copyright 2020 Tianshu AI Platform. All Rights Reserved.

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
from utils.redis_utils import RedisInstance
import json
import time
import datetime


def isExpired(value):
    return not value - time.time() >= 0


def monitoring():
    keys = RedisInstance.keys("*is_alive")
    for k in keys:
        uid = k.split("_is_alive")[0]
        v = RedisInstance.get(k)
        if isExpired(float(v)):
            print('{} kill user: {}'.format(datetime.datetime.now(), uid))
            RedisInstance.send_message(json.dumps({
                "type": "kill",
                "uid": uid
            }))


if __name__ == "__main__":
    print("Monitoring whether users are active")
    while True:
        monitoring()
        time.sleep(60)
