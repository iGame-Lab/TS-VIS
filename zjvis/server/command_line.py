# -*- coding: utf-8 -*-
# @Time    : 2021/7/15 21:55
# @Author  : MSH
# @FileName: command_line.py
# @Software: PyCharm
import sys
import argparse

DEFAULT_PORT = "9898"

class CommandLine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        parser = argparse.ArgumentParser(prog='zjvis')
        subparsers = parser.add_subparsers(help='sub-command help')
        parser.add_argument('--logdir', type=str,
                            help='Specify visual log directory', required=False)
        parser.add_argument('--port', type=str, default=DEFAULT_PORT,
                            help='Specify HTTP server port.', required=False)
        parser.add_argument('--version', '-v', action="store_true",
                            help='Print version of zjvis and exit.')

        parser_rs = subparsers.add_parser('runserver', help='Start local Zjvis server')
        parser_rs.add_argument('--logdir', type=str,
                               help='Specify visual log directory', required=True)
        parser_rs.add_argument('--port', type=str, help='Specify HTTP server port.', required=False,
                               default=DEFAULT_PORT)
        parser_rs.set_defaults(action="runserver")

        # 添加子命令 migrate
        parser_mr = subparsers.add_parser('migrate', help='Run migrate for django server')
        parser_mr.set_defaults(action="migrate")

        # 添加子命令 test
        parser_ts = subparsers.add_parser('test', help='Run test for RESTful API')
        parser_ts.add_argument('--testdir', dest="logdir", type=str,
                               help='Specify test log directory', required=True)
        parser_ts.add_argument('testcase', type=str, help='Testcase for test')
        parser_ts.set_defaults(action="test")

        if len(sys.argv) < 2:
            parser.error("A logdir must be specified. "
                         "For example `zjvis --logdir mylogdir`.\n"
                         "Run `zjvis --help` for details.")

        args = parser.parse_args()

        if getattr(args, "version", None) is True:
            _action = "version"
        else:
            if getattr(args, "action", None) is None:
                _action = "runserver"
            else:
                _action = args.action

        self.action = _action
        self.args = args


_cmd_line = CommandLine()

def get_cmd_line():
    return _cmd_line
