# frontend

> Visual web project for deep learning

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```
## 文件说明
``` bash
# 组件说明
1. 目前只提供9个组件接口供大家调试接口在:/components/ 下包括scalars，images...

2. 每个组件下面有两个子组件如:Scalars.vue、ScalarsPanel.vue 分别对应内容(展示图表等)和参数选项(参数设置)；
大家可以把自己的组件写到这两个组件里面作为他们的子组件。(组件不推荐很大，大家可以灵活的将自己负责的组件拆分成小组件，放在对应的目录下)；

3. 样式部分推荐用less、sass，在组件中使用<style scoped></style>不对其它组件造成污染；

4. 一些全局的常量我再/components/下放了个constants.js 大家可以试着放进去，在组件中只需要导入就好了，或者大家在各自负责的组件中加入个constants.js，我后面整合...；

5. 前后端数据交互，在src下面编写了api.js这个文件是用于和Django交互使用，提供Get和Post两种请求方式具体看函数内部(一定要开启Django服务器才能使用)；

6. 推荐每组指派一人辅助编写可视化后端数据处理部分，配合前端可视化成员进行数据的交互，后端使用详情请看backend/README.md；
```
## 数据获取api
``` bash
# /utils/api.js
 manage: {
    initCategory: '/api/getCategory'
  },
  category: {
    scalar: '/api/getScalar', // 获取scalar
    media: '/api/getMedia',  // 获取media
    graph: '/api/getGraph',  // ...
    statistic: '/api/getStatistic',
    embedding: '/api/getEmbedding',
    hyperparm: '/api/getHyperparm',
    features: '/api/featuremap',
    transformer: '/api/transformer',
    state: '/api/state',
    custom: '/api/getCustom',

  }
# 使用方法：
import http from '@/utils/request'
import port from '@/utils/api'

http中有封装了两种方法(get, post)：
port对应具体的请求内容，对象类型，通过.来调用
可通过：
http.useGet(port.manage.initCategory, parm).then(res => {
  console.log(res) //promise对象
  //处理自己的逻辑函数
})；//parm = {step=1} => http://localhost:8080/api/getScalar?step=1

http.usePost(port.manage.initCategory, parm).then(res => {
  console.log(res) //promise对象
  //处理自己的逻辑函数
})；// parm = {} => type json,
详情请百度查看'post'和'get'的区别(基础知识)
```
## 初始tag分配 (2020/5/16更新) 
``` bash
1. 初始系统，返回run文件及tag， 每个类目下分发run及tag信息会得到一个数组
   形式如：[
            ['.', 'vgg'， 'train'], // run信息
            [
              {},  // '.' 对应的具体tag
              {},  // 'vgg' 对应的具体tag
              {}   // 'train' 对应的具体tag
            ],
            {'initStateFlag': true} // 是否为初始界面
          ]
    ******** 可自行查看vuex中各自类目得到的具体信息，再通过该类目信息请求数据 *********
2. 各自模块对应的run可通过layout中上方select选择，选择信息保存在layout.js下state中的'userSelectRunFile'，各子类目可通过监听该状态，改变对应的run ## 对于初始选择显示的 run文件，推荐可根据自己模块决定：graph显示一个run(如果是多run)，其它全部选择显示；
```
## 初始tag分配 (2020/5/18更新) 
``` bash
1. 初始系统，返回run文件及tag， 每个类目下分发run及tag信息会得到一个数组
   形式如：[
            ['.', 'vgg'， 'train'], // 如果该run文件下有相应的类目返回对应的run文件
            [
              {},  // '.' 对应的具体tag
              {},  // 'vgg' 对应的具体tag
              {}   // 'train' 对应的具体tag
            ],
            {'initStateFlag': true} // 是否为初始界面
          ]
    ******** 可自行查看vuex中各自类目得到的具体信息，再通过该类目信息请求数据 *********
2. 各自模块对应的run可通过layout中上方select选择，选择信息保存在layout.js下state中的'userSelectRunFile'，各子类目可通过监听该状态，改变对应的run 
3. run文件选择栏根据不同类目分为单选和多选（自己看看自己相应的类目，对于多选类目默认选择全部，单选类目默认选择index=0的项，后期只能单选）
```