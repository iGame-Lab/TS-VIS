<template>
  <div class="radial-bar-chart">
    <div class="title">
      <div class="square"></div>
      <span>统计信息图</span>
    </div>
    <div class="filter">
      <el-select v-model="metric_value" placeholder="过滤标准" class="selection"
        size="small" style="display:block">
        <el-option v-for="item in metrics" :key="item.value" :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>

      <el-select v-model="tag_value" placeholder="过滤符号" class="selection"
        size="small" style="display:block">
        <el-option v-for="item in tags" :key="item.value" :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>

      <el-input v-model="input" placeholder="过滤值" clearable
        class="selection-input" size="small" style="display:block">
      </el-input>

      <button class="filter-button"
        @click="filter(metric_value, tag_value, input, data)">过滤
      </button>
    </div>
    <div class="chart"></div>
  </div>
</template>

<script>
import { createNamespacedHelpers } from "vuex";

const {
  mapGetters: mapTransformerGetters,
  mapActions: mapTransformerActions,
  mapMutations: mapTransformerMutations,
} = createNamespacedHelpers("transformer");
import * as d3 from "d3";
import $ from "jquery";
import StrategyMap from "./strategies";
export default {
  name: 'RadialBarChart',
  components: {},
  props: {
    statisticsData: Array
  },
  data () {
    return {
      data: [],
      metric_value: '',
      tag_value: '',
      metrics: [
        { value: 'Max', label: 'Max' },
        { value: 'Min', label: 'Min' },
        { value: 'Quar', label: 'Quar' },
        { value: 'Vari', label: 'Vari' },
      ],
      tags: [
        { value: '<', label: '<' },
        { value: '<=', label: '<=' },
        { value: '>=', label: '>=' },
        { value: '>', label: '>' },
      ],
      input: '',
      screenHeight: 0,
      screenWidth: 0,
    }
  },
  computed: {
    ...mapTransformerGetters([
      "getAttentionLayers",
      "getSelectedLH",
      "getChartWidthScale",
      "getChartHeightScale"
    ])
  },
  watch: {
    getChartWidthScale (val) {
      this.drawRadialBar(this.data);
    },
    getChartHeightScale (val) {
      this.drawRadialBar(this.data)
    },
  },
  created () {
    this.$nextTick(() => {
      this.data = [...this.statisticsData]
    })
  },
  mounted () {
    this.screenHeight = window.innerHeight;
    this.screenWidth = window.innerWidth;
    this.$nextTick(function () {
      this.drawRadialBar(this.data);
    })
  },
  updated () {
    window.onresize = () => {
      return (() => {
        this.screenHeight = window.innerHeight;
        this.screenWidth = window.innerWidth;
      })();
    };
  },
  methods: {
    ...mapTransformerMutations([
      'setAttentionInfoData',
      'setSelectedLH',
    ]),
    filter (metric, tag, number, data) {
      let filtered_data = StrategyMap[metric](tag, number, data);

      this.drawRadialBar(filtered_data);
    },
    drawRadialBar (data) {
      let that = this;

      $(".chart").empty();

      if (data.length !== 0) {
        let width, height;
        if (this.getChartWidthScale == 1 && this.getChartHeightScale == 1) {
          width = this.screenWidth * 0.25;
          height = this.screenHeight * 0.6;
        } else {
          width = 350 * this.getChartWidthScale * 0.8;
          height = 350 * this.getChartHeightScale * 0.8;
        }
        let svg = d3
          .select(".chart")
          .append("svg")
          .attr("class", "bar-chart")
          .attr("width", width + "px")
          .attr("height", height + "px");

        let innerRadius = width / 2 * 0.3;
        let outerRadius = width / 2 * 0.75;

        let variMax = d3.max(this.data, d => d.vari);
        let variMin = d3.min(this.data, d => d.vari);

        let interpolator = d3.interpolate(variMin, variMax);
        let colorDomain = d3.quantize(interpolator, 3);
        let color = d3.scaleLinear(
          colorDomain,
          ["#DAE1FF", "#6584FF", "#6D0094"]
        );

        let layers = this.getAttentionLayers;
        layers = this.moveElementLeft(layers, -3)

        let xScale = d3.scaleBand(
          this.data.map(d => d.head),
          [0, 2 * Math.PI]
        );

        let yMax = d3.max(this.data, d => d.max);
        let yMin = d3.min(this.data, d => d.min);

        let yScale = d3.scaleLinear()
          .domain([yMin, yMax])
          .range([innerRadius, outerRadius]);

        let arc = d3.arc()
          .innerRadius(d => yScale(d.min))
          .outerRadius(d => yScale(d.max))
          .startAngle(d => xScale(d.head))
          .endAngle(d => xScale(d.head) + xScale.bandwidth())
          .padAngle(0.05)
          .padRadius(innerRadius);

        let xAxis = g => g
          .attr('text-anchor', 'middle')
          .call(g => g.selectAll('g')
            .data(layers)
            .join('g')
            .attr('transform', (d, i, arr) => `
          rotate(${i * 360 / arr.length})
          translate(${innerRadius},0)
        `)
            .call(g => g.append('line')
              .attr('x1', -5)
              .attr('x2', outerRadius - innerRadius + 10)
              .style('stroke', '#aaa'))
            .call(g => g.append('text')
              .attr('transform', (d, i, arr) => ((i * 360 / arr.length) % 360 > 180
                ? "rotate(90)translate(0,16)"
                : "rotate(-90)translate(0,-9)"))
              .style('font-family', 'sans-serif')
              .style('font-size', 10)
              .text(d => d)));

        let yAxis = g => g
          .attr('text-anchor', 'middle')
          .call(g => g.append('text')
            .attr('text-anchor', 'end')
            .attr('x', '-0.5em')
            .attr('y', d => -yScale(yScale.ticks(5).pop()) - 10)
            .attr('dy', '-1em')
            .style('fill', '#1a1a1a')
          )
          .call(g => g.selectAll('g')
            .data(yScale.ticks(5))
            .join('g')
            .attr('fill', 'none')
            .call(g => g.append('circle')
              .style('stroke', '#aaa')
              .style('stroke-opacity', 0.5)
              .attr('r', yScale))
            .call(g => g.append('text')
              .attr('y', d => -yScale(d))
              .attr('dy', '0.35em')
              .style('stroke', '#fff')
              .style('stroke-width', 5)
              .style("fill", '#1a1a1a')
              .text(yScale.tickFormat(6, 's'))
              .clone(true)
              .style('stroke', 'none')));

        let Tooltip = d3.select(".chart")
          .append("div")
          .style("position", "absolute")
          .attr("class", "tooltip")
          .style("background-color", "white")
          .style("border", "solid")
          .style("border-width", "2px")
          .style("border-radius", "5px")
          .style("padding", "5px")
          .style("opacity", 0);

        let mouseover = function (d) {
          Tooltip
            .style("opacity", 1)
          d3.select(this)
            .style("stroke", "black")
            .style("opacity", 1)
        };

        let mousemove = function (d) {
          let param = [d.head, d.max, d.min, d.quar, d.vari];
          that.setAttentionInfoData(param);
          Tooltip
            .html(function () {
              let headInfo = 'Head: ' + d.head + '<br />' +
                'Max: ' + d.max + '<br />' +
                'Min: ' + d.min + '<br />' +
                'Quar: ' + d.quar + '<br />' +
                'Vari: ' + d.vari
              return headInfo;
            })
            .style("left", (d3.event.pageX - 120) + "px")
            .style("top", (d3.event.pageY - 100) + "px")
        };

        let mouseleave = function (d) {
          that.setAttentionInfoData([]);
          Tooltip
            .style("opacity", 0)
          d3.select(this)
            .style("stroke", "none")
            .style("opacity", 0.8)
        };

        let mouseclick = function (d) {
          that.setSelectedLH(d.head);
        }

        const container = svg.append('g')
          .attr('class', 'container')
          .attr('transform', `translate(${width / 2},${height / 2})`)
          .style('font-size', 10)
          .style('font-family', 'sans-serif');

        container
          .selectAll('path')
          .data(data)
          .join('path')
          .style('fill', d => color(d.vari))
          .style('stroke', d => color(d.vari))
          .attr('d', arc)
          .on("mouseover", mouseover)
          .on("mousemove", mousemove)
          .on("mouseleave", mouseleave)
          .on("click", mouseclick);

        container.append('g')
          .call(xAxis);

        container.append('g')
          .call(yAxis);

        const defs = svg.append("defs");

        const top_text = svg
          .append("text")
          .text(variMin)
          .attr("x", 0)
          .attr("y", "28%")
          .style("font-size", "12");

        const bottom_text = svg
          .append("text")
          .text(variMax)
          .attr("x", 0)
          .attr("y", "64%")
          .style("font-size", "12");

        const linearGradient = defs
          .append("linearGradient")
          .attr("id", "gradient")
          .attr('x1', '0%')
          .attr('x2', '0%')
          .attr('y1', '0%')
          .attr('y2', '100%');

        linearGradient
          .append("stop")
          .attr("offset", "0%")
          .attr("stop-color", color(variMin));
        linearGradient
          .append("stop")
          .attr("offset", "50%")
          .attr("stop-color", color((variMax - variMin) / 2))
        linearGradient
          .append("stop")
          .attr("offset", "100%")
          .attr("stop-color", color(variMax));

        let defsWidth = 10 * this.getChartWidthScale;
        let defsHeight = height * 0.3;

        const rect = svg //插入rect
          .append("rect")
          .attr("x", "2%")
          .attr("y", "30%")
          .attr("height", defsHeight)
          .attr("width", defsWidth)
          .style("fill", "url('#gradient')");//用linearGradient填充矩形
      }
    },
    moveElementLeft (arr, n) {
      if (Math.abs(n) > arr.length) n = n % arr.length
      return arr.slice(-n).concat(arr.slice(0, -n))
    }
  }
}
</script>

<style scoped lang="less">
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

.filter {
  display: flex;
  flex-direction: row;

  text-align: center;
  align-items: center;
  display: -webkit-flex;
  height: 40px;

  .selection {
    width: 25%;
    margin: 2% 2% 2% 0;
  }

  /deep/ .el-input__inner {
    font-size: 14px;
    text-align: center;
    border: #fff;
    box-shadow: 0 0 5px 0 rgba(143, 143, 180, 0.24);
  }

  .selection-input {
    width: 25%;
    margin: 2% 2% 2% 0;
  }

  .filter-button {
    width: 15%;
    height: 90%;
    vertical-align: middle;
    background-color: #7f7cc0;
    border: none;
    border-radius: 5px;
    color: white;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 14px;
  }
}
</style>
