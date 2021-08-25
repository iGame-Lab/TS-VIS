
import axios from 'axios'
// import Config from '@/settings'
// import { getToken } from '@/utils/auth'
import store from '@/store/modules/layout'

import constants from './constants'
import NProgress from 'nprogress' // 引入nprogress插件
import 'nprogress/nprogress.css' // 这个nprogress样式必须引入
// console.log(constants.HOSTNAME)
const service = axios.create({
  // baseURL: constants.DJANGOHOSTNAME,
  // baseURL: process.env.VUE_APP_VISUAL_API,
  // timeout: Config.timeout, // 请求超时时间
  baseURL: constants.DJANGOHOSTNAME,
  timeout: 35000, // 请求超时时间  
  withCredentials: true
})

// 请求拦截,暂时未用
service.interceptors.request.use(
  function(config) {
    NProgress.start() // 设置加载进度条(开始..)
    // if (getToken()) {
    //   config.headers['Authorization'] = getToken() // 让每个请求携带自定义token 请根据实际情况自行修改
    // }
    return config
  },
  error => {
    console.log('error', error)
    return Promise.reject(error)
  }
)

// 响应拦截,暂时未用
service.interceptors.response.use(
  function (response) {
    NProgress.done() // 设置加载进度条(结束..)
    return response
  },
  function(error) {
    return Promise.reject(error)
  }
)

const useGet = (url, params) => {
  const user = store.state.params
  // params['trainJobName'] = user.trainJobName
  // console.log(url, params)
  return service.get(url, { params })
}

const usePost = (url, jsonData) => {
  return service.post(url, jsonData)
}

export default { useGet, usePost }
