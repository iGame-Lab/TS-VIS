/** Copyright 2020 Tianshu AI Platform. All Rights Reserved.
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
.temp {
  height: 100px;

  .test1 {
    margin: 3% 0 0 0;
    text-align: center;
  }
}

.show {
  display: none;
}

.infoTitle {
  height: 30px;
  padding-left: 5%;
  font-size: 12px;
  line-height: 30px;
  color: white;
  text-align: left;
  background-color: #625eb3;
  border-radius: 3px;

  .dot {
    margin-right: 2%;
  }
}

.statisticPanelContent {
  padding: 5% 10% 8% 10%;
  font-size: 11px;
  text-align: left;
  border-radius: 0 0 3px 3px;
}

.selectMode {
  margin-top: 12%;
  line-height: 30px;
}

.scroll1 {
  margin-top: 7%;
}

.scroll .rangeNumber {
  margin-top: 1%;
}

.statisticInfo {
  margin-top: 6%;
}

.info {
  width: 100%;
}

.infoContent {
  padding: 5% 10% 3% 10%;
  font-size: 11px;
  text-align: left;
}

.infoContent div {
  margin-bottom: 3%;
}

.el-select-dropdown__item.selected {
  color: #625eb3;
}

.el-select-dropdown__item {
  font-size: 11px;
}
</style>
<template>
  <div style="display: flex; flex-direction: column; height: 100%;">
    <div id="8888" style="height: 50%; overflow: auto;" :class="[scalar ? '' : 'show']">
      <el-col :span="24">
        <ScalarsPanel style="clear: both;" />
        <div />
      </el-col>
    </div>

    <div />
    <div v-if="statistics" id="9999" class="statisticPanelTemp">
      <el-card>
        <div class="infoTitle"><i class="el-icon-chat-dot-round dot" /><span>统计分析</span></div>
        <div class="statisticPanelContent">
          <div class="scroll scroll1">
            <span>数据显示比率({{ statisticShowNumber }}%)</span>
            <el-slider
              v-model="statisticShowNumber"
              :min="1"
              :max="100"
              class="rangeNumber"
              @change="setStatisticShowNumber(statisticShowNumber)"
            />
          </div>
          <div class="selectMode">
            <el-row>
              <el-col :span="8">模式</el-col>
              <el-col :span="16">
                <el-select
                  v-model="statisticMode"
                  class="histmodeselect"
                  @change="setStatisticMode(statisticMode)"
                >
                  <el-option value="三维">三维</el-option>
                  <el-option value="二维">二维</el-option>
                </el-select>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-card>
      <div class="statisticInfo">
        <el-card>
          <div class="infoTitle"><i class="el-icon-chat-dot-round dot" />数据信息栏</div>
          <div v-show="!statisticInfoShowFlag" class="infoContent">暂无信息</div>
          <div v-show="statisticInfoShowFlag" class="infoContent">
            <div>
              <el-row>
                <el-col :span="10">step&nbsp;：</el-col>
                <el-col :span="14">{{ getStatisticInfo[0] }}</el-col>
              </el-row>
            </div>
            <div>
              <el-row>
                <el-col :span="10">数据总量&nbsp;：</el-col>
                <el-col :span="14">{{ getStatisticInfo[1] }}</el-col>
              </el-row>
            </div>
            <div>
              <el-row>
                <el-col :span="10">count最小值&nbsp;：</el-col>
                <el-col :span="14">{{ getStatisticInfo[2] }}</el-col>
              </el-row>
            </div>
            <div>
              <el-row>
                <el-col :span="10">count最大值&nbsp;：</el-col>
                <el-col :span="14">{{ getStatisticInfo[3] }}</el-col>
              </el-row>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>
<script>
import { createNamespacedHelpers } from 'vuex';
import ScalarsPanel from '@/components/scalars/ScalarsPanel.vue';
const { mapMutations: mapCustomMutations, mapGetters: mapCustomGetters } = createNamespacedHelpers(
  'custom'
);
const { mapGetters: mapStatisticGatters } = createNamespacedHelpers('statistic');
export default {
  components: {
    ScalarsPanel,
  },
  data() {
    return {
      scalar: 0,
      statistics: 0,
      statisticMode: '三维',
      statisticShowNumber: 30,
      statisticInfoShowFlag: false,
    };
  },
  computed: {
    ...mapCustomGetters([
      'getAudioData',
      'getTextData',
      'getTextChecked',
      'getImageData',
      'getScalarData',
      'getStatisticData',
      'getStatisticMode',
      'getStatisticShowNumber',
    ]),
    ...mapStatisticGatters(['getStatisticInfo']),
  },
  watch: {
    getStatisticData() {
      this.statistics = this.getStatisticData.length;
    },
    getStatisticInfo(val) {
      if (val.length) {
        this.statisticInfoShowFlag = true;
      } else {
        this.statisticInfoShowFlag = false;
      }
    },
  },
  mounted() {
    this.statistics = this.getStatisticData.length;
    this.statisticMode = this.getStatisticMode;
    this.statisticShowNumber = this.getStatisticShowNumber;
  },
  methods: {
    ...mapCustomMutations(['setStatisticMode', 'setStatisticShowNumber']),
  },
};
</script>
