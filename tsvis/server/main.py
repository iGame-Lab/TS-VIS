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
import sys
from tsvis.server import manage
from .command_line import get_cmd_line

def run_migrate(args):
    argvs = [
        sys.argv[0],
        "migrate",
    ]
    manage.main(argvs)

def run_test(args):
    argvs = [
        sys.argv[0],
        "test",
        args.testcase
    ]
    manage.main(argvs)

def run_main(args):
    argvs = [
        sys.argv[0],
        "runserver",
        "0.0.0.0:" + args.port,
        "--noreload",
        "--insecure"
    ]
    manage.main(argvs)

def print_version(*args, **kwargs):
    import tsvis
    sys.stdout.write(f"Version: {tsvis.__version__}\n")
    sys.stdout.write(f"Commit: {tsvis.__git_version__}\n")

def run():
    programs = {
        "runserver": run_main,
        "migrate": run_migrate,
        "test": run_test,
        "version": print_version
    }
    cmd_line = get_cmd_line()
    programs[cmd_line.action](cmd_line.args)


if __name__ == "__main__":
    run()
