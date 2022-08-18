<template>
  <div class="state-vis">
    <div class="header">
      <div class="title">
        <div class="square"></div>
        <span>隐状态折线图</span>
      </div>
      <div class="move-button-zrea">
        <div class="move-left"><button @click="turnToleft"><img
              src="@/assets/arrow-left-circle.svg"
              style="height: 20px"></button>
        </div>
        <div class="move-right"><button @click="turnToRight"><img
              src="@/assets/arrow-right-circle.svg"
              style="height: 20px"></button>
        </div>
      </div>
    </div>

    <div class="state-vis-box"></div>
    <div class="state-vis-axis"></div>
    <div class="row-divider-line"></div>
    <div class="title">
      <div class="square"></div>
      <span>匹配结果</span>
    </div>
    <div class="match-content" v-if="getStateMatchData.length">
      <el-table class="match-content-table" :data="getStateMatchData" stripe
        border style="width: 100%" @cell-click="cellClick"
        :header-cell-style="getRowClass">
        <el-table-column prop="id" label="ID" width="100px" align="center">
        </el-table-column>
        <el-table-column prop="data" label="Message" align="center">
        </el-table-column>
        <el-table-column prop="start_pos" label="Start pos" width="100px"
          align="center">
        </el-table-column>
      </el-table>
    </div>
    <div class="match-content" v-else>
      <div class="match-result-label">暂 无 匹 配 结 果 !</div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import { createNamespacedHelpers } from "vuex";

const {
  mapGetters: mapHiddenStateGetters,
  mapMutations: mapHiddenStateMutations,
  mapActions: mapHiddenStateActions
} = createNamespacedHelpers("hiddenstate");

