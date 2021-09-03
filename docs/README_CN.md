<p align="center">
  <img src="https://raw.githubusercontent.com/iGame-Lab/TS-VIS/master/docs/images/logo.svg"></img>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-361"><img src="https://img.shields.io/badge/Python-%3E=3.6-blue.svg"></img></a>
  <a><img src="https://img.shields.io/badge/Version-0.4.2-rgb(68,204,17).svg"></img></a>
  <a><img src="https://img.shields.io/badge/pypi-v0.4.2-blue.svg"></img></a>
</p>

TS-VIS（天枢Vis）是[天枢人工智能开源开放平台](https://gitee.com/zhijiangtianshu/Dubhe)的可视化组件，支持TensorFlow、PyTorch、OneFlow等主流深度学习框架的可视化功能。

**[文档: https://feyily.github.io/tsvis-document/](https://feyily.github.io/tsvis-document/)**

![](https://raw.githubusercontent.com/iGame-Lab/TS-VIS/master/docs/images/demo.gif)

## 亮点

* 框架无关，支持TensorFlow、PyTorch、OneFlow等主流深度学习框架可视化
* 超快的响应速度
* 支持大规模的可视化
* 支持训练过程实时可视化
* 支持降维分析样本可视化
* 支持神经网络异常可视化

## 支持功能

- 模型结构可视化：可视化网络结构，包括计算图和结构图
- 标量数据可视化：可视化包括`accuary`和`loss`等在内的任意标量数据
- 媒体数据可视化：可视化包括图像、文字、音频在内的媒体数据
- 统计分析可视化：可视化神经网络中权重、偏置等的分布
- 降维分析可视化：通过降维算法，可视化任意高维数据
- 超参分析可视化：可视化不同超参数下的神经网络指标
- 异常检测可视化：将神经网络张量数据映射到二维，可视化张量数据统计信息
- 用户定制可视化：可以将标量、媒体、和统计分析中的图表移动到该模块进行对比查看

## 安装

我们提供了两种安装方式：pip安装和源码安装，不管通过哪种方式安装，都需要确保你的Python版本为3.6以上，如果不满足请先升级Python

### 使用pip安装

```
pip install tsvis
```

### 从源码安装

TS-VIS采用前后端分离的架构，所以从源码安装需要分别编译前端、后端

- **从源码编译前端：**

  ```
  cd webapp
  ```

  首先安装依赖

  ```
  npm install
  ```

  使用命令打包前端生成静态文件
  ```
  npm run build
  ```

- **从源码编译后端：**

  从源码安装后端需要先将前端编译生成的静态文件移动到`tsvis/server/frontend`文件夹下

  然后安装Python依赖包`setuptools`
  
  ```
  pip install setuptools
  ```
  
  执行`setup.py`文件安装TS-VIS到Python环境
  
  ```
  python setup.py install
  ```

### 运行

安装完成之后，可以通过下面的命令查看当前安装版本号。若安装成功，则会输出版本信息到控制台

```
tsvis -v
```

若TS-VIS已正确安装，则可以通过下面命令运行可视化

```
tsvis --logdir path/to/logdir/
```

默认情况下，可视化服务会启动在`http://127.0.0.1:9898`，打开浏览器访问即可查看可视化内容
