import axios from "axios";
import store from "@/store/modules/layout";

import constants from "./constants";
import NProgress from "nprogress"; // 引入nprogress插件
import "nprogress/nprogress.css"; // 这个nprogress样式必须引入
const service = axios.create({
  baseURL: constants.DJANGOHOSTNAME,
  timeout: 35000, // 请求超时时间
  withCredentials: true
});

// 请求拦截,暂时未用
service.interceptors.request.use(
  function(config) {
    NProgress.start(); // 设置加载进度条(开始..)
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截,暂时未用
service.interceptors.response.use(
  function(response) {
    NProgress.done(); // 设置加载进度条(结束..)
    return response;
  },
  function(error) {
    return Promise.reject(error);
  }
);

// 单机版不加trainJobName
const useGet = (url, params) => {
  const user = store.state.params;
  return service.get(url, { params });
};

const usePost = (url, jsonData) => {
  return service.post(url, jsonData);
};

export default { useGet, usePost };
