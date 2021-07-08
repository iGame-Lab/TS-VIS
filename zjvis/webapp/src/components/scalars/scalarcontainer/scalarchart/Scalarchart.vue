<!--
 * @Descripttion: loss
 * @version: 1.0
 * @Author: xds
 * @Date: 2020-04-24 15:23:44
 * @LastEditors: xds
 * @LastEditTime: 2020-05-04 21:12:44
 -->
 <style lang="less" scoped>
   .chart{
     height:100%;
     width:100%;
     background-color: white;
     position: relative;
   }
   .tooltip{
     background-color:rgba(0, 73, 134);
     border-radius:5px;
     position:absolute;
     padding:5px;
     visibility:hidden;
     margin-left: 5%;
     margin-right: 5%;
     width:90%;
     bottom:5%;
     color:white;
   }
   .font1{
     font-size: 30px;
   }
   .font2{
     font-size: 10px;
   }
   table{
     width:100%;
   }
   td{
     text-align:center;
   }
   .td1{
     width: 40%;
   }
   .td2{
     width: 20%;
   }
 </style>
<template>
  <div :id="classname" class="chart">
    <div :class="['tooltip',scaleLargeSmall?'font1':'font2']" :scale="scaleLargeSmall">
      <table>
        <tr>
          <td class="td1">wall_time</td>
          <td class="td2">step</td>
          <td class="td1">value</td>
        </tr>
        <tr>
          <td :id="'td1'+ classname" class="td1" />
          <td :id="'td2'+ classname" class="td2" />
          <td :id="'td3'+ classname" class="td1" />
        </tr>
      </table>
    </div>
  </div>

</template>
<script>

import * as d3 from 'd3'
import { createNamespacedHelpers } from 'vuex'
const { mapMutations: mapScalarMutations, mapGetters: mapScalarGetters } = createNamespacedHelpers('scalar')
const { mapMutations: mapCustomMutations } = createNamespacedHelpers('custom')

