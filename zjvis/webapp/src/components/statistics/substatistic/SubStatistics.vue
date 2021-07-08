<style lang='less' scoped>
.statistics-container {
  background-color: #FFF;
  margin-bottom:0.5%;
  .statistics-title {
    height: auto;
    display: flex;
    align-items: center;
    color: white;
    background-color: white;
  }
  .statistics-content {
    margin-left: 1%;
    position: relative;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
    height: 100%;
    .allStatisticContainer{
      width: 31%; // 一行放三个
      height: 100%;
      margin: 0.8%;
      background-color:white;
      .statisticContaierContent{
        width: 100%;
        .runTag{
          width:100%;
        }
      }
    }
  }
}
.showClass {
  display: none;
}
.my-label{
  display:flex;
  width: 100%;
  cursor: pointer;
  .triangle{
    position: absolute;
    width: 0px;
    height: 0px;
    overflow: hidden;
    border-top-width: 15px;
    border-bottom-width: 15px;
    border-left-width: 18px;
    border-right-width: 18px;
    border-style: dashed  dashed  dashed solid;
    border-color: transparent transparent   transparent #7f7cc1;
  }
  .triangle-father{
    position: relative;
  }
  .circle-father{
    height: 30px;
    width: 15%;
    position: relative;
    background-color:#7f7cc1;
  }
  .circle{
    position: absolute;
    width:8px;
    height: 8px;
    border-radius: 50%;
    background-color: white;
    left: 50%;
    top: 50%;
    transform: translateX(-50%) translateY(-50%);
  }
  .my-text{
    width: 70%;
    height: 30px;
    text-align: center;
    vertical-align: center;
    background-color:#7f7cc1;
  }
  span{
    align-items: center;
    line-height: 30px;
    color:white;
  }
}
.sub .triangle{
  border-color: transparent transparent   transparent #b8c6ff;
}
.sub .circle-father{
  background-color:#b8c6ff;
}
.sub .my-text{
  background-color:#b8c6ff;
}
.sub{
  background-size: 100% 100%;
  width: 9.5%;
  height:30px;
  display: flex;
  align-items: center;
  font-family: sans-serif;
  font-size: 12px;
  color: #FFF;
}
.sub1{
  background-size: 100% 100%;
  width: 9.5%;
  height:30px;
  display: flex;
  align-items: center;
  font-family: sans-serif;
  font-size: 12px;
  color: #FFF;
}
.line1 {
  height: 1px;
  width: 88%;
  background-color: #F4F6FF;
}
.line2 {
  height: 5px;
  width:2.5%;
  background-color: #625EB3;
}
.linestyle{
  background-color: #b9c6ff;
}
</style>
<template>
  <div class="statistics-container">
    <div class="statistics-title" @click="showContent()">
      <div :class="[showFlag?'sub1':'sub']">
        <div class="my-label">
          <div class="my-text"><span>{{ categoryName }}</span></div>
          <div class="circle-father"><div class="circle" /></div>
          <div class="triangle-father">
            <div class="triangle" />
          </div>
        </div>
      </div>
      <div class="line1" />
      <div :class="['line2', showFlag?'':'linestyle']" />
    </div>
    <div :class="[showFlag?'':'showClass']">
      <div>
        <div v-for="(oneRunData, runIdx) in runData" :key="runIdx" :class="['statistics-content']">
          <div v-for="(item, index) in oneRunData" v-show="getDataSetsState[item[0]]" :id="[idArray[item[4]]]" :key="index" class="allStatisticContainer">
            <statisticContainer
              :data="item[2]"
              :ttlabel="item[0]"
              :tag="item[1]"
              :itemp="item[4]"
              :componentName="componentName"
              :runColor="getStatisticColor[item[3] % 5]"
              :divId="idArray[item[4]]"
              :parentComponent="parentComponent"
              checked="false"
              class="statisticContaierContent"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { statisticContainer } from '../drawStatistic'
