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
    height: 100px
  }
  .excepPanel{
    width: 100%;
    text-align: left;
  }
  .infoTitle{
  background-color:#625eb3;
  border-radius: 3px;
  color:white;
  text-align:left;
  height:30px;
  line-height: 30px;
  padding-left:5%;
  font-size: 12px;
  .dot{
    margin-right:2%;
  }
}
.infoContent{
  font-size: 11px;
  padding:5%;
  text-align: left;
}
.item{
  margin-top: 5%;
}
.subButtonDiv{
  display: flex;
}
.subButton{
  width: 18%;
  margin-left: auto;
  margin-right: 1%;
}
.el-checkbox__input.is-focus .el-checkbox__inner {
  border-color:#625eb3;
}
.excepPanelSelect {
  line-height: 30px;
}
</style>
<template>
  <div class="temp">
    <div class="excepPanel">
      <el-card>
        <!-- 盒线图倍数相关信息 -->
        <div>
          <div class="infoTitle"><i class="el-icon-chat-dot-round dot" />箱线图相关信息：</div>
          <!-- <div v-show="!boxInfoShowFlag" class="infoContent">暂无信息</div> -->
          <div v-if="getCurRunTag !== null" class="infoContent">
            <el-row class="item">
              <el-col :span="colSpan1[0]">标&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;签&nbsp;:</el-col>
              <el-col :span="colSpan1[1]">
                <el-select
                  v-model="curTag"
                  class="histmodeselect"
                  placeholder="请选择"
                >
                  <el-option
                    v-for="item in getTag[getCurRunTag.index]"
                    :key="item"
                    :value="item"
                    :label="item"
                  />
                </el-select>
              </el-col>
            </el-row>
            <div v-if="boxInfoShowFlag">
              <!-- <el-row class="item">
                <el-col :span="colSpan0[0]">run&nbsp;：</el-col>
                <el-col :span="colSpan0[1]">{{ curBoxInfo.run }}</el-col>
              </el-row>
              <el-row class="item">
                <el-col :span="colSpan0[0]">tag&nbsp;：</el-col>
                <el-col :span="colSpan0[1]">{{ curBoxInfo.tag }}</el-col>
              </el-row>
              <el-row class="item">
                <el-col :span="colSpan0[0]">step&nbsp;：</el-col>
                <el-col :span="colSpan0[1]">{{ curBoxInfo.step }}</el-col>
              </el-row> -->
              <div v-if="!dq0Show">
                <el-row class="item">
                  <el-col :span="colSpan1[0]">联&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;动&nbsp;：</el-col>
                  <el-col :span="colSpan1[1]"><el-checkbox v-model="myLinkChecked" /></el-col>
                </el-row>
                <el-row class="item excepPanelSelect">
                  <el-col :span="colSpan1[0]">上四分位距倍数&nbsp;：</el-col>
                  <el-col :span="colSpan1[1]"><el-input v-model="curBoxInfo.upTimes" type="number" @change="changeUpTimes()" /></el-col>
                </el-row>
                <el-row class="item excepPanelSelect">
                  <el-col :span="colSpan1[0]">下四分位距倍数&nbsp;：</el-col>
                  <el-col :span="colSpan1[1]"><el-input v-model="curBoxInfo.downTimes" type="number" @change="changeDownTimes()" /></el-col>
                </el-row>
                <div class="item subButtonDiv">
                  <el-button class="subButton" @click="submitBoxInfo()">确定</el-button>
                </div>
              </div>
              <div v-if="dq0Show">
                <el-row class="item">
                  <el-col :span="colSpan1[0]">上边界数值&nbsp;：</el-col>
                  <el-col :span="colSpan1[1]">{{ upDownValue[0] }}</el-col>
                </el-row>
                <el-row class="item">
                  <el-col :span="colSpan1[0]">下边界数值&nbsp;：</el-col>
                  <el-col :span="colSpan1[1]">{{ upDownValue[1] }}</el-col>
                </el-row>
              </div>
              <div v-show="excepBoxStatisticFlag">
                <el-row class="item">
                  <el-col :span="colSpan1[0]">异常点总个数&nbsp;：</el-col>
                  <el-col :span="colSpan1[1]">{{ excepBoxStatistic[0] }}</el-col>
                </el-row>
                <el-row class="item">
                  <el-col :span="colSpan1[0]">异常点百分比&nbsp;：</el-col>
                  <el-col :span="colSpan1[1]">{{ excepBoxStatistic[1] }}%</el-col>
                </el-row>
              </div>
            </div>
          </div>
        </div>
      </el-card>
      <el-card>
        <!-- 对应颜色矩阵中的行列数值 -->
        <div class="infoTitle"><i class="el-icon-chat-dot-round dot" />颜色矩阵像素点相关信息：</div>
        <div v-show="!rectInfoShowFlag" class="infoContent">暂无信息</div>
        <div v-show="rectInfoShowFlag" class="infoContent">
          <div v-for="(item, index) in curRectInfoHead" :key="index">
            <el-row class="item">
              <el-col :span="colSpan0[0]">{{ item }}&nbsp;：</el-col>
              <el-col :span="colSpan0[1]">{{ curRectInfo[index] }}</el-col>
            </el-row>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>