const {
  mapState: mapLayoutStates
} = createNamespacedHelpers("layout");
export default {
  props: {
    stateData: Array
  },
  data () {
    return {
      jointData: [],
      isChangingThreshold: false,
      bottomBrushSelection: []
    }
  },
  computed: {
    ...mapHiddenStateGetters([
      "getStateData",
      "getSentence",
      "getMaxValue",
      "getMinValue",
      "getStateRun",
      "getStateTag",
      "getPos",
      "getRightWordsLength",
      "getRange",
      "getThreshold",
      "getSelectedLineIndexs",
      "getSelectedRange",
      "getSignature",
      "getIsMatching",
      "getStateMatchData"
    ]),
    ...mapLayoutStates([
      "userSelectRunFile"
    ]),
  },
  watch: {
    getStateData (val) {
      this.jointData = this.getJointData(val);
      this.drawStateVisBox();
      this.drawStateVisAxis();
    },
    getThreshold (val) {
      this.watchValueChange();
    },
    getSelectedRange (val) {
      this.watchValueChange();
    },
    bottomBrushSelection (val) {
      this.watchValueChange();
    },
    getRange (val) {
      this.drawStateVisBox();
      this.drawStateVisAxis();
    }
  },
  created () {
    this.jointData = this.getJointData(this.stateData);
  },
  mounted () {
    this.drawStateVisBox();
    this.drawStateVisAxis();
  },
  methods: {
    ...mapHiddenStateActions([
      "getHiddenStateData"
    ]),
    ...mapHiddenStateMutations([
      "setMaxValue",
      "setMinValue",
      "setThreshold",
      "setSelectedLineIndexs",
      "setSelectedRange",
      "setSignature",
      "setPos",
      "setStateMatchData"
    ]),
    // 折线区域绘制函数
    drawStateVisBox () {
      d3.select(".state-vis-box").select('svg').remove();
      let tooltipList = document.querySelectorAll(".tooltip");
      for (let i = 0; i < tooltipList.length; ++i) {
        tooltipList[i].remove();
      }

      // 隐状态显示区域
      const stateVisBox = d3.select(".state-vis-box")
        .append("svg")
        .attr("class", "hidden-state-box")
        .attr("width", "90%")
        .attr("height", 280 + "px")

      let xScale = this.getXScale();
      let yScale = this.getYScale();

      // 创建y轴
      let yAxis = stateVisBox.append("g")
        .attr("class", "y-axis")
        .attr("transform", "translate(45, 20)")

      // 创建y轴刻度
      yAxis.append("g")
        .attr("class", "ticks")
        .call(d3.axisLeft(yScale)
          .ticks(5)
          .tickSize(10)
          .tickPadding(10));

      yAxis.selectAll("line").remove();

      yAxis.select(".domain").remove();

      const ticksArr = [];
      d3.selectAll(".tick>text")
        .nodes()
        .map(function (t) {
          ticksArr.push(t.innerHTML);
        });

      // 创建y轴滑条
      yAxis.append('line')
        .attr("class", "slider-bg")
        .attr("y1", yScale.range()[1])
        .attr("y2", yScale.range()[0])
        .style("stroke-width", 20)
        .style("stroke", "black")
        .style("opacity", 0)
        .call(d3.drag()
          .on("start drag", this.yAxisSliderDragging)
          .on("end", this.yAxisSliderDragEnd));

      // 创建y轴滑轴圆点
      yAxis.append('circle')
        .attr("class", "slider-handle non-active")
        .attr("cy", yScale(this.getThreshold))
        .attr("r", 5)

      // 折线显示主区域
      let main = stateVisBox.append("g")
        .attr("class", "main")
        .attr("transform", "translate(50, 20)")

      for (let i = 0; i < ticksArr.length; i++) {
        main.append('line')
          .attr('class', 'tickLine id-' + i)
          .attr("x1", xScale.range()[0])
          .attr("x2", xScale.range()[1] - 30)
          .attr("y1", yScale(Number(ticksArr[i])))
          .attr("y2", yScale(Number(ticksArr[i])));
      }

      // 绘制隐状态折线
      const lineOpacity = this.lineOpacity(this.jointData);
      const lineGenerator = this.lineGenerator(xScale, yScale);
      this.drawValueLines(main, this.jointData, lineGenerator, lineOpacity);

      // 遮盖区域，用于高亮选中维度的折线和threshold线绘制
      let overlay = stateVisBox.append("g")
        .attr("class", "overlay")
        .attr("transform", "translate(50, 20)");

      // threshold线
      overlay.append('line')
        .attr('class', 'thresholdLine')
        .attr("x1", xScale.range()[0])
        .attr("x2", xScale.range()[1] - 30)
        .attr("y1", yScale(this.getThreshold))
        .attr("y2", yScale(this.getThreshold));

      let Tooltip = d3.select(".state-vis-box")
        .append("div")
        .style("position", "absolute")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px");
      // 绘制高亮选中维度折线
      if (Array.isArray(this.getSelectedLineIndexs) && this.getSelectedLineIndexs.length) {
        let highlightedValueLinesData = this.jointData.filter(d => _.includes(this.getSelectedLineIndexs, d.dim));
        let lineOpacity = this.lineOpacity(highlightedValueLinesData);
        let lineGenerator = this.lineGenerator(xScale, yScale);
        this.drawValueLines(overlay, highlightedValueLinesData, lineGenerator, lineOpacity);

        // 触碰高亮蓝线变红
        overlay.selectAll('.valueLine')
          .on("mouseenter", d => {
            overlay.selectAll('.valueLine')
              .classed('hovered', hoveredLine => {
                return hoveredLine.dim === d.dim
              });
          })
          .on("mouseout", d => {
            overlay.selectAll('.valueLine')
              .classed('hovered', false);
          })
          .on("mouseover", d => {
            if (!this.isChangingThreshold) {
              Tooltip.html(d.dim)
                .style("left", (d3.event.pageX - 120) + "px")
                .style("top", (d3.event.pageY - 10) + "px")
                .style("opacity", 1.0);
            }

          })
          .on("mousemove", d => {
            if (!this.isChangingThreshold) {
              Tooltip
                .style("left", (d3.event.pageX - 120) + "px")
                .style("top", (d3.event.pageY - 10) + "px");
            }

          })
          .on("mouseleave", d => {
            if (!this.isChangingThreshold) {
              Tooltip.style("opacity", 0);
            }
          })
      }
    },
    // 绘制折线并添加class
    drawValueLines (container, data, lineGenerator, lineOpacity) {

      const valueLines = container.selectAll('.valueLine').data(data);
      valueLines.exit().remove();

      return valueLines
        .enter()
        .append("path")
        .merge(valueLines)
        .attr("class", d => "valueLine id_" + d.dim)
        .attr("d", d => lineGenerator(d.value))
        .style("opacity", lineOpacity)
    },
    // 根据阈值变化或者搜索范围变化更新高亮折线
    watchValueChange () {
      const lineIndexs = [];

      if (this.getSelectedRange.length && this.bottomBrushSelection.length) {
        const leftBound = this.getSelectedRange[0] - this.bottomBrushSelection[0];
        const rightBound = this.getSelectedRange[1] + this.bottomBrushSelection[1];

        let signature = this.selectedRangeIndexs(leftBound, rightBound)
          .map(v => (v >= this.getSelectedRange[0] && v < this.getSelectedRange[1]) ? 1 : 0)
          .join('');

        this.setSignature(signature);

        this.jointData.forEach((lineData, index) => {
          const testSignature = lineData.value.slice(leftBound, rightBound)
            .map(v => (v.item >= this.getThreshold) ? 1 : 0)
            .join('');
          if (testSignature === this.getSignature) lineIndexs.push(index);
        })
      }
      this.setSelectedLineIndexs(lineIndexs);
      this.drawStateVisBox();
    },
    // 文本条区域绘制函数
    drawStateVisAxis () {
      d3.select(".state-vis-axis").select('svg').remove();

      let xScale = this.getXScale();

      // 文本条显示区域
      const stateVisAxis = d3.select(".state-vis-axis")
        .append("svg")
        .attr("class", "hidden-state-axis")
        .attr("width", "90%")
        .attr("height", 50 + "px")
        .attr("transform", "translate(0, 0)");

      // 掩层区域
      const overlay = stateVisAxis.append("g")
        .attr("class", "overlay");

      // 数据组装临时区域
      const measure = stateVisAxis.append("g")
        .attr("class", "measure");

      // 文本显示区域
      const textArea = stateVisAxis.append("g")
        .attr("class", "textArea")
        .attr("width", "90%")
        .attr("height", 24 + "px");

      // 选取文本滚动区域
      const brush = stateVisAxis.append("g")
        .attr("class", "brush")
        .attr("transform", "translate(35, 0)");

      // 选取文本滚动区域左右侧严格小于
      const bottomBrush = stateVisAxis.append("g")
        .attr("class", "bottomBrush")
        .attr("transform", "translate(35, 30)");

      // 文本组装，返回文本对象，包含每个字符及其宽高信息
      const measureText = measure.append('text')
        .attr("class", "text")
        .attr("x", "35")
        .attr("y", "0");
      let jointWords = this.getJointWords(measureText, this.getSentence);

      // 数据注入
      let wordCellList = textArea.selectAll(".word").data(jointWords);
      wordCellList.exit().remove();

      const wordEnter = wordCellList.enter().append("g");
      wordEnter.append('rect');
      wordEnter.append('text');

      wordCellList = wordEnter.merge(wordCellList);

      // 设置每个字符的class及位置
      wordCellList
        .attr("class", d => `word noselect word_${d.index}`)
        .attr('transform', (d, i) => `translate(${xScale(i) + 35}, 0)`);

      // 为每个字符绘制rect和text
      wordCellList.select('rect')
        .attr("y", 0)
        .attr("width", 30)
        .attr("height", 24);
      wordCellList.select('text')
        .text(d => d.text);

      // 设置字符缩放，以防有些英文单词过长
      wordCellList.select('text')
        .attr("transform", d => {
          const scaleX = (30 - 4) / d.length;
          const scaleY = 20 / d.height;
          const translate = `translate(15, 12.5)`;

          if (scaleX < 1 && scaleY < 1) {
            return `${translate}scale(${scaleX},${scaleY})`;
          } else if (scaleX < 1 && scaleY > 1) {
            return `${translate}scale(${scaleX},1)`;
          } else if (scaleX > 1 && scaleY > 1) {
            return `${translate}scale(1,${scaleY})`;
          } else {
            return translate;
          }
        });

      // 渲染滑动条
      this.renderBrush(brush, bottomBrush, xScale);
    },
    // 渲染brush
    renderBrush (brush, bottomBrush, xScale) {
      let moveBrush = false;

      const brushing = () => {
        const ev = d3.event;

        if (ev.sourceEvent && ev.sourceEvent.type === 'mousemove') {
          const rangeRaw = d3.event.selection.map(xScale.invert)
          const range = rangeRaw.map(d => Math.round(d));

          if (!moveBrush) {
            range[0] = Math.floor(rangeRaw[0]);
            range[1] = Math.round(rangeRaw[1]);
          }

          if (!this.sameRange(this.getSelectedRange, range)) {
            this.setSelectedRange(range);
          }

          d3.event.target.move(brush, range.map(xScale));

          if (this.getSelectedRange.length) {
            this.renderBottomBrush(bottomBrush, xScale);
          }
        }
      };

      const brushEnd = () => {
        const ev = d3.event;

        if (ev.sourceEvent && ev.sourceEvent.type === 'mouseup') {
          if (ev.type === 'end' && ev.selection === null) {
            this.setSelectedRange([]);
            this.setStateMatchData([]);
            this.renderBottomBrush(bottomBrush, xScale);
            this.setSignature("");
          }
        }
      };

      const brushStart = () => {
        const ev = d3.event;
        if (ev.selection) {
          moveBrush = ev.selection[0] !== ev.selection[1];
        }
      };

      const brushX = d3.brushX()
        .extent([[xScale.range()[0], 4], [xScale.range()[1], 20]])
        .on("start", brushStart)
        .on("brush", brushing)
        .on("end", brushEnd)

      brush.call(brushX);

      if (this.getSelectedRange.length > 0) {
        brushX.move(brush, this.getSelectedRange.map(xScale));
      }
      else {
        brushX.move(brush, [0, 0]);
      }

      this.renderBottomBrush(bottomBrush, xScale)
    },
    // 渲染严格小于brush
    renderBottomBrush (bottomBrush, xScale) {
      const dragging = () => {
        const ev = d3.event;
        const subject = ev.subject;

        let newBottomPos = Math.max(-1, Math.round(xScale.invert(ev.x + 3)))

        if (subject.handle === 'l') {
          if (newBottomPos > this.getSelectedRange[0]) {
            newBottomPos = this.getSelectedRange[0];
          }
          const diff0 = this.getSelectedRange[0] - newBottomPos;
          this.$set(this.bottomBrushSelection, 0, diff0);
        } else if (subject.handle === 'r') {
          if (newBottomPos < this.getSelectedRange[1]) {
            newBottomPos = this.getSelectedRange[1];
          }
          const diff1 = newBottomPos - this.getSelectedRange[1];
          this.$set(this.bottomBrushSelection, 1, diff1);
        }

        const newBottomX = xScale(newBottomPos) - 3;

        bottomBrush.selectAll(`.bottomBrushHandle.handle-${subject.handle}`)
          .attr("cx", newBottomX);

        const wisker = bottomBrush.selectAll(`.bottomBrushWisker.handle-${subject.handle}`);

        if (subject.handle === 'l') {
          wisker.attr("x1", newBottomX);
        }
        else {
          wisker.attr("x2", newBottomX);
        }
      }

      const dragEnd = () => {
        this.renderBottomBrush(bottomBrush, xScale);
      }


      if (this.bottomBrushSelection.length) {
        this.bottomBrushSelection = this.bottomBrushSelection;
      } else {
        this.bottomBrushSelection = [0, 0];
      }

      if (this.getSelectedRange.length) {
        const bbs = this.bottomBrushSelection;
        const ext = [
          { l: this.getSelectedRange[0] - bbs[0], r: this.getSelectedRange[0], handle: "l" },
          { l: this.getSelectedRange[1], r: this.getSelectedRange[1] + bbs[1], handle: "r" }
        ];

        const bottomBrushHandles = bottomBrush.selectAll(".bottomBrushHandle").data(ext, d => d.handle);
        bottomBrushHandles.exit().remove()
        bottomBrushHandles.enter().append("circle").attr("class", d => "bottomBrushDeco bottomBrushHandle handle-" + d.handle)
          .merge(bottomBrushHandles)
          .attr("cx", d => xScale(d[d.handle]))
          .attr("cy", 15)
          .attr("r", 5)
          .call(d3.drag()
            .on("drag", dragging)
            .on("end", dragEnd)
          );

        const bottomBrushWiskers = bottomBrush.selectAll(".bottomBrushWisker").data(ext);
        bottomBrushWiskers.exit().remove()
        bottomBrushWiskers.enter().append("line").attr("class", d => "bottomBrushDeco bottomBrushWisker handle-" + d.handle)
          .merge(bottomBrushWiskers)
          .attr("x1", d => xScale(d.l))
          .attr("x2", d => xScale(d.r))
          .attr("y1", 17)
          .attr("y2", 17);

        const signatureLineData = [
          [this.getSelectedRange[0], 17],
          [this.getSelectedRange[0], 3],
          [this.getSelectedRange[1], 3],
          [this.getSelectedRange[1], 17]
        ];
        const signatureLine = d3.line().x(d => xScale(d[0])).y(d => d[1]);

        const sl = bottomBrush.selectAll(".signatureLine").data([signatureLineData])
        sl.enter().append("path").attr("class", "bottomBrushDeco signatureLine")
          .merge(sl)
          .attr("d", signatureLine);
      } else {
        bottomBrush.selectAll(".bottomBrushDeco").remove();
      }
    },
    // y轴滑条滑动事件，设置threshold
    yAxisSliderDragging () {
      this.isChangingThreshold = true;
      const newThreshold = this.round(this.getClampedYScale().invert(d3.event.y - 120), 3);
      this.setThreshold(newThreshold);
    },
    yAxisSliderDragEnd () {
      this.isChangingThreshold = false;
    },
    // 折线生成器
    lineGenerator (xScale, yScale) {
      return d3.line()
        .x(d => xScale(+d.index))
        .y(d => yScale(+d.item));
    },
    // 设置所绘折线的透明度
    lineOpacity (lines) {
      return 1.0 / (Math.sqrt(lines.length) + 0.00001);
    },
    // 原始数据组装
    getJointData (data) {
      const dims = data[0].length;

      const jointData = [];
      for (let i = 0; i < dims; i++) {
        jointData.push({ dim: i, value: this.arrayColumn(data, i) });
      }

      return jointData;
    },
    // 原始文本组装，返回单个字符组合对象
    getJointWords (element, sentence) {
      const textArea = sentence.map((d, i) => {
        if (d == "￥") {
          return {
            text: "UNK",
            index: i,
            length: this.getTextLength(element, "UNK"),
            height: this.getTextHeight(element, "UNK")
          }
        }
        return {
          text: d,
          index: i,
          length: this.getTextLength(element, d),
          height: this.getTextHeight(element, d)
        }
      });

      return textArea;
    },
    // 获取二维数组的某一列数据，并返回编号和数据
    arrayColumn (array, column) {
      const array_column = [];
      for (let i = 0; i < array.length; i++) {
        array_column.push({
          index: i,
          item: array[i][column]
        });
      }
      return array_column;
    },
    // 获取每个字符长度
    getTextLength (element, text) {
      element.text(text);
      const length = element.node().getComputedTextLength();
      element.text('');
      return length;
    },
    // 获取每个字符高度
    getTextHeight (element, text) {
      element.text(text);
      const height = element.node().getBBox().height.toFixed(0);
      element.text('');
      return Number(height);
    },
    // 根据所显示文字长度确定xScale
    getXScale () {
      return d3.scaleLinear()
        .domain([0, this.getRange])
        .range([0, this.getRange * 30]);
    },
    // 根据日志数据的最大最小值确定yScale
    getYScale () {
      return d3.scaleLinear()
        .domain([this.getMinValue, this.getMaxValue])
        .range([250, 0]);
    },
    // 截断的yScale
    getClampedYScale () {
      return this.getYScale().copy().clamp(true);
    },
    // 四舍五入到最接近的整数
    round (number, precision) {
      const factor = Math.pow(10, precision);
      const tempNumber = number * factor;
      const roundedTempNumber = Math.round(tempNumber);

      return roundedTempNumber / factor;
    },
    // 统计选中文本index
    selectedRangeIndexs (start, end) {
      return [...new Array(end - start)].map((v, i) => i + start);
    },
    // 判断range是否相同
    sameRange (a, b) {
      return (a[0] === b[0]) && (a[1] === b[1]);
    },
    // 单元格点击事件
    cellClick (row, column, cell, event) {
      let startToEnd = this.getPos + this.getRightWordsLength;
      if (startToEnd < row.start_pos) {
        this.setPos(Number(startToEnd));
        const param = {
          run: this.getStateRun,
          tag: this.getStateTag,
          pos: this.getPos,
          range: this.getRange,
        }
        this.getHiddenStateData(param);
        this.$message.warning("已到达最右！");
      } else {
        this.setPos(Number(row.start_pos));
        const param = {
          run: this.getStateRun,
          tag: this.getStateTag,
          pos: this.getPos,
          range: this.getRange,
        }
        this.getHiddenStateData(param);
      }
    },
    // 设置匹配表格表头样式
    getRowClass ({ row, column, rowIndex, columnIndex }) {
      if (rowIndex === 0) {
        return 'color:#000;font-size:14px;font-weight:bold;'
      } else {
        return ''
      }
    },
    // 左移功能
    turnToleft () {
      if (this.getPos >= 5) {
        this.setPos(this.getPos - 5);
        this.pos = this.getPos;
        const param = {
          run: this.getStateRun,
          tag: this.getStateTag,
          pos: this.getPos,
          range: this.getRange,
        }
        this.getHiddenStateData(param);
      } else {
        this.$message.warning("已到达最左！");
      }
    },
    // 右移功能
    turnToRight () {
      if (this.getRightWordsLength >= 5) {
        this.setPos(this.getPos + 5);
        this.pos = this.getPos;
        const param = {
          run: this.getStateRun,
          tag: this.getStateTag,
          pos: this.getPos,
          range: this.getRange,
        }
        this.getHiddenStateData(param);
      } else if (this.getRightWordsLength > 0) {
        this.setPos(this.getPos + this.getRightWordsLength);
        this.pos = this.getPos;
        const param = {
          run: this.getStateRun,
          tag: this.getStateTag,
          pos: this.getPos,
          range: this.getRange,
        }
        this.getHiddenStateData(param);
      } else {
        this.$message.warning("已到达最右！");
      }
    }
  }
}
</script>

