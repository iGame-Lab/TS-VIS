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
        <div v-if="getExceptionShow">
          <excepContainer :oneData="getAllData[0]" :index="0" :oneAllStep="getAllStep[0]" />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { createNamespacedHelpers } from 'vuex'
import excepContainer from './excepContainer'

const { mapActions: mapExceptionActions, mapGetters: mapExceptionGetters, mapMutations: mapExceptionMutations } = createNamespacedHelpers('exception')
const { mapState: mapLayoutStates, mapGetters: mapLayoutGetters } = createNamespacedHelpers('layout')
export default {
  components: {
    excepContainer
  },
  computed: {
    ...mapExceptionGetters(['getRun', 'getTag', 'getAllStep', 'getAllData', 'getInitStateFlag', 'getErrorMessage', 'getExceptionShow']),
    ...mapLayoutStates(['userSelectRunFile']),
    ...mapLayoutGetters(['getTimer'])
  },
  watch: {
    userSelectRunFile(val) {
      if (!this.getExceptionShow) return
      // 稳定后再响应run的变化
      let index = 0
      for (let i = 0; i < this.getRun.length; i++) {
        if (val === this.getRun[i]) {
          index = i
          break
        }
      }
      const param = { run: val, tag: this.getTag[index][0], index: index }
      this.setCurRunTag(param)
      this.fetchAllStep()
    },
    getErrorMessage(val) {
      this.$message({
        message: val,
        type: 'error'
      })
    },
    getTimer() {
      this.fetchAllStep()
      this.setRectCurInfo([])
      this.setCurIqrTimes(['', '', '', 1.50, 1.50])
    }
  },
  created() {
    if (this.getRun.length && this.getAllStep.length === 0) {
      // 本页不是第一个时
      this.fetchAllStep()
    }
  },
  methods: {
    ...mapExceptionActions(['fetchAllStep', 'fetchAllData']),
    ...mapExceptionMutations(['setInitStateFlag', 'setRectCurInfo', 'setCurIqrTimes', 'setCurRunTag'])
  }
}
</script>
