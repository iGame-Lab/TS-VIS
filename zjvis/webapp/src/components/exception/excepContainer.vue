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

<style scoped>
.exceptionContainer{
  margin:1%;
}
.excepContainerHead1, .excepContainerHead2{
  margin-bottom: 1%;
  text-align: left;
  display: flex;
  border-radius: 3px;
  padding-left: 1%;
  height: 30px;
  line-height: 30px;
  color: white;
}
.excepContainerHead1{
  background-color: rgba(104,101,182,0.8);
}
.excepContainerHead2{
  background-color: rgba(104,101,182,1);
}
.curStep{
  margin-left: 5%;
}
.excepContainerContent{
  padding: 1%;
}
.colorMatrix {
  padding: 1% 2% 3% 2%;
}
.excepRectDiv {
  border: 1px dashed grey;
  padding: 1%;
}
.excepRectLegend{
  height: 410px;
}
@media screen and (max-width: 1600px) {
  .excepRectLegend{
    height: 330px;
  }
}
@media screen and (max-width: 1300px) {
  .excepRectLegend{
    height: 280px;
  }
}
@media screen and (max-width: 1000px) {
  .excepRectLegend{
    height: 250px;
  }
}
</style>
<template>
  <div class="exceptionContainer">
    <el-card style="height:100%;">
      <div :class="excepContainerHeadShow?'excepContainerHead2':'excepContainerHead1'">
        <div class="excepHead"><span style="font-weight:600;">{{ oneData[0] }}</span>/<span>{{ oneData[1] }}</span></div>
        <div class="curStep">当前步：{{ myAllStep[curStepIndex] }}</div>
      </div>
      <el-row :gutter="24" class="excepContainerContent">
        <el-col :span="12">
          <div class="excepBoxStep">
            <div :id="excepBoxId" class="excepBox" />
            <div :id="excepStepAxisId" class="excepStepAxis" />
          </div>
        </el-col>
        <el-col :span="12" class="excepLeft">
          <div :id="excepHistId" class="excepHist" />
        </el-col>
      </el-row>
      <div class="colorMatrix">
        <el-row>
          <el-col v-show="!canvasScale" :span="19" :offset="1" class="excepRectLegend">
            <div class="excepRectDiv" style="height:100%;">
              <el-scrollbar style="height:100%;">
                <canvas :id="excepCanvasId">
                  您的浏览器不支持 HTML5 canvas 标签。
                </canvas>
              </el-scrollbar>
            </div>
          </el-col>
          <el-col v-show="canvasScale" :span="19" :offset="1" class="excepRectLegend">
            <div class="excepRectDiv" style="height:100%;">
              <el-scrollbar style="height:100%;">
                <canvas id="excepCanvasIdTemp">
                  您的浏览器不支持 HTML5 canvas 标签。
                </canvas>
              </el-scrollbar>
            </div>
          </el-col>
          <el-col :span="2" :offset="1" class="excepLegend">
            <div :id="excepLegendId" />
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>
<script>
import * as d3 from 'd3'
import { createNamespacedHelpers } from 'vuex'