<style scoped lang="less">
.state-vis {
  font-size: 14px;
  margin: 0 5%;
}
/deep/ .title {
  display: flex;
  flex-direction: row;

  .square {
    width: 20px;
    height: 20px;
    border-radius: 5px;
    background: #625eb3;
    margin-right: 5px;
  }

  span {
    font-weight: bold;
    font-size: 20px;
    line-height: 20px;
    font-family: 'Times New Roman', Times, serif;
  }
}
/deep/ .header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin: 3% 0;

  .move-button-zrea {
    display: flex;
    flex-direction: row;
    margin-right: 8%;

    .move-left {
      flex-grow: 1;
      display: flex;
      align-items: center;

      img {
        margin-top: 5px;
        margin-bottom: 5px;
      }

      button {
        width: 50px;
        height: 30px;
        border: none;
        border-radius: 5px;
        background-color: #625eb3;
        color: white;
        font-size: 11px;
        flex: 0 0 60px;
      }
    }

    .move-right {
      flex-grow: 1;
      display: flex;
      align-items: center;
      margin-left: 30px;

      img {
        margin-top: 5px;
        margin-bottom: 5px;
      }

      button {
        width: 50px;
        height: 30px;
        border: none;
        border-radius: 5px;
        background-color: #625eb3;
        color: white;
        font-size: 11px;
        flex: 0 0 60px;
        margin-left: 5px;
      }
    }
  }
}