import { createNamespacedHelpers } from 'vuex'
const {
  mapGetters: mapStatisticGetters,
  mapActions: mapStatisticActions,
  mapMutations: mapStatisticMutations
} = createNamespacedHelpers('statistic')
const { mapState: mapLayoutStates } = createNamespacedHelpers('layout')
export default {
  components: {
    statisticContainer
  },
  props: {
    categoryInfo: String
  },
  data() {
    return {
      showFlag: '',
      componentName: this.categoryInfo,
      categoryName: '',
      allData: [],
      runData: [],
      idArray: [],
      parentComponent: true
    }
  },
  computed: {
    ...mapStatisticGetters([
      'getInitStateFlag',
      'getBinNum',
      'getDistData',
      'getHistData',
      'getMode',
      'getShowStatisticFlag',
      'getDataSets',
      'getDataSetsState',
      'getStatisticColor',
      'getHistShow',
      'getDistShow'
    ]),
    ...mapLayoutStates([
      'userSelectRunFile'
    ])
  },
  watch: {
    getMode(curMode) {
      if (this.categoryInfo === 'histogram') {
        if (curMode === '三维') {
          this.componentName = 'threed'
        } else {
          this.componentName = 'orthographic'
        }
      }
    },
    getBinNum(newBinNum) {
      if (this.categoryInfo === 'histogram') {
        this.manageHistData(true)
      }
    },
    getHistData(data) {
      if (this.categoryInfo === 'histogram') {
        this.allData = data
        this.idArray = []
        for (let i = 0; i < this.allData.length; i++) {
          this.idArray.push('myHistogramScale' + i)
        }
        this.setRunData()
      }
    },
    getDistData(data) {
      if (this.categoryInfo === 'distribution') {
        this.allData = data
        this.idArray = []
        for (let i = 0; i < this.allData.length; i++) {
          this.idArray.push('myDistributionScale' + i)
        }
        this.setRunData()
      }
    },
    userSelectRunFile: function() {
      this.setDatasetsShow()
    },
    getHistShow(val) {
      if (this.categoryInfo === 'histogram') {
        this.showFlag = val
        if (val) {
          document.getElementsByClassName('statistics-container')[0].scrollIntoView(true)
        }
      }
    },
    getDistShow(val) {
      if (this.categoryInfo === 'distribution') {
        this.showFlag = val
        if (val) {
          this.setDistData()
          document.getElementsByClassName('statistics-container')[1].scrollIntoView(true) // 书签滑到页面最顶端
        }
      }
    }
  },
  created() {
    if (this.categoryInfo === 'histogram') {
      this.categoryName = '直方图'
      this.showFlag = true
      this.setHistShow(true) // 初始默认
      this.setHistData()
    } else {
      this.categoryName = '分布图'
      this.showFlag = false
      this.setDistShow(false)
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll, true) // 监听滑动条
    this.setDatasetsShow()
  },
  methods: {
    ...mapStatisticActions(['featchAllDistData', 'featchAllHistData']),
    ...mapStatisticMutations([
      'manageHistData',
      'setDataSetsState',
      'setInitStateFlag',
      'setHistShow',
      'setDistShow'
    ]),
    showContent() {
      if (this.categoryInfo === 'histogram') {
        this.setHistShow(!this.showFlag)
      } else {
        this.setDistShow(!this.showFlag)
      }
    },
    setHistData() {
      if (this.getMode === '三维') {
        this.componentName = 'threed'
      } else {
        this.componentName = 'orthographic'
      }
      // 如果第一个页面标记为true，不用再重新获取数据
      if (this.getInitStateFlag) {
        this.setInitStateFlag(false)
        return
      }
      if (!this.getInitStateFlag && this.getHistData.length === 0) {
        this.featchAllHistData()
        return
      }
      // 有数据
      this.allData = this.getHistData
      this.idArray = []
      for (let i = 0; i < this.allData.length; i++) {
        this.idArray.push('myHistogramScale' + i)
      }
      this.setRunData()
    },
    setDistData() {
      this.componentName = 'overlook'
      if (this.getDistData.length === 0) {
        this.featchAllDistData()
        return
      }
      this.allData = this.getDistData
      this.idArray = []
      for (let i = 0; i < this.allData.length; i++) {
        this.idArray.push('myDistributionScale' + i)
      }
      this.setRunData()
    },
    handleScroll(e) { // 页面滑动过程中修改histDist标志，高亮右侧控制面板
      if (document.getElementsByClassName('statistics-container')[1] !== undefined) {
        const curDistHeight = document.getElementsByClassName('statistics-container')[1].getBoundingClientRect().top
        if (curDistHeight < window.innerHeight * 0.7) {
          this.setDistShow(true)
        } else if (curDistHeight > window.innerHeight) {
          this.setHistShow(true)
        }
      }
    },
    setDatasetsShow() {
      const stateTemp = []
      for (let i = 0; i < this.getDataSets.length; i++) {
        stateTemp[this.getDataSets[i]] = false
      }
      for (let i = 0; i < this.userSelectRunFile.length; i++) {
        stateTemp[this.userSelectRunFile[i]] = true
      }
      // userselectRunFiles没有保存状态，statistic保存run状态
      this.setDataSetsState(stateTemp)
    },
    setRunData() { // 按run对得到的数据再处理一下
      if (this.allData.length === 0) {
        this.runData = []
        return
      }
      let count = 0
      const runDataTemp = [[this.allData[0]]]
      for (let i = 1; i < this.allData.length; i++) {
        if (this.allData[i][0] !== this.allData[i - 1][0]) {
          count++
          runDataTemp.push([])
        }
        runDataTemp[count].push(this.allData[i])
      }
      this.runData = runDataTemp
    }
  }
}
</script>
