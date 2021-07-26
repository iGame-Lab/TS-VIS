<style lang='less' scoped>
.statisticContainer {
  background-color: white;
  width: 100%;
  height: 100%;
  .statisticContainerTitle, .statisticContainerTitleLarge{
    color: white;
    text-align: left;
    padding: 0 2% 0 2%;
    border-radius:2px;
    display:flex;
    height: 30px;
    line-height: 30px;
    .scale:hover, .checkedBox:hover{
      cursor: pointer;
    }
    .titleRight{
      margin-left: auto;
      margin-right: 1%;
    }
  }
  .statisticContainerTitle{
    font-size: 11px;
    .iconfont{
      font-size: 11px;
    }
  }
  .statisticContainerTitleLarge {
    font-size: 16px;
    .iconfont{
      font-size: 16px;
    }
  }
}
</style>
<template>
  <div class="statisticContainer">
    <el-card>
      <div :class="[scaleLargeSmall?'statisticContainerTitleLarge':'statisticContainerTitle']" :style="{'background-color':runColor}">
        <div>
          <span style="font-weight:600;">{{ ttlabel }}</span>
          <span class="tagShow">{{ newTag }}</span>
        </div>
        <div class="titleRight">
          <span class="scale" @click="scaleLarge()"><i class="iconfont icon-fangda" /></span>
          <span class="scale" @click="scaleSmall()"><i class="iconfont icon-suoxiao1" /></span>
          <span v-if="!parentComponent" class="checkedBox" @click="setRightTopShow()"><i class="close-i el-icon-circle-close" /></span>
          <span v-if="parentComponent" v-show="!rightTopShow" class="checkedBox" @click="setRightTopShow()"><i class="iconfont icon-weixuanzhong1" /></span>
          <span v-if="parentComponent" v-show="rightTopShow" class="checkedBox" @click="setRightTopShow()"><i class="iconfont icon-xuanzhong1" /></span>
        </div>
      </div>
      <component
        :is="componentName"
        :data="rateData"
        :ttlabel="ttlabel"
        :tag="tag"
        :itemp="itemp"
        :className="className"
        :runColor="runColor"
      />
    </el-card>
  </div>