export default {

  props: {
    chartdata: Object,
    start: Boolean,
    end: Boolean,
    ytext: String,
    scaleLargeSmall: Boolean,
    classname: String,
    isaddmain: Boolean,
    title: String
  },
  data() {
    return {
      data: [],
      yname: [],
      mergeddata: [],
      mergeddata0: [],
      mergeddata1: [],
      mergetype: '',
      yname0: [],
      yname1: [],
      legendnumber: 0,
      drawnumber: 0,
      thisid: '',
      customcontent: {}
    }
  },
  computed: {
    ...mapScalarGetters([
      'smoothvalue', 'yaxis', 'mergeditem', 'checkedorder', 'freshnumber', 'grade'
    ])
  },
  watch: {
    freshnumber: function(val) {
      if (this.mergetype === '') {
        d3.select('#svg' + this.classname).remove()
        this.SvgDraw()
      }
    },
    isaddmain: function(val) {
      if (val) {
        if (this.mergetype === 'single') {
          this.thisid = ''
          for (let i = 0; i < this.mergeddata.length; i++) {
            this.thisid = this.thisid + this.mergeddata[i].run + this.mergeddata[i].tag
          }
          this.customcontent = { 'title': this.title, 'mergetype': this.mergetype, 'legendnumber': this.legendnumber, 'value': this.mergeddata }
          this.setScalar([this.thisid, this.customcontent])
        } else if (this.mergetype === 'double') {
          this.thisid = ''
          for (let i = 0; i < this.mergeddata0.length; i++) {
            this.thisid = this.thisid + this.mergeddata0[i].run + this.mergeddata0[i].tag
          }
          for (let i = 0; i < this.mergeddata1.length; i++) {
            this.thisid = this.thisid + this.mergeddata1[i].run + this.mergeddata1[i].tag
          }
          this.customcontent = { 'title': this.title, 'mergetype': this.mergetype, 'legendnumber': this.legendnumber, 'value0': this.mergeddata0, 'value1': this.mergeddata1 }
          this.setScalar([this.thisid, this.customcontent])
        }
      } else {
        this.deleteScalar(this.thisid)
      }
    },
    smoothvalue: function() {
      if (this.grade[this.classname] === 'main') {
        if (this.mergetype === 'single') {
          d3.select('#svg' + this.classname).remove()
          this.MergeSvgDraw()
        } else if (this.mergetype === 'double') {
          d3.select('#svg' + this.classname).remove()
          this.DYMergeSvgDraw()
        }
      } else {
        d3.select('#svg' + this.classname).remove()
        this.SvgDraw()
      }
    },
    yaxis: function() {
      if (this.grade[this.classname] === 'main') {
        if (this.mergetype === 'single') {
          d3.select('#svg' + this.classname).remove()
          this.MergeSvgDraw()
        } else if (this.mergetype === 'double') {
          d3.select('#svg' + this.classname).remove()
          this.DYMergeSvgDraw()
        }
      } else {
        d3.select('#svg' + this.classname).remove()
        this.SvgDraw()
      }
    },
    start: function(val) {
      if (val) {
        if (Object.keys(this.mergeditem[this.classname]).length === 1) {
          this.mergetype = 'single'
          this.legendnumber = this.checkedorder.length
          this.mergeddata = [].concat(this.mergeditem[this.classname][Object.keys(this.mergeditem[this.classname])[0]])
          d3.select('#svg' + this.classname).remove()
          this.MergeSvgDraw()
        } else if (Object.keys(this.mergeditem[this.classname]).length === 2) {
          this.mergetype = 'double'
          this.legendnumber = this.checkedorder.length
          this.mergeddata0 = [].concat(this.mergeditem[this.classname][Object.keys(this.mergeditem[this.classname])[0]])
          this.mergeddata1 = [].concat(this.mergeditem[this.classname][Object.keys(this.mergeditem[this.classname])[1]])
          d3.select('#svg' + this.classname).remove()
          this.yname0[0] = Object.keys(this.mergeditem[this.classname])[0]
          this.yname0[1] = 'log(' + this.yname0[0] + ')'
          this.yname1[0] = Object.keys(this.mergeditem[this.classname])[1]
          this.yname1[1] = 'log(' + this.yname1[0] + ')'
          this.DYMergeSvgDraw()
        }
        this.setmergestep()
      }
    },
    end: function(val) {
      if (val) {
        this.deleteScalar(this.thisid)
        this.mergeddata = []
        this.mergeddata0 = []
        this.mergeddata1 = []
        this.mergetype = ''
        this.yname0 = []
        this.yname1 = []
        this.data = this.chartdata.value[Object.keys(this.chartdata.value)[0]]
        this.yname[0] = this.ytext
        this.yname[1] = 'log(' + this.ytext + ')'
        d3.select('#svg' + this.classname).remove()
        this.SvgDraw()
      }
    }
  },
  created() {
    if (this.grade[this.classname] === 'main') {
      if (Object.keys(this.mergeditem[this.classname]).length === 1) {
        this.mergetype = 'single'
        this.mergeddata = [].concat(this.mergeditem[this.classname][Object.keys(this.mergeditem[this.classname])[0]])
        this.legendnumber = this.mergeddata.length
        this.MergeSvgDraw()
      } else if (Object.keys(this.mergeditem[this.classname]).length === 2) {
        this.mergetype = 'double'
        this.mergeddata0 = [].concat(this.mergeditem[this.classname][Object.keys(this.mergeditem[this.classname])[0]])
        this.mergeddata1 = [].concat(this.mergeditem[this.classname][Object.keys(this.mergeditem[this.classname])[1]])
        this.legendnumber = this.mergeddata0.length + this.mergeddata1.length
        this.yname0[0] = Object.keys(this.mergeditem[this.classname])[0]
        this.yname0[1] = 'log(' + this.yname0[0] + ')'
        this.yname1[0] = Object.keys(this.mergeditem[this.classname])[1]
        this.yname1[1] = 'log(' + this.yname1[0] + ')'
        this.DYMergeSvgDraw()
      }
    } else {
      if (Object.keys(this.chartdata).length === 2) {
        this.data = this.chartdata.value[Object.keys(this.chartdata.value)[0]]
        this.yname[0] = this.ytext
        this.yname[1] = 'log(' + this.ytext + ')'
      } else if (Object.keys(this.chartdata).length === 4) {
        this.mergetype = 'single'
        this.legendnumber = this.chartdata.legendnumber
        this.mergeddata = this.chartdata.value
      } else if (Object.keys(this.chartdata).length === 5) {
        this.mergetype = 'double'
        this.legendnumber = this.chartdata.legendnumber
        this.mergeddata0 = this.chartdata.value0
        this.mergeddata1 = this.chartdata.value1
        const arr0 = this.mergeddata0[0].tag.split('/')
        const arr1 = this.mergeddata1[0].tag.split('/')
        this.yname0[0] = arr0[arr0.length - 1]
        this.yname0[1] = 'log(' + this.yname0[0] + ')'
        this.yname1[0] = arr1[arr1.length - 1]
        this.yname1[1] = 'log(' + this.yname1[0] + ')'
      }
    }
  },
  mounted() {
    if (this.mergetype === 'double') {
      this.DYMergeSvgDraw()
    } else if (this.mergetype === 'single') {
      this.MergeSvgDraw()
    } else {
      this.SvgDraw()
    }
  },
  methods: {
    ...mapScalarMutations([
      'setmergestep'
    ]),
    ...mapCustomMutations([
      'setScalar', 'deleteScalar'
    ]),
    SvgDraw() {
      let data = [].concat(JSON.parse(JSON.stringify(this.data)))
      const datamid = [].concat(JSON.parse(JSON.stringify(this.data)))
      const smooth = this.smoothvalue * 1
      let yaxis = this.yname[0]
      if (this.yaxis === 'log-linear') {
        let flag = 0
        for (let i = 0; i < data.length; i++) {
          if (datamid[i].value > 0) {
            datamid[i].value = Math.log(datamid[i].value)
          } else {
            flag = 1
            break
          }
        }
        if (flag === 0) {
          yaxis = this.yname[1]
          data = datamid
        }
      }
      const smoothdata = [].concat(JSON.parse(JSON.stringify(data)))
      let last = smoothdata[0].value
      for (let i = 1; i < smoothdata.length; i++) {
        smoothdata[i].value = last * smooth + (1 - smooth) * smoothdata[i].value
        last = smoothdata[i].value
      }
      // set the dimensions and margins of the graph
      var margin = { top: 20, right: 20, bottom: 70, left: 70 }
      var width = 350 - margin.left - margin.right
      var height = 270 - margin.top - margin.bottom

      // append the svg object to the body of the page
      var svg = d3.select('#' + this.classname)
        .append('svg')
        .attr('id', 'svg' + this.classname)
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('preserveAspectRatio', 'xMidYMid meet')
        .attr('viewBox', '0 0 350 270')
        .append('g')
        .attr('transform',
          'translate(' + margin.left + ',' + margin.top + ')')

      // add arrow
      svg.append('defs').append('marker')
        .attr('id', 'xarrowhead' + this.classname)
        .attr('markerUnits', 'strokeWidth')
        .attr('markerWidth', '15')
        .attr('markerHeight', '15')
        .attr('viewBox', '0 0 12 12')
        .attr('refX', '5')
        .attr('refY', '6')
        .append('path')
        .attr('d', 'M2,2 L10,6 L2,10 L6,6 L2,2')

      svg.append('defs').append('marker')
        .attr('id', 'yarrowhead' + this.classname)
        .attr('markerUnits', 'strokeWidth')
        .attr('markerWidth', '15')
        .attr('markerHeight', '15')
        .attr('viewBox', '0 0 12 12')
        .attr('refX', '5')
        .attr('refY', '6')
        .attr('orient', '-90deg')
        .append('path')
        .attr('d', 'M2,2 L10,6 L2,10 L6,6 L2,2')

      // Add X axis
      const xdomain = d3.extent(data, function(d) { return d.step })
      const xgap = xdomain[1] - xdomain[0]
      // xdomain[0] = xdomain[0] - xgap / 4
      xdomain[1] = xdomain[1] + xgap / 4
      var x = d3.scaleLinear()
        .domain(xdomain)
        .rangeRound([0, width])
      var xAxis = svg.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
      xAxis.select('path').attr('marker-end', 'url(#xarrowhead' + this.classname + ')')
      svg.append('text')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', height + margin.top + 20)
        .text('step')

      // Add Y axis
      const ydomain = d3.extent(data, function(d) { return d.value })
      const ygap = ydomain[1] - ydomain[0]
      ydomain[0] = ydomain[0] - ygap / 4
      ydomain[1] = ydomain[1] + ygap / 4
      var y = d3.scaleLinear()
        .domain(ydomain)
        .rangeRound([height, 0])
      var yAxis = svg.append('g')
        .call(
          d3.axisLeft(y)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
      yAxis.select('path').attr('marker-end', 'url(#yarrowhead' + this.classname + ')')
      svg.append('text')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .attr('y', -margin.left + 20)
        .attr('x', -height / 2)
        .text(yaxis)

      // Add a clipPath: everything out of this area won't be drawn.
      svg.append('defs').append('svg:clipPath')
        .attr('id', 'clip' + this.classname)
        .append('svg:rect')
        .attr('width', width)
        .attr('height', height)
        .attr('x', 0)
        .attr('y', 0)

      // Add brushing
      var brush = d3.brush()
        .extent([[0, 0], [width, height]])
        .on('end', updateChart)

      // Create the line variable: where both the line and the brush take place
      var line = svg.append('g')
        .attr('clip-path', 'url(#clip' + this.classname + ')')
      // Add the original line
      line.append('path')
        .datum(data)
        .attr('class', 'originalline')
        .attr('fill', 'none')
        .attr('stroke', 'blue')
        .attr('stroke-width', 1.5)
        .attr('stroke-opacity', 0.2)
        .attr('d', d3.line()
          .x(function(d) { return x(d.step) })
          .y(function(d) { return y(d.value) })
        )
      // Add the smooth line
      line.append('path')
        .datum(smoothdata)
        .attr('class', 'smoothline')
        .attr('fill', 'none')
        .attr('stroke', 'blue')
        .attr('stroke-width', 1.5)
        .attr('d', d3.line()
          .x(function(d) { return x(d.step) })
          .y(function(d) { return y(d.value) })
        )
      // Add the brushing
      line
        .append('g')
        .attr('class', 'brush')
        .call(brush)
      // create a tooltip
      var Tooltip = d3.select('#' + this.classname).select('.tooltip')
      var td1 = d3.select('#td1' + this.classname)
      var td2 = d3.select('#td2' + this.classname)
      var td3 = d3.select('#td3' + this.classname)

      line
        .selectAll('.myCircle')
        .data(smoothdata)
        .enter()
        .append('circle')
        .attr('class', 'myCircle')
        .attr('cx', function(d) { return x(d.step) })
        .attr('cy', function(d) { return y(d.value) })
        .attr('r', 3)
        .attr('stroke-width', 10)
        .attr('stroke', 'black')
        .attr('fill', 'black')
        .attr('fill-opacity', 0)
        .attr('stroke-opacity', 0)
        .on('mouseover', function(d) {
          d3.select(this).attr('fill-opacity', 1)
          Tooltip.style('visibility', 'visible')
        })
        .on('mousemove', function(d) {
          const unixTimestamp = new Date(d.wall_time * 1000)
          const commonTime = unixTimestamp.toLocaleString('en-GB', { hour12: false })
          const tim = commonTime.split('\/')
          const year = tim[2].split(',')[0]
          const month = tim[1]
          const day = tim[0]
          const tt = tim[2].split(',')[1]

          let vv = d.value
          const absd = Math.abs(vv)
          if (absd > 10000) {
            const numLen = absd.toString().length - 1
            vv = vv / Math.pow(10, numLen) + 'e+' + numLen
          } else if (absd < 0.01 && absd !== 0) {
            const dString = absd.toString()
            let i = 3
            for (; i < dString.length; i++) {
              if (dString[i] !== '0') {
                break
              }
            }
            vv = (vv * Math.pow(10, i - 1)).toFixed(7) + 'e-' + (i - 1)
          } else {
            vv = vv.toFixed(7)
          }
          td1.html(year + '/' + month + '/' + day + tt)
          td2.html(d.step)
          td3.html(vv)
        })
        .on('mouseout', function(d) {
          d3.select(this).attr('fill-opacity', 0)
          Tooltip.style('visibility', 'hidden')
        })
      // A function that set idleTimeOut to null
      var idleTimeout
      function idled() { idleTimeout = null }

      // A function that update the chart for given boundaries
      function updateChart() {
      // What are the selected boundaries?
        var extent = d3.event.selection
        if (!extent) {
          if (!idleTimeout) {
            idleTimeout = setTimeout(idled, 350)
            return idleTimeout
          } // This allows to wait a little bit
          x.domain(xdomain)
          y.domain(ydomain)
        } else {
          x.domain([x.invert(extent[0][0]), x.invert(extent[1][0])])
          y.domain([y.invert(extent[1][1]), y.invert(extent[0][1])])
          line.select('.brush').call(brush.move, null)
        }

        // Update axis and line position
        xAxis.transition().duration(1000).call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        yAxis.transition().duration(1000).call(
          d3.axisLeft(y)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        line
          .select('.smoothline')
          .transition()
          .duration(1000)
          .attr('d', d3.line()
            .x(function(d) { return x(d.step) })
            .y(function(d) { return y(d.value) })
          )
        line
          .select('.originalline')
          .transition()
          .duration(1000)
          .attr('d', d3.line()
            .x(function(d) { return x(d.step) })
            .y(function(d) { return y(d.value) })
          )
        line
          .selectAll('.myCircle')
          .transition()
          .duration(1000)
          .attr('cx', function(d) { return x(d.step) })
          .attr('cy', function(d) { return y(d.value) })
      }
      // If user double click, reinitialize the chart
      svg.on('dblclick', function() {
        x.domain(xdomain)
        xAxis.transition().call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        y.domain(ydomain)
        yAxis.transition().call(
          d3.axisLeft(y)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        line
          .selectAll('.smoothline')
          .transition()
          .duration(1000)
          .attr('d', d3.line()
            .x(function(d) { return x(d.step) })
            .y(function(d) { return y(d.value) })
          )
        line
          .selectAll('.originalline')
          .transition()
          .duration(1000)
          .attr('d', d3.line()
            .x(function(d) { return x(d.step) })
            .y(function(d) { return y(d.value) })
          )
        line
          .selectAll('.myCircle')
          .transition()
          .duration(1000)
          .attr('cx', function(d) { return x(d.step) })
          .attr('cy', function(d) { return y(d.value) })
      })
    },
    MergeSvgDraw() {
      const legendnumber = this.legendnumber
      let data = [].concat(JSON.parse(JSON.stringify(this.mergeddata)))
      const datamid = [].concat(JSON.parse(JSON.stringify(this.mergeddata)))
      const smooth = this.smoothvalue * 1
      let yaxis = this.yname[0]
      if (this.yaxis === 'log-linear') {
        let flag = 0
        for (let i = 0; i < data.length; i++) {
          for (let j = 0; j < data[i].value.length; j++) {
            if ((datamid[i].value)[j].value > 0) {
              (datamid[i].value)[j].value = Math.log((datamid[i].value)[j].value)
            } else {
              flag = 1
              break
            }
          }
          if (flag === 1) break
        }
        if (flag === 0) {
          yaxis = this.yname[1]
          data = datamid
        }
      }
      const smoothdata = [].concat(JSON.parse(JSON.stringify(data)))
      for (let i = 0; i < smoothdata.length; i++) {
        let last = (smoothdata[i].value)[0].value
        for (let j = 1; j < smoothdata[i].value.length; j++) {
          (smoothdata[i].value)[j].value = last * smooth + (1 - smooth) * (smoothdata[i].value)[j].value
          last = (smoothdata[i].value)[j].value
        }
      }
      let dataset0 = []
      let dataset = []
      for (let i = 0; i < data.length; i++) {
        data[i].order = i
        smoothdata[i].order = i
        dataset0 = dataset0.concat(data[i].value)
        dataset = dataset.concat(smoothdata[i].value)
      }
      // color palette
      var res = data.map(function(d) { return d.order }) // list of group names
      var color = d3.scaleOrdinal()
        .domain(res)
        .range(['#ed357b', '#1d276e', '#6ec6d0', '#0c9257', '#ffdf1e', '#fe8325'])
      // set the dimensions and margins of the graph
      var margin = { top: 20, right: 20, bottom: 50 + 20 * legendnumber, left: 70 }
      var width = 350 - margin.left - margin.right
      var height = 250 + 20 * legendnumber - margin.top - margin.bottom

      // append the svg object to the body of the page
      var svg = d3.select('#' + this.classname)
        .append('svg')
        .attr('id', 'svg' + this.classname)
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('preserveAspectRatio', 'xMidYMid meet')
        .attr('viewBox', '0 0 350 ' + (250 + 20 * legendnumber).toString())
        .append('g')
        .attr('transform',
          'translate(' + margin.left + ',' + margin.top + ')')

      // add arrow
      svg.append('defs').append('marker')
        .attr('id', 'xarrowhead' + this.classname)
        .attr('markerUnits', 'strokeWidth')
        .attr('markerWidth', '15')
        .attr('markerHeight', '15')
        .attr('viewBox', '0 0 12 12')
        .attr('refX', '5')
        .attr('refY', '6')
        .append('path')
        .attr('d', 'M2,2 L10,6 L2,10 L6,6 L2,2')

      svg.append('defs').append('marker')
        .attr('id', 'yarrowhead' + this.classname)
        .attr('markerUnits', 'strokeWidth')
        .attr('markerWidth', '15')
        .attr('markerHeight', '15')
        .attr('viewBox', '0 0 12 12')
        .attr('refX', '5')
        .attr('refY', '6')
        .attr('orient', '-90deg')
        .append('path')
        .attr('d', 'M2,2 L10,6 L2,10 L6,6 L2,2')

      // Add X axis
      const xdomain = d3.extent(dataset0, function(d) { return d.step })
      const xgap = xdomain[1] - xdomain[0]
      xdomain[0] = xdomain[0] - xgap / 4
      xdomain[1] = xdomain[1] + xgap / 4
      var x = d3.scaleLinear()
        .domain(xdomain)
        .rangeRound([0, width])
      var xAxis = svg.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
      xAxis.select('path').attr('marker-end', 'url(#xarrowhead' + this.classname + ')')
      svg.append('text')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', height + margin.top + 20)
        .text('step')

      // Add Y axis
      const ydomain = d3.extent(dataset0, function(d) { return d.value })
      const ygap = ydomain[1] - ydomain[0]
      ydomain[0] = ydomain[0] - ygap / 4
      ydomain[1] = ydomain[1] + ygap / 4
      var y = d3.scaleLinear()
        .domain(ydomain)
        .rangeRound([height, 0])
      var yAxis = svg.append('g')
        .call(
          d3.axisLeft(y)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
      yAxis.select('path').attr('marker-end', 'url(#yarrowhead' + this.classname + ')')
      svg.append('text')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .attr('y', -margin.left + 20)
        .attr('x', -height / 2)
        .text(yaxis)

      // Add a clipPath: everything out of this area won't be drawn.
      svg.append('defs').append('svg:clipPath')
        .attr('id', 'clip' + this.classname)
        .append('svg:rect')
        .attr('width', width)
        .attr('height', height)
        .attr('x', 0)
        .attr('y', 0)

      // Add brushing
      var brush = d3.brush() // Add the brush feature using the d3.brush function
        .extent([[0, 0], [width, height]]) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
        .on('end', updateChart) // Each time the brush selection changes, trigger the 'updateChart' function

      // Create the line variable: where both the line and the brush take place
      var line = svg.append('g')
        .attr('clip-path', 'url(#clip' + this.classname + ')')
      // Add the smooth line
      line.selectAll('.smoothline')
        .data(smoothdata)
        .enter()
        .append('path')
        .attr('class', 'smoothline')
        .attr('fill', 'none')
        .attr('stroke', function(d) { return color(d.order) })
        .attr('stroke-width', 1.5)
        .attr('d', function(d) {
          return d3.line()
            .x(function(d) { return x(d.step) })
            .y(function(d) { return y(d.value) })(d.value)
        })
      // Add the brushing
      line
        .append('g')
        .attr('class', 'brush')
        .call(brush)
      // create a tooltip

      var Tooltip = d3.select('#' + this.classname).select('.tooltip')
      var td1 = d3.select('#td1' + this.classname)
      var td2 = d3.select('#td2' + this.classname)
      var td3 = d3.select('#td3' + this.classname)

      line
        .selectAll('.myCircle')
        .data(dataset)
        .enter()
        .append('circle')
        .attr('class', 'myCircle')
        .attr('cx', function(d) { return x(d.step) })
        .attr('cy', function(d) { return y(d.value) })
        .attr('r', 3)
        .attr('stroke', 'black')
        .attr('stroke-width', 10)
        .attr('fill', 'black')
        .attr('fill-opacity', 0)
        .attr('stroke-opacity', 0)
        .on('mouseover', function(d) {
          d3.select(this).attr('fill-opacity', 1)
          Tooltip.style('visibility', 'visible')
        })
        .on('mousemove', function(d) {
          const unixTimestamp = new Date(d.wall_time * 1000)
          const commonTime = unixTimestamp.toLocaleString('en-GB', { hour12: false })
          const tim = commonTime.split('\/')
          const year = tim[2].split(',')[0]
          const month = tim[1]
          const day = tim[0]
          const tt = tim[2].split(',')[1]

          let vv = d.value
          const absd = Math.abs(vv)
          if (absd > 10000) {
            const numLen = absd.toString().length - 1
            vv = vv / Math.pow(10, numLen) + 'e+' + numLen
          } else if (absd < 0.01 && absd !== 0) {
            const dString = absd.toString()
            let i = 3
            for (; i < dString.length; i++) {
              if (dString[i] !== '0') {
                break
              }
            }
            vv = (vv * Math.pow(10, i - 1)).toFixed(7) + 'e-' + (i - 1)
          } else {
            vv = vv.toFixed(7)
          }
          td1.html(year + '/' + month + '/' + day + tt)
          td2.html(d.step)
          td3.html(vv)
        })
        .on('mouseout', function(d) {
          d3.select(this).attr('fill-opacity', 0)
          Tooltip.style('visibility', 'hidden')
        })

      // add the legend
      var legend = svg.selectAll('.legend')
        .data(smoothdata)
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform', function(d, i) {
          return 'translate(0,' + i * 20 + ')'
        })

      legend.append('rect')
        .attr('x', -40)
        .attr('y', height + margin.top + 40)
        .attr('width', 18)
        .attr('height', 4)
        .style('fill', function(d) {
          return color(d.order)
        })

      legend.append('text')
        .attr('x', -16)
        .attr('y', height + margin.top + 40)
        .attr('dy', '.5em')
        .attr('font-size', '10px')
        .style('text-anchor', 'start')
        .text(function(d) { return d.run + ',' + d.tag })
      // A function that set idleTimeOut to null
      var idleTimeout
      function idled() { idleTimeout = null }

      // A function that update the chart for given boundaries
      function updateChart() {
      // What are the selected boundaries?
        var extent = d3.event.selection

        // If no selection, back to initial coordinate. Otherwise, update X axis domain
        if (!extent) {
          if (!idleTimeout) {
            idleTimeout = setTimeout(idled, 350)
            return idleTimeout
          } // This allows to wait a little bit
          x.domain(xdomain)
          y.domain(xdomain)
        } else {
          x.domain([x.invert(extent[0][0]), x.invert(extent[1][0])])
          y.domain([y.invert(extent[1][1]), y.invert(extent[0][1])])
          line.select('.brush').call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
        }

        // Update axis and line position
        xAxis.transition().duration(1000).call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        yAxis.transition().duration(1000).call(
          d3.axisLeft(y)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        line
          .selectAll('.smoothline')
          .transition()
          .duration(1000)
          .attr('d', function(d) {
            return d3.line()
              .x(function(d) { return x(d.step) })
              .y(function(d) { return y(d.value) })(d.value)
          })
        line
          .selectAll('.myCircle')
          .transition()
          .duration(1000)
          .attr('cx', function(d) { return x(d.step) })
          .attr('cy', function(d) { return y(d.value) })
      }
      // If user double click, reinitialize the chart
      svg.on('dblclick', function() {
        x.domain(xdomain)
        xAxis.transition().call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        y.domain(ydomain)
        yAxis.transition().call(
          d3.axisLeft(y)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        line
          .selectAll('.smoothline')
          .transition()
          .duration(1000)
          .attr('d', function(d) {
            return d3.line()
              .x(function(d) { return x(d.step) })
              .y(function(d) { return y(d.value) })(d.value)
          })
        line
          .selectAll('.myCircle')
          .transition()
          .duration(1000)
          .attr('cx', function(d) { return x(d.step) })
          .attr('cy', function(d) { return y(d.value) })
      })
    },
    DYMergeSvgDraw() {
      const legendnumber = this.legendnumber
      let data0 = [].concat(JSON.parse(JSON.stringify(this.mergeddata0)))
      let data1 = [].concat(JSON.parse(JSON.stringify(this.mergeddata1)))
      const datamid0 = [].concat(JSON.parse(JSON.stringify(this.mergeddata0)))
      const datamid1 = [].concat(JSON.parse(JSON.stringify(this.mergeddata1)))
      const smooth = this.smoothvalue * 1
      let yaxis0 = this.yname0[0]
      let yaxis1 = this.yname1[0]
      if (this.yaxis === 'log-linear') {
        let flag = 0
        for (let i = 0; i < data0.length; i++) {
          if (flag === 1) break
          for (let j = 0; j < data0[i].value.length; j++) {
            if ((datamid0[i].value)[j].value > 0) {
              (datamid0[i].value)[j].value = Math.log((datamid0[i].value)[j].value)
            } else {
              flag = 1
              break
            }
          }
        }
        for (let i = 0; i < data1.length; i++) {
          if (flag === 1) break
          for (let j = 0; j < data1[i].value.length; j++) {
            if ((datamid1[i].value)[j].value > 0) {
              (datamid1[i].value)[j].value = Math.log((datamid1[i].value)[j].value)
            } else {
              flag = 1
              break
            }
          }
        }
        if (flag === 0) {
          yaxis0 = this.yname0[1]
          yaxis1 = this.yname1[1]
          data0 = datamid0
          data1 = datamid1
        }
      }
      const smoothdata0 = [].concat(JSON.parse(JSON.stringify(data0)))
      const smoothdata1 = [].concat(JSON.parse(JSON.stringify(data1)))
      for (let i = 0; i < smoothdata0.length; i++) {
        let last = (smoothdata0[i].value)[0].value
        for (let j = 1; j < smoothdata0[i].value.length; j++) {
          (smoothdata0[i].value)[j].value = last * smooth + (1 - smooth) * (smoothdata0[i].value)[j].value
          last = (smoothdata0[i].value)[j].value
        }
      }
      for (let i = 0; i < smoothdata1.length; i++) {
        let last = (smoothdata1[i].value)[0].value
        for (let j = 1; j < smoothdata1[i].value.length; j++) {
          (smoothdata1[i].value)[j].value = last * smooth + (1 - smooth) * (smoothdata1[i].value)[j].value
          last = (smoothdata1[i].value)[j].value
        }
      }
      let dataset00 = []
      let dataset11 = []
      let dataset0 = []
      let dataset1 = []
      for (let i = 0; i < data0.length; i++) {
        data0[i].order = i
        smoothdata0[i].order = i
        dataset00 = dataset00.concat(data0[i].value)
        dataset0 = dataset0.concat(smoothdata0[i].value)
      }
      for (let i = 0; i < data1.length; i++) {
        data1[i].order = i
        smoothdata1[i].order = i
        dataset11 = dataset11.concat(data1[i].value)
        dataset1 = dataset1.concat(smoothdata1[i].value)
      }
      // color palette
      var res0 = data0.map(function(d) { return d.order }) // list of group names
      var color0 = d3.scaleOrdinal()
        .domain(res0)
        .range(['#ed357b', '#1d276e', '#6ec6d0', '#0c9257', '#ffdf1e', '#fe8325'])
      var res1 = data1.map(function(d) { return d.order }) // list of group names
      var color1 = d3.scaleOrdinal()
        .domain(res1)
        .range(['#fe8325', '#ffdf1e', '#0c9257', '#6ec6d0', '#1d276e', '#ed357b'])

      // set the dimensions and margins of the graph
      var margin = { top: 20, right: 70, bottom: 50 + 20 * legendnumber, left: 70 }
      var width = 350 - margin.left - margin.right
      var height = 250 + 20 * legendnumber - margin.top - margin.bottom

      // append the svg object to the body of the page
      var svg = d3.select('#' + this.classname)
        .append('svg')
        .attr('id', 'svg' + this.classname)
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('preserveAspectRatio', 'xMidYMid meet')
        .attr('viewBox', '0 0 350 ' + (250 + 20 * legendnumber).toString())
        .append('g')
        .attr('transform',
          'translate(' + margin.left + ',' + margin.top + ')')

      // add arrow
      svg.append('defs').append('marker')
        .attr('id', 'yarrowhead' + this.classname)
        .attr('markerUnits', 'strokeWidth')
        .attr('markerWidth', '15')
        .attr('markerHeight', '15')
        .attr('viewBox', '0 0 12 12')
        .attr('refX', '5')
        .attr('refY', '6')
        .attr('orient', '-90deg')
        .append('path')
        .attr('d', 'M2,2 L10,6 L2,10 L6,6 L2,2')

      // Add X axis
      const xdomain0 = d3.extent(dataset00, function(d) { return d.step })
      const xdomain1 = d3.extent(dataset11, function(d) { return d.step })
      const xdomain = []
      xdomain[0] = Math.min(xdomain0[0], xdomain1[0])
      xdomain[1] = Math.max(xdomain0[1], xdomain1[1])
      const xgap = xdomain[1] - xdomain[0]
      xdomain[0] = xdomain[0] - xgap / 4
      xdomain[1] = xdomain[1] + xgap / 4
      var x = d3.scaleLinear()
        .domain(xdomain)
        .rangeRound([0, width])
      var xAxis = svg.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
      svg.append('text')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', height + margin.top + 20)
        .text('step')

      // Add Y0 axis
      const ydomain0 = d3.extent(dataset00, function(d) { return d.value })
      const ygap0 = ydomain0[1] - ydomain0[0]
      ydomain0[0] = ydomain0[0] - ygap0 / 4
      ydomain0[1] = ydomain0[1] + ygap0 / 4
      var y0 = d3.scaleLinear()
        .domain(ydomain0)
        .rangeRound([height, 0])
      var yAxis0 = svg.append('g')
        .call(
          d3.axisLeft(y0)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
      yAxis0.select('path').attr('marker-end', 'url(#yarrowhead' + this.classname + ')')
      svg.append('text')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .attr('y', -margin.left + 20)
        .attr('x', -height / 2)
        .text(yaxis0)

      // Add Y1 axis
      const ydomain1 = d3.extent(dataset11, function(d) { return d.value })
      const ygap1 = ydomain1[1] - ydomain1[0]
      ydomain1[0] = ydomain1[0] - ygap1 / 4
      ydomain1[1] = ydomain1[1] + ygap1 / 4
      var y1 = d3.scaleLinear()
        .domain(ydomain1)
        .rangeRound([height, 0])
      var yAxis1 = svg.append('g')
        .attr('transform', 'translate(' + width + ',0)')
        .call(
          d3.axisRight(y1)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
      yAxis1.select('path').attr('marker-end', 'url(#yarrowhead' + this.classname + ')')
      svg.append('text')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .attr('y', width + margin.left - 10)
        .attr('x', -height / 2)
        .text(yaxis1)
      // Add a clipPath: everything out of this area won't be drawn.
      svg.append('defs').append('svg:clipPath')
        .attr('id', 'clip' + this.classname)
        .append('svg:rect')
        .attr('width', width)
        .attr('height', height)
        .attr('x', 0)
        .attr('y', 0)

      // Add brushing
      var brush = d3.brush() // Add the brush feature using the d3.brush function
        .extent([[0, 0], [width, height]]) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
        .on('end', updateChart) // Each time the brush selection changes, trigger the 'updateChart' function

      // Create the line variable: where both the line and the brush take place
      var line = svg.append('g')
        .attr('clip-path', 'url(#clip' + this.classname + ')')

      // Add the smooth line
      line.selectAll('.smoothline0')
        .data(smoothdata0)
        .enter()
        .append('path')
        .attr('class', 'smoothline0')
        .attr('fill', 'none')
        .attr('stroke', function(d) { return color0(d.order) })
        .attr('stroke-width', 1.5)
        .attr('d', function(d) {
          return d3.line()
            .x(function(d) { return x(d.step) })
            .y(function(d) { return y0(d.value) })(d.value)
        })
      line.selectAll('.smoothline1')
        .data(smoothdata1)
        .enter()
        .append('path')
        .attr('class', 'smoothline1')
        .attr('fill', 'none')
        .attr('stroke', function(d) { return color1(d.order) })
        .attr('stroke-width', 1.5)
        .attr('d', function(d) {
          return d3.line()
            .x(function(d) { return x(d.step) })
            .y(function(d) { return y1(d.value) })(d.value)
        })
      // Add the brushing
      line
        .append('g')
        .attr('class', 'brush')
        .call(brush)
      // create a tooltip

      var Tooltip = d3.select('#' + this.classname).select('.tooltip')
      var td1 = d3.select('#td1' + this.classname)
      var td2 = d3.select('#td2' + this.classname)
      var td3 = d3.select('#td3' + this.classname)

      line
        .selectAll('.myCircle0')
        .data(dataset0)
        .enter()
        .append('circle')
        .attr('class', 'myCircle0')
        .attr('cx', function(d) { return x(d.step) })
        .attr('cy', function(d) { return y0(d.value) })
        .attr('r', 3)
        .attr('stroke', 'black')
        .attr('stroke-width', 10)
        .attr('fill', 'black')
        .attr('fill-opacity', 0)
        .attr('stroke-opacity', 0)
        .on('mouseover', function(d) {
          d3.select(this).attr('fill-opacity', 1)
          Tooltip.style('visibility', 'visible')
        })
        .on('mousemove', function(d) {
          const unixTimestamp = new Date(d.wall_time * 1000)
          const commonTime = unixTimestamp.toLocaleString('en-GB', { hour12: false })
          const tim = commonTime.split('\/')
          const year = tim[2].split(',')[0]
          const month = tim[1]
          const day = tim[0]
          const tt = tim[2].split(',')[1]

          let vv = d.value
          const absd = Math.abs(vv)
          if (absd > 10000) {
            const numLen = absd.toString().length - 1
            vv = vv / Math.pow(10, numLen) + 'e+' + numLen
          } else if (absd < 0.01 && absd !== 0) {
            const dString = absd.toString()
            let i = 3
            for (; i < dString.length; i++) {
              if (dString[i] !== '0') {
                break
              }
            }
            vv = (vv * Math.pow(10, i - 1)).toFixed(7) + 'e-' + (i - 1)
          } else {
            vv = vv.toFixed(7)
          }
          td1.html(year + '/' + month + '/' + day + tt)
          td2.html(d.step)
          td3.html(vv)
        })
        .on('mouseout', function(d) {
          d3.select(this).attr('fill-opacity', 0)
          Tooltip.style('visibility', 'hidden')
        })
      line
        .selectAll('.myCircle1')
        .data(dataset1)
        .enter()
        .append('circle')
        .attr('class', 'myCircle1')
        .attr('cx', function(d) { return x(d.step) })
        .attr('cy', function(d) { return y1(d.value) })
        .attr('r', 3)
        .attr('stroke', 'black')
        .attr('stroke-width', 10)
        .attr('fill', 'black')
        .attr('fill-opacity', 0)
        .attr('stroke-opacity', 0)
        .on('mouseover', function(d) {
          d3.select(this).attr('fill-opacity', 1)
          Tooltip.style('visibility', 'visible')
        })
        .on('mousemove', function(d) {
          const unixTimestamp = new Date(d.wall_time * 1000)
          const commonTime = unixTimestamp.toLocaleString('en-GB', { hour12: false })
          const tim = commonTime.split('\/')
          const year = tim[2].split(',')[0]
          const month = tim[1]
          const day = tim[0]
          const tt = tim[2].split(',')[1]

          let vv = d.value
          const absd = Math.abs(vv)
          if (absd > 10000) {
            const numLen = absd.toString().length - 1
            vv = vv / Math.pow(10, numLen) + 'e+' + numLen
          } else if (absd < 0.01 && absd !== 0) {
            const dString = absd.toString()
            let i = 3
            for (; i < dString.length; i++) {
              if (dString[i] !== '0') {
                break
              }
            }
            vv = (vv * Math.pow(10, i - 1)).toFixed(7) + 'e-' + (i - 1)
          } else {
            vv = vv.toFixed(7)
          }
          td1.html(year + '/' + month + '/' + day + tt)
          td2.html(d.step)
          td3.html(vv)
        })
        .on('mouseout', function(d) {
          d3.select(this).attr('fill-opacity', 0)
          Tooltip.style('visibility', 'hidden')
        })

      const firstdatanumber = smoothdata0.length
      // add the legend0
      var legend0 = svg.selectAll('.legend0')
        .data(smoothdata0)
        .enter()
        .append('g')
        .attr('class', 'legend0')
        .attr('transform', function(d, i) {
          return 'translate(0,' + i * 20 + ')'
        })

      legend0.append('rect')
        .attr('x', -40)
        .attr('y', height + margin.top + 40)
        .attr('width', 18)
        .attr('height', 4)
        .style('fill', function(d) {
          return color0(d.order)
        })

      legend0.append('text')
        .attr('x', -16)
        .attr('y', height + margin.top + 40)
        .attr('dy', '.5em')
        .attr('font-size', '10px')
        .style('text-anchor', 'start')
        .text(function(d) { return d.run + ',' + d.tag })
      // add the legend0
      var legend1 = svg.selectAll('.legend1')
        .data(smoothdata1)
        .enter()
        .append('g')
        .attr('class', 'legend1')
        .attr('transform', function(d, i) {
          return 'translate(0,' + (firstdatanumber + i) * 20 + ')'
        })

      legend1.append('rect')
        .attr('x', -40)
        .attr('y', height + margin.top + 40)
        .attr('width', 18)
        .attr('height', 4)
        .style('fill', function(d) {
          return color1(d.order)
        })

      legend1.append('text')
        .attr('x', -16)
        .attr('y', height + margin.top + 40)
        .attr('dy', '.5em')
        .attr('font-size', '10px')
        .style('text-anchor', 'start')
        .text(function(d) { return d.run + ',' + d.tag })
      // A function that set idleTimeOut to null
      var idleTimeout
      function idled() { idleTimeout = null }

      // A function that update the chart for given boundaries
      function updateChart() {
      // What are the selected boundaries?
        var extent = d3.event.selection

        // If no selection, back to initial coordinate. Otherwise, update X axis domain
        if (!extent) {
          if (!idleTimeout) {
            idleTimeout = setTimeout(idled, 350)
            return idleTimeout
          } // This allows to wait a little bit
          x.domain(xdomain)
          y0.domain(ydomain0)
          y1.domain(ydomain1)
        } else {
          x.domain([x.invert(extent[0][0]), x.invert(extent[1][0])])
          y0.domain([y0.invert(extent[1][1]), y0.invert(extent[0][1])])
          y1.domain([y1.invert(extent[1][1]), y1.invert(extent[0][1])])
          line.select('.brush').call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
        }

        // Update axis and line position
        xAxis.transition().duration(1000).call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        yAxis0.transition().duration(1000).call(
          d3.axisLeft(y0)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        yAxis1.transition().duration(1000).call(
          d3.axisRight(y1)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        line
          .selectAll('.smoothline0')
          .transition()
          .duration(1000)
          .attr('d', function(d) {
            return d3.line()
              .x(function(d) { return x(d.step) })
              .y(function(d) { return y0(d.value) })(d.value)
          })
        line
          .selectAll('.smoothline1')
          .transition()
          .duration(1000)
          .attr('d', function(d) {
            return d3.line()
              .x(function(d) { return x(d.step) })
              .y(function(d) { return y1(d.value) })(d.value)
          })
        line
          .selectAll('.myCircle0')
          .transition()
          .duration(1000)
          .attr('cx', function(d) { return x(d.step) })
          .attr('cy', function(d) { return y0(d.value) })
        line
          .selectAll('.myCircle1')
          .transition()
          .duration(1000)
          .attr('cx', function(d) { return x(d.step) })
          .attr('cy', function(d) { return y1(d.value) })
      }
      // If user double click, reinitialize the chart
      svg.on('dblclick', function() {
        x.domain(xdomain)
        xAxis.transition().call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        y0.domain(ydomain0)
        yAxis0.transition().call(
          d3.axisLeft(y0)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        y1.domain(ydomain1)
        yAxis1.transition().call(
          d3.axisRight(y1)
            .tickSizeOuter(0)
            .ticks(5)
            .tickFormat(d => {
              const absd = Math.abs(d)
              if (absd > 10000) {
                const numLen = absd.toString().length - 1
                return d / Math.pow(10, numLen) + 'e+' + numLen
              } else if (absd < 0.001) {
                if (d === 0) return d
                const dString = absd.toString()
                let i = 3
                for (; i < dString.length; i++) {
                  if (dString[i] !== '0') {
                    break
                  }
                }
                return (d * Math.pow(10, i - 1)).toFixed(1) + 'e-' + (i - 1)
              }
              return d
            })
        )
        line
          .selectAll('.smoothline0')
          .transition()
          .duration(1000)
          .attr('d', function(d) {
            return d3.line()
              .x(function(d) { return x(d.step) })
              .y(function(d) { return y0(d.value) })(d.value)
          })
        line
          .selectAll('.myCircle0')
          .transition()
          .duration(1000)
          .attr('cx', function(d) { return x(d.step) })
          .attr('cy', function(d) { return y0(d.value) })
        line
          .selectAll('.smoothline1')
          .transition()
          .duration(1000)
          .attr('d', function(d) {
            return d3.line()
              .x(function(d) { return x(d.step) })
              .y(function(d) { return y1(d.value) })(d.value)
          })
        line
          .selectAll('.myCircle1')
          .transition()
          .duration(1000)
          .attr('cx', function(d) { return x(d.step) })
          .attr('cy', function(d) { return y1(d.value) })
      })
    }
  }
}
</script>
