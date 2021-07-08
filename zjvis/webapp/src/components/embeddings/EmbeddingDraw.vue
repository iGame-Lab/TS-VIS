<style lang="less" scoped>
/deep/.dimension{
  .axis text{
    font-size: 12px;
    stroke: rgb(115, 111, 188);
  }
  .axis path{
    stroke: rgb(115, 111, 188);
    stroke-width: 2px;
  }
  .axis line{
    stroke: rgb(115, 111, 188);
    stroke-width: 2px;
  }
}
/deep/#subgroup{
  circle{
    cursor: pointer;
  }
}
/deep/#foreground{
  path{
    cursor: pointer;
  }
}
#background path {
  fill: none;
  stroke: #ccc;
  stroke-opacity: .4;
  shape-rendering: crispEdges;
}

.brush .extent {
  fill-opacity: .3;
  stroke: #fff;
  shape-rendering: crispEdges;
}
  svg{
  /* border: 1px solid #e1e1e1; */
  border-radius: 10px;
  padding: 10px;
  }
  .draw{
    width: 100%;
    height: 100%;
    display: block;
  }
  .container{
    width: 100%;
    height: 100%;
    display: block;
    position: relative
  }
  #threeDimension{
    width: 100%;
    height: 100%;
    display: block;
  }
  #towDimension{
    width: 100%;
    height: 100%;
    display: block;
  }
  .loading{
    position: fixed;
    width: 400px;
    height: 400px;
    /* z-index: 9999; */
    top: 50%;
    left: 50%;
    -webkit-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    border-radius: 50%;
  }
  .noloading{
    position: fixed;
    width: 400px;
    height: 400px;
    /* z-index: -9999; */
    display: none;
    top: 50%;
    left: 50%;
    -webkit-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }
  #echarts{
    border: 1px solid #e1e1e1;
    border-radius: 10px;
    padding: 10px;
    display: block;
    width: 100%;
    height: 100%;
  }
  #title{
    margin-top: 2%;
    color: #1363A0;
    font-size: 20px;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }
  .image {
    width: 100%;
    display: block;
  }
  .labelBackground {
    background-color: yellowgreen;
  }
</style>

