/** Copyright 2020 Zhejiang Lab. All Rights Reserved.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
* =============================================================
*/

<style lang="less" scoped>
.temp{
  height: 100%;
  overflow-y: hidden;
  width: 100%;
  background-color:white;
}
.display-panel{
  margin: 1% 1% 0 1%;
  height: 97.5%;
  border-radius: 5px 5px 0 0;
  box-shadow: rgba(0,0,0,.3) 0px 0px 10px;
  background-color: white;
  overflow-y: auto;
}
</style>
<template>
  <div>
    <div class="temp">
      <div id="excepDisplay" :class="['display-panel']">
        <div v-for="(item, index) in allData" v-show="excepRunShow[item[0]]" :key="index" class="excepContDiv">
          <excepContainer :oneData="item" :index="index" :oneAllStep="allStep[index]" />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { createNamespacedHelpers } from 'vuex'
import excepContainer from './excepContainer'

const { mapActions: mapExceptionActions, mapGetters: mapExceptionGetters, mapMutations: mapExceptionMutations } = createNamespacedHelpers('exception')
const { mapState: mapLayoutStates } = createNamespacedHelpers('layout')
export default {
  components: {
    excepContainer
  },
  data() {
    return {
      allData: [],
      allStep: [],
      excepRunShow: {}
    }
  },
  computed: {
    ...mapExceptionGetters(['getRun', 'getAllStep', 'getAllData', 'getInitStateFlag', 'getErrorMessage', 'getFreshFlag']),
    ...mapLayoutStates(['userSelectRunFile'])
  },
  watch: {
    getAllData(val) {
      this.allData = val
    },
    getAllStep(val) {
      this.allStep = val
      this.fetchAllData()
    },
    userSelectRunFile() {
      this.setRunShow()
    },
    getErrorMessage(val) {
      this.$message({
        message: val,
        type: 'error'
      })
    }
  },
  created() {
    // 在当前页面刷新时，先执行这个钩子函数再执行exception.js中获取类目信息的函数
    // 不在当前页面刷新时，先存入类目信息，点击本页面时才开始渲染
    if (this.getRun.length === 0) return // 类目信息都还没有分发
    this.setRunShow()
    if (this.getAllStep.length === 0) {
      this.fetchAllStep()
    } else if (this.getAllStep.length !== 0 && this.getAllData.length === 0) {
      this.fetchAllData()
    } else if (this.getAllStep.length !== 0 && this.getAllData.length !== 0) {
      this.allStep = this.getAllStep
      this.allData = this.getAllData
    }
  },
  methods: {
    ...mapExceptionActions(['fetchAllStep', 'fetchAllData']),
    ...mapExceptionMutations(['setInitStateFlag', 'setFreshFlag', 'setRectCurInfo', 'setCurIqrTimes']),
    setRunShow() {
      const stateTemp = []
      for (let i = 0; i < this.getRun.length; i += 1) {
        stateTemp[this.getRun[i]] = false
      }
      for (let i = 0; i < this.userSelectRunFile.length; i += 1) {
        stateTemp[this.userSelectRunFile[i]] = true
      }
      this.excepRunShow = stateTemp
      if (this.userSelectRunFile.length === 0) { // 没有选择任何run时清空控制面板数据
        this.setRectCurInfo(['', '', '', '', '', '', ''])
        this.setCurIqrTimes(['', '', '', '', '', '', ''])
      }
    }
  }
}
</script>