<script>
import { createNamespacedHelpers } from 'vuex'

const { mapGetters: mapExceptionGetters, mapMutations: mapExceptionMutations, mapActions: mapExceptionActions } = createNamespacedHelpers('exception')
export default {
  data() {
    return {
      curRectInfoHead: ['run', 'tag', 'step', 'row', 'column', 'value'],
      curRectInfo: [],
      curRunTag: [], // 不同的run对应不同的tag数组
      curRunTagStep: [], // 当前run，tag对应的step数组
      curBoxInfo: { run: '', tag: '', step: '', upTimes: '', downTimes: '' },
      myLinkChecked: this.getLinkChecked,
      boxInfoShowFlag: false,
      rectInfoShowFlag: false,
      excepBoxStatistic: [],
      excepBoxStatisticFlag: false,
      downUpChange: 'up',
      dq0Show: true,
      upDownValue: [0, 0],
      colSpan0: [7, 17],
      colSpan1: [12, 12],
      curTag: ''
    }
  },
  computed: {
    ...mapExceptionGetters([
      'getRectCurInfo',
      'getCurIqrTimes',
      'getRun',
      'getTag',
      'getAllStep',
      'getLinkChecked',
      'getExcepBoxStatistic',
      'getDq0Show',
      'getUpDownValue',
      'getExceptionShow',
      'getCurRunTag',
      'getTag'
    ])
  },
  watch: {
    getCurRunTag() {
      this.curTag = this.getCurRunTag.tag
    },
    curTag(newVal) {
      if (newVal === this.getCurRunTag.tag) return
      const temp = {}
      temp['run'] = this.getCurRunTag.run
      temp['tag'] = newVal
      temp['index'] = this.getCurRunTag.index
      this.setCurRunTag(temp)
      this.fetchAllStep()
    },
    getRectCurInfo(val) {
      this.curRectInfo = val
      if (this.curRectInfo[0] === '') {
        this.rectInfoShowFlag = false
      } else {
        this.rectInfoShowFlag = true
      }
    },
    getCurIqrTimes(val) {
      if (val[0] === '') {
        this.boxInfoShowFlag = false
        return
      }
      this.boxInfoShowFlag = true;
      [this.curBoxInfo.run, this.curBoxInfo.tag, this.curBoxInfo.step, this.curBoxInfo.upTimes, this.curBoxInfo.downTimes] = val
      this.runSeletChange()
      this.tagSeletChange()
    },
    myLinkChecked() {
      this.setLinkChecked(this.myLinkChecked)
    },
    getExcepBoxStatistic(val) {
      this.excepBoxStatisticFlag = true
      this.excepBoxStatistic = val
    },
    getDq0Show(val) {
      this.dq0Show = val
    },
    getUpDownValue(val) {
      this.upDownValue = val
    }
  },
  mounted() {
    this.curTag = this.getCurRunTag ? this.getCurRunTag.tag : ''
    this.dq0Show = this.getDq0Show
    this.setRectCurInfo(['', '', '', '', '', '', ''])
  },
  methods: {
    ...mapExceptionMutations(['setCurIqrTimes', 'setLinkChecked', 'setRectCurInfo', 'setCurRunTag']),
    ...mapExceptionActions(['fetchAllStep']),
    mySetCurIqrTimes() {
      this.setCurIqrTimes([this.curBoxInfo.run, this.curBoxInfo.tag, this.curBoxInfo.step, this.curBoxInfo.upTimes, this.curBoxInfo.downTimes])
    },
    runSeletChange() {
      for (let i = 0; i < this.getRun.length; i += 1) {
        if (this.getRun[i] === this.curBoxInfo.run) {
          this.curRunTag = this.getTag[i]
          break
        }
      }
    },
    tagSeletChange() {
      for (let i = 0; i < this.getAllStep.length; i += 1) {
        if (this.getAllStep[i][0] === this.curBoxInfo.run && this.getAllStep[i][1] === this.curBoxInfo.tag) {
          this.curRunTagStep = this.getAllStep[i][2].step
          break
        }
      }
    },
    computeMaxTimes() {
      let curStepBox = []
      for (let i = 0; i < this.getAllStep.length; i += 1) {
        if (this.getAllStep[i][0] === this.curBoxInfo.run && this.getAllStep[i][1] === this.curBoxInfo.tag) {
          let k = 0
          for (let j = 0; j < this.curRunTagStep.length; j += 1) {
            if (this.curRunTagStep[j] === this.curBoxInfo.step) {
              k = j
              break
            }
          }
          curStepBox = this.getAllStep[i][2].box[k]
          break
        }
      }
      const dq = curStepBox[0][1] - curStepBox[0][3]
      const maxUpTimes = (curStepBox[1][5] - curStepBox[0][1]) / dq
      const maxDownTimes = (curStepBox[0][3] - curStepBox[1][0]) / dq
      return [maxDownTimes, maxUpTimes]
    },
    changeUpTimes() {
      this.downUpChange = 'up'
      if (Number(this.curBoxInfo.upTimes) < 0) {
        this.$message({
          message: '倍数不能为负数',
          type: 'warning'
        })
        return
      }
      const [maxDownTimes, maxUpTimes] = this.computeMaxTimes()
      if (this.curBoxInfo.upTimes > maxUpTimes) {
        this.$message({
          message: `上四分位距的倍数最大只能为：${maxUpTimes}`,
          type: 'warning'
        })
        this.curBoxInfo.upTimes = maxUpTimes
      }
      // 联动
      if (this.getLinkChecked) {
        let downTimesTemp = this.curBoxInfo.upTimes
        if (maxDownTimes < downTimesTemp) {
          this.$message({
            message: `下四分位距的倍数最大只能为：${maxDownTimes}`,
            type: 'warning'
          })
          downTimesTemp = maxDownTimes
          // 反过来又会影响downTimes，因为联动，希望上下倍数相同
          this.curBoxInfo.upTimes = maxDownTimes
        }
        this.curBoxInfo.downTimes = downTimesTemp
      }
    },
    changeDownTimes() {
      this.downUpChange = 'down'
      if (Number(this.curBoxInfo.downTimes) < 0) {
        this.$message({
          message: '倍数不能为负数',
          type: 'warning'
        })
        return
      }
      const [maxDownTimes, maxUpTimes] = this.computeMaxTimes()
      if (this.curBoxInfo.downTimes > maxDownTimes) {
        this.$message({
          message: `下四分位距的倍数最大只能为：${maxDownTimes}`,
          type: 'warning'
        })
        this.curBoxInfo.downTimes = maxDownTimes
      }
      // 联动
      if (this.getLinkChecked) {
        let upTimesTemp = this.curBoxInfo.downTimes
        if (maxUpTimes < upTimesTemp) {
          this.$message({
            message: `上四分位距的倍数最大只能为：${maxUpTimes}`,
            type: 'warning'
          })
          upTimesTemp = maxUpTimes
          // 反过来又会影响downTimes，因为联动，希望上下倍数相同
          this.curBoxInfo.downTimes = maxUpTimes
        }
        this.curBoxInfo.upTimes = upTimesTemp
      }
    },
    submitBoxInfo() {
      // 需要先判断一下再存进去，数据没变也不提交
      // 都不为空，以及倍数不能为负数
      if (Number(this.curBoxInfo.upTimes) !== Number(this.curBoxInfo.downTimes) && this.myLinkChecked) {
        if (this.downUpChange === 'downUp') {
          this.changeDownTimes()
        } else {
          this.changeUpTimes()
        }
      }
      // 如果没有变化就不提交
      if (Number(this.curBoxInfo.upTimes) === this.getCurIqrTimes[3] && Number(this.curBoxInfo.downTimes) === this.getCurIqrTimes[4]) return
      if (Number(this.curBoxInfo.upTimes) < 0 || Number(this.curBoxInfo.downTimes) < 0) {
        this.$message({
          message: '倍数不能为负数',
          type: 'warning'
        })
        return
      }
      this.setCurIqrTimes([this.curBoxInfo.run, this.curBoxInfo.tag, this.curBoxInfo.step, Number(this.curBoxInfo.upTimes), Number(this.curBoxInfo.downTimes)])
    }
  }
}
</script>
<style>
/* el-card */
.excepPanel .el-card__body  {
  border-radius: 0 0 3px 3px;
  padding: 0;
}
.excepPanel .el-card{
  margin:3.5% 5% 4% 0%;
  border-top: 0px;
}
/* 输入框 */
.excepPanel .el-input__inner{
  border-radius: 50px;
  height: 30px;
  line-height: 30px;
  font-size:11px;
  border-color: #8c89c7;
  color: #625eb3;
}
/* button */
.excepPanel .el-button{
  font-size: 12px;
  padding: 8px;
  border-radius: 10px;
}
.excepPanel .el-button:active{
  color:#8c89c7;
  border-color:#625eb3;
}
.excepPanel .el-button:focus,.excepPanel .el-button:hover{
  color:#8c89c7;
  border-color:#d9d8f5;
  background-color: #d9d8f5;
}
/* 复选框 */
.excepPanel .el-checkbox__inner,
.excepPanel .el-checkbox__inner:hover {
  border-color:#625eb3;
}
.excepPanel .el-checkbox__input.is-checked .el-checkbox__inner
.excepPanel .el-checkbox__input.is-indeterminate .el-checkbox__inner{
  background-color: #625eb3;
  border-color:#625eb3;
}
</style>
