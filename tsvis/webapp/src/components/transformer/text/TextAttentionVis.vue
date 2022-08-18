<template>
  <div id="transformer-text-vis">
    <div class="attention-info">
      <div class="info-table">
        <attention-info :infoData="infoData"></attention-info>
      </div>

      <div class="column-divider-line"></div>

      <div class="info-bar-chart">
        <radial-bar-chart :statisticsData="infoData"></radial-bar-chart>
      </div>
    </div>

    <div class="row-divider-line"></div>

    <div class="attention-vis">
      <div class="title">
        <div class="square"></div>
        <span>AttentionVis</span>
        <span class="layer-head-select">
          <span class="select-label">Layer: </span>
          <select id="attention-select-layer" v-model="layer_selected"></select>
          <span class="select-label">Head: </span>
          <select id="attention-select-head" v-model="head_selected"></select>
          <span class="select-label" v-if="is_sentence_pair">Attention:
          </span>
          <select id="filter" v-if="is_sentence_pair">
            <option value="all">All</option>
            <option value="a2a">Sentence A -> Sentence A</option>
            <option value="a2b">Sentence A -> Sentence B</option>
            <option value="b2a">Sentence B -> Sentence A</option>
            <option value="b2b">Sentence B -> Sentence B</option>
          </select>
        </span>
      </div>
      <div id="vis"></div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import $ from "jquery";
import AttentionInfo from "./attentionInfo/AttentionInfo";
import RadialBarChart from "./attentionInfo/RadialBarChart";

import { createNamespacedHelpers } from "vuex";

const {
  mapGetters: mapTransformerGetters,
  mapMutations: mapTransformerMutations,
} = createNamespacedHelpers("transformer");

// 常量
const TEXTBOX_PADDING = 40;
const LEFT2RIGHT_WIDTH = 20;
const LEFT2RIGHT = 170;
const MATRIX_CELL_WIDTH = 20
const TEXTBOX_HEIGHT = 38;
const TEXT_SIZE = 15;
const TEXTBOXWIDTH = TEXT_SIZE * 8;
const TEXTBOXHEIGHT = 22;

const PALETTE = {
  dark: {
    attn: "#2994de",
    pos: "#2090dd",
    text: "#ccc",
    selected_text: "white",
    heading_text: "white",
    text_highlight_left: "#1b86cd",
    text_highlight_right: "#1b86cd",
    background: "black",
    text_color: "white"
  },
  light: {
    attn: "#625eb3",
    pos: "#0c36d8",
    text: "#202020",
    selected_text: "black",
    heading_text: "black",
    text_highlight_left: "#e5e5e5",
    text_highlight_right: "#478be8",
    background: "white",
    text_color: "black"
  },
};

// 全局参数
const config = {};

