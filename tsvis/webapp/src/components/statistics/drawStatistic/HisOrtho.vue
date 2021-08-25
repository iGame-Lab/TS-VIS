<template>
  <div :class="className" />
</template>
<script>
import { createNamespacedHelpers } from 'vuex'
import * as d3 from 'd3'
const { mapGetters: mapStatisticGetters, mapMutations: mapStatisticMutations } = createNamespacedHelpers('statistic')
export default {
  name: 'Oneorthographic',
  props: {
    data: Array,
    ttlabel: String,
    tag: String,
    itemp: Number,
    className: String,
    runColor: String
  },
  data() {
    return {
      id: 'overlay' + this.itemp
    }
  },
  computed: {
    ...mapStatisticGetters(['getShowNumber']),
    changeDraw() {
      return this.data
    }
  },
  watch: {
    getShowNumber(newNumber) {
      this.showrate = newNumber / 100
    },
    data: function() {
      // 清空原先所有图形，用清空dom的方式
      document.getElementsByClassName(this.className)[0].innerHTML = ''
      // 重绘
      this.drawOverlay()
    }
  },
  mounted() {
    this.drawOverlay()
  },
  methods: {
    ...mapStatisticMutations(['setStatisticInfo']),
    // 科学计数法
    numberChangeToE(d) {
      if (Math.abs(d) > 10000) {
        let numLen = numLen = d.toString().length - 1
        if (d < 0) {
          numLen = d.toString().length - 2
        }
        return `${(d / Math.pow(10, numLen)).toFixed(2)}e+${numLen}`
      } else if (Math.abs(d) < 0.001) {
        if (d === 0) return d
        const dString = d.toString()
        if (dString.indexOf('e') !== -1) return d
        let i = 3
        if (d < 0) {
          i = 4
        }
        for (; i < dString.length; i++) {
          if (dString[i] !== '0') {
            break
          }
        }
        if (d < 0) {
          i = i - 1
        }
        return `${(d * Math.pow(10, i - 1)).toFixed(2)}e-${(i - 1)}`
      }
      return d
    },
    drawOverlay: function() {
      // label是这组数据的标签，ttlabel是这组数据属于哪个集合
      const label = this.id
      const data = this.data
      const className = '.' + this.className
      const that = this
      // 先找到value和number的最大值和最小值
      let numberMin = 10000
      let numberMax = 0
      for (let i = 0; i < data.length; i++) {
        for (let j = 0; j < data[i].length; j++) {
          if (numberMin > data[i][j][1]) numberMin = data[i][j][1]
          if (numberMax < data[i][j][1]) numberMax = data[i][j][1]
        }
      }
      const valueMin = data[0][0][0]
      const valueMax = data[0][data[0].length - 1][0]
      // 生成svg
      const padding = { top: 10, right: 45, bottom: 20, left: 10 }
      const svgWidth = 290
      const svgHeight = 250
      const width = svgWidth - padding.left - padding.right
      const height = svgHeight - padding.top - padding.bottom
      const div = d3
        .select(className)
        .append('div')
        .attr('id', label + 'div')
      const outersvg = div
        .append('svg')
        .attr('id', label) // 在放大缩小时有用
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('preserveAspectRatio', 'xMidYMid meet')
        .attr('viewBox', '0 0 290 250')
      const svg = outersvg.append('g')
      svg
        .append('g')
        .append('rect')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('fill', 'white')
      // 画坐标轴，纵轴科学计数法，tickformat
      const xscale = d3
        .scaleLinear()
        .domain([valueMin, valueMax])
        .rangeRound([0, width])
        .nice()
      svg
        .append('g')
        .attr('class', 'axis')
        .attr(
          'transform',
          'translate(' + padding.left + ',' + (padding.top + height) + ')'
        )
        .call(
          d3
            .axisBottom()
            .scale(xscale)
            .ticks(5)
            .tickSize(-height)
            .tickFormat(d => this.numberChangeToE(d))
        )
      const yscale = d3
        .scaleLinear()
        .domain([numberMin, numberMax])
        .rangeRound([height, 0])
        .nice()
      svg
        .append('g')
        .attr('class', 'axis')
        .attr(
          'transform',
          'translate(' + (padding.left + width) + ',' + padding.top + ')'
        )
        .call(
          d3
            .axisRight()
            .scale(yscale)
            .tickFormat(d => this.numberChangeToE(d))
            .tickSize(-width)
        )
      svg.append('g').append('text')
        .attr('transform', 'rotate(90)')
        .attr('y', -(svgWidth - 13))
        .attr('x', svgHeight / 2)
        .attr('fill', 'grey')
        .attr('font-size', '10px')
        .text('count')
      // 用于显示信息
      const pathg = svg.append('g')
      svg
        .append('g')
        .append('line')
        .attr('class', 'xaxisline')
        .attr('stroke-dasharray', '10')
        .attr('stroke', 'black')
      svg
        .append('g')
        .append('line')
        .attr('class', 'yaxisline')
        .attr('stroke-dasharray', '10')
        .attr('stroke', 'black')
      svg
        .append('g')
        .append('rect')
        .attr('y', padding.top + height + 1)
        .attr('width', 32)
        .attr('height', 15)
        .attr('fill', 'white')
        .attr('class', 'xrect')
        .attr('visibility', 'hidden')
      svg
        .append('g')
        .append('rect')
        .attr('x', padding.left + width + 1)
        .attr('width', padding.right - 1)
        .attr('height', 15)
        .attr('fill', 'white')
        .attr('class', 'yrect')
        .attr('visibility', 'hidden')
      svg
        .append('g')
        .append('text')
        .attr('class', 'textbox')
        .attr('visibility', 'hidden')
        .attr('fill', 'black')
        .style('font-size', '10px')
      svg
        .append('g')
        .append('text')
        .attr('class', 'xcoord')
        .attr('visibility', 'hidden')
        .attr('fill', 'black')
        .attr('x', padding.left)
        .attr('y', padding.top + height + 10)
        .style('font-size', '10px')
      svg
        .append('g')
        .append('text')
        .attr('class', 'ycoord')
        .attr('visibility', 'hidden')
        .attr('fill', 'black')
        .attr('x', padding.left + width + 2)
        .style('font-size', '10px')

      svg
        .append('g')
        .append('path')
        .attr('stroke', 'green')
        .attr('stroke-width', 1.5)
        .attr('fill', 'none')
        .attr('class', 'lastline') // 如果加了这条线，就不能滑动了--解决方法：给这条线添加mousemove操作
      let lastLineData = [] // 不然无法计算step
      // 画线
      const lineFunction = d3
        .line()
        .x(function(d) {
          return xscale(d[0])
        })
        .y(function(d) {
          return yscale(d[1])
        })
      // 为了实现光晕效果
      const haloData = []
      for (let i = 0; i < data.length; i++) {
        haloData.push(data[i]) // i%2==0是白线
        haloData.push(data[i]) // i%2==1是数据
      }
      const dc = 255 / (haloData.length - 1) // 红->蓝
      pathg
        .selectAll('path')
        .data(haloData)
        .enter()
        .append('g')
        .append('path')
        .attr(
          'transform',
          'translate(' + padding.left + ',' + padding.top + ')'
        )
        .attr('fill', 'none')
        .attr('d', function(d) {
          return lineFunction(d)
        })
        .attr('stroke', function(d, i) {
          if (i % 2 === 0) return 'white'
          else {
            const redcolor = 255 - i * dc
            const bluecolor = i * dc
            return 'rgb(' + redcolor + ',0,' + bluecolor + ')'
          }
        })
        .attr('stroke-width', function(d, i) {
          if (i % 2 === 0) return 0.8
          else return 0.4
        })
        .style('opacity', function(d, i) {
          if (i % 2 === 0) return 0.6
          else return 1.0
        })
        .attr('id', function(d, i) {
          // 白线也要给id，方便隐藏
          return label + 'step' + i
        })
        .attr('class', function(d, i) {
          return i
        })
        .on('mousemove', function(d, i) {
          // 可以直接用xscale，yscale，各图之间没有影响,svg也无影响
          lastLineData = d
          svg
            .select('.lastline')
            .attr('visibility', 'visible')
            .attr('d', lineFunction(d))
            .attr(
              'transform',
              'translate(' + padding.left + ',' + padding.top + ')'
            )
            .on('mousemove', function() {
              mouseMoveFunc(lastLineData)
            })
          mouseMoveFunc(d)
        })
      function mouseMoveFunc(myData) {
        const curX = d3.mouse(svg.node())[0]
        const curY = d3.mouse(svg.node())[1]
        svg
          .select('.xcoord')
          .attr('visibility', 'visible')
          .attr('x', curX - 10)
          .text(Math.ceil(xscale.invert(curX - padding.left) * 1000) / 1000)
        svg
          .select('.xrect')
          .attr('visibility', 'visible')
          .attr('x', curX - 10)

        let ytext = yscale.invert(curY - padding.top).toFixed(2)
        if (ytext > 10000) {
          ytext = Math.ceil(ytext)
          const numLen = ytext.toString().length - 1
          ytext =
            Math.ceil((ytext / Math.pow(10, numLen)) * 100) / 100 +
            'e+' +
            numLen
        }
        svg
          .select('.ycoord')
          .attr('visibility', 'visible')
          .attr('y', curY + 5)
          .text(ytext)
        svg
          .select('.yrect')
          .attr('visibility', 'visible')
          .attr('y', curY - 5)
          .attr('width', ytext.toString().length * 7)
        svg
          .select('.textbox')
          .attr('visibility', 'visible')
          .text('step:' + myData[0][2])
          .attr('x', curX + 5)
          .attr('y', curY - 10)

        svg
          .select('.xaxisline')
          .attr('x1', curX)
          .attr('y1', curY)
          .attr('x2', curX)
          .attr('y2', height + padding.top)
        svg
          .select('.yaxisline')
          .attr('x1', curX)
          .attr('y1', curY)
          .attr('x2', padding.left + width)
          .attr('y2', curY)
        // 添加控制面板数据
        // 这个数据不准确，把所有相加
        const curDataCountSum = d3.sum(myData, function(d) {
          return d[1]
        })
        const curCountMin = d3.min(myData, function(d) {
          return d[1]
        })
        let curCountMax = 0
        for (let it = 0; it < myData.length; it++) {
          if (curCountMax < myData[it][1]) {
            curCountMax = myData[it][1]
          }
        }
        that.setStatisticInfo([myData[0][2], Math.ceil(curDataCountSum), curCountMin, curCountMax.toFixed(2)])
      }
      svg.on('mouseleave', function() {
        svg.select('.steprect').attr('visibility', 'hidden')
        svg.select('.textbox').attr('visibility', 'hidden')
        svg
          .select('.xaxisline')
          .attr('x1', 0)
          .attr('y1', 0)
          .attr('x2', 0)
          .attr('y2', 0)
        svg
          .select('.yaxisline')
          .attr('x1', 0)
          .attr('y1', 0)
          .attr('x2', 0)
          .attr('y2', 0)
        svg.select('.xrect').attr('visibility', 'hidden')
        svg.select('.yrect').attr('visibility', 'hidden')
        svg.select('.xcoord').attr('visibility', 'hidden')
        svg.select('.ycoord').attr('visibility', 'hidden')
        svg.select('.lastline').attr('visibility', 'hidden')
        that.setStatisticInfo([])
      })
    }
  }
}
</script>
