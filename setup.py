# -*- coding: UTF-8 -*-
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

import os
import sys
import subprocess
import shutil
from setuptools import setup, find_packages

VERSION = "0.4.2"

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.realpath(os.path.dirname(__file__))
preparing_PyPI_package = 'sdist' in sys.argv or 'bdist_wheel' in sys.argv

def clean():
    for name in ['build', 'dist', 'tsvis.egg-info']:
        path = os.path.join(CUR_PATH, name)
        if os.path.isdir(path):
            print('INFO del dir ', path)
            shutil.rmtree(path)

def read(name):
    return open(os.path.join(ROOT, name)).read()

def get_git_version():
    _git_vetsion = ""
    if os.path.exists('.git'):
        sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
        _git_vetsion = sha
    return _git_vetsion

def write_version():
    _git = get_git_version()
    with open("tsvis/__init__.py", "r") as f:
        _file = f.readlines()[0: -2]
    with open("tsvis/__init__.py", "w") as f:
        _file.append(f"__version__ = '{VERSION}'\n")
        _file.append(f"__git_version__ = '{_git}'\n")
        f.writelines(_file)


INSTALL_REQUIRES = read("requirements.txt")
README = read('README.md')
write_version()
setup(
    name='TS-VIS',
    version=VERSION,
    author='iGame',
    author_email='',
    long_description=README,
    long_description_content_type='text/markdown',
    # url='',
    license = 'Apache License',
    description="TS-VIS is a Python module for deep learning visualization",
    packages=find_packages(),
    include_package_data=True,  # 启用清单文件MANIFEST.in,包含数据文件
    entry_points={'console_scripts': ['tsvis = tsvis.server.main:run'] },
    install_requires=INSTALL_REQUIRES,
)
if not preparing_PyPI_package:
    clean()
