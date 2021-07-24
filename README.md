# zjvis
Zjvis is a Python module for deep learning visualization developed by Hangzhou Dianzi University (HDU) & Zhejiang Lab

## 部署

安装依赖

```
pip install -r requirements.txt
```

## 启动服务

```
python -m zjvis.server.main --logdir=/path/to/logdir
```

## 前端请求

- 前端请求需要在之江网络版的基础上进行修改

- 所有请求参数都不再需要`uid`和`trainJobName`，这两个参数**一定要去掉**

- 初始访问时保持与之江网络版一致，先访问初始化api：`api/init`待接口返回后再请求`api/getCategory`

- 初始化api完成后，进行每个模块数据的请求，请求方式和参数与之江网络版相同，但需要去掉参数`uid`和`trainJobName`

