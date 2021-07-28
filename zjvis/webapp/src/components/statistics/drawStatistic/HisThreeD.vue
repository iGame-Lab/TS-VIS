<template>
  <div :class="className" style="width:100%;height:100%" />
</template>

<script>
import * as d3 from 'd3'
import { createNamespacedHelpers } from 'vuex'
const { mapGetters: mapStatisticGetters, mapMutations: mapStatisticMutations } = createNamespacedHelpers('statistic')

export default {
  name: 'Onethreed',
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
      id: 'offset' + this.itemp
    }
  },
  computed: {
    ...mapStatisticGetters(['getShowNumber'])
  },
  watch: {
    data: function() {
      // 清空原先所有图形，用清空dom的方式
      document.getElementsByClassName(this.className)[0].innerHTML = ''
      // 重绘
      this.drawOffset()
    }
  },
  mounted() {
    this.drawOffset()
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
    // 显示比率
    drawOffset: function() {
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
      // 左右上下增加一个宽度，防止顶格
      const valueMin = data[0][0][0]
      const valueMax = data[0][data[0].length - 1][0]
      // 画svg
      const areaHeight = 50
      const heightTop = 10
      const padding = { top: areaHeight + heightTop, right: 45, bottom: 20, left: 10 }
      const svgWidth = 290
      const svgHeight = 250
      const width = svgWidth - padding.left - padding.right
      const height = svgHeight - padding.top - padding.bottom
      const div = d3
        .select(className)
        .append('div')
        .attr('id', label + 'div')
        .attr('width', '100%')
        .attr('height', '100%')
      const outersvg = div
        .append('svg')
        .attr('id', label) // 在放大缩小时有用
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('preserveAspectRatio', 'xMidYMid meet')
        .attr('viewBox', '0 0 290 250')
      const svg = outersvg.append('g')

      // 画坐标轴
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
        .call(d3.axisBottom()
          .scale(xscale)
          .ticks(5)
        )
      const stepscale = d3
        .scaleLinear()
        .domain([data[0][0][2], data[data.length - 1][0][2]])
        .rangeRound([0, height])
        .nice()
      svg
        .append('g')
        .attr('class', 'axis stepaxis')
        .attr(
          'transform',
          'translate(' + (padding.left + width) + ',' + padding.top + ')'
        )
        .call(d3.axisRight()
          .scale(stepscale)
          .tickFormat(d => this.numberChangeToE(d))
        )
      const yscale = d3
        .scaleLinear()
        .domain([numberMin, numberMax])
        .rangeRound([areaHeight, 0])
      // 显示信息
      svg.append('g').append('text')
        .attr('transform', 'rotate(90)')
        .attr('y', -(svgWidth - 13))
        .attr('x', svgHeight / 2)
        .attr('fill', 'grey')
        .attr('font-size', '10px')
        .text('step')
      const pathg = svg.append('g').attr('class', 'areapathg')
      svg
        .append('g')
        .append('text')
        .attr('class', 'textbox')
        .attr('visibility', 'hidden')
        .attr('fill', 'black')
        .attr('x', padding.left - 20)
        .attr('y', padding.top - 30)
        .style('font-size', '9px')
      svg
        .append('g')
        .append('line')
        .attr('class', 'allpoints')
        .attr('y1', 0)
        .attr('y2', svgHeight)
        .attr('stroke', 'black')
        .attr('visibility', 'hidden')
      const circleg = svg.append('g')
      for (let i = 0; i < data.length; i++) {
        circleg
          .append('circle')
          .attr('fill', '#fff45a')
          .attr('class', 'circle' + i)
          .attr('id', label + 'circle' + i)
      }
      svg
        .append('g')
        .append('line')
        .attr('id', 'xaxisline')
        .attr('stroke-dasharray', '10')
        .attr('visibility', 'hidden')
      svg
        .append('g')
        .append('rect')
        .attr('y', padding.top + height + 7)
        .attr('width', 32)
        .attr('height', 15)
        .attr('fill', 'white')
        .attr('class', 'xrect')
        .attr('visibility', 'hidden')
      svg
        .append('g')
        .append('text')
        .attr('class', 'xcoord')
        .attr('visibility', 'hidden')
        .attr('fill', 'black')
        .attr('x', padding.left)
        .attr('y', padding.top + height + 15)
        .style('font-size', '9px')
      svg
        .append('g')
        .append('rect')
        .attr('width', 24)
        .attr('height', 15)
        .attr('fill', 'white')
        .attr('class', 'steprect')
        .attr('visibility', 'hidden')
        .attr('x', padding.left + width + 7)
      svg
        .append('g')
        .append('text')
        .attr('class', 'ycoord')
        .attr('visibility', 'hidden')
        .attr('fill', 'black')
        .attr('x', padding.left + width + 8)
        .style('font-size', '9px')
      // 画图
      const lineFunction = d3
        .line()
        .x(function(d) {
          return xscale(d[0])
        })
        .y(function(d) {
          return yscale(d[1])
        })
      pathg
        .selectAll('path')
        .data(data)
        .enter()
        .append('g')
        .append('path')
        .attr('stroke', 'gainsboro')
        .attr('stroke-width', '0.5')
        .attr('d', function(d) {
          return lineFunction(d)
        })
        .attr('transform', function(d, i) {
          const translateHeight = stepscale(d[0][2]) + heightTop
          return 'translate(' + padding.left + ',' + translateHeight + ')'
        })
        .attr('fill', this.runColor)
        .attr('class', function(d, i) {
          return 'step' + i
        })
        .attr('id', function(d, i) {
          return label + 'step' + i
        })
        // 添加鼠标操作:珠子+数值
        .on('mousemove', function(d, i) {
          // 计算珠子
          const curX = d3.mouse(svg.node())[0]
          const curY = d3.mouse(svg.node())[1]
          svg
            .select('.allpoints')
            .attr('x1', curX - padding.left)
            .attr('x2', curX - padding.left)
          const len = data.length
          // 2D.js计算交点
          // 计算了所有的交点，这里应该会导致鼠标操作不那么流畅
          const shapes = []
          const children = svg.select('.areapathg').selectAll('path')
          for (let j = 0; j < len; j++) {
            const child = children._groups[0][j]
            // eslint-disable-next-line no-undef
            const shape = new Path(child)
            shapes.push(shape)
          }
          const linechild = svg.select('.allpoints')
          // eslint-disable-next-line no-undef
          const lineshape = new Line(linechild._groups[0][0])
          const points = []
          for (let j = 0; j < len; j++) {
            // eslint-disable-next-line no-undef
            const inter = Intersection.intersectShapes(lineshape, shapes[j])
            points.push(inter.points[0])
          }
          // 没有交点是undefined
          // 遮挡情况就不考虑了，因为有透明的操作
          for (let j = 0; j < points.length; j++) {
            if (points[j] === undefined) {
              svg.select('.circle' + j).attr('r', '0')
            } else {
              svg
                .select('.circle' + j)
                .attr('r', '1')
                .attr('cx', points[j].x + padding.left)
                .attr('cy', heightTop + stepscale(data[j][0][2]) + points[j].y)
            }
          }
          svg.select('.areapathg')
            .selectAll('path')
            .style('opacity', 1.0)
            .attr('stroke', 'gainsboro')
            .attr('stroke-width', '0.5')
          svg.select('.step' + i).attr('stroke', '#fff45a').attr('stroke-width', '1')
          // 控制面板需要显示数据
          // 当前step，是对多少个数据进行统计的，统计个数的最小值和最大值，和最大值对应的区间
          // 这个数据不准确，把所有相加
          const curDataCountSum = d3.sum(data[i], function(d) {
            return d[1]
          })
          const curCountMin = d3.min(data[i], function(d) {
            return d[1]
          })
          let curCountMax = 0
          for (let it = 0; it < data[i].length; it++) {
            if (curCountMax < data[i][it][1]) {
              curCountMax = data[i][it][1]
            }
          }
          that.setStatisticInfo([data[i][0][2], Math.ceil(curDataCountSum), curCountMin, curCountMax.toFixed(2)])
          svg
            .select('.xrect')
            .attr('visibility', 'visible')
            .attr('x', curX - 15)
          svg
            .select('.xcoord')
            .attr('visibility', 'visible')
            .attr('x', curX - 13)
            .text(Math.floor(xscale.invert(curX - padding.left) * 1000) / 1000)

          svg
            .select('.steprect')
            .attr('visibility', 'visible')
            .attr('y', padding.top + stepscale(d[0][2]) - 8)
            .attr('width', d[0][2].toString().length * 7)
          svg
            .select('.ycoord')
            .attr('visibility', 'visible')
            .attr('y', padding.top + stepscale(d[0][2]) + 3)
            .text(d[0][2])
          svg
            .select('.textbox')
            .attr('visibility', 'visible')
            .text('count:' + yscale.invert(points[i].y).toFixed(2))
            .attr('x', curX + 5)
            .attr('y', curY - 10)

          // 透明效果
          // 遍历整个数据比较高度
          const dh = height / (data[data.length - 1][0][2] - 1)
          const count = Math.ceil(areaHeight / dh)
          const curHeight = []
          // yscale，值越大高度越小
          for (let j = 0; j < d.length; j++) {
            curHeight.push(stepscale(d[j][2]) - (areaHeight - yscale(d[j][1])))
          }
          for (let j = i + 1; j <= i + count && j < len; j++) {
            const onedata = data[j]
            for (let k = 0; k < onedata.length; k++) {
              const heightk = stepscale(onedata[k][2]) - (areaHeight - yscale(onedata[k][1]))
              if (heightk <= curHeight[k]) {
                svg.select('.step' + j).style('opacity', 0.5)
                break
              }
            }
          }
        })
      svg.on('mouseleave', function() {
        // 用mouseout光标会闪烁
        svg
          .select('.areapathg')
          .selectAll('path')
          .style('opacity', 1.0)
          .attr('stroke', 'gainsboro')
          .attr('stroke-width', '0.5')
        svg.select('.textbox').attr('visibility', 'hidden')
        svg.selectAll('circle').attr('r', '0')
        svg
          .select('.xaxisline')
          .attr('x1', '0')
          .attr('y1', '0')
          .attr('x2', '0')
          .attr('y2', '0')
        svg.select('.xrect').attr('visibility', 'hidden')
        svg.select('.xcoord').attr('visibility', 'hidden')
        svg.select('.steprect').attr('visibility', 'hidden')
        svg.select('.ycoord').attr('visibility', 'hidden')
        // 控制面板为空
        that.setStatisticInfo([])
      })
      // 在只显示若干条数据时，在纵轴上移动显示中间步骤
      svg.select('.stepaxis').on('mousemove', function() {
        const curY = d3.mouse(svg.node())[1]
        const step = parseInt(stepscale.invert(curY - padding.top))
        let k = 0
        for (let i = 0; i < data.length; i++) {
          if (data[i][0][2] > step) {
            k = i
            if (i !== 0 && data[i][0][2] - step > step - data[i - 1][0][2]) {
              k = k - 1
            }
            break
          }
        }
        svg
          .select('.areapathg')
          .selectAll('path')
          .attr('stroke', 'gainsboro')
          .attr('stroke-width', '0.5')
        d3.select('#' + label + 'step' + k)
          .attr('stroke', '#fff45a')
          .attr('visibility', 'visible')
          .attr('stroke-width', '1')
        svg
          .select('.steprect')
          .attr('visibility', 'visible')
          .attr('y', curY - 7)
        svg
          .select('.ycoord')
          .attr('visibility', 'visible')
          .attr('y', curY + 5)
          .text(data[k][0][2])
      })
    }
  }
}
</script>
