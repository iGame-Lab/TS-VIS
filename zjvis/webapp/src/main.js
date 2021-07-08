/*
 * @Description: main.js
 * @version: 1.0
 * @Author: xds
 * @Date: 2020-05-08 10:52:00
 * @LastEditors: xds
 * @LastEditTime: 2020-05-22 13:21:44
 */
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
// import iView from 'view-design'
// import 'view-design/dist/styles/iview.css'
import store from './store'
import request from './utils/request'
import port from './utils/api'
import createNamespacedHelpers from 'vuex'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/icon/iconfont.css'
// import '//at.alicdn.com/t/font_1809513_34f3xf94tc.css'

Vue.config.productionTip = false
// Vue.use(iView)
Vue.use(ElementUI)
Vue.use(createNamespacedHelpers)
Vue.prototype.$http = request
Vue.prototype.$port = port

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  store
})