const { mapActions: mapExceptionActions, mapGetters: mapExceptionGetters, mapMutations: mapExceptionMutations } = createNamespacedHelpers('exception')
export default {
  name: 'ExcepContainer',
  props: { oneData: Array, index: Number, oneAllStep: Array },
  data() {
    return {
      excepContainerHeadShow: false,
      excepHistId: `excepHist${this.index}`,
      excepRectId: `excepRect${this.index}`,
      excepCanvasId: `excepCanvas${this.index}`,
      excepLegendId: `excepLegend${this.index}`,
      excepBoxId: `excepBox${this.index}`,
      excepStepAxisId: `excepStepAxis${this.index}`,
      curStepIndex: 0, // 当前显示的step的索引
      boxLeftIndex: 0, // 刷子获取的范围
      boxRightIndex: 4,
      curExcepBox: [], // 当前双击选中的盒线图中的异常点
      myOneData: this.oneData, // 因为会被修改，不直接用Props中的变量
      myAllStep: this.oneAllStep[2].step, // step数组，用的比较多
      myBoxPercent: this.oneAllStep[2].box, // 六个百分点数组，也会被修改
      rectColor: ['#79a3da', '#fefebe', '#fe193f'], // 小：蓝色；大：红色
      rectColorRgb: [[121, 163, 218], [254, 254, 180], [254, 25, 63]],
      histxScale: '', // 在直方图标记up和down需要使用
      drawRectFinished: true, // 在盒线图上操作后，获取颜色矩阵并画好的标志
      getCurNewExcepBoxFlag: false, // 在盒线图图上操作后，获取新的异常数据点
      boxYScale: '', // 监听Panel选择上下界的操作，需要根据数值计算上下界的线所在的高度
      rectMin: this.oneData[3][1],
      rectMax: this.oneData[3][2],
      rectScale: 1.0,
      canvasScale: false,
      rectMinWidth: 15,
      rectMinHeight: 15
    }
  },
  computed: {
    ...mapExceptionGetters([
      'getCurNewData',
      'getCurNewExcepBox',
      'getCurIqrTimes',
      'getLinkChecked',
      'getDq0Show',
      'getUpDownValue'
    ])
  },
  watch: {
    getCurNewData(val) {
      if (this.myOneData[0] === val[0] && this.myOneData[1] === val[1]) {
        this.myOneData = val
        this.drawExcepHist()
        // eslint-disable-next-line
        this.rectMin = this.myOneData[3][1];
        // eslint-disable-next-line
        this.rectMax = this.myOneData[3][2];
        this.rectScale = 1.0
        this.canvasScale = false
        this.drawCanvasRect()
        this.drawRectFinished = true
        this.drawExcepLedgend()
      }
    },
    // step不变时，只需要单独获取异常点
    getCurNewExcepBox(val) {
      if (this.myOneData[0] === val[0] && this.myOneData[1] === val[1]) {
        this.getCurNewExcepBoxFlag = true
        // eslint-disable-next-line
        this.curExcepBox = val[2];
        this.drawExcepBox()
        // 盒须图高亮
        d3.select(`#${this.excepBoxId}`).select(`.boxRect${this.curStepIndex}`).style('fill', '#B0B6E6')
      }
    },
    getCurIqrTimes(val) {
      // 控制面板修改参数后，这边如何处理
      this.excepContainerHeadShow = false
      const getOneStepDataFlag = false
      if (this.myOneData[0] === val[0] && this.myOneData[1] === val[1]) { // 是不是当前这个子组件中的数据
        // 边框高亮
        this.excepContainerHeadShow = true
        if (this.myAllStep[this.curStepIndex] !== val[2]) { // step发生变化
          let k = 0
          for (let i = 0; i < this.myAllStep.length; i += 1) {
            if (this.myAllStep[i] === val[2]) {
              k = i
              break
            }
          }
          this.getOneStepDataFlag = true
          this.getOneStepData(k)
        }
        // 数据变化才会存进来，上下界变化
        const dq = this.myBoxPercent[this.curStepIndex][0][1] - this.myBoxPercent[this.curStepIndex][0][3]
        if (dq !== 0) {
          // 修改这个子组件中的数据
          this.myBoxPercent[this.curStepIndex][0][0] = this.myBoxPercent[this.curStepIndex][0][1] + val[3] * dq
          this.myBoxPercent[this.curStepIndex][0][4] = this.myBoxPercent[this.curStepIndex][0][3] - val[4] * dq
          // 修改vuex中保存的数据
          this.setAllStepBoxUp({ index: this.index, step: this.curStepIndex, up: this.myBoxPercent[this.curStepIndex][0][0] })
          this.setAllStepBoxDown({ index: this.index, step: this.curStepIndex, down: this.myBoxPercent[this.curStepIndex][0][4] })
        }
        const paramTemp = { run: this.myOneData[0], tag: this.myOneData[1], step: this.myAllStep[this.curStepIndex], down: this.myBoxPercent[this.curStepIndex][0][4], up: this.myBoxPercent[this.curStepIndex][0][0] }
        this.fetchExcepBox(paramTemp)
        if (!getOneStepDataFlag) { // 没有重新获取颜色矩阵，也需要重新绘制，因为之前的path还存在
          // 这里只重新绘制
          this.rectScale = 1.0
          this.canvasScale = false
          this.drawCanvasRect()
        }
      }
    },
    drawRectFinished() {
      if (this.getCurNewExcepBoxFlag && this.drawRectFinished) {
        this.setRectExcepBox()
        this.getCurNewExcepBoxFlag = false
      }
    },
    getCurNewExcepBoxFlag() {
      if (this.getCurNewExcepBoxFlag && this.drawRectFinished) {
        this.setRectExcepBox()
        this.getCurNewExcepBoxFlag = false
      }
    }
  },
  mounted() {
    this.drawExcepHist()
    this.drawCanvasRect()
    this.CanvasRectMouseOperator()
    this.drawExcepLedgend()
    if (this.myAllStep.length < 5) {
      this.boxRightIndex = this.myAllStep.length - 1
    }
    this.curStepIndex = this.myAllStep.indexOf(this.oneData[2])
    if (this.curStepIndex > 5) {
      this.boxLeftIndex = this.curStepIndex - 4
      this.boxRightIndex = this.curStepIndex
    }
    this.drawExcepBox()
    this.drawExcepStepAxis()
    d3.select(`#${this.excepBoxId}`).select(`.boxRect${this.curStepIndex}`).style('fill', '#B0B6E6')
    // 当鼠标进入颜色矩阵区域禁止滑动条的滚轮操作，不在颜色矩阵区域就允许滑动条的滚轮操作
    d3.select(`#${this.excepCanvasId}`).on('mouseover', () => {
      document.getElementById('excepDisplay').onmousewheel = () => {
        return false
      }
    })
    d3.select(`#${this.excepCanvasId}`).on('mouseout', () => {
      document.getElementById('excepDisplay').onmousewheel = () => {
        return true
      }
    })
  },
  methods: {
    ...mapExceptionActions(['fetchOneData', 'fetchExcepBox']),
    ...mapExceptionMutations([
      'setAllStepBoxDown',
      'setAllStepBoxUp',
      'setRectCurInfo',
      'setCurIqrTimes',
      'setExcepBoxStatistic',
      'setDq0Show',
      'setUpDownValue'
    ]),
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
    // 画直方图
    drawExcepHist() {
      d3.select(`#${this.excepHistId}`).select('svg').remove()
      const histSvgWidth = 630
      const histSvgHeight = 240
      const padding = { top: 25, right: 30, bottom: 25, left: 50 }
      const histWidth = histSvgWidth - padding.left - padding.right
      const histHeight = histSvgHeight - padding.top - padding.bottom
      const histOuterSvg = d3.select(`#${this.excepHistId}`).append('svg')
        .attr('width', '100%').attr('height', '100%')
        .attr('preserveAspectRatio', 'xMidYMid meet').attr('viewBox', `0 0 ${histSvgWidth} ${histSvgHeight}`)
      const histSvg = histOuterSvg.append('g').attr('width', histSvgWidth).attr('height', histSvgHeight)
        .attr('transform', `translate(${padding.left},${padding.top})`)
      const histData = this.myOneData[4]
      this.histxScale = d3.scaleLinear().domain([histData[0], histData[1]]).range([0, histWidth]).nice()
      const histCountMax = d3.max(histData[2], function _nonName(d) {
        return d[2]
      })
      const histyScale = d3.scaleLinear().domain([0, histCountMax]).range([histHeight, 0]).nice()
      const histxAxis = d3.axisBottom()
        .scale(this.histxScale)
        .ticks(7)
        .tickFormat(d => this.numberChangeToE(d))
      const histyAxis = d3.axisLeft()
        .scale(histyScale)
        .ticks(7)
        .tickFormat(d => this.numberChangeToE(d))
      histSvg.append('g').call(histxAxis).attr('transform', `translate(0, ${histHeight})`)
      histSvg.append('g').call(histyAxis)
      const that = this
      histSvg.append('g')
        .selectAll('rect')
        .data(histData[2])
        .enter()
        .append('g')
        .append('rect')
        .attr('x', function _nonName(d) {
          return that.histxScale(d[0])
        })
        .attr('y', function _nonName(d) {
          return histyScale(d[2])
        })
        .attr('width', function _nonName(d) {
          return that.histxScale(d[1]) - that.histxScale(d[0])
        })
        .attr('height', function _nonName(d) {
          return histHeight - histyScale(d[2])
        })
        .attr('fill', '#B0B6E6')
      // 把盒线图中的up和down标记出来
      const min = this.myBoxPercent[this.curStepIndex][0][4]
      const max = this.myBoxPercent[this.curStepIndex][0][0]
      histSvg.append('g').append('rect')
        .attr('x', this.histxScale(min))
        .attr('y', histHeight - 5).attr('width', '3')
        .attr('height', '10').attr('fill', 'red')
        .attr('class', 'minLine')
      histSvg.append('g').append('rect')
        .attr('x', this.histxScale(max))
        .attr('y', histHeight - 5).attr('width', '3')
        .attr('height', '10').attr('fill', 'red')
        .attr('class', 'maxLine')
    },
    // 为画布添加鼠标操作，只需要初始添加一次
    CanvasRectMouseOperator() {
      // 每次放大缩小都要重新渲染，性能太差！
      const excepCanvas = document.getElementById(this.excepCanvasId)
      const excepCanvasTemp = document.getElementById('excepCanvasIdTemp')
      // 鼠标悬浮计算当前点的行列
      const that = this
      function onMouseMoveFunc(e) {
        const rectDw = that.rectMinWidth * that.rectScale
        const rectDh = that.rectMinHeight * that.rectScale
        const row = Math.floor(e.layerY / rectDh)
        const col = Math.floor(e.layerX / rectDw)
        if (row < 0 || col < 0) return
        that.setRectCurInfo([that.myOneData[0], that.myOneData[1], that.myAllStep[that.curStepIndex], row, col, that.myOneData[3][4][row][col]])
      }
      // 鼠标滚轮放大，禁用滑动条的滚轮事件
      // 只允许缩小，不允许大于1倍
      function onMouseWheelFunc(e) {
        if (e.wheelDelta < 0) { // 缩小
          if (that.rectScale <= 0.1) return
          that.rectScale *= 0.9
          that.canvasScale = true
          excepCanvasTemp.width = excepCanvas.width * that.rectScale
          excepCanvasTemp.height = excepCanvas.height * that.rectScale
          const excepCanvasTemp2d = excepCanvasTemp.getContext('2d')
          excepCanvasTemp2d.drawImage(excepCanvas, 0, 0, excepCanvas.width, excepCanvas.height, 0, 0, excepCanvasTemp.width, excepCanvasTemp.height)
        } else { // 放大
          if (that.rectScale >= 1) return // 再大就会黑屏
          that.rectScale *= 1.1
          that.canvasScale = true
          excepCanvasTemp.width = excepCanvas.width * that.rectScale
          excepCanvasTemp.height = excepCanvas.height * that.rectScale
          const excepCanvasTemp2d = excepCanvasTemp.getContext('2d')
          excepCanvasTemp2d.drawImage(excepCanvas, 0, 0, excepCanvas.width, excepCanvas.height, 0, 0, excepCanvasTemp.width, excepCanvasTemp.height)
        }
      }
      // 鼠标点击还原
      function onClickFunc() {
        that.rectScale = 1.0
        that.canvasScale = false
      }
      excepCanvas.onmousemove = onMouseMoveFunc
      excepCanvas.onclick = onClickFunc
      excepCanvas.onmousewheel = onMouseWheelFunc
      excepCanvasTemp.onmousemove = onMouseMoveFunc
      excepCanvasTemp.onclick = onClickFunc
      excepCanvasTemp.onmousewheel = onMouseWheelFunc
    },
    // 重绘矩阵时，可不可以直接重用各小矩阵，只改变大小和颜色？
    // 画颜色矩阵
    drawCanvasRect() {
      const min = this.rectMin
      const max = this.rectMax
      const n = this.myOneData[3][0][0]
      const m = this.myOneData[3][0][1]
      const rectDw = this.rectMinWidth * this.rectScale
      const rectDh = this.rectMinHeight * this.rectScale
      const rectWidth = rectDw * m
      const rectHeight = rectDh * n
      const excepCanvas = document.getElementById(this.excepCanvasId)
      // canvas画布宽高变化，就清空了原先的内容
      excepCanvas.width = rectWidth + 20
      excepCanvas.height = rectHeight
      const colorLinear = d3.scaleLinear().domain([min, (min + max) / 2, max]).range(this.rectColor)
      // 离散颜色映射
      const colorMap = []
      const threshold = 100
      const minvalue = (max - min) / threshold
      let value = min
      for (let i = 0; i < threshold; i++) {
        colorMap.push(colorLinear(value))
        value += minvalue
      }
      const excepCanvas2d = excepCanvas.getContext('2d')
      const colorMatrixData = this.myOneData[3][4]
      // 不在[min, max]范围内的方块
      excepCanvas2d.fillStyle = '#eeeeee'
      for (let i = 0; i < n; i += 1) {
        const rectH = i * rectDh
        for (let j = 0; j < m; j += 1) {
          const t = colorMatrixData[i][j]
          if (t < min && t > max) {
            excepCanvas2d.fillRect(j * rectDw, rectH, rectDw, rectDh)
          }
        }
      }
      for (let k = 0; k < threshold; k++) {
        excepCanvas2d.fillStyle = colorMap[k]
        const leftvalue = k * minvalue + min
        const rightvalue = (k + 1) * minvalue + min
        for (let i = 0; i < n; i++) {
          const rectH = i * rectDh
          for (let j = 0; j < m; j += 1) {
            const t = colorMatrixData[i][j]
            if (t >= leftvalue && t < rightvalue) {
              excepCanvas2d.fillRect(j * rectDw, rectH, rectDw, rectDh)
            }
          }
        }
      }
      // 画白色边界
      let lineY = 0
      for (let i = 0; i < n; i += 1) {
        excepCanvas2d.beginPath()
        excepCanvas2d.moveTo(0, lineY)
        excepCanvas2d.lineTo(rectWidth, lineY)
        excepCanvas2d.strokeStyle = 'rgba(255, 255, 255)'
        excepCanvas2d.stroke()
        lineY += rectDh
      }
      let lineX = 0
      for (let i = 0; i < m; i += 1) {
        excepCanvas2d.beginPath()
        excepCanvas2d.moveTo(lineX, 0)
        excepCanvas2d.lineTo(lineX, rectHeight)
        excepCanvas2d.strokeStyle = 'rgba(255, 255, 255)'
        excepCanvas2d.stroke()
        lineX += rectDw
      }
      this.setRectCurInfo([])
    },
    // 画颜色矩阵的legend
    drawExcepLedgend() {
      d3.select(`#${this.excepLegendId}`).select('svg').remove()
      const legendWidth = 120
      const legendHeight = 300
      const legendRectWidth = 25
      const legendRectHeight = 135
      const top = 100
      const left = 20
      const legendSvg = d3.select(`#${this.excepLegendId}`).append('svg').attr('width', legendWidth).attr('height', legendHeight)
        .attr('width', '100%').attr('height', '100%').attr('preserveAspectRatio', 'xMidYMid meet')
        .attr('viewBox', `0 0 ${legendWidth} ${legendHeight}`).append('g').attr('transform', `translate(${left},${top})`)
      const min = this.myOneData[3][1]
      const max = this.myOneData[3][2]
      const minMaxFormat = d3.format('.4f')
      const curMinText = legendSvg
        .append('g')
        .append('text')
        .text(minMaxFormat(min))
        .attr('x', legendRectWidth + 15)
        .attr('y', legendRectHeight)
        .attr('stroke', 'black')
        .style('font-size', '10px')
      const curMaxText = legendSvg
        .append('g')
        .append('text')
        .text(minMaxFormat(max))
        .attr('x', legendRectWidth + 15)
        .attr('y', 0)
        .attr('stroke', 'black')
        .style('font-size', '10px')
      const valuescale = d3.scaleLinear().domain([min, max]).range([legendRectHeight, 0])
      // 背景矩形
      legendSvg.append('g').append('rect').attr('x', 0).attr('y', 0).attr('width', legendRectWidth)
        .attr('height', legendRectHeight).attr('fill', '#eeeeee')
      // legend矩形，上下边界会变化，自己配渐变颜色
      // 定义一个线性渐变
      const defs = legendSvg.append('defs')
      const legendId = `linearColor${this.index}`
      const linearGradient = defs.append('linearGradient')
        .attr('id', legendId)
        .attr('x1', '0')
        .attr('y1', '0')
        .attr('x2', '0')
        .attr('y2', '100%')
      linearGradient.append('stop')
        .attr('offset', '0%')
        .style('stop-color', this.rectColor[2])
      linearGradient.append('stop')
        .attr('offset', '50%')
        .style('stop-color', this.rectColor[1])
      linearGradient.append('stop')
        .attr('offset', '100%')
        .style('stop-color', this.rectColor[0])
      const myLegend = legendSvg.append('g').append('rect').attr('x', 0).attr('y', 0)
        .attr('width', legendRectWidth).attr('height', legendRectHeight)
        .style('fill', `url(#${legendId})`)
      const upDownRect = legendSvg.append('g')
      let upHeight = 0
      let downHeight = legendRectHeight
      let curMin = min
      let curMax = max
      // 上三角形的信息
      const lengthTri = 10
      const that = this
      upDownRect.append('g').append('path').attr('d', `m${legendRectWidth} 0L${legendRectWidth + lengthTri} ${-lengthTri}L${legendRectWidth + lengthTri} 0 Z`)
        .attr('fill', this.rectColor[2])
        .on('mouseover', function _nonName() {
          d3.select(this).style('cursor', 's-resize')
        })
        .call(
          d3.drag().on('drag', function _nonName() {
            d3.select(this).style('cursor', 's-resize')
            if (d3.event.y < 0 || d3.event.y > downHeight) upHeight = 0
            else upHeight = d3.event.y
            d3.select(this).attr('d', `m${legendRectWidth} ${0 + upHeight}L${legendRectWidth + lengthTri} ${-lengthTri + upHeight}L${legendRectWidth + lengthTri} ${+upHeight} Z`)
            myLegend.attr('y', upHeight).attr('height', downHeight - upHeight)
            curMax = valuescale.invert(upHeight)
            curMaxText.text(minMaxFormat(curMax)).attr('y', upHeight)
          })
            .on('end', function _nonName() {
              that.rectMin = curMin
              that.rectMax = curMax
              that.rectScale = 1.0
              that.canvasScale = false
              that.drawCanvasRect()
              that.setRectExcepBox()
            }),
        )
      // 下三角形信息
      upDownRect.append('g').append('path').attr('d', `m${legendRectWidth} ${legendRectHeight}L${legendRectWidth + lengthTri} ${legendRectHeight + lengthTri}L${legendRectWidth + lengthTri} ${legendRectHeight} Z`)
        .attr('fill', this.rectColor[0])
        .on('mouseover', function _nonName() {
          d3.select(this).style('cursor', 's-resize')
        })
        .call(
          d3.drag().on('drag', function _nonName() {
            d3.select(this).style('cursor', 's-resize')
            if (d3.event.y > legendRectHeight || d3.event.y < upHeight) downHeight = legendRectHeight
            else downHeight = d3.event.y
            d3.select(this).attr('d', `m${legendRectWidth} ${downHeight}L${legendRectWidth + lengthTri} ${lengthTri + downHeight}L${legendRectWidth + lengthTri} ${downHeight} Z`)
            myLegend.attr('height', downHeight - upHeight)
            curMin = valuescale.invert(downHeight)
            curMinText.text(minMaxFormat(curMin)).attr('y', downHeight + 10)
          })
            .on('end', function _nonName() {
              that.rectMin = curMin
              that.rectMax = curMax
              that.rectScale = 1.0
              that.canvasScale = false
              that.drawCanvasRect()
              that.setRectExcepBox()
            }),
        )
    },
    // 画step坐标轴
    drawExcepStepAxis() {
      d3.select(`#${this.excepStepAxisId}`).select('svg').remove()
      const stepSvgWidth = 630
      const stepSvgHeight = 40
      const padding = { left: 50, top: 10, right: 30, bottom: 10 }
      const stepWidth = stepSvgWidth - padding.left - padding.right
      const stepSvg = d3.select(`#${this.excepStepAxisId}`).append('svg').attr('width', '100%').attr('height', '100%')
        .attr('preserveAspectRatio', 'xMidYMid meet').attr('viewBox', `0 0 ${stepSvgWidth} ${stepSvgHeight}`) // .append('g')
      const allStep = this.myAllStep
      const stepArrayLen = allStep.length - 1
      const maxStep = allStep[stepArrayLen]
      const stepXScale = d3.scaleLinear().domain([allStep[0], maxStep]).range([0, stepWidth]) // .nice()
      // const stepXScale2 = d3.scalePoint().domain(this.myAllStep).range([0, stepWidth]) // 不连续domain与连续的range之间的映射
      // const stepXAxis = stepSvg.append('g').call(d3.axisBottom().scale(stepXScale2)) // 好像没有必要
      const stepXAxis = stepSvg.append('g').call(d3.axisBottom().scale(stepXScale))
        .attr('transform', `translate(${padding.left},${padding.top})`)
      stepSvg.append('g').append('text').text('step:').attr('x', 20).attr('y', padding.top + 5)
        .attr('fill', 'black').style('font-size', '12px')
      const that = this
      // 加刷子操作
      // 限制brush刷取的操作
      // 固定刷子宽度
      const brush = d3.brushX()
        .extent([[0, -7], [stepWidth, 7]])
        .on('end', function _nonName() {
          if (d3.event.selection === null) {
            return
          }
          const brushLeft = stepXScale.invert(d3.event.selection[0])
          const brushRight = stepXScale.invert(d3.event.selection[1])
          if (brushLeft > maxStep && brushRight > maxStep) return
          let leftK = 0
          let rightK = stepArrayLen
          for (let i = 1; i <= stepArrayLen; i += 1) {
            if (brushLeft < allStep[i]) {
              leftK = i - 1
              if (brushLeft - allStep[i - 1] > allStep[i] - brushLeft) {
                leftK = i
              }
              break
            }
          }
          for (let i = leftK + 1; i <= stepArrayLen; i += 1) {
            if (brushRight < allStep[i]) {
              rightK = i - 1
              if (brushRight - allStep[i - 1] > allStep[i] - brushRight) {
                rightK = i
              }
              break
            }
          }
          if (leftK === that.boxLeftIndex && rightK === that.boxRightIndex) {
            return
          }
          if (that.curStepIndex < leftK || that.curStepIndex > rightK) {
            that.curExcepBox = []
            that.getOneStepData(leftK)
          }
          that.boxLeftIndex = leftK
          that.boxRightIndex = rightK
          that.drawExcepBox()
          d3.select(`#${that.excepBoxId}`).select(`.boxRect${that.curStepIndex}`).style('fill', '#B0B6E6')
        })
      stepXAxis.append('g')
        .attr('class', 'brush')
        .call(brush)
        .call(brush.move, [allStep[that.boxLeftIndex], allStep[that.boxRightIndex]].map(stepXScale)) // 默认选五步
      // removes handle to resize the brush
      d3.select(`#${this.excepStepAxisId}`).selectAll('.brush>.handle').remove()
      // removes crosshair cursor
      d3.select(`#${this.excepStepAxisId}`).selectAll('.brush>.overlay').remove()
    },
    // 画盒须图
    drawExcepBox() {
      d3.select(`#${this.excepBoxId}`).select('svg').remove()
      const leftIndex = this.boxLeftIndex
      const rightIndex = this.boxRightIndex
      const dw = 110 // 一个box的宽度
      const allStep = this.myAllStep
      const bigBoxSvgHeight = 240
      const padding = { top: 20, right: 30, bottom: 40, left: 50 }
      const bigBoxSvgWidth = 650
      const bigBoxHeight = bigBoxSvgHeight - padding.top - padding.bottom
      const bigBoxSvg = d3.select(`#${this.excepBoxId}`).append('svg')
        .attr('width', '100%').attr('height', '100%')
        .attr('preserveAspectRatio', 'xMidYMid meet').attr('viewBox', `0 0 ${bigBoxSvgWidth} ${bigBoxSvgHeight}`)
        .append('g')
      const stepSlice = allStep.slice(leftIndex, rightIndex + 1)
      const stepDomain = []
      for (let i = 0; i <= rightIndex - leftIndex + 1; i += 1) {
        stepDomain.push((i + 0.5) * dw)
      }
      const boxXScale = d3.scaleOrdinal().domain(stepSlice).range(stepDomain)
      bigBoxSvg.append('g').call(d3.axisBottom().scale(boxXScale))
        .attr('transform', `translate(${padding.left - dw / 2},${bigBoxHeight + padding.top})`) // .attr('class', 'axis')
        .selectAll('text').attr('dx', dw / 2).style('font-size', '11px').style('font-weight', '600')
      // 被选中的step中的最大值最小值中的最大值最小值（包括异常点吗）
      const boxPercent = this.myBoxPercent
      const selectBoxData = boxPercent.slice(leftIndex, rightIndex + 1)
      let valueMax1 = d3.max(selectBoxData, function _nonName(d) {
        return d[0][0]
      })
      let valueMin1 = d3.min(selectBoxData, function _nonName(d) {
        return d[0][4]
      })
      const valueMax2 = d3.max(selectBoxData, function _nonName(d) {
        return d[1][5]
      })
      const valueMin2 = d3.min(selectBoxData, function _nonName(d) {
        return d[1][0]
      })
      if (valueMax2 > valueMax1) {
        valueMax1 = valueMax2
      }
      if (valueMin2 < valueMin1) {
        valueMin1 = valueMin2
      }
      this.boxYScale = d3.scaleLinear().domain([valueMin1, valueMax1]).range([bigBoxHeight, 0]).nice()
      bigBoxSvg.append('g').call(d3.axisLeft().scale(this.boxYScale).ticks(7).tickFormat(d => this.numberChangeToE(d)))
        .attr('transform', `translate(${padding.left},${padding.top})`)
      const width = (dw - 10) / 2
      const rectWidth = dw - 6
      const that = this
      for (let i = leftIndex; i <= rightIndex; i += 1) {
        const center = boxXScale(allStep[i]) + padding.left
        const oneBoxSvg = bigBoxSvg.append('g') // 用svg可以通过zoom局部放大
        oneBoxSvg.append('rect')
          .attr('x', center - rectWidth / 2)
          .attr('y', padding.top)
          .attr('height', bigBoxHeight - 1)
          .attr('width', rectWidth)
          .attr('stroke', 'white')
          .attr('class', `boxRect${i}`)
          .style('fill', '#edf1fd')
          .on('mousemove', function _nonName() {
            d3.select(this).style('cursor', 'pointer')
          })
          .on('click', function _nonName() { // 单击获取当前步的数据
            const idx = Number(d3.select(this).attr('class').slice(7))
            const dq = that.myBoxPercent[idx][0][1] - that.myBoxPercent[idx][0][3]
            let uptimes = that.myBoxPercent[idx][0][0]
            let downtimes = that.myBoxPercent[idx][0][4]
            if (dq === 0) {
              that.setDq0Show(true)
              that.setUpDownValue([that.myBoxPercent[idx][0][0], that.myBoxPercent[idx][0][4]])
            } else {
              that.setDq0Show(false)
              uptimes = (that.myBoxPercent[idx][0][0] - that.myBoxPercent[idx][0][1]) / dq
              downtimes = (that.myBoxPercent[idx][0][3] - that.myBoxPercent[idx][0][4]) / dq
            }
            that.setCurIqrTimes([that.myOneData[0], that.myOneData[1], that.myAllStep[idx], uptimes, downtimes])
          })
        this.drawOneBox(oneBoxSvg, this.boxYScale, i, center, width, padding.top)
      }
    },
    drawOneBox(svg, y, index, center, width, top) {
      const boxPercent = this.myBoxPercent
      const q1 = boxPercent[index][0][3]
      const median = boxPercent[index][0][2]
      const q3 = boxPercent[index][0][1]
      const min = boxPercent[index][0][4]
      const max = boxPercent[index][0][0]

      const centerLine = svg.append('g')
        .append('line')
        .attr('x1', center)
        .attr('x2', center)
        .attr('y1', top + y(min))
        .attr('y2', top + y(max))
        .attr('stroke', 'black')

      svg.append('g')
        .append('rect')
        .attr('x', center - width / 2)
        .attr('y', top + y(q3))
        .attr('height', (y(q1) - y(q3)))
        .attr('width', width)
        .attr('stroke', 'black')
        .style('fill', '#8F8BD8')

      svg.append('g')
        .append('line')
        .attr('x1', center - width / 2)
        .attr('x2', center + width / 2)
        .attr('y1', function _nonName() {
          return top + y(median)
        })
        .attr('y2', function _nonName() {
          return top + y(median)
        })
        .attr('stroke', 'black')
      const upText = svg.append('g').append('text').attr('x', center - width / 3).attr('stroke', 'black').attr('font-size', '10px') // 上下线的y值
      const downText = svg.append('g').append('text').attr('x', center - width / 3).attr('stroke', 'black').attr('font-size', '10px')
      // min
      const that = this
      const minUp = y(q1) + top // min往上走不能超过minUp
      const minDown = y(boxPercent[index][1][0]) + top // min往下走不能超过minDown
      let curMinPosition = top + y(min)
      const ming = svg.append('g')
      // min line的背景，扩大鼠标的选中的范围
      ming.append('line')
        .attr('class', `excepDownLine${index}`)
        .attr('x1', center - width / 2)
        .attr('x2', center + width / 2)
        .attr('y1', function _nonName() {
          return top + y(min)
        })
        .attr('y2', function _nonName() {
          return top + y(min)
        })
        .attr('stroke', 'black')
        .attr('stroke-width', '20')
        .attr('stroke-opacity', '0')

      const minLineFront = ming.append('line')
        .attr('class', `excepDownLine${index}`)
        .attr('x1', center - width / 2)
        .attr('x2', center + width / 2)
        .attr('y1', function _nonName() {
          return top + y(min)
        })
        .attr('y2', function _nonName() {
          return top + y(min)
        })
        .attr('stroke', 'black')
        .attr('stroke-width', '2')
      ming.on('mouseover', function _nonName() {
        d3.select(this).style('cursor', 's-resize')
      })
        .call(d3.drag().on('drag', function _nonName() {
          if (d3.event.y > minDown || d3.event.y < minUp) return
          curMinPosition = d3.event.y
          d3.select(this).attr('y1', curMinPosition).attr('y2', curMinPosition)
          centerLine.attr('y1', curMinPosition)
          downText.attr('y', curMinPosition + 10).text(y.invert(curMinPosition - top).toFixed(4))
          minLineFront.attr('y1', curMinPosition).attr('y2', curMinPosition)
        })
          .on('end', function _nonName() {
            // 停止拖拽时更新js中的min和max，并向后端请求数据
            that.getOneStepBoxData('down', y.invert(curMinPosition - top), index)
            d3.select(`#${that.excepHistId}`).select('svg').select('.minLine').attr('x', that.histxScale(y.invert(curMinPosition - top)))
          }),
        )
      // max
      const maxDown = y(q3) + top
      const maxUp = y(boxPercent[index][1][5]) + top
      let curMaxPosition = top + y(max)
      // max
      const maxg = svg.append('g')
      // max line的背景，扩大鼠标的选中的范围
      maxg.append('line')
        .attr('class', `excepUpLine${index}`)
        .attr('x1', center - width / 2)
        .attr('x2', center + width / 2)
        .attr('y1', function _nonName() {
          return top + y(max)
        })
        .attr('y2', function _nonName() {
          return top + y(max)
        })
        .attr('stroke', 'black')
        .attr('stroke-width', '20')
        .attr('stroke-opacity', '0')
      const maxLineFront = maxg.append('line')
        .attr('class', `excepUpLine${index}`)
        .attr('x1', center - width / 2)
        .attr('x2', center + width / 2)
        .attr('y1', function _nonName() {
          return top + y(max)
        })
        .attr('y2', function _nonName() {
          return top + y(max)
        })
        .attr('stroke', 'black')
        .attr('stroke-width', '2')
      maxg.on('mouseover', function _nonName() {
        d3.select(this).style('cursor', 's-resize')
      })
        .call(d3.drag().on('drag', function _nonName() {
          if (d3.event.y < maxUp || d3.event.y > maxDown) return
          curMaxPosition = d3.event.y
          d3.select(this).attr('y1', curMaxPosition).attr('y2', curMaxPosition)
          centerLine.attr('y2', curMaxPosition)
          upText.attr('y', curMaxPosition).text(y.invert(curMaxPosition - top).toFixed(4))
          maxLineFront.attr('y1', curMaxPosition).attr('y2', curMaxPosition)
        })
          .on('end', function _nonName() {
            that.getOneStepBoxData('up', y.invert(curMaxPosition - top), index)
            d3.select(`#${that.excepHistId}`).select('svg').select('.maxLine').attr('x', that.histxScale(y.invert(curMaxPosition - top)))
          }),
        )
      // 六个百分比
      svg.append('g').selectAll('circle').data(boxPercent[index][1]).enter()
        .append('g').append('circle')
        .attr('r', '3').attr('cx', center).attr('cy', function _nonName(d) { return top + y(d) })
        .attr('fill', 'blue')
        .style('opacity', '0.5')
      // 画异常点
      if (this.curExcepBox.length && this.curStepIndex === index) {
        // 定为最多只画100个异常点
        const threshold = 200
        let exceptionPoints = [[], []]
        if (this.curExcepBox[0].length <= threshold) {
          exceptionPoints = this.curExcepBox
        } else {
          const len = this.curExcepBox[0].length
          const minv = Math.floor(len / threshold)
          let j = 0
          for (let i = 0; i < threshold; i += 1) {
            exceptionPoints[0].push(this.curExcepBox[0][j])
            exceptionPoints[1].push(this.curExcepBox[1][j])
            j += minv
          }
        }
        svg.append('g').attr('class', 'excepCircles').selectAll('circle').data(exceptionPoints[0]).enter().append('g').append('circle')
          .attr('r', '2').attr('cx', center).attr('cy', function _nonName(d) { return top + y(d) }).attr('fill', '#fe5c66').style('opacity', '0.3')
          .on('mouseover', function _nonName(d, i) {
            // 是一维的
            let curRow = 0
            let curColumn = exceptionPoints[1][i][0]
            // 是二维的
            if (that.oneData[3][4].length > 1) {
              // eslint-disable-next-line
              curRow = exceptionPoints[1][i][0];
              // eslint-disable-next-line
              curColumn = exceptionPoints[1][i][1];
            }
            that.setRectCurInfo([that.myOneData[0], that.myOneData[1], that.myAllStep[that.curStepIndex], curRow, curColumn, that.oneData[3][4][curRow][curColumn]])
          })
      }
    },
    // 获取一步数据
    getOneStepData(idx) {
      if (this.curStepIndex === idx) return
      this.drawRectFinished = false
      this.curStepIndex = idx
      const param = { run: this.myOneData[0], tag: this.myOneData[1], step: this.myAllStep[idx], index: this.index }
      this.fetchOneData(param)
    },
    getOneStepBoxData(flag, value, idx) { // 调整，获取新的异常点
      this.getCurNewExcepBoxFlag = false
      const dq = this.myBoxPercent[idx][0][1] - this.myBoxPercent[idx][0][3]
      if (dq === 0) {
        this.setDq0Show(true)
        this.setCurIqrTimes([this.myOneData[0], this.myOneData[1], this.myAllStep[idx], value, 0])
        if (flag === 'up') {
          this.myBoxPercent[idx][0][0] = value
          this.setAllStepBoxUp({ index: idx, step: this.myAllStep[idx], up: value })
        } else if (flag === 'down') {
          this.myBoxPercent[idx][0][4] = value
          this.setAllStepBoxDown({ index: idx, step: this.myAllStep[idx], down: value })
        }
        this.setUpDownValue([this.myBoxPercent[idx][0][0], this.myBoxPercent[idx][0][4]])
      } else if (flag === 'up') {
        this.setDq0Show(false)
        this.myBoxPercent[idx][0][0] = value
        let upTimes = (value - this.myBoxPercent[idx][0][1]) / dq
        // up和down联动
        let downTimes = (this.myBoxPercent[idx][0][3] - this.myBoxPercent[idx][0][4]) / dq
        if (this.getLinkChecked) {
          downTimes = upTimes
          const maxDownTimes = (this.myBoxPercent[idx][0][3] - this.myBoxPercent[idx][1][0]) / dq
          if (downTimes > maxDownTimes) {
            this.$message({
              message: `下四分位距的倍数最大只能为：${maxDownTimes}`,
              type: 'warning'
            })
            upTimes = maxDownTimes
            downTimes = maxDownTimes
          }
          let newDown = this.myBoxPercent[idx][0][3] - downTimes * dq
          if (newDown < this.myBoxPercent[idx][1][0]) {
            // eslint-disable-next-line
            newDown = this.myBoxPercent[idx][1][0];
          }
          this.myBoxPercent[idx][0][4] = newDown
        }
        this.setCurIqrTimes([this.myOneData[0], this.myOneData[1], this.myAllStep[idx], upTimes, downTimes])
      } else if (flag === 'down') {
        this.myBoxPercent[idx][0][4] = value
        // up和down联动
        let downTimes = (this.myBoxPercent[idx][0][3] - value) / dq
        let upTimes = (this.myBoxPercent[idx][0][0] - this.myBoxPercent[idx][0][1]) / dq
        if (this.getLinkChecked) {
          upTimes = downTimes
          const maxUpTimes = (this.myBoxPercent[idx][1][5] - this.myBoxPercent[idx][0][1]) / dq
          if (upTimes > maxUpTimes) {
            this.$message({
              message: `上四分位距的倍数最大只能为：${maxUpTimes}`,
              type: 'warning'
            })
            upTimes = maxUpTimes
            downTimes = maxUpTimes
          }
          let newUp = this.myBoxPercent[idx][0][1] + upTimes * dq
          if (newUp > this.myBoxPercent[idx][1][5]) {
            // eslint-disable-next-line
            newUp = this.myBoxPercent[idx][1][5];
          }
          this.myBoxPercent[idx][0][0] = newUp
        }
        this.setCurIqrTimes([this.myOneData[0], this.myOneData[1], this.myAllStep[idx], upTimes, downTimes])
      }
    },
    setRectExcepBox() { // 异常点有数据后,颜色矩阵边界高亮
      if (this.curExcepBox.length) {
        const n = this.myOneData[3][0][0]
        // const m = this.myOneData[3][0][1];
        const rectWidth = this.rectMinWidth * this.rectScale
        const rectHeight = this.rectMinHeight * this.rectScale
        const excepCanvas = document.getElementById(this.excepCanvasId)
        const excepCanvas2d = excepCanvas.getContext('2d')
        const curExcepBoxData = this.curExcepBox[1]
        for (let k = 0, len = this.curExcepBox[0].length; k < len; k += 1) {
          let leftX = curExcepBoxData[k][0] * rectWidth
          let leftY = 0
          if (n !== 1) {
            leftX = curExcepBoxData[k][1] * rectWidth
            leftY = curExcepBoxData[k][0] * rectHeight
          }
          excepCanvas2d.beginPath()
          excepCanvas2d.moveTo(leftX, leftY)
          excepCanvas2d.lineTo(leftX + rectWidth, leftY)
          excepCanvas2d.lineTo(leftX + rectWidth, leftY + rectHeight)
          excepCanvas2d.lineTo(leftX, leftY + rectHeight)
          excepCanvas2d.lineTo(leftX, leftY)
          excepCanvas2d.strokeStyle = '#8933e0'
          excepCanvas2d.stroke()
        }
        // 统计异常点:异常点个数，占所有数据的百分比
        this.setExcepBoxStatistic([this.curExcepBox[0].length, (this.curExcepBox[0].length * 100.0 / (this.myOneData[3][0][0] * this.myOneData[3][0][1])).toFixed(2)])
      }
    }
  }
}
</script>
<style>
.exceptionContainer .el-scrollbar__thumb:hover{
  background-color: #B0B6E6;
}
.exceptionContainer .el-scrollbar__thumb{
  background-color: #B0B6E6;
}
.exceptionContainer .el-card__body {
  padding: 0px;
  height: 100%;
}
/* 隐藏原生滑动轴 */
.excepRectDiv .el-scrollbar__wrap{
  overflow: hidden;
}
</style>
