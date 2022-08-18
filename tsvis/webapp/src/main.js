/*
 * @Description: main.js
 * @version: 1.0
 * @Author: xds
 * @Date: 2020-05-08 10:52:00
 * @LastEditors: xds
 * @LastEditTime: 2020-05-22 13:21:44
 */
import Vue from "vue";
import App from "./App";
import store from "./store";
import request from "./utils/request";
import port from "./utils/api";
import createNamespacedHelpers from "vuex";
import ElementUI from "element-ui";
import VueContextMenu from "vue-contextmenu";
import "element-ui/lib/theme-chalk/index.css";
import "./assets/icon/iconfont.css";
import router from "./router";

Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.use(VueContextMenu);
Vue.use(createNamespacedHelpers);
Vue.prototype.$http = request;
Vue.prototype.$port = port;

/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  components: { App },
  template: "<App/>",
  store
});
