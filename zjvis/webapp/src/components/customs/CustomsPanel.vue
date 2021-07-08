<!--
 * @Descripttion: Customs paramenter panel
 * @version: 1.0
 * @Author: xds
 * @Date: 2020-04-22 00:56:46
 * @LastEditors: xds
 * @LastEditTime: 2020-06-05 19:36:50
 -->
<style lang="less" scoped>
  .temp{
      height: 100px;
      .test1{
        margin: 3% 0 0 0;
        text-align: center;
      }
  }
  .show{
    display:none;
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
  .statisticPanelContent{
    padding:5% 10% 8% 10%;
    // padding: 2% 5% 5% 5%;
    border-radius: 0 0 3px 3px;
    text-align: left;
    font-size:11px;
  }
  .selectMode{
    margin-top: 12%;
    line-height: 30px;
  }
  .scroll1{
    margin-top:7%;
  }
  .scroll .rangeNumber{
    margin-top:1%;
    // width: 94%;
  }
  .statisticInfo {
    margin-top: 6%;
  }
  .info{
    width:100%;
  }
  .infoContent{
    font-size: 11px;
    padding:5% 10% 3% 10%;
    text-align: left;
  }
  .infoContent div {
    margin-bottom: 3%;
  }
  .el-select-dropdown__item.selected{
    color:#625eb3;
  }
  .el-select-dropdown__item{
    font-size: 11px;
  }
</style>
<template>
  <div style="height:100%;display:flex;flex-direction: column">
    <div id="8888" :class="[scalar?'':'show']" style="overflow:auto;height:50%">
      <el-col :span="24">
        <ScalarsPanel style="clear:both" />
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
                <el-select v-model="statisticMode" class="histmodeselect" @change="setStatisticMode(statisticMode)">
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
            <!-- <div><span>统计个数最大值对应的区间中心点：{{getStatisticInfo[4]}}</span></div> -->
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>
<script>
import { createNamespacedHelpers } from 'vuex'
import ScalarsPanel from '@/components/scalars/ScalarsPanel.vue'
// import StatisticsPanel from '@/components/statistics/StatisticsPanel.vue'
// import category from './Category'
const { mapMutations: mapCustomMutations, mapGetters: mapCustomGetters } = createNamespacedHelpers('custom')
const { mapGetters: mapStatisticGatters } = createNamespacedHelpers('statistic')
export default {
  components: {
    ScalarsPanel
    // StatisticsPanel
    // category
  },
  data() {
    return {
      scalar: 0,
      statistics: 0,
      statisticMode: '三维',
      statisticShowNumber: 30,
      // statisticBinNumber: 30,
      statisticInfoShowFlag: false
    }
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
      'getStatisticShowNumber'
    ]),
    ...mapStatisticGatters(['getStatisticInfo'])
  },
  watch: {
    // getScalarData(val) {
    //   this.scalar = this.getScalarData.length
    // },
    getStatisticData(val) {
      this.statistics = this.getStatisticData.length
    },
    getStatisticInfo(val) {
      if (val.length) {
        this.statisticInfoShowFlag = true
      } else {
        this.statisticInfoShowFlag = false
      }
    }
  },
  mounted() {
    // this.scalar = this.getScalarData.length
    this.statistics = this.getStatisticData.length
    this.statisticMode = this.getStatisticMode
    this.statisticShowNumber = this.getStatisticShowNumber
  },
  methods: {
    ...mapCustomMutations(['setStatisticMode', 'setStatisticShowNumber'])
  }
}
</script>