</template>
<script>
import * as d3 from 'd3'
import { createNamespacedHelpers } from 'vuex'
import threed from './HisThreeD'
import orthographic from './HisOrtho'
import overlook from './HisOverlook'
const { mapGetters: mapStatisticGetters, mapMutations: mapStatisticMutations } = createNamespacedHelpers('statistic')
const { mapMutations: mapCustomMutations, mapGetters: mapCustomGetters } = createNamespacedHelpers('custom')
const { mapGetters: mapLayoutGetters } = createNamespacedHelpers('layout')
export default {
  components: {
    threed,
    orthographic,
    overlook
  },
  props: {
    data: Array,
    ttlabel: String,
    tag: String,
    itemp: Number,
    componentName: String,
    runColor: String,
    divId: String,
    parentComponent: Boolean
  },
  data() {
    return {
      className: this.componentName + this.itemp,
      newTag: this.tag,
      rightTopShow: false,
      scaleLargeSmall: false, // false表示未放大，true表示放大
      rateData: [] // 按显示比率从data中取部分data
    }
  },
  computed: {
    ...mapStatisticGetters([
      'getDistCheckedArray',
      'getHistCheckedArray',
      'getShowNumber',
      'getDownLoadArray'
    ]),
    ...mapCustomGetters(['getStatisticShowNumber']),
    ...mapLayoutGetters(['setDownloadSvgClass'])
  },
  watch: {
    getShowNumber(val) {
      this.setRangeNumber()
    },
    getStatisticShowNumber(val) { // 用户定制控制面板
      this.setRangeNumber()
    },
    data: function() {
      if (this.componentName === 'threed' || this.componentName === 'orthographic') {
        this.setRangeNumber()
      } else {
        this.rateData = this.data
      }
    }
  },
  created() {
    // 根据显示比率只给后面一定数据
    if (this.componentName === 'threed' || this.componentName === 'orthographic') {
      this.setRangeNumber()
    } else {
      this.rateData = this.data
    }
    let idx = this.itemp
    if (this.itemp >= 1000) idx = idx - 1000 // 这是用户定制的itemp
    if (this.tag.length > 20) this.newTag = this.tag.slice(0, 20) + '...' // 省略显示字符
    if (this.componentName === 'threed' || this.componentName === 'orthographic') {
      this.rightTopShow = this.getHistCheckedArray[idx]
    } else {
      this.rightTopShow = this.getDistCheckedArray[idx]
    }
    this.setDownloadSvgClass['statistic'] = this.getDownLoadArray
  },
  methods: {
    ...mapStatisticMutations(['setHistCheckedArray', 'setDistCheckedArray', 'setDownLoadArray']),
    ...mapCustomMutations(['setStatisticData']),
    scaleLarge() {
      this.scaleLargeSmall = true
      d3.select('#' + this.divId).style('width', '63.5%')
      if (this.tag.length > 40) this.newTag = this.tag.slice(0, 40) + '...'
      else this.newTag = this.tag
    },
    scaleSmall() {
      this.scaleLargeSmall = false
      d3.select('#' + this.divId).style('width', '31%')
      if (this.tag.length > 20) this.newTag = this.tag.slice(0, 20) + '...'
    },
    setRightTopShow() {
      if (this.rightTopShow || this.parentComponent) {
        let idx = this.itemp
        if (this.itemp >= 1000) idx = idx - 1000
        if (this.componentName === 'threed' || this.componentName === 'orthographic') {
          this.rightTopShow = !this.rightTopShow
          this.setHistCheckedArray({ idx: idx, value: this.rightTopShow })
        } else {
          this.rightTopShow = !this.rightTopShow
          this.setDistCheckedArray({ idx: idx, value: this.rightTopShow })
        }
      }
      // 用户定制
      // substatistics中的操作在statistic上
      // custom中的×点击直接操作在statisticData上
      let componentNameTemp = this.componentName
      if (componentNameTemp === 'orthographic') componentNameTemp = 'threed'
      const param = { componentName: componentNameTemp, ttlabel: this.ttlabel, tag: this.tag, data: this.data, runColor: this.runColor, itemp: this.itemp, divId: '', delete: false } // delete表示不直接删除statisticData中的, checked: this.rightTopShow,
      if (!this.parentComponent) param.delete = true
      this.setStatisticData(param)
      // 复选框复用，下载按钮
      // 不用考虑用户定制里的
      if (this.itemp > 1000) return
      let idTemp = '#dist' + this.itemp
      if (this.componentName === 'threed') {
        idTemp = '#offset' + this.itemp
      } else if (this.componentName === 'orthographic') {
        idTemp = '#overlay' + this.itemp
      }
      this.setDownLoadArray([this.rightTopShow, idTemp])
      this.setDownloadSvgClass['statistic'] = this.getDownLoadArray
    },
    setRangeNumber: function() {
      if (this.componentName !== 'overlook') {
        let newNumber = this.getShowNumber
        if (!this.parentComponent) newNumber = this.getStatisticShowNumber
        const datalen = this.data.length
        const count = Math.ceil(newNumber / 100.0 * datalen)
        const stepspace = datalen / count
        this.rateData = []
        for (let j = 0; j < count; j++) {
          const step = Math.floor(stepspace * j)
          this.rateData.push(this.data[step])
        }
      }
    }
  }
}
</script>
<style lang='less'>
.statisticContainer .axis line,
.statisticContainer .axis path {
  stroke: gainsboro;
}
.statisticContainer .axis text {
  color: grey;
  font-size: 6px;
}
.statisticContainer .grid {
  stroke: gainsboro;
}
.statisticContainer .el-card__body {
  padding: 0px;
}
.statisticContainer .el-card{
  border-radius: 0 0 3px 3px;
}
</style>