// 顶部折线样式区域
/deep/ .non-active {
  pointer-events: none;
}

/deep/ .slider-handle {
  fill: #625eb3;
}

/deep/ .state-vis-box .overlay .thresholdLine {
  stroke: #625eb3;
  stroke-width: 2;
  fill: none;
  stroke-dasharray: 10, 5;
}

/deep/ .state-vis-box .main .tickLine {
  stroke: #b5c3ff;
  stroke-width: 1;
  fill: none;
  stroke-dasharray: 2 2;
}

/deep/ .state-vis-box .valueLine {
  stroke: black;
  stroke-width: 1;
  fill: none;
}

/deep/ .state-vis-box .overlay .valueLine {
  stroke: #3399b2;
  stroke-width: 3;
}

/deep/ .state-vis-box .overlay .valueLine.hovered {
  stroke: red;
}

// 底部文本条样式
/deep/ .state-vis-axis .overlay .paddingLine {
  stroke: #333;
  stroke-width: 2;
}

/deep/ .state-vis-axis .textArea .word rect {
  fill: lightgray;
  stroke: none;
  opacity: 0.5;
  cursor: crosshair;
}

/deep/ .state-vis-axis .textArea .word.hovered rect {
  stroke: #ff4340;
  stroke-width: 2;
}

