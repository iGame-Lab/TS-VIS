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
from absl import app, flags
import manage
import sys
sys.path.append("../service_utils")

FLAGS = flags.FLAGS
flags.DEFINE_string("port", "9898", "Specify HTTP server port.")
flags.DEFINE_string("logdir", None, "Specify visual log directory")

# 指定必须输入的参数
flags.mark_flag_as_required("logdir")

def run_migrate(argv):
    argvs = [
        argv[0],
        "migrate",
    ]
    manage.main(argvs)


def run_main(argv):
    argvs = [
        argv[0],
        "runserver",
        "0.0.0.0:" + FLAGS.port,
        "--noreload",
    ]
    manage.main(argvs)


if __name__ == "__main__":
    # app.run(run_migrate)
    app.run(run_main)
