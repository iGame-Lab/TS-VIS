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
import pickle

class CacheIO:
    file_io = {}

    def __init__(self, file_path):
        self.file_path = file_path

    def get_file_io(self):
        # 判断该文件是否打开，若存在则返回file_io
        if self.file_path in self.file_io.keys():
            f = self.file_io[self.file_path]
        else:
            # 判断文件是否存在，不存在则创建并打开返回文件指针
            if not self.file_path.parent.exists():
                self.file_path.parent.mkdir(parents=True, exist_ok=True)
            f = open(self.file_path, 'wb')
            self.file_io[self.file_path] = f
        return f

    def set_cache(self, data):
        f = self.get_file_io()
        pickle.dump(data, f)
        f.flush()

    def get_cache(self):
        res = []
        if self.file_path.exists():
            with open(self.file_path, 'rb') as f:
                while True:
                    try:
                        item = pickle.load(f)
                        res.append(item)
                    except EOFError:
                        break
            return self.filter_data(data=res)
        else:
            return None

    def filter_data(self, data):
        path_str = str(self.file_path)
        if 'graph' in path_str:
            res = data[0]
        elif 'hyperparm' in path_str and 'metrics' in path_str:
            res = list(set(data))
        else:
            res = data
        return res
