import os, shutil
from setuptools import setup, find_packages

#移除构建的build文件夹
CUR_PATH = os.path.dirname(os.path.abspath(__file__))

def clean():
    for name in ['build', 'dist', 'zjvis.egg-info']:
        path = os.path.join(CUR_PATH, name)
        if os.path.isdir(path):
            print('INFO del dir ', path)
            shutil.rmtree(path)

clean()
setup(
    name = 'zjvis',
    version = '0.1',
    author = 'hdu',
    # url='',
    # license = '',
    description="Visualize the training process of the neural network",
    packages = find_packages(),
    include_package_data = True, #启用清单文件MANIFEST.in,包含数据文件
    entry_points={'console_scripts' : ['zjvis = server.main:run'] }, #动态法线服务和插件
    install_requires = [#自动安装依赖
        'watchdog>=2.1.3',
        'tsne-mp>=0.1.13',
        'soundfile>=0.10.3',
        'six>=1.16.0',
        'protobuf>=3.17.2',
        'pillow>=8.2.0',
        'numpy>=1.16.6',
        'django>=3.2.4',
        'django-cors-headers>=3.7.0',
        'crc32c>=2.2'
    ],
)
clean()