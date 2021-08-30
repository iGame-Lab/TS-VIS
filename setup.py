# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import shutil
from setuptools import setup, find_packages

# 移除构建的build文件夹
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
VERSION = "0.4.2"
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
write_version()
setup(
    name='tsvis',
    version=VERSION,
    author='hdu',
    author_email='',
    # url='',
    # license = '',
    description="Visualize the training process of the neural network",
    packages=find_packages(),
    include_package_data=True,  # 启用清单文件MANIFEST.in,包含数据文件
    entry_points={'console_scripts': ['tsvis = tsvis.server.main:run'] },  # 动态法线服务和插件
    install_requires=INSTALL_REQUIRES,
)
if not preparing_PyPI_package:
    clean()