<template>
  <div class="container">
    <span id="title">#{{ getCurInfo.curMethod }} - {{ getCurInfo.curDim }} | Current-Step : {{ getCurInfo.curMapStep }}</span>
    <div id="main" ref="draw" class="draw">
      <div v-show="getCurInfo.curDim === '3维'" id="threeDimension" style="width:100%" />
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import echarts from 'echarts'
import constant from '@/utils/constants'
import 'echarts-gl'
import { createNamespacedHelpers } from 'vuex'
const {
  mapGetters: mapEmbeddingGetters,
  mapMutations: mapEmbeddingMutations
} = createNamespacedHelpers('embedding')
const { mapState: mapLayoutStates } = createNamespacedHelpers('layout')
export default {
  data() {
    return {
      width: '100%',
      height: '100%',
      loadFlag: true,
      halfHight: 0,
      halfWidth: 0,
      circleUpdate: '',
      circleEnter: '',
      circleExit: '',
      axisPoint: [
        [100, 0, 0],
        [0, 100, 0],
        [0, 0, 100]
      ],
      axisUpdate: '',
      axisEnter: '',
      axisExit: '',
      position: 0, // 鼠标拖拽功能
      xAxisFloat: 80,
      yAxisFloat: 60,
      xScale: '',
      yScale: '', // 缩放统一
      xAxis: '',
      yAxis: '',
      margin: {
        top: 100,
        right: 120,
        bottom: 100,
        left: 120
      },
      dataAttr: {
        maxX: 0,
        maxY: 0,
        minX: 0,
        minY: 0
      },
      ParaCoor: {
        backgroundUpdate: '',
        backgroundExit: '',
        backgroundEnter: '',
        foregroundUpdate: '',
        foregroundExit: '',
        foregroundEnter: '',
        dimensionsUpdate: '',
        dimensionsExit: '',
        dimensionsEnter: '',
        dimensionFlag: false // 是否已经加入坐标轴
      },
      clickEle: false, // 是否选点
      myChart: '',
      localCurInfo: {}
    }
  },
  computed: {
    ...mapEmbeddingGetters([
      'getCurInfo',
      'getCurData',
      'getCheckLabels',
      'getLegendColor',
      'getLineWidth'
    ]),
    ...mapLayoutStates([
      'userSelectRunFile'
    ]),
    clickEleCumputed: {
      get: function() {
        return this.clickEle
      },
      set: function(val) {
        this.clickEle = val
      }
    }
  },
  watch: {
    getLineWidth: function() {
      this.renderUpdate(this.getCurData)
    },
    getCurInfo: {
      handler: function(val, olVal) {
        if (JSON.stringify(this.localCurInfo) === '{}') {
          this.localCurInfo = JSON.parse(JSON.stringify(val))
          this.renderInit()
        } else {
          if (val.curDim !== this.localCurInfo.curDim) {
            this.localCurInfo = JSON.parse(JSON.stringify(val))
            this.renderInit()
          }
        }
      },
      deep: true
    },
    getCurData: {
      handler: function(val, olVal) {
        this.renderUpdate(val)
      },
      deep: true
    },
    getCheckLabels: function() {
      this.renderUpdate(this.getCurData)
    },
    userSelectRunFile: function() {
      this.renderInit()
    }
  },
  mounted() {
    this.renderInit()
    if (typeof (this.getCurData) !== 'undefined') {
      this.renderUpdate(this.getCurData)
    }
  },
  methods: {
    ...mapEmbeddingMutations(['setMessage']),
    renderInit: function() {
      if (JSON.stringify(this.localCurInfo) === '{}') {
        return
      } else if (parseInt(this.localCurInfo.curDim) === 3) { // 是3维显示
        this.renderThreeInit()
      } else if (parseInt(this.localCurInfo.curDim) === 2) {
        this.renderTwoInit()
      } else {
        this.renderNInit()
      }
    },
    unique(array) {
      return Array.from(new Set(array))
    },
    renderTwoInit: function(data) {
      var vm = this
      this.height = d3.select(this.$refs.draw).node().getBoundingClientRect().height
      this.width = d3.select(this.$refs.draw).node().getBoundingClientRect().width
      d3.select(this.$refs.draw).select('svg').remove() // 先清空svg
      const svg = d3.select(this.$refs.draw).append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('preserveAspectRatio', 'xMidYMid meet') // 自适应相关
        .attr('viewBox', `0 0 ${this.width} ${this.height}`)
      vm.margin = {
        top: 100,
        right: 120,
        bottom: 100,
        left: 120
      }
      const g = svg.append('g')
        .attr('transform', `translate(${vm.margin.left}, ${vm.margin.top})`)
        .attr('id', 'maingroup')
      vm.xScale = d3.scaleLinear()
        .domain([vm.dataAttr.minX, vm.dataAttr.maxX])
        .range([0, this.width - this.margin.left - this.margin.right])
      vm.yScale = d3.scaleLinear()
        .domain([vm.dataAttr.minY, vm.dataAttr.maxY].reverse())
        .range([0, this.height - this.margin.top - this.margin.bottom])
      g
        .append('defs')
        .append('clipPath')
        .attr('id', 'clip')
        .append('rect')
        .attr('width', (vm.width - vm.margin.left - vm.margin.right))
        .attr('height', (vm.height - vm.margin.top - vm.margin.bottom))
        .attr('x', 0) // margin.left
        .attr('y', 0) // margin.top
      vm.yAxis = d3.axisLeft(vm.yScale)
        .tickSize(-(this.width - this.margin.left - this.margin.right))
        .tickPadding(10) // .tickPadding is used to prevend intersection of ticks
      vm.xAxis = d3.axisBottom(vm.xScale)
        .tickSize(-(this.height - this.margin.top - this.margin.bottom))
        .tickPadding(10)
      // eslint-disable-next-line
      const xAxisLabel = 'X'
      // eslint-disable-next-line
      const yAxisLabel = 'Y'
      // eslint-disable-next-line
      var yAxisGroup = g
        .append('g')
        .call(vm.yAxis)
        .attr('id', 'yaxis')
        .attr('font-size', '16px')
        .attr('color', '#736FBC')
      // yAxisGroup
      //   .append('text')
      //   .attr('transform', `rotate(-90)`)
      //   .attr('x', -(this.height - this.margin.top - this.margin.bottom) / 2)
      //   .attr('y', -vm.yAxisFloat)
      //   .attr('fill', '#333333')
      //   .attr('font-size', '20px')
      //   .text(yAxisLabel)
      //   .attr('text-anchor', 'middle') // Make label at the middle of axis.
      // eslint-disable-next-line
      var xAxisGroup = g
        .append('g')
        .call(vm.xAxis)
        .attr('transform', `translate(${0}, ${(vm.height - vm.margin.top - vm.margin.bottom)})`)
        .attr('id', 'xaxis')
        .attr('font-size', '16px')
        .attr('color', '#736FBC')
      // xAxisGroup
      //   .append('text')
      //   .attr('y', vm.xAxisFloat)
      //   .attr('x', (this.width - this.margin.left - this.margin.right) / 2)
      //   .attr('fill', '#333333')
      //   .text(xAxisLabel)
      // 新增 tooltip
      d3.select(this.$refs.draw).selectAll('.tooltip').remove()
      d3.select(this.$refs.draw).append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0)
        .style('background-color', 'white')
        .style('border', 'solid')
        .style('border-width', '1px')
        .style('border-radius', '20px')
        .style('padding', '10px')
        .style('position', 'absolute')
        .style('z-index', '5')
        .style('left', '0')
        .style('top', '0')
        .style('color', '#7C78C0')
      var brush = d3
        .brush()
        .extent([
          [0, 0],
          [(vm.width - vm.margin.left - vm.margin.right), (vm.height - vm.margin.top - vm.margin.bottom)]
        ])
        .on('end', () => {
          var s = d3.event.selection // brushended 会触发两次为什么么
          if (!s) {
            if (!idleTimeout) return (idleTimeout = setTimeout(idled, idleDelay)) //  方法用于在指定的毫秒数后调用函数或计算表达式。
            // 还原
            vm.xScale
              .domain(d3.extent(vm.getCurData.data, (d) => d[0]))
              .range([0, (vm.width - vm.margin.left - vm.margin.right)])
              .nice()
            vm.yScale
              .domain(d3.extent(vm.getCurData.data, (d) => d[1]).reverse()) // remember to use reverse() to make y-axis start from the bottom
              .range([0, (vm.height - vm.margin.top - vm.margin.bottom)])
              .nice()
          } else {
            // 逻辑上是缩放
            vm.xScale
              .domain([s[0][0], s[1][0]].map(vm.xScale.invert, vm.xScale)) // X1 X2
              .range([0, (vm.width - vm.margin.left - vm.margin.right)])
              .nice()
            vm.yScale
              .domain([s[0][1], s[1][1]].map(vm.yScale.invert, vm.yScale)) // Y1 Y2
              .range([0, (vm.height - vm.margin.top - vm.margin.bottom)])
              .nice()
            g.select('.brush').call(brush.move, null)
          }
          zoom()
        })
      var idleTimeout = null
      var idleDelay = 350
      g.append('g')
        .attr('class', 'brush')
        .call(brush)
      var gscatter = g
        .append('g')
        .attr('clip-path', 'url(#clip)')
        .attr('id', 'subgroup')

      function idled() {
        idleTimeout = null
      }

      function zoom() {
        var t = gscatter.transition().duration(750)
        g.select('#xaxis')
          .transition(t)
          .call(vm.xAxis)
        g.select('#yaxis')
          .transition(t)
          .call(vm.yAxis)
        gscatter
          .selectAll('circle')
          .transition(t)
          .attr('cx', datum => {
            return vm.xScale(datum[0])
          })
          .attr('cy', datum => {
            return vm.yScale(datum[1])
          })
      }
    },
    renderThreeInit: function(data) {
      d3.select('#threeDimension').selectAll('div').remove()
      d3.select('#threeDimension')
        .append('div')
        .attr('id', 'threeChild')
        .style('width', '100%')
        .style('height', '100%')
        .style('display', 'block')
      var vm = this
      this.height = d3.select(this.$refs.draw).node().getBoundingClientRect().height
      this.width = d3.select(this.$refs.draw).node().getBoundingClientRect().width

      d3.select(this.$refs.draw).select('svg').remove() // 先清空svg
      vm.margin = {
        top: 100,
        right: 120,
        bottom: 100,
        left: 120
      }
    },
    renderNInit: function(data) {
      var vm = this
      this.height = d3.select(this.$refs.draw).node().getBoundingClientRect().height
      this.width = d3.select(this.$refs.draw).node().getBoundingClientRect().width
      d3.select(this.$refs.draw).select('svg').remove() // 先清空svg
      this.margin.top = 100
      this.margin.left = 10
      this.margin.bottom = 100
      this.margin.right = 10
      const svg = d3.select(this.$refs.draw).append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('preserveAspectRatio', 'xMidYMid meet')
        .attr('viewBox', `0 0 ${this.width} ${this.height}`)

      const gMain = svg
        .append('g')
        .attr('id', 'mainGroup')
        .attr('transform', `translate(${vm.margin.left}, ${vm.margin.top})`)
      gMain
        .append('g')
        .attr('id', 'background')
      gMain
        .append('g')
        .attr('id', 'foreground')
      vm.ParaCoor.dimensionFlag = false
      d3.select(this.$refs.draw).selectAll('.tooltip').remove()
      d3.select(this.$refs.draw).append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0)
        .style('background-color', 'white')
        .style('border', 'solid')
        .style('border-width', '1px')
        .style('border-radius', '20px')
        .style('padding', '10px')
        .style('position', 'absolute')
        .style('z-index', '5')
        .style('left', '0')
        .style('top', '0')
        .style('color', '#7C78C0')
    },
    renderNUpdate: function(localData) {
      var vm = this
      var x = d3.scalePoint().rangeRound([0, vm.width]).padding(1)
      var y = {}
      var dragging = {}
      var data = []
      var dimensions
      var line = d3.line()
      var myEPS = 0.0000000001
      var minValue = {} // 每个维度对应的最大最小值
      var maxValue = {}
      const str = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
      const strChange = ['1st dim', '2nd dim', '3rd dim', '4th dim', '5th dim', '6th dim', '7th dim', '8th dim']
      var quantP = function(v) {
        return (parseFloat(v) === v) || (v === '')
      }
      for (let i = 0; i < localData.data.length; i++) {
        const tmp = {}
        for (let j = 0; j < localData.data[i].length; j++) {
          tmp[str[j]] = localData.data[i][j]
        }
        data.push(tmp)
      }
      // 得到全局维度的最大最小值
      dimensions = d3.keys(data[0])
      x.domain(dimensions)

      dimensions.forEach(function(d) {
        var vals = data.map(function(p) {
          return p[d] // 取出每个维度对应的数值
        })
        if (vals.every(quantP)) {
          maxValue[d] = d3.max(data, function(p) { return +p[d] })
          minValue[d] = d3.min(data, function(p) { return +p[d] })
          y[d] = d3.scaleLinear()
            .domain([minValue[d], maxValue[d]])
            .range([vm.height - vm.margin.top - vm.margin.bottom, 0])
        } else {
          vals.sort()
          y[d] = d3.scalePoint()
            .domain(vals.filter(function(v, i) {
              return vals.indexOf(v) === i
            }))
            .range([vm.height - vm.margin.top - vm.margin.bottom, 0], 1)
        }
      })
      const gMain = d3.select('#mainGroup')
      const gMainBackground = gMain.select('#background')
      // background
      vm.ParaCoor.backgroundUpdate = gMainBackground
        .selectAll('path')
        .data(data)
      vm.ParaCoor.backgroundExit = vm.ParaCoor.backgroundUpdate.exit()
      vm.ParaCoor.backgroundEnter = vm.ParaCoor.backgroundUpdate.enter().append('path')
        .attr('d', path)
        .attr('fill', 'none')
        .attr('stroke-width', vm.getLineWidth.toString())
      vm.ParaCoor.backgroundUpdate.merge(vm.ParaCoor.backgroundEnter).transition().ease(d3.easeLinear).duration(1000)
        .attr('d', path)
        .attr('fill', 'none')
        .attr('stroke', '#ccc')
        .attr('stroke-width', vm.getLineWidth.toString())
      // foreground
      const gMainFroeground = gMain.select('#foreground')
      vm.ParaCoor.foregroundUpdate = gMainFroeground
        .selectAll('path')
        .data(data)
      vm.ParaCoor.foregroundExit = vm.ParaCoor.foregroundUpdate.exit()
      vm.ParaCoor.foregroundEnter = vm.ParaCoor.foregroundUpdate.enter().append('path')
        .attr('d', path)
        .attr('fill', 'none')
        .on('mouseover', function(d, i) {
          // 提示框
          const div = d3.selectAll('div.tooltip')
          const value = localData.label[i]
          div
            .style('opacity', 0.9)
          div.html(`第${i + 1}个数据，标签为${value}`)
            .style('left', (d3.event.offsetX + 30) + 'px')
            .style('top', (d3.event.offsetY - 10) + 'px')
            .style('z-index', 5)
          vm.ParaCoor.foregroundUpdate.merge(vm.ParaCoor.foregroundEnter).style('display', 'none')
          d3.select(this)
            .transition()
            .duration('50')
            .attr('stroke-width', '5px')
            .attr('stroke-opacity', '1')
            .style('display', null)
        })
        .on('mouseout', function(d, i) {
          vm.ParaCoor.foregroundUpdate.merge(vm.ParaCoor.foregroundEnter).style('display', null)
          d3.select(this)
            .transition()
            .duration('50')
            .attr('stroke-width', vm.getLineWidth.toString())
            .attr('stroke-opacity', '0.4')
          const div = d3.selectAll('div.tooltip')
          div
            .style('opacity', 0)
            .style('z-index', -1)
        })
        .on('click', function(d, i) {
          d3.event.stopPropagation() // 阻止事件冒泡即可
          d3.select(this)
            .transition()
            .duration(50)
            .attr('opacity', 1) // 自己的透明度为1i
          const value = localData.label[i]
          vm.setMessage([`${constant.IMGURl}/api/projector_sample?run=${vm.userSelectRunFile}&tag=${vm.getCurInfo.curTag}&index=${i}`, `第${i + 1}个点,标签为${value}`])
        })
        .attr('stroke', function(datum, index) {
          if (typeof (vm.getCurData.labelTypeColor[localData.label[index].toString()]) !== 'undefined') {
            return vm.getCurData.labelTypeColor[localData.label[index].toString()]
          } else {
            return vm.getLegendColor[9]
          }
        })
      vm.ParaCoor.foregroundUpdate.merge(vm.ParaCoor.foregroundEnter).transition().ease(d3.easeLinear).duration(1000)
        .attr('d', path)
        .attr('fill', 'none')
        .attr('stroke-opacity', '0.4')
        .attr('stroke-width', vm.getLineWidth.toString())
        .attr('padding', '2px')
        .attr('stroke', function(datum, index) {
          if (typeof (vm.getCurData.labelTypeColor[localData.label[index].toString()]) !== 'undefined') {
            return vm.getCurData.labelTypeColor[localData.label[index].toString()]
          } else {
            return vm.getLegendColor[9]
          }
        })
      // dimensions
      vm.ParaCoor.dimensionsUpdate = gMain.selectAll('.dimension').data(dimensions)
      vm.ParaCoor.dimensionsExit = vm.ParaCoor.dimensionsUpdate.exit()
      vm.ParaCoor.dimensionsEnter = vm.ParaCoor.dimensionsUpdate.enter().append('g')
        .attr('class', 'dimension')
        .attr('transform', function(d) {
          return 'translate(' + x(d) + ')'
        })
      vm.ParaCoor.dimensionsUpdate.merge(vm.ParaCoor.dimensionsEnter)
        .transition().ease(d3.easeLinear).duration(1000)
      gMain.selectAll('.dimension').selectAll('g').remove()
      // 构建 柱状图显示结构体
      // 加入 坐标轴 和 标题
      const ticksAmount = 15 // ticks 条数
      const ticksHis = ticksAmount * 5 // 要显示的柱状图分支
      gMain.selectAll('.dimension')
        .append('g')
        .attr('class', 'axis')
        .each(function(d) {
          const tickStep = (maxValue[d] - minValue[d]) / (ticksAmount)
          const step = tickStep
          d3.select(this).call(
            d3.axisLeft(y[d])
              .ticks(ticksAmount)
              .tickFormat(function(d) {
                if (tickStep > 0.002 && tickStep < 1000) {
                  return d3.format('.3f')(d)
                } else {
                  return d3.format('.2e')(d)
                }
              })
              .tickValues(d3.range(minValue[d], maxValue[d] + step - myEPS, step)))
        })
        .append('g')
        .attr('class', 'labelBackground')
        .append('text')
        .attr('class', 'textShow')
        .attr('fill', '#1363a0')
        .style('text-anchor', 'middle')
        .attr('y', vm.height + 30 - vm.margin.top - vm.margin.bottom) // 显示 上标
        .text(function(d) {
          return strChange[d.charCodeAt() - 'a'.charCodeAt()]
        })
      d3.selectAll('.dimension')
        .each(function(d, i) {
          const t = d3.select(this).select('.labelBackground').node().getBBox()
          d3.select(this).select('.labelBackground').insert('rect', '.textShow')
            .attr('x', (i) => {
              return -(t.width + 10) / 2
            })
            .attr('y', vm.height + 10 - vm.margin.top - vm.margin.bottom)
            .attr('rx', '5')
            .attr('ry', '5')
            .attr('height', t.height + 10)
            .attr('width', t.width + 10)
            .attr('fill', '#e9ecff')
            .attr('opacity', '1')
        })
      // 加入矩形框显示
      if (!this.getStartStop && vm.getCheckLabels.length > 0) {
        gMain.selectAll('.dimension')
          .append('g')
          .attr('class', 'myRect')
          .each(function(d) {
            const tickStep = (maxValue[d] - minValue[d]) / (ticksHis)
            const step = tickStep
            const tmp = d3.range(minValue[d], maxValue[d] + step - myEPS, step) // 每一隔的间距
            // 计算每一个的高度
            const oneHight = (vm.height - vm.margin.top - vm.margin.bottom) / (tmp.length - 1)
            // 改造tmp2 分段统计数据，里面只有选中的数据
            // [{
            //     "0": 0,
            //     "1": 0
            //   },
            //   {
            //     "0": 0,
            //     "1": 0
            //   }
            // ]
            const tmp2 = []
            for (let in1 = 0; in1 < tmp.length - 1; in1++) {
              tmp2.push({}) // 每一个区块也是json对象？
              for (let in2 = 0; in2 < vm.getCheckLabels.length; in2++) {
                tmp2[in1][vm.getCheckLabels[in2].toString()] = 0 // 所选类别个数暂时为0
              }
            }
            let otherCheck = false
            for (let i = 0; i < vm.getCheckLabels.length; i++) {
              if (vm.getCheckLabels[i] === '其他') {
                otherCheck = true
              }
            }
            data.forEach(function(p, index) {
              for (let in2 = 1; in2 < tmp.length; in2++) { // 比较耗时的计算每个间隔的每个分类的个数
                if (+p[d] <= tmp[in2] && +p[d] >= tmp[in2 - 1]) {
                  if (vm.getCheckLabels.indexOf(localData.label[index].toString()) !== -1) {
                    tmp2[in2 - 1][localData.label[index].toString()]++
                    break
                  }
                  if (otherCheck) {
                    if (vm.getCurData.labelType.indexOf(localData.label[index].toString()) === -1) {
                      tmp2[in2 - 1]['其他']++
                      break
                    }
                  }
                }
              }
            })
            const rectOffset = 1.5
            d3.select(this).selectAll('.lessRect')
              .data(tmp2)
              .enter()
              .append('g')
              .attr('class', 'lessRect')
              .each(function(datum, index) { // 一个对象里面存着所有要显示的标签的统计数据 也就是一个小ticks中要显示的所有数据
                const tmpKeys = Object.keys(datum) // 现在这个里面只有两个数据了，关于其他的处理方式，注意
                for (let in1 = 0; in1 < tmpKeys.length; in1++) {
                  d3.select(this)
                    .append('rect')
                    .attr('y', function(datum) {
                      return y[d](tmp[index + 1]) + oneHight * 0.1
                    })
                    .attr('x', function(datum) {
                      // 记住前一个label的x
                      let xTmp = 0
                      xTmp = datum[tmpKeys[in1]]
                      if (in1 === 0) { // 为正
                        xTmp = 0 + rectOffset
                      } else {
                        xTmp = -1 * xTmp / localData.echaLabelNumber[tmpKeys[in1]] * x.step() * 0.2
                      }
                      return xTmp
                    }) // x 要动
                    .attr('width', function(datum) {
                      return datum[tmpKeys[in1]] / localData.echaLabelNumber[tmpKeys[in1]] * x.step() * 0.2
                    })
                    .attr('height', oneHight * 0.8)
                    .attr('fill', function() {
                      if (typeof (vm.getCurData.labelTypeColor[tmpKeys[in1]]) !== 'undefined') {
                        return vm.getCurData.labelTypeColor[tmpKeys[in1]]
                      } else {
                        return vm.getLegendColor[9]
                      }
                    })
                    .attr('opacity', 1)
                  d3.select(this)
                    .append('path')
                    .attr('d', function(datum) {
                      let xTmp = 0
                      xTmp = datum[tmpKeys[in1]]
                      if (in1 === 0) { // 为正
                        xTmp = 0 + rectOffset
                      } else {
                        xTmp = -1 * xTmp / localData.echaLabelNumber[tmpKeys[in1]] * x.step() * 0.2
                      }
                      const letWidth = datum[tmpKeys[in1]] / localData.echaLabelNumber[tmpKeys[in1]] * x.step() * 0.2
                      let rlt = ''
                      if (letWidth === 0) {
                        return rlt
                      }
                      rlt = `m${xTmp} ${y[d](tmp[index + 1]) + oneHight * 0.1} L${(xTmp + letWidth)} ${y[d](tmp[index + 1]) + oneHight * 0.1} L${(xTmp + letWidth)} ${y[d](tmp[index + 1]) + oneHight * 0.1 + oneHight * 0.8} L${xTmp} ${y[d](tmp[index + 1]) + oneHight * 0.1 + oneHight * 0.8} Z`
                      return rlt
                    })
                    .attr('fill', 'none')
                    .attr('stroke', '#736FBC')
                }
              })
          })
      }

      // legend
      d3.select('#mainGroup').selectAll('.legend').remove()
      var legend = d3.select('#mainGroup').selectAll('.legend')
        .data(localData.labelType)
        .enter().append('g')
        .attr('class', 'legend')
        .attr('transform', function(d, i) { return 'translate(' + (vm.width - vm.margin.left - vm.margin.right - 80) + ',' + (-(i + 1) * 25 + vm.height - vm.margin.bottom - vm.margin.top) + ')' })

      // draw legend colored rectangles
      legend.append('circle')
        .data(localData.labelType)
        .attr('cx', '15')
        .attr('cy', '10')
        .attr('r', 8)
        .style('fill', function(d, i) {
          return vm.getLegendColor[localData.labelType.length - 1 - i]
        })
      // draw legend text
      legend.append('text')
        .data(localData.labelType)
        .attr('class', 'legend_text')
        .attr('x', 40)
        .attr('y', 9)
        .attr('dy', '.5em')
        .attr('fill', 'black')
        .style('text-anchor', 'start')
        .text(function(d, i) { return localData.labelType[localData.labelType.length - 1 - i] })

      function position(d) {
        var v = dragging[d]
        return v == null ? x(d) : v
      }

      function path(d) {
        return line(dimensions.map(function(p) {
          return [position(p), y[p](d[p])]
        }))
      }
    },
    renderTwoUpdate: function(localData) {
      var vm = this
      const g = d3.select('#maingroup')
      const gscatter = d3.select('#subgroup')
      this.dataAttr.minX = d3.min(localData.data, function(d) { return d[0] })
      this.dataAttr.maxX = d3.max(localData.data, function(d) { return d[0] })
      this.dataAttr.minY = d3.min(localData.data, function(d) { return d[1] })
      this.dataAttr.maxY = d3.max(localData.data, function(d) { return d[1] })
      this.height = d3.select(this.$refs.draw).node().getBoundingClientRect().height
      this.width = d3.select(this.$refs.draw).node().getBoundingClientRect().width
      vm.halfHight = this.height / 2
      vm.halfWidth = this.width / 2
      vm.xScale = d3.scaleLinear()
        .domain([vm.dataAttr.minX, vm.dataAttr.maxX])
        .range([0, this.width - this.margin.left - this.margin.right])
        .nice()
      vm.yScale = d3.scaleLinear()
        .domain([vm.dataAttr.minY, vm.dataAttr.maxY].reverse())
        .range([0, this.height - this.margin.top - this.margin.bottom])
        .nice()
        // Adding axes
      vm.yAxis = d3.axisLeft(vm.yScale)
        .tickSize(-(this.width - this.margin.left - this.margin.right))
      vm.xAxis = d3.axisBottom(vm.xScale)
        .tickSize(-(this.height - this.margin.top - this.margin.bottom))
        .tickPadding(10)
      var t = gscatter.transition().duration(750)
      g.select('#xaxis')
        .transition(t)
        .call(vm.xAxis)
      g.select('#yaxis')
        .transition(t)
        .call(vm.yAxis)

      vm.circleUpdate = gscatter.selectAll('circle').data(localData.data)
      vm.circleExit = vm.circleUpdate.exit()
      vm.circleEnter = vm.circleUpdate.enter().append('circle')
        .attr('cy', (datum) => { return vm.yScale(datum[1]) })
        .attr('cx', (datum) => { return vm.xScale(datum[0]) })
        .attr('r', 3)
        .attr('fill', function(datum, index) {
          if (typeof (vm.getCurData.labelTypeColor[localData.label[index].toString()]) !== 'undefined') {
            return vm.getCurData.labelTypeColor[localData.label[index].toString()]
          } else {
            return vm.getLegendColor[9]
          }
        })
        .attr('opacity', 1)
        .on('click', function(datum, i) {
          d3.event.stopPropagation() // 阻止事件冒泡即可
          vm.clickEleCumputed = true
          // d3.select(this)
          //   .transition()
          //   .duration(50)
          //   .attr('opacity', 1) // 自己的透明度为1
          const value = localData.label[i]
          vm.setMessage([`${constant.IMGURl}/api/projector_sample?run=${vm.userSelectRunFile}&tag=${vm.getCurInfo.curTag}&index=${i}`, `第${i + 1}个点,标签为${value}`])
        })
        .on('mouseover', function(datum, index) {
          const div = d3.selectAll('div.tooltip')
          const value = localData.label[index]
          div
            .style('opacity', 0.9)
            .style('left', (d3.event.offsetX + 30) + 'px')
            .style('top', (d3.event.offsetY - 10) + 'px')
            .style('z-index', 5)
          div.html(`第${index + 1}个点，标签为${value}`)
        })
        .on('mouseout', function(datum) {
          const div = d3.select('div.tooltip')
          div
            .style('opacity', 0)
            .style('z-index', -1)
        })
      vm.circleUpdate.merge(vm.circleEnter).transition().ease(d3.easeLinear).duration(1000)
        .attr('cy', (datum) => { return vm.yScale(datum[1]) })
        .attr('cx', (datum) => { return vm.xScale(datum[0]) })
        .attr('fill', function(datum, index) {
          if (typeof (vm.getCurData.labelTypeColor[localData.label[index].toString()]) !== 'undefined') {
            return vm.getCurData.labelTypeColor[localData.label[index].toString()]
          } else {
            return vm.getLegendColor[9]
          }
        })
      vm.circleExit.remove()

      // draw legend 颜色校验等增加鼠标点击的事件吧
      // 删除所有legend
      d3.select('#maingroup').selectAll('.legend').remove()
      var legend = d3.select('#maingroup').selectAll('.legend')
        .data(localData.labelType)
        .enter().append('g')
        .attr('class', 'legend')
        .attr('transform', function(d, i) { return 'translate(' + (vm.width - vm.margin.left - vm.margin.right + 30) + ',' + (-(i + 1) * 25 + vm.height - vm.margin.bottom - vm.margin.top) + ')' })
      // draw legend colored rectangles
      legend.append('circle')
        .data(localData.labelType)
        .attr('cx', '15')
        .attr('cy', '10')
        .attr('r', 8)
        .style('fill', function(d, i) {
          return vm.getLegendColor[localData.labelType.length - 1 - i]
        })
      // draw legend text
      legend.append('text')
        .data(localData.labelType)
        .attr('class', 'legend_text')
        .attr('x', 40)
        .attr('y', 9)
        .attr('dy', '.5em')
        .attr('fill', 'black')
        .style('text-anchor', 'start')
        .text(function(d, i) { return localData.labelType[localData.labelType.length - 1 - i] })
    },
    renderThreeUpdate: function(localData) {
      var vm = this
      // 开始数据投篮栏
      var myData = {}
      for (let i = 0; i < localData.labelType.length; i++) {
        myData[localData.labelType[i]] = []
        myData[localData.labelType[i]].push(['x', 'y', 'z', 'index'])
      }
      for (let i = 0; i < localData.label.length; i++) {
        if (localData.labelType.indexOf(localData.label[i].toString()) >= 10 || localData.labelType.indexOf(localData.label[i].toString()) === -1) { // 序列大于10
          myData[localData.labelType[9]].push(localData.data[i].concat(i))
          continue
        }
        myData[localData.label[i].toString()].push(localData.data[i].concat(i))
      }
      // 数据分栏结束
      var option = {
        tooltip: {
          trigger: 'item',
          backgroundColor: 'rgba(255,255,255,0.8)',
          borderWidth: 1,
          borderColor: 'rgb(124,120,192)',
          padding: [5, 5, 5, 5],
          textStyle: {
            color: 'rgb(124,120,192)'
          },
          formatter: function(params) {
            const value = localData.label[params.data[3]]
            return `第${params.data[3]}个点，标签为${value}`
          }
        },
        grid3D: {
          viewControl: {
            minDistance: -100
          }
        },
        xAxis3D: {
          color: '#FFFFFF'
        },
        yAxis3D: {
          color: '#FFFFFF'
        },
        zAxis3D: {
          color: '#FFFFFF'
        },
        color: this.getLegendColor,
        legend: {
          right: 50,
          bottom: 50,
          data: localData.labelType,
          orient: 'vertical'
        },
        label: {
          formatter: function(params) {
            return params.name
          },
          position: 'right',
          show: false,
          color: '#FFFFFF'
        },
        emphasis: {
          label: {
            show: true
          }
        },
        series: []
      }
      for (let i = 0; i < localData.labelType.length; i++) {
        option.series.push({
          name: localData.labelType[i],
          type: 'scatter3D',
          symbolSize: 5,
          data: myData[localData.labelType[i]],
          itemStyle: {
          }
        })
      }
      this.myChart = echarts.init(document.getElementById('threeChild'), 'light')
      this.myChart.setOption(option)
      this.myChart.on('click', function(params) {
        const value = localData.label[params.data[3]]
        vm.setMessage([`${constant.IMGURl}/api/projector_sample?run=${vm.userSelectRunFile}&tag=${vm.getCurInfo.curTag}&index=${params.data[3]}`, `点击第${params.data[3]}个点,标签为${value}`])
      })

      window.addEventListener('resize', () => {
        if (this.myChart) { // 会报一定的错误但是确实可以实现echarts的自适应
          this.myChart.resize()
        }
      })
    },
    renderUpdate: function(localData) {
      if (JSON.stringify(this.localCurInfo) === '{}') {
        return
      }
      if (parseInt(this.localCurInfo.curDim) === 3) { // 是3维显示
        this.renderThreeUpdate(localData)
      } else if (parseInt(this.localCurInfo.curDim) === 2) {
        this.renderTwoUpdate(localData)
      } else {
        this.renderNUpdate(localData)
      }
    }
  }
}
</script>
