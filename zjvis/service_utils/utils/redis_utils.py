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
import redis
from pathlib import Path
from .config_utils import ConfigInstance


# Singleton mode
class RedisUtils:
    def __init__(self):
        self.conn = redis.Redis(
            host=ConfigInstance.conf_redis_host(),
            port=ConfigInstance.conf_redis_port(),
            password=ConfigInstance.conf_redis_password(),
            decode_responses=True,
            db=ConfigInstance.conf_redis_db()
        )

    def get_file_path(self, uid, run, type, tag):
        _key = uid + '_' + run + '_' + type + '_' + tag
        return Path(self.conn.get(_key))

    def send_message(self, msg):
        self.conn.lpush("sessions", msg)

    def lpush(self, name, value):
        self.conn.lpush(name, value)

    def brpop(self, name, timeout=0):
        return self.conn.brpop(name, timeout)

    def exist(self, name):
        return self.conn.exists(name)

    def get(self, name):
        return self.conn.get(name)

    def set(self, name, value):
        self.conn.set(name, value)

    def flushdb(self):
        self.conn.flushdb()

    def delete(self, name):
        self.conn.delete(name)

    def keys(self, pattern='*'):
        return self.conn.keys(pattern)


RedisInstance = RedisUtils()
