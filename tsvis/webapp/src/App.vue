<!--
 * @Description: app
 * @version: 1.0
 * @Author: xds
 * @Date: 2020-05-08 10:52:00
 * @LastEditors: xds
 * @LastEditTime: 2020-06-10 08:40:18
-->
<template>
  <div id="app">
    <!-- <Layout></Layout> -->
    <router-view></router-view>
  </div>
</template>

<script>
import Layout from '@/components/layout/Layout.vue'

export default{
  components: {
    Layout
  }
}
</script>

<style lang='less' scoped>
#app {
  // font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  display: flex;
  height: 100%;
  user-select: none;
  // font-family: "Arial","Microsoft YaHei","黑体","宋体",sans-serif;;
  ::-webkit-scrollbar {
      width: 5px;
      height: 1px;
      background-color: white;
    }
    /*定义滚动条轨道 内阴影+圆角*/
    ::-webkit-scrollbar-track{
      box-shadow: inset 0 0 6px rgba(0,0,0,0.1);
      border-radius: 0px;
    }
    /*定义滑块 内阴影+圆角*/
    ::-webkit-scrollbar-thumb{
      border-radius: 10px;
      /*-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);*/
      background-color: #ccc;
    }
}
</style>