export default {
  components: {
    AttentionInfo,
    RadialBarChart
  },
  props: { allAttentionData: Object },
  data () {
    return {
      infoData: [],
      layer_selected: 0,
      head_selected: 0,
    };
  },
  computed: {
    ...mapTransformerGetters([
      "getSelectedLH",
      "getChartWidthScale",
      "getChartHeightScale"
    ]),
    is_sentence_pair: function () {
      if (this.allAttentionData) {
        if (this.allAttentionData.hasOwnProperty("attention")) {
          return Object.keys(this.allAttentionData["attention"]).length > 1
            ? true
            : false;
        }
      }
    },
  },
  created () {
    if (this.allAttentionData) {
      config.attention = this.allAttentionData["attention"]; // 后端数据中的attention数据
      config.filter = this.allAttentionData["default_filter"]; // 默认为all
      config.bidirectional = this.allAttentionData["bidirectional"]; // 是否是双向注意力
      config.displayMode = this.allAttentionData["displayMode"]; // 显示模式，分为dark和light
      config.layer = this.allAttentionData["layer"]; // 默认显示层
      config.head = this.allAttentionData["head"]; // 默认显示头

      let attentionFilter = config.attention[config.filter]; // 提取默认过滤器（all）的数据
      config.nLayers = attentionFilter["attn"].length; // 模型注意力层数
      config.nHeads = attentionFilter["attn"][0].length; // 每层头个数
      let leftLength = attentionFilter.left_text.length;
      let rightLength = attentionFilter.right_text.length;
      config.textLength = Math.max(leftLength, rightLength);

      this.getInfoData(config.attention[config.filter]);
    }
  },
  mounted () {
    this.$nextTick(function () {
      // 当layer select or head select or attention select发生变化时，重新渲染
      const layerSelect = $(".attention-vis #attention-select-layer");
      layerSelect.empty();
      for (let i = 0; i < config.nLayers; i++) {
        layerSelect.append($("<option />").val(i).text(i));
      }
      layerSelect.val(config.layer).change();
      layerSelect.on("change", (e) => {
        config.layer = +e.currentTarget.value;
        this.render();
      });

      const headSelect = $(".attention-vis #attention-select-head");
      headSelect.empty();
      for (let i = 0; i < config.nHeads; i++) {
        headSelect.append($("<option />").val(i).text(i));
      }
      headSelect.val(config.head).change();
      headSelect.on("change", (e) => {
        config.head = +e.currentTarget.value;
        this.render();
      });

      this.render();
    });
  },
  watch: {
    getSelectedLH (val) {
      let [layer, head] = val.split("-");
      this.layer_selected = Number(layer);
      this.head_selected = Number(head);
      config.layer = Number(layer);
      config.head = Number(head);
      this.render();
    },
    layer_selected (val) {
      let layer, head;
      if (val < 10) {
        layer = `0${val}`;
      } else {
        layer = String(val);
      }
      if (config.head < 10) {
        head = `0${config.head}`;
      } else {
        head = String(config.head);
      }
      this.setSelectedLH(`${layer}-${head}`);
    },
    head_selected (val) {
      let layer, head;
      if (val < 10) {
        head = `0${val}`;
      } else {
        head = String(val);
      }
      if (config.layer < 10) {
        layer = `0${config.layer}`;
      } else {
        layer = String(config.layer);
      }
      this.setSelectedLH(`${layer}-${head}`);
    }
  },
  methods: {
    ...mapTransformerMutations([
      "setSelectedLH",
    ]),
    render () {
      if (config.attention) {
        let filterData = config.attention[config.filter];
        let leftText = filterData.left_text;
        let rightText = filterData.right_text;

        $("#transformer-text-vis #vis").empty();

        let width = TEXTBOXWIDTH * 2 + LEFT2RIGHT + 60;
        let height = config.textLength * TEXTBOXHEIGHT + TEXTBOX_PADDING;
        let svg = d3
          .select("#transformer-text-vis #vis")
          .append("svg")
          .attr("width", "50%")
          .attr("height", "100%")
          .attr('preserveAspectRatio', 'xMidYMid meet')
          .attr('viewBox', `0 0 ${width * 1.1} ${height * 1.1}`);

        let attentionLines = svg.append("g")
          .attr('width', width)
          .attr('height', height)
          .attr("class", "attention-lines")
          .attr("display", "flex");

        d3.select("#transformer-text-vis").style(
          "background-color",
          this.getColor("background")
        );
        d3.selectAll("#transformer-text-vis .select-label").style(
          "color",
          this.getColor("text_color")
        );

        let posLeftText = 0;
        let posAttention = posLeftText + TEXTBOXWIDTH;
        let posRightText = posAttention + LEFT2RIGHT + LEFT2RIGHT_WIDTH;

        this.renderText(attentionLines, leftText, "leftText", posLeftText);
        this.renderAttentionLines(attentionLines, posAttention, posRightText);
        this.renderText(attentionLines, rightText, "rightText", posRightText);

        svg = d3.select("#transformer-text-vis #vis")
          .append("svg")
          .attr("width", "50%")

        this.renderMatrix(svg, filterData);

        let line_height = document.getElementsByClassName("attention-lines")[0].attributes.height.value;

        svg.append("g")
          .append("line")
          .style("stroke", "gainsboro")
          .style("stroke-width", 2 + "px")
          .attr("x1", 0)
          .attr("y1", 0)
          .attr("x2", 0)
          .attr("y2", line_height * 1.4);
      }
    },
    renderText (svg, text, id, leftPos) {
      let wordContainer = svg
        .append("svg:g")
        .attr("id", id)
        .selectAll("g")
        .data(text)
        .enter()
        .append("g");

      if (id == "leftText" || id == "rightText") {
        let fillColor;
        if (id == "leftText") {
          fillColor = this.getColor("text_highlight_left");
        }
        if (id == "rightText") {
          fillColor = this.getColor("text_highlight_right");
        }

        // 为每个字符添加rect
        wordContainer
          .append("rect")
          .classed("highlight", true)
          .attr("fill", fillColor)
          .style("opacity", 0.0)
          .attr("height", TEXTBOXHEIGHT)
          .attr("width", TEXTBOXWIDTH)
          .attr("x", leftPos)
          .attr("y", function (d, i) {
            return i * TEXTBOXHEIGHT + TEXTBOX_HEIGHT - 1;
          });
      }

      let offset;
      if (id == "leftText") {
        offset = -8;
      } else {
        offset = 8;
      }

      // 为每个字符添加text
      let textContainer = wordContainer
        .append("text")
        .classed("token", true)
        .text(function (d) {
          return d;
        })
        .attr("font-size", TEXT_SIZE + "px")
        .style("fill", this.getColor("text"))
        .style("cursor", "default")
        .style("-webkit-user-select", "none")
        .attr("x", leftPos + offset)
        .attr("y", function (d, i) {
          return i * TEXTBOXHEIGHT + TEXTBOX_HEIGHT;
        })
        .attr("height", TEXTBOXHEIGHT)
        .attr("width", TEXTBOXWIDTH)
        .attr("dy", TEXT_SIZE);

      if (id == "leftText") {
        // 为左边的字符添加动态触碰效果
        textContainer.style("text-anchor", "end").attr("dx", TEXTBOXWIDTH - 2);
        wordContainer.on("mouseover", (d, index) => {
          config.index = index;
          this.highlightSelection(svg, index);
        });
        wordContainer.on("mouseleave", () => {
          config.index = null;
          this.unhighlightSelection(svg);
        });
      }
    },
    renderAttentionLines (svg, start_pos, end_pos) {
      // 选择头发生变化时，获取对应数据进行渲染
      let attentionMatrix =
        config.attention[config.filter].attn[config.layer][config.head];
      let attentionContainer = svg.append("svg:g");
      attentionContainer
        .selectAll("g")
        .data(attentionMatrix)
        .enter()
        .append("g")
        .classed("attention-line-group", true)
        .attr("source-index", function (d, i) {
          return i;
        })
        .selectAll("line")
        .data(function (d) {
          return d;
        })
        .enter()
        .append("line")
        .attr("x1", start_pos)
        .attr("y1", function (d) {
          let sourceIndex = +this.parentNode.getAttribute("source-index");
          return sourceIndex * TEXTBOXHEIGHT + TEXTBOX_HEIGHT + TEXTBOXHEIGHT / 2;
        })
        .attr("x2", end_pos)
        .attr("y2", function (d, targetIndex) {
          return targetIndex * TEXTBOXHEIGHT + TEXTBOX_HEIGHT + TEXTBOXHEIGHT / 2;
        })
        .attr("stroke-width", 2)
        .attr("stroke", this.getColor("attn"))
        .attr("stroke-opacity", function (d) {
          return d;
        });
    },
    renderMatrix (svg, filterData) {
      let xAxisBox = svg.append("g");
      let yAxisBox = svg.append("g");
      let gradientColorBar = svg.append("g");
      let matrixData = filterData["attn"][config.layer][config.head];
      let axisData = filterData["left_text"];
      let axisSpace = [];
      let maxAttn = this.getMax(filterData["attn"]);
      let minAttn = this.getMin(filterData["attn"]);

      let axisMaxLength = 0;
      axisData.forEach((data) => {
        if (data.length > axisMaxLength) {
          axisMaxLength = data.length;
        }
      })
      let xAxisHeight = axisMaxLength * 7.5;
      let yAxisWidth = axisMaxLength * 8;

      for (let i = 0; i < axisData.length; i++) {
        axisSpace.push(i * MATRIX_CELL_WIDTH);
      }
      let xScale = d3
        .scaleOrdinal()
        .domain(d3.range(0, axisData.length))
        .range(axisSpace);

      let xAxis = d3
        .axisTop()
        .scale(xScale)
        .tickFormat(function (d) {
          return axisData[d];
        });
      xAxisBox
        .attr(
          "transform",
          `translate(${yAxisWidth + (MATRIX_CELL_WIDTH - 2) / 2 + 80},${xAxisHeight})`
        )
        .call(xAxis)
        .selectAll("text")
        .attr("fill", "#000")
        .style("font-size", "12")
        .style("font-weight", "500")
        .style("text-anchor", "start")
        .attr("dx", "0.7em")
        .attr("dy", "0.4em")
        .attr("transform", "rotate(-65)");

      axisData = filterData["right_text"];
      axisSpace = [];
      for (let i = 0; i < axisData.length; i++) {
        axisSpace.push(i * MATRIX_CELL_WIDTH);
      }
      let yScale = d3
        .scaleOrdinal()
        .domain(d3.range(0, axisData.length))
        .range(axisSpace);
      let yAxis = d3
        .axisLeft()
        .scale(yScale)
        .tickFormat(function (d) {
          return axisData[d];
        });
      yAxisBox
        .attr(
          "transform",
          `translate(${yAxisWidth + 80},${xAxisHeight + (MATRIX_CELL_WIDTH - 2) / 2})`
        )
        .call(yAxis)
        .selectAll("text")
        .attr("fill", "#000")
        .style("font-size", "12")
        .style("font-weight", "500");
      d3.select("body").selectAll(".domain").remove();

      for (let i = 0; i < matrixData.length; i++) {
        for (let j = 0; j < matrixData[0].length; j++) {
          let fill = this.getMatrixColor(matrixData[i][j], maxAttn, minAttn);
          svg
            .append("g")
            .append("rect")
            .attr("width", MATRIX_CELL_WIDTH - 2 + "px")
            .attr("height", MATRIX_CELL_WIDTH - 2 + "px")
            .attr("fill", "#" + fill)
            .attr("x", yAxisWidth + j * MATRIX_CELL_WIDTH + "px")
            .attr("y", xAxisHeight + i * MATRIX_CELL_WIDTH + "px")
            .attr("id", `attention_${i}_${j}`)
            .attr("transform", `translate(80, 0)`)
        }
      }

      gradientColorBar
        .append("text")
        .text(maxAttn.toFixed(4))
        .attr("x", yAxisWidth + matrixData[0].length * MATRIX_CELL_WIDTH + 5)
        .attr("y", xAxisHeight + (matrixData[0].length * MATRIX_CELL_WIDTH - 100) / 2 - 5)
        .attr("transform", `translate(80, 0)`)
        .style("font-size", "12");
      let linear = d3.scaleLinear().domain([0, 100]).range([0, 1]);
      let compute = d3.interpolate("#3E39A3", "#DAE1FF");
      gradientColorBar
        .selectAll("rect")
        .data(d3.range(100))
        .enter()
        .append("rect")
        .attr("x", yAxisWidth + matrixData[0].length * MATRIX_CELL_WIDTH + 20)
        .attr("y", (d, i) => i + xAxisHeight + (matrixData[0].length * MATRIX_CELL_WIDTH - 100) / 2)
        .attr("width", 10)
        .attr("height", 10)
        .attr("transform", `translate(80, 0)`)
        .style("fill", (d, i) => compute(linear(d)));
      gradientColorBar
        .append("text")
        .text(minAttn.toFixed(4))
        .attr("x", yAxisWidth + matrixData[0].length * MATRIX_CELL_WIDTH + 5)
        .attr("y", xAxisHeight + (matrixData[0].length * MATRIX_CELL_WIDTH + 100) / 2 + 23)
        .attr("transform", `translate(80, 0)`)
        .style("font-size", "12");

      let width = yAxisWidth + matrixData[0].length * MATRIX_CELL_WIDTH + 50;
      let height = xAxisHeight + matrixData[0].length * MATRIX_CELL_WIDTH;

      svg.attr('preserveAspectRatio', 'xMidYMid meet')
        .attr('viewBox', `0 0 ${width * 1.5} ${height * 1.5}`);
    },
    highlightSelection (svg, index) {
      svg
        .select("#leftText")
        .selectAll(".highlight")
        .style("opacity", function (d, i) {
          return i == index ? 1.0 : 0.0;
        });
      svg
        .select("#leftText")
        .selectAll(".token")
        .style("fill", (d, i) => {
          return i == index
            ? this.getColor("selected_text")
            : this.getColor("text");
        });
      svg
        .select("#leftText")
        .selectAll(".plus-sign")
        .style("opacity", function (d, i) {
          return i == index ? 1.0 : 0.0;
        });
      svg.selectAll(".i-index").text(index);
      svg.selectAll(".attention-line-group").style("opacity", function (d, i) {
        return i == index ? 1.0 : 0.0;
      });
    },
    unhighlightSelection (svg) {
      svg.select("#leftText").selectAll(".highlight").style("opacity", 0.0);
      svg
        .select("#leftText")
        .selectAll(".token")
        .style("fill", this.getColor("text"));
      svg.select("#leftText").selectAll(".minus-sign").style("opacity", 0);
      svg.select("#leftText").selectAll(".plus-sign").style("opacity", 0);
      svg.selectAll(".i-index").text("i");
      svg.selectAll(".attention-line-group").style("opacity", 1);
    },
    getColor (name) {
      return PALETTE[config.displayMode][name];
    },
    getMatrixColor (score, max, min) {
      let scale = (score - min) / (max - min);
      let red = parseInt(scale * (62 - 218) + 218).toString(16);
      let green = parseInt(scale * (57 - 224) + 225).toString(16);
      let blue = parseInt(scale * (163 - 255) + 255).toString(16);
      return String(red) + String(green) + String(blue);
    },
    getInfoData (data) {
      if (Object.keys(data).length !== 0) {
        const layers = data['attn'].length;
        const heads = data['attn'][0].length;
        const textLength = data['left_text'].length;

        for (let i = 0; i < layers; i++) {
          for (let j = 0; j < heads; j++) {
            let headScoreMatrix = [].concat.apply([], data['attn'][i][j]);
            headScoreMatrix.sort((a, b) => a - b);
            let len = headScoreMatrix.length;

            // 单个头，注意力矩阵的最大值
            let max = headScoreMatrix[len - 1].toFixed(5);
            // 单个头，注意力矩阵的最小值
            let min = headScoreMatrix[0].toFixed(5);
            // 单个头，注意力矩阵的平均值，用于计算方差和离散系数
            let sum = headScoreMatrix.reduce((pre, cur) => pre + cur, 0).toFixed(5);
            let avg = (sum / (textLength) ** 2).toFixed(5);

            // 单个头，注意力矩阵的方差
            let vari = headScoreMatrix.reduce((pre, cur) => {
              return pre + Math.abs(cur - avg) ** 2;
            }, 0) / len;
            vari = vari.toFixed(5);

            // 单个头，注意力矩阵的四分位差
            let quartile = (headScoreMatrix[Math.floor(len / 4 * 3)] - headScoreMatrix[Math.floor(len / 4)]).toFixed(5);

            let head = '';
            if (i > 9) {
              if (j > 9) {
                head = i.toString() + '-' + j.toString();
              } else {
                head = i.toString() + '-' + '0' + j.toString();
              }
            } else {
              if (j > 9) {
                head = '0' + i.toString() + '-' + j.toString();
              } else {
                head = '0' + i.toString() + '-' + '0' + j.toString();
              }
            }
            let param = {
              'head': head,
              'max': max,
              'min': min,
              'quar': quartile,
              'vari': vari
            }

            this.infoData.push(param);
          }
        }
      }
    },
    //获取二维数组最大值
    getMax (arr) {
      let ta = arr.join(",").split(",")
      return Math.max.apply(null, ta)
    },
    //获取二维数组最小值
    getMin (arr) {
      let ta = arr.join(",").split(",")
      return Math.min.apply(null, ta)
    }
  },
};
</script>
<style lang="less" scoped>
/deep/ .title {
  margin-bottom: 20px;
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

/deep/ .attention-info {
  height: 50%;
  display: flex;
  flex-direction: row;
  margin-top: 3%;
  margin-left: 5%;
  margin-right: 5%;
  margin-bottom: 2%;

  justify-content: start;

  .info-table {
    width: 50%;
    margin-right: 3%;
  }

  .column-divider-line {
    border-right: 1px solid gainsboro;
  }

  .info-bar-chart {
    width: 50%;
    margin-left: 3%;
  }
}

/deep/ .row-divider-line {
  position: relative;
  width: 90%;
  height: 1px;
  margin: auto;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: gainsboro;
}

/deep/ .attention-vis {
  margin-top: 5%;
  margin-left: 5%;
  margin-right: 5%;
  span {
    user-select: none;
  }

  .layer-head-select {
    margin-left: 20px;

    .select-label {
      font-size: 16px;
      color: black;
      margin-left: 20px;
    }
  }

  #vis {
    display: flex;
    flex-direction: row;
  }
}
</style>