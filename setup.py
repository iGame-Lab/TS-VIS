import os
import sys
import subprocess
import shutil
from setuptools import setup, find_packages

# 移除构建的build文件夹
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
VERSION = "0.4.1"
preparing_PyPI_package = 'sdist' in sys.argv or 'bdist_wheel' in sys.argv

def clean():
    for name in ['build', 'dist', 'zjvis.egg-info']:
        path = os.path.join(CUR_PATH, name)
        if os.path.isdir(path):
            print('INFO del dir ', path)
            shutil.rmtree(path)

def get_git_version():
    _git_vetsion = ""
    if os.path.exists('.git'):
        sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
        _git_vetsion = sha
    return _git_vetsion

def write_version():
    _git = get_git_version()
    with open("zjvis/__init__.py", "r") as f:
        _file = f.readlines()[0: -2]
    with open("zjvis/__init__.py", "w") as f:
        _file.append(f"__version__ = '{VERSION}'\n")
        _file.append(f"__git_version__ = '{_git}'\n")
        f.writelines(_file)


write_version()
setup(
    name='zjvis',
    version=VERSION,
    author='hdu',
    author_email='',
    # url='',
    # license = '',
    description="Visualize the training process of the neural network",
    packages=find_packages(),
    include_package_data=True,  # 启用清单文件MANIFEST.in,包含数据文件
    entry_points={'console_scripts': ['zjvis = zjvis.server.main:run'] },  # 动态法线服务和插件
    install_requires=[  # 自动安装依赖
        'watchdog>=2.1.3',
        'tsne-mp>=0.1.13',
        'soundfile>=0.10.3',
        'six>=1.16.0',
        'protobuf>=3.15.8',
        'pillow>=8.2.0',
        'numpy>=1.16.6',
        'django>=3.2.4',
        'django-cors-headers>=3.7.0',
        'crc32c>=2.2'
    ],
)
if not preparing_PyPI_package:
    clean()