/deep/ .state-vis-axis .textArea .word.selected rect {
  stroke: #2d57b2;
  stroke-width: 3;
}

/deep/ .state-vis-axis .textArea .word text {
  pointer-events: none;
  dominant-baseline: central;
  text-anchor: middle;
}

/deep/ .state-vis-axis .brush .selection {
  stroke: white;
  border-radius: 5px;
  fill: #625eb3;
}

/deep/ .state-vis-axis .bottomBrush .bottomBrushWisker {
  stroke: gray;
}

/deep/ .state-vis-axis .bottomBrush .signatureLine {
  stroke: gray;
  fill: none;
}

/deep/ .state-vis-axis .bottomBrush .bottomBrushHandle {
  border-radius: 5px;
  fill: #625eb3;
}

/deep/ .row-divider-line {
  position: relative;
  width: 100%;
  height: 1px;
  margin: 3% 0;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: gainsboro;
}

/deep/ .match-content {
  margin-top: 3%;
  margin-left: 5%;
  margin-right: 5%;

  .match-result-label {
    font-weight: bold;
    font-size: 20px;
    line-height: 30px;
    font-family: 'Times New Roman', Times, serif;
    border: 2px solid gainsboro;
  }

  .match-content-table {
    margin-top: 3%;

    .el-table__header-wrapper {
      th {
        border-left: none;
        border-right: none;
      }
    }

    .el-table__body-wrapper {
      td {
        border-left: none;
        border-right: none;
      }
    }
  }
}

/deep/ .active-row {
  background: #cfd8ff;
}
</style>
