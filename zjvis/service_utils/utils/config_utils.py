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
import configparser
from os import path


# Singleton mode
class ConfigUtils:
    def __init__(self, config_name):
        if not path.exists(config_name):
            raise FileNotFoundError("Configuration file not found!")
        config = configparser.RawConfigParser()
        config.read(config_name, encoding="UTF-8")
        self.config = config

    def conf_django_debug(self):
        try:
            _debug = self.config['httpserver']['DjangoDebug']
            return _debug == 'True'
        except Exception:
            return True

    def conf_logdir_base(self):
        try:
            return self.config['parser']['LogdirBase']
        except KeyError:
            raise Exception(
                'The root path of the visualization log must be set'
            )

    def conf_redis_host(self):
        try:
            return self.config['common']['RedisHost']
        except KeyError:
            return "localhost"

    def conf_redis_port(self):
        try:
            _port = self.config['common']['RedisPort']
            return int(_port)
        except Exception:
            return 6379

    def conf_redis_db(self):
        try:
            _db = self.config['common']['RedisDB']
            return int(_db)
        except Exception:
            return 1

    def conf_redis_password(self):
        try:
            return self.config['common']['RedisPassword']
        except KeyError:
            return None

    def conf_user_expiration_time(self):
        try:
            _time = self.config['common']['UserExpirationTime']
            return int(_time)
        except Exception:
            return 60


ConfigInstance = ConfigUtils(
    path.split(path.realpath(__file__))[0] + '/../../config.ini'
)
