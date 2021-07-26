<style lang="less" scoped>
.statisticPanel {
  width: 100%;
}
.rangeNumber:hover {
  cursor: pointer;
}
.statisticPanelContent{
  padding:5% 10% 8% 10%;
  border-radius: 0 0 3px 3px;
  text-align: left;
  font-size:11px;
}
.spanCenter{
  text-align: center;
}
.scroll1{
  margin-top:7%;
}
.scroll2{
  margin-top:10%;
}
.scroll .rangeNumber{
  margin-top:1%;
}
.selectMode{
  margin-top: 12%;
  line-height: 30px;
}
.statisticInfo {
  margin-bottom: 6%;
}
.info{
  width:100%;
}
.statisticPanel .infoTitle:hover {
  cursor: pointer;
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
  <div class="temp statisticPanelTemp">
    <div v-show="myHistShow" class="statisticInfo">
      <el-card>
        <div class="statisticPanel">
          <div class="infoTitle" @click="scrollToTop(0)">直方图</div>
          <div class="statisticPanelContent">

            <div class="histPanel">
              <div class="scroll scroll1">
                <span>数据显示比率({{ showNumber }}%)</span>
                <el-slider
                  v-model="showNumber"
                  :min="1"
                  :max="100"
                  class="rangeNumber"
                  @change="myChangeShownumber(showNumber)"
                />
              </div>
              <div class="scroll scroll2">
                <span>统计区间个数({{ binNumber }})</span>
                <el-slider
                  v-model="binNumber"
                  :min="10"
                  :max="100"
                  class="rangeNumber"
                  style="color:red"
                  @change="mySetBinNum(binNumber)"
                />
              </div>
              <div class="selectMode">
                <el-row>
                  <el-col :span="8">模式</el-col>
                  <el-col :span="16">
                    <el-select v-model="mode" class="histmodeselect" @change="myChangeMode(mode)">
                      <el-option value="三维">三维</el-option>
                      <el-option value="二维">二维</el-option>
                    </el-select>
                  </el-col>
                </el-row>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
    <div v-show="myDistShow" class="statisticInfo">
      <el-card>
        <div class="statisticPanel">
          <div class="infoTitle" @click="scrollToTop(1)">分布图</div>
          <div class="statisticPanelContent spanCenter">
            <span>暂无功能</span>
          </div>
        </div>
      </el-card>
    </div>
    <div class="statisticInfo">
      <el-card>
        <div class="info">
          <div class="infoTitle"><i class="el-icon-chat-dot-round dot" />数据信息栏</div>
          <div v-show="!infoShowFlag" class="statisticPanelContent spanCenter"><span>暂无信息</span></div>
          <div v-show="infoShowFlag" class="infoContent">
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
        </div>
      </el-card>
    </div>
  </div>
</template>
<script>
import { createNamespacedHelpers } from 'vuex'
const {
  mapMutations: mapStatisticMutations,
  mapGetters: mapStatisticGatters
} = createNamespacedHelpers('statistic')

export default {
  name: 'HistPanel',
  data() {
    return {
      mode: '三维',
      showNumber: 50,
      binNumber: 30,
      infoShowFlag: false,
      myHistShow: true,
      myDistShow: false
    }
  },
  computed: {
    ...mapStatisticGatters([
      'getShowNumber',
      'getMode',
      'getBinNum',
      'getStatisticInfo',
      'getHistShow',
      'getDistShow',
      'getFeatchDataFinished'
    ])
  },
  // 控制面板和左侧内容绑定
  // 监听滑动
  watch: {
    getStatisticInfo(val) {
      if (val.length) {
        this.infoShowFlag = true
      } else {
        this.infoShowFlag = false
      }
    },
    getShowNumber(val) {
      this.showNumber = val
    },
    getHistShow(val) {
      this.myHistShow = val
    },
    getDistShow(val) {
      this.myDistShow = val
    }
  },
  created() {
    this.mode = this.getMode
    this.showNumber = this.getShowNumber
    this.binNumber = this.getBinNum
    this.myHistShow = this.getHistShow
    this.myDistShow = this.getDistShow
  },
  methods: {
    ...mapStatisticMutations([
      'changeShownumber',
      'changeMode',
      'setBinNum',
      'setDataSetsState',
      'setHistShow',
      'setDistShow'
    ]),
    scrollToTop(index) {
      document.getElementsByClassName('statistics-container')[index].scrollIntoView(true)
    },
    myChangeShownumber(showNumber) {
      if (!this.getFeatchDataFinished) { // 没有绘制完，不允许操作控制面板，并还原数据
        this.$message({
          message: '统计分析页面还在渲染中，勿操作控制面板',
          type: 'warning'
        })
        this.showNumber = this.getShowNumber
      } else {
        this.changeShownumber(showNumber)
      }
    },
    myChangeMode(mode) {
      if (!this.getFeatchDataFinished) {
        this.$message({
          message: '统计分析页面还在渲染中，勿操作控制面板',
          type: 'warning'
        })
        this.mode = this.getMode
      } else {
        this.changeMode(mode)
      }
    },
    mySetBinNum(binNumber) {
      if (!this.getFeatchDataFinished) {
        this.$message({
          message: '统计分析页面还在渲染中，勿操作控制面板',
          type: 'warning'
        })
        this.binNumber = this.getBinNum
      } else {
        this.setBinNum(binNumber)
      }
    }
  }
}
</script>
<style>
.rangeNumber .el-slider__bar{
  background-color: #625eb3;
}
.rangeNumber .el-slider__button{
  border-color: #625eb3;
}
.histmodeselect .el-input__inner{
  border-radius: 50px;
  height: 30px;
  line-height: 30px;
  font-size:11px;
  border-color: #8c89c7;
  color: #625eb3;
}
.histmodeselect .el-input.is-focus .el-input__inner {
  border-color:#625eb3;
}
.histmodeselect .el-input__inner:focus{
  border-color:#625eb3;
}
.histmodeselect .el-input__icon{
  line-height: 30px;
}

.statisticPanelTemp .el-card__body  {
  border-radius: 0 0 3px 3px;
  padding: 0px;
}
.statisticPanelTemp .el-card{
  margin:3.5% 5% 4% 0%;
  border-top: 0px;
}
.histmodeselect .el-input .el-select__caret{
  color: #9492cb;
  font-size:20px;
}
.histmodeselect [class*=" el-icon-"], [class^=el-icon-]{
  font-weight: 900;
}
.el-select:hover .el-input__inner{
  border-color:#625eb3;
}
.rangeNumber .el-slider__button{
  width: 8px;
  height: 8px;
}
.rangeNumber .el-slider__runway, .rangeNumber .el-slider__bar{
  height: 5px;
}
</style>
