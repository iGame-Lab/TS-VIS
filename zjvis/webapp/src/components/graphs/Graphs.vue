/** Copyright 2020 Tianshu AI Platform. All Rights Reserved.
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

<template>
  <div>
    <div class="temp">
      <div id="test" class="Graph">
        <svg id="svg-canvas" style="float: left;">
          <defs>
            <marker
              id="dot"
              markerUnits="strokeWidth"
              markerWidth="10"
              markerHeight="10"
              viewBox="0 0 20 20"
              refX="10"
              refY="10"
            >
              <circle cx="10" cy="10" r="4" style="fill: black;" />
            </marker>
          </defs>
          <g id="draw" />
        </svg>
        <div
          v-show="showTag"
          id="assist"
          class="assist"
          style="right: 0%; display: flex; flex-direction: column; width: 20%; height: 100%; background-color: white;"
        >
          <div style="height: 20px;"><span>删除节点</span></div>
          <div style="height: calc(100% - 20px);"><svg /></div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import * as d3 from 'd3'
import dagreD3 from 'dagre-d3/dist/dagre-d3'
import $ from 'jquery'
import 'jquery-contextmenu'
import 'jquery-contextmenu/dist/jquery.contextMenu.css'

import { createNamespacedHelpers } from 'vuex'

let expandNode = []
let delStageNode = []
let reserverStageNode = []
let clickDel = []
let changeTag = 0
let tmp = []
const {
  mapGetters: mapGraphGetters,
  mapActions: mapGraphActions,
  mapMutations: mapGraphMutations,
  mapState: mapGraphStates
} = createNamespacedHelpers('graph')
const { mapState: mapLayoutStates } = createNamespacedHelpers('layout')
export default {
  name: 'Graph',
  data() {
    return {
      showTag: false,
      graphData: '',
      degreeInput: 100,
      retList: '',
      reg: '',
      sign: 0,
      srcData: {},
      reserve: [],
      nodeInfo: [],
      nnodeInfo: [],
      restoreNode: '',
      lastClick: '',
      initDraw: 0,
      lastAssistClick: '',
      curg: ''
    }
  },
  computed: {
    ...mapGraphGetters([
      'getGraphData',
      'getRetList',
      'getReg',
      'getClear',
      'getHidden',
      'getRun',
      'getPre',
      'getTagName',
      'getRunName',
      'getCurTag',
      'getRunChangeTag',
      'getIsDrawing'
    ]),
    ...mapLayoutStates(['userSelectRunFile']),
    ...mapGraphStates(['copy'])
  },
  watch: {
    getRetList(val) {
      this.retList = val
    },
    getGraphData(val) {
      this.graphData = val
      this.nodeInfo.splice(0, this.nodeInfo.length)
      expandNode = []
      delStageNode = []
      reserverStageNode = []
      clickDel = []
      changeTag = 0
      tmp = []
      this.getNodeInfo(JSON.stringify({ info: 'init' }))
      this.drawGraph()
      this.setRunChangeTag(false)
      this.setIsDrawing(false)
    },
    getReg(val) {
      this.reg = val
    },
    getHidden() {
      this.hidden()
    },
    getRun() {
      this.run()
    },
    getPre() {
      this.pre()
    },
    getClear() {
      delStageNode = []
      reserverStageNode = []
      this.drawGraph()
    },
    userSelectRunFile(val) {
      this.setRunChangeTag(true)
      this.setIsDrawing(true)
      let k = 0
      for (let i = 0; i < this.getRunName.length; i += 1) {
        if (val === this.getRunName[i]) {
          k = i
          break
        }
      }
      this.setCurTag(this.getTagName[k][0])
      const param = { run: val, tag: this.getCurTag }
      this.getFullData(param)
    },
    getCurTag(val) {
      if (!this.getRunChangeTag) {
        if (!this.getIsDrawing) {
          this.setIsDrawing(true)
          const param = { run: this.userSelectRunFile, tag: val }
          this.getFullData(param)
        }
      }
    }
  },
  mounted() {
    this.graphData = this.getGraphData
    this.retList = this.getRetList
    this.initDraw += 1
    this.regularEx('')
    for (let i = 0; i < reserverStageNode.length; i += 1) {
      reserverStageNode[i].sign = 1
    }
    if (this.getGraphData.length === 0) {
      let k = 0
      for (let i = 0; i < this.getRunName.length; i += 1) {
        if (this.userSelectRunFile === this.getRunName[i]) {
          k = i
          break
        }
      }
      if (this.getTagName[k]) {
        this.setCurTag(this.getTagName[k][0])
        const param = { run: this.userSelectRunFile, tag: this.getCurTag }
        this.getFullData(param)
      }
    } else {
      this.drawGraph()
    }
  },
  methods: {
    ...mapGraphActions(['getFullData']),
    ...mapGraphMutations([
      'getNodeInfo',
      'getClickDel',
      'setCurTag',
      'setRunChangeTag',
      'setIsDrawing',
      'regularEx'
    ]),
    drawGraph() {
      const self = this
      const { drawCircleTag, getDelNodeInfo, getModifyClick, drawAssist, nodeInfo, idTransformerFrontend, edgeLabelAnimation, colorCopy, colour } = this
      const getInfo = this.getNodeInfo
      const data = this.graphData
      if (data === undefined) {
        return
      }
      const color = d3.scaleOrdinal().range([
        '#e8c5df', // Convolution
        '#daf4cc', // Normalization
        '#d7dafb', // Math&Activation&Pooling
        '#b1cbe8', // Sparse Tensors&Tensor Transformations
        '#cdf6e8', // ControlFlow
        '#feedd3', // Losses&Metrics
        '#d2f5f9', // InputsandReaders
        '#dcdcdc', // default
        '#dcdcdc', // empty
        '#dcdcdc', // backup
        '#dcdcdc' // backup
      ])
      const isDashed = {}
      const isLines = {}
      const titleHeight = 40
      const cornerR = 5
      const lineWidth = 1
      const opdata = {}
      const nodedata = {}
      const SpecialNodeList = ['conv', 'dense', 'pool', 'norm']
      // 判断 补上edge的虚节点
      function IsVirtualNode(itemnode) {
        if (!itemnode) {
          return false
        }
        if (itemnode.label.toLowerCase().indexOf('(') >= 0) {
          return true
        }
        return false
      }
      // 绘制  补上edge的虚节点
      function DrawVirtualNodes(graph) {
        d3.selectAll(`.nodes .node`)
          // 1:卷积层,2:全连接层,3:池化层,4:归一化
          // eslint-disable-next-line
          .attr('temp', function(uid) {
            if (!nodedata[uid] || !IsVirtualNode(nodedata[uid])) {
              return ''
            }
            const node = graph.node(uid)
            if (!node) {
              return ''
            }
            d3.select(this)
              .select('rect')
              .style('stroke-dasharray', '5,3')
              .style('stroke', '#696969')
              .style('stroke-width', '1.5px')
          })
      }
      // 判断是否为计算图特殊节点
      function IsSpecialNode(itemnode) {
        if (!itemnode) {
          return false
        }
        if (itemnode.op !== '') {
          return false
        }
        // *******判断是否展开了子节点*******
        if (itemnode.sub_net.length > 0) {
          for (const n in itemnode.sub_net) {
            const size = d3.selectAll(`[id="${itemnode.sub_net[n].id}"]`).size()
            if (size > 0) {
              return false
            }
          }
        }
        for (const n in itemnode.sub_net) {
          // 卷积层
          if (itemnode.sub_net[n].op.toLowerCase().indexOf(SpecialNodeList[0].toLowerCase()) >= 0) {
            return 1
          }
          // 全连接层
          if (itemnode.label.toLowerCase().indexOf(SpecialNodeList[1].toLowerCase()) >= 0) {
            return 2
          }
          // 池化层
          if (itemnode.label.toLowerCase().indexOf(SpecialNodeList[2].toLowerCase()) >= 0) {
            return 3
          }
          // 归一化
          if (itemnode.label.toLowerCase().indexOf(SpecialNodeList[3].toLowerCase()) >= 0) {
            return 4
          }
          return false
        }
      }
      // 绘制计算图特殊节点
      function DrawSpecialNodes(graph) {
        d3.selectAll(`.nodes .node`)
          // eslint-disable-next-line
          .attr('temp', function(uid) {
            const rectColor = { 1: '#e8c5df', 2: '#b7d4ae', 3: '#d7dafb', 4: '#daf4cc' }
            if (!nodedata[uid]) {
              return ''
            }
            const node = graph.node(uid)
            const nodeType = IsSpecialNode(nodedata[uid])
            if (!node || !(nodeType in rectColor)) {
              return ''
            }
            d3.select(this)
              .select('rect')
              .style('fill', rectColor[nodeType])
          })
      }
      // 判断结构图是否要双层节点 或者 特殊颜色
      function IsDoubleNode(itemnode) {
        if (!itemnode) {
          return false
        }
        // 1:卷积层,2:全连接层,3:池化层,4:归一化
        if (itemnode.op.toLowerCase().indexOf(SpecialNodeList[0].toLowerCase()) >= 0) {
          return 1
        }
        if (itemnode.op.toLowerCase().indexOf(SpecialNodeList[1].toLowerCase()) >= 0) {
          return 2
        }
        if (itemnode.op.toLowerCase().indexOf(SpecialNodeList[2].toLowerCase()) >= 0) {
          return 3
        }
        if (itemnode.op.toLowerCase().indexOf(SpecialNodeList[3].toLowerCase()) >= 0) {
          return 4
        }
        return false
      }
      // 绘制特殊节点,绘制结构图双层节点
      function DrawDoubleNodes(graph) {
        d3.selectAll(`.nodes .node`)
          // eslint-disable-next-line
          .attr('temp', function(uid) {
            if (!nodedata[uid] || !IsDoubleNode(nodedata[uid])) {
              return ''
            }
            const node = graph.node(uid)
            if (!node) {
              return ''
            }
            const width = node.width + 20
            const height = node.height + 30
            if (IsDoubleNode(nodedata[uid]) !== 4) {
              // 分层的下层背景
              d3.select(this)
                .select('.label')
                .attr('transform', `translate(0,-${height / 4})`)
              d3.select(this)
                .selectAll('.special-layer-2')
                .data([0])
                .enter()
                .append('rect')
                .attr('class', 'special-layer-2')
                .style('fill', '#ffffff')
              // 下层空白
              d3.select(this)
                .selectAll('.special-layer-2')
                .attr('x', -width / 2 + lineWidth)
                .attr('y', -titleHeight + titleHeight / 2 - lineWidth + 20)
                .attr('rx', cornerR + 6)
                .attr('ry', cornerR + 6)
                .attr('width', width - lineWidth * 2)
                .attr('height', height - titleHeight - 5)
                .style('fill', '#fff')
                .style('opacity', 1)
                .style('stroke-width', 0)
              d3.select(this)
                .selectAll('.special-layer-1')
                .data([0])
                .enter()
                .append('rect')
                .attr('class', 'special-layer-1')
                .style('fill', '#fff')
              d3.select(this)
                .selectAll('.special-layer-1')
                .attr('x', -width / 2 + lineWidth)
                .attr('y', -5)
                .attr('width', width - lineWidth * 2)
                .attr('height', 15)
                .style('opacity', 1)
                .style('fill', '#fff')
                .style('stroke-width', 0)
              const text1 = { 1: 'kernel_size', 2: 'units', 3: 'pool_size' }
              const text2 = { 1: 'strides', 2: 'activation', 3: 'strides' }
              const nodeType = IsDoubleNode(nodedata[uid])
              if (nodeType in text1) {
                const ATTR = nodedata[uid].attrs
                d3.select(this)
                  .selectAll('.special-layer-text1')
                  .data([0])
                  .enter()
                  .append('text')
                  .attr('class', 'special-layer-text')
                  .attr('x', -width / 2 + 15)
                  .attr('y', 8)
                d3.select(this)
                  .selectAll('.special-layer-text')
                  .html(`● ${text1[nodeType]}: ${JSON.stringify(ATTR[text1[nodeType]])}`)
                  .style('font-size', '12px')
                d3.select(this)
                  .selectAll('.special-layer-text2')
                  .data([0])
                  .enter()
                  .append('text')
                  .attr('class', 'special-layer-text')
                  .attr('x', -width / 2 + 15)
                  .attr('y', 25)
                  .html(`● ${text2[nodeType]}: : ${JSON.stringify(ATTR[text2[nodeType]])}`)
                  .style('font-size', '12px')
              }
            }
          })
      }
      // op格式规范化，返回相对应颜色
      function GetColorByOP(op) {
        if (opdata[op.toLowerCase()]) {
          return color(opdata[op.toLowerCase()].parent)
        }
        if (opdata[op.toLowerCase().replace(/_/g, '')]) {
          return color(opdata[op.toLowerCase().replace(/_/g, '')].parent)
        }
        return color(op)
      }
      function GetColorByNode(g, node) {
        let op = ''
        const { uid } = node
        if (nodedata[uid]) {
          op = nodedata[uid].op
        } else {
          if (g.node(uid)) {
            op = g.node(uid).op
            nodedata[uid] = g.node(uid)
          }
          if (g.node.sub_net) {
            const index = g.node.sub_net.findIndex((e) => e.uid === uid)
            if (index >= 0) {
              op = g.node.sub_net[index].op
              nodedata[uid] = g.node.sub_net[index]
            }
          }
        }
        if (op === '') {
          op = 'empty'
        }
        return GetColorByOP(op)
      }
      const retlist = this.retList
      retlist.forEach((d) => {
        d.list.forEach((tk) => {
          opdata[tk] = {
            op: tk,
            parent: d.op
          }
          if (tk.indexOf('_') >= 0) {
            opdata[tk] = {
              op: tk.replace(/_/g, ''),
              parent: d.op
            }
          }
        })
      })
      color.domain(
        retlist.map((d) => {
          return d.op
        })
      )
      // 判断该节点是否可用
      const find = (id) => {
        const names = id.split('/')
        const namesLength = names.length
        if (namesLength === 1) {
          for (let i = 0; i < expandNode.length; i += 1) {
            if (id === expandNode[i].uid) {
              return false
            }
          }
          return true
        }
        let sign = 0
        const pre = names.slice(0, namesLength - 1).join('/')
        for (let i = 0; i < expandNode.length; i += 1) {
          if (pre === expandNode[i].uid) {
            sign = 1
            break
          }
        }
        for (let i = 0; i < expandNode.length; i += 1) {
          if (id === expandNode[i].uid) {
            sign = 0
            break
          }
        }
        if (sign) {
          return true
        }
        return false
      }
      // 保存节点及相关边,sign标记保存入边(0)或出边(1)
      const nodeHold = (nodeUid, edgeUid, srcNode, sign, op, attrs) => {
        // eslint-disable-next-line no-unused-vars
        let index = -1
        for (let i = 0; i < nodeInfo.length; i += 1) {
          if (nodeInfo[i].uid === nodeUid) {
            index = i
            if (sign) {
              if (srcNode) {
                nodeInfo[i].outNode.push(srcNode)
              }
              if (attrs && JSON.stringify(attrs) !== '{}') {
                nodeInfo[i].attr = attrs
              }
              nodeInfo[i].op = op
            } else {
              if (srcNode) {
                nodeInfo[i].inNode.push(srcNode)
              }
              if (attrs && JSON.stringify(attrs) !== '{}') {
                nodeInfo[i].attr = attrs
              }
            }
            return true
          }
        }
        const node = { uid: nodeUid, inNode: [], outNode: [], op: '' }
        if (sign) {
          if (srcNode) {
            node.outNode.push(srcNode)
          }
          node.op = op
          if (attrs && JSON.stringify(attrs) !== '{}') {
            node.attr = attrs
          }
          nodeInfo.push(node)
        } else {
          if (srcNode) {
            node.inNode.push(srcNode)
          }
          if (attrs && JSON.stringify(attrs) !== '{}') {
            node.attr = attrs
          }
          nodeInfo.push(node)
        }
      }
      // 画图
      // eslint-disable-next-line
      const draw = function(data, init) {
        self.lastClick = ''
        self.lastAssistClick = ''
        nodeInfo.splice(0, nodeInfo.length)
        d3.select('#svg-canvas')
          .select('g')
          .selectAll('g')
          .remove()
        const g = new dagreD3.graphlib.Graph({ compound: true })
          .setGraph({})
          .setDefaultEdgeLabel(() => {
            return {}
          })
        data.forEach((v) => {
          v.id = v.uid
          v.clicked = false
          if (v.label) {
            if (v.label.length > 12) {
              if (v.label.search(/\n/g) < 0) {
                v.name = v.label
              }
              v.label = v.name
              let label = `${v.label.slice(0, 13)}\n`
              label +=
                v.label.length > 26
                  ? `...${v.label.substring(v.label.length - 13)}`
                  : `${v.label.substring(13, v.label.length)}`
              v.label = label
            }
          }
          if (find(v.uid)) {
            g.setNode(v.uid, v)
            v.targets.forEach((u) => {
              if (find(u.id)) {
                const edgeLabel = `${v.uid}__${u.id}`
                g.setEdge(v.uid, u.id, { id: edgeLabel, label: u.info, curve: d3.curveBasis })
                isDashed[edgeLabel] = u.control
                isLines[edgeLabel] = u.num
                nodeHold(v.uid, edgeLabel, u.id, 1, v.op, v.attrs)
                nodeHold(u.id, edgeLabel, v.uid, 0, undefined, u.attrs)
              }
            })
            nodeHold(v.uid, '', '', 1, v.op, v.attrs)
          } else {
            v.clusterLabelPos = 'top'
            if (v.name) {
              v.label = v.name
            }
            g.setNode(v.uid, v)
          }
        })
        for (let i = 0; i < expandNode.length; i += 1) {
          const sub = expandNode[i].sub_net
          // eslint-disable-next-line
          sub.forEach((v) => {
            v.id = v.uid
            if (v.label) {
              if (v.label.length > 12) {
                if (v.label.search(/\n/g) < 0) {
                  v.name = v.label
                }
                v.label = v.name
                let label = `${v.label.slice(0, 13)}\n`
                label +=
                  v.label.length > 26
                    ? `...${v.label.substring(v.label.length - 13)}`
                    : `${v.label.substring(13, v.label.length)}`
                v.label = label
              }
            }
            g.setParent(v.uid, expandNode[i].uid)
            if (find(v.uid)) {
              g.setNode(v.uid, v)
              v.targets.forEach((u) => {
                if (find(u.id)) {
                  const edgeLabel = `${v.uid}__${u.id}`
                  g.setEdge(v.uid, u.id, { id: edgeLabel, label: u.info, curve: d3.curveBasis })
                  isDashed[edgeLabel] = u.control
                  isLines[edgeLabel] = u.num
                  nodeHold(v.uid, edgeLabel, u.id, 1, v.op, v.attrs)
                  nodeHold(u.id, edgeLabel, v.uid, 0, undefined)
                }
              })
              nodeHold(v.uid, '', '', 1, v.op, v.attrs)
            } else {
              v.clusterLabelPos = 'top'
              if (v.name) {
                v.label = v.name
              }
              g.setNode(v.uid, v)
            }
          })
        }
        // 设置节点样式
        g.nodes().forEach((v) => {
          const node = g.node(v)
          if (node !== undefined) {
            let fill = GetColorByNode(g, v)
            const expand = expandNode.find((item) => item.uid === v)
            if (expand !== undefined) {
              fill = expand.fill || fill
            }
            node.rx = node.ry = 10
            node.width = 125
            node.height = 20
            node.style = `fill:${fill};rx:12.5px;ry:12.5px;stroke-width:1px;stroke:#696969`
            if (IsDoubleNode(node) && IsDoubleNode(node) !== 4 && self.getCurTag !== 'c_graph') {
              node.height = 50
            }
          }
        })
        for (let i = 0; i < delStageNode.length; i += 1) {
          for (let j = 0; j < delStageNode[i].length; j += 1) {
            g.removeNode(delStageNode[i][j])
          }
        }
        for (let i = 0; i < tmp.length; i += 1) {
          g.removeNode(tmp[i].nodeId)
        }
        // eslint-disable-next-line new-cap
        const render = new dagreD3.render()
        const svg = d3.select('#svg-canvas')
        render(d3.select('#svg-canvas g'), g)
        d3.selectAll('.edgeLabel').style('visibility', 'hidden')
        d3.select('#svg-canvas')
          .attr('width', '100%')
          .attr('height', '100%')
        self.srcData = data
        if (!reserverStageNode.length) {
          const tmp1 = { sign: 1 }
          tmp1.nodeInfo = JSON.parse(JSON.stringify(nodeInfo))
          reserverStageNode.push(tmp1)
          const nnodeInfo = reserverStageNode[0].nodeInfo
          for (let i = 0; i < tmp.length; i += 1) {
            const tmpItem = tmp[i]
            for (let j = nnodeInfo.length - 1; j >= 0; j -= 1) {
              if (nnodeInfo[j].uid === tmpItem.nodeId) {
                nnodeInfo.splice(j, 1)
              } else {
                const { inNode } = nnodeInfo[j]
                const { outNode } = nnodeInfo[j]
                for (let z = 0; z <= inNode.length; z += 1) {
                  if (inNode[z] === tmpItem.nodeId) {
                    inNode.splice(z, 1)
                    break
                  }
                }
                for (let z = 0; z <= outNode.length; z += 1) {
                  if (outNode[z] === tmpItem.nodeId) {
                    outNode.splice(z, 1)
                    break
                  }
                }
              }
            }
          }
        }
        self.reserve = reserverStageNode
        self.curg = g
        // 初次绘制中将图居中,并设置zoom的初始位置
        if (init) {
          init = false
          const canvas = d3.select('#svg-canvas')._groups[0][0]
          const canvasHeight = canvas.scrollHeight
          const canvasWidth = canvas.scrollWidth
          const graph = d3.select('#svg-canvas g')._groups[0][0]
          const graphHeight = graph.getBBox().height
          const graphWidth = graph.getBBox().width
          const index = Math.min(canvasHeight / graphHeight, canvasWidth / graphWidth, 1)
          const scale = `scale(${index})`
          d3.select('#svg-canvas g').attr(
            'transform',
            ` translate(${(canvasWidth - graphWidth * index) / 2},${(canvasHeight -
              graphHeight * index) /
              2}) ${scale}`
          )
          const transform = d3
            .zoomTransform(0)
            .translate(
              (canvasWidth - graphWidth * index) / 2,
              (canvasHeight - graphHeight * index) / 2
            )
            .scale(index)
          d3.zoom().transform(svg, transform)
        }
        edgeLabelAnimation()
        drawAssist('white')
        const zoom = d3.zoom().on('zoom', () => {
          d3.select('#svg-canvas g').attr('transform', d3.event.transform)
        })
        svg.call(zoom).on('dblclick.zoom', null)
        // 自动调节节点位置
        function PosAdaption(itemnode) {
          if (itemnode) {
            const str = d3.select('#svg-canvas g').attr('transform')
            let [xCoor, yCoor] = str.substring(str.indexOf('(') + 1, str.indexOf(')')).split(',')
            const { x: xCurrent, y: yCurrent } = itemnode
            const svgWidth = d3
              .select('#svg-canvas')
              .style('width')
              .replace('px', '')
            const svgHeight = d3
              .select('#svg-canvas')
              .style('height')
              .replace('px', '')
            xCoor = Number(svgWidth) / 2 - xCurrent
            yCoor = Number(svgHeight) / 2 - yCurrent
            d3.select('#svg-canvas g').attr('transform', `translate(${xCoor}, ${yCoor})`)
            const transform = d3.zoomTransform(0).translate(xCoor, yCoor)
            d3.zoom().transform(svg, transform)
          }
        }
        // 确定所有节点对应颜色
        d3.selectAll('.node rect')
          // eslint-disable-next-line
          .style('fill', function(uid) {
            let op = ''
            if (nodedata[uid]) {
              op = nodedata[uid].op
            } else {
              if (g.node(uid)) {
                op = g.node(uid).op
                nodedata[uid] = JSON.parse(JSON.stringify(g.node(uid)))
              }
              if (g.node.sub_net && g.node.sub_net.length) {
                const index = g.node.sub_net.findIndex((e) => e.uid === uid)
                if (index !== -1) {
                  op = g.node.sub_net[index].op
                  nodedata[uid] = JSON.parse(JSON.stringify(g.node.sub_net[index]))
                }
              }
            }
            if (op === '') {
              op = 'empty'
            }
            d3.select(this).attr('op', op)
            return GetColorByOP(op)
          })
        // 绘制虚接节点样式
        DrawVirtualNodes(g, data)
        if (self.getCurTag === 'c_graph') {
          DrawSpecialNodes(g, data)
        }
        if (self.getCurTag === 's_graph') {
          DrawDoubleNodes(g, data)
        }
        self.glitter(self.restoreNode)
        d3.selectAll('.path')
          .style('fill-opacity', 1)
          .style('stroke', 'black')
          .style('stroke-opacity', 1)
          .attr('marker-start', 'url(#dot)')
        // 子节点动作：双击展开，自动调整位置，边框标红
        d3.selectAll('.node').on('dblclick', (v) => {
          if (g.node(v).sub_net.length !== 0) {
            const names = v.split('/')
            const layer = names.length
            const fillCurrent = d3
              .select(`[id="${v}"]`)
              .select('rect')
              .style('fill')
            expandNode.push({
              uid: v,
              layer,
              sub_net: g.node(v).sub_net,
              label: g.node(v).label,
              fill: fillCurrent
            })
            nodeInfo.splice(0, nodeInfo.length)
            reserverStageNode = []
            delStageNode = []
            draw(data, init)
            self.lastClick = ''
            d3.select(`[id="${v}"]`)
              .select('rect')
              .style('stroke-width', '2.5')
              .style('stroke', 'red')
              .style('fill', fillCurrent)
              .style('opacity', '0.8')
            setTimeout(() => {
              d3.select(`[id="${v}"]`)
                .select('rect')
                .style('stroke-width', '1')
                .style('stroke', '#696969')
            }, 1000)
            let currentNode = data.find((item) => item.uid === v)
            if (!currentNode && expandNode && expandNode.length) {
              // eslint-disable-next-line no-labels
              loopExpandNode: for (const expand of expandNode) {
                for (const sub of expand.sub_net) {
                  if (sub.uid === v) {
                    currentNode = sub
                    // eslint-disable-next-line no-labels
                    break loopExpandNode
                  }
                }
              }
            }
            PosAdaption(currentNode)
          }
        })
        // 父节点动作：双击缩小，自动调整位置，边框标红
        d3.selectAll('.cluster')
          .style('fill-opacity', '0.55')
          .attr('font-weight', '600')
          .on('dblclick', (v) => {
            const indexRecord = []
            const names = v.split('/')
            const namesLength = names.length
            for (let i = expandNode.length - 1; i >= 0; i -= 1) {
              const { uid } = expandNode[i]
              const uids = uid.split('/')
              const uidLength = uids.length
              if (uidLength >= namesLength) {
                if (uids.slice(0, namesLength).join('/') === v) {
                  indexRecord.push(i)
                }
              }
              for (let j = 0; j < indexRecord.length; j += 1) {
                expandNode.splice(indexRecord[j], 1)
              }
            }
            nodeInfo.splice(0, nodeInfo.length)
            reserverStageNode = []
            delStageNode = []
            draw(data, init)
            self.lastClick = ''
            d3.select(`[id="${v}"]`)
              .select('rect')
              .style('stroke-width', '1.5')
              .style('stroke', 'red')
            setTimeout(() => {
              d3.select(`[id="${v}"]`)
                .select('rect')
                .style('stroke-width', '1.5')
                .style('stroke', '#696969')
            }, 1000)
            // 获取当前点击节点信息, 如果节点是最外层节点, 在 data 中查找, 否则在扩展节点中的 sub_net 中查找
            let currentNode = data.find((item) => item.uid === v)
            if (!currentNode && expandNode && expandNode.length) {
              // eslint-disable-next-line no-labels
              loopExpandNode: for (const expand of expandNode) {
                for (const sub of expand.sub_net) {
                  if (sub.uid === v) {
                    currentNode = sub
                    // eslint-disable-next-line no-labels
                    break loopExpandNode
                  }
                }
              }
            }
            PosAdaption(currentNode)
          })
        // eslint-disable-next-line
        d3.select('#assist').select('svg').selectAll('g').on('dblclick', function() {
          const nodeId = this.id.split('__')[1]
          self.restoreNode = nodeId
          const index = tmp.findIndex((item) => item.nodeId === nodeId)
          drawAssist('white')
          tmp.splice(index, 1)
          getModifyClick(nodeId)
          draw(data, init)
          // eslint-disable-next-line
        }).on('click', function() {
          const nodeId = this.id.split('__')[1]
          let info = getDelNodeInfo(nodeId, nodeInfo)
          if (self.lastClick) {
            self.restoreLastClick()
          }
          if (self.lastAssistClick && self.lastAssistClick !== this.id) {
            self.restoreLastClickRight()
          }
          if (!info) {
            info = { info: '无信息' }
          } else {
            const { inNode, outNode } = info
            for (let i = 0; i < inNode.length; i += 1) {
              const nodeId = `#${idTransformerFrontend(inNode[i])}`
              if (
                !d3
                  .select(nodeId)
                  .select('rect')
                  .attr('tag')
              ) {
                const old = d3
                  .select(nodeId)
                  .select('rect')
                  .style('fill')
                d3.select(nodeId)
                  .select('rect')
                  .attr('tag', old)
                d3.select(nodeId)
                  .select('rect')
                  .style('fill', 'blue')
                  .attr('dir', 'in')
                drawCircleTag(nodeId, 'out', 1)
              } else {
                const old = d3
                  .select(nodeId)
                  .select('rect')
                  .attr('tag')
                d3.select(nodeId)
                  .select('rect')
                  .style('fill', old)
                d3.select(nodeId)
                  .select('rect')
                  .attr('tag', null)
                drawCircleTag(nodeId, 'out', 0)
              }
            }
            if (self.lastAssistClick === this.id) {
              self.lastAssistClick = ''
            } else {
              self.lastAssistClick = this.id
            }
            for (let i = 0; i < outNode.length; i += 1) {
              const nodeId = `#${idTransformerFrontend(outNode[i])}`
              if (
                !d3
                  .select(nodeId)
                  .select('rect')
                  .attr('tag')
              ) {
                const old = d3
                  .select(nodeId)
                  .select('rect')
                  .style('fill')
                d3.select(nodeId)
                  .select('rect')
                  .attr('tag', old)
                d3.select(nodeId)
                  .select('rect')
                  .style('fill', 'red')
                  .attr('dir', 'out')
                drawCircleTag(nodeId, 'in', 1)
              } else {
                const old = d3
                  .select(nodeId)
                  .select('rect')
                  .attr('tag')
                d3.select(nodeId)
                  .select('rect')
                  .style('fill', old)
                d3.select(nodeId)
                  .select('rect')
                  .attr('tag', null)
                drawCircleTag(nodeId, 'in', 0)
              }
            }
            let initInfo
            for (let i = 0; i < nodeInfo.length; i += 1) {
              if (nodeInfo[i].uid === info.uid) {
                initInfo = nodeInfo[i]
                break
              }
            }
            for (let i = 0; i < tmp.length; i += 1) {
              if (initInfo.inNode.indexOf(tmp[i].nodeId) >= 0) {
                info.inNode.push(tmp[i].nodeId)
                var oldfill = d3
                  .select(
                    `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  )
                  .select('rect')
                  .attr('oldfill')
                if (oldfill) {
                  // oldfill = d3
                  //   .select(
                  //     `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  //   )
                  //   .select('rect')
                  //   .attr('oracle')

                  d3.select(
                    `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  )
                    .select('rect')
                    .attr('dir', null)
                    // .style('fill', oldfill)
                  d3.select(
                    `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  )
                    .select('rect')
                    .attr('oldfill', undefined)

                  colour(`#del__${idTransformerFrontend(tmp[i].nodeId)}`)
                } else {
                  const fill = d3
                    .select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                    .select('rect')
                    .attr('fill')
                  d3.select(
                    `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  )
                    .select('rect')
                    .style('fill', 'blue')
                    .attr('dir', 'in')
                  d3.select(
                    `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  )
                    .select('rect')
                    .attr('oldfill', fill)
                }
              }
              if (initInfo.outNode.indexOf(tmp[i].nodeId) >= 0) {
                info.outNode.push(tmp[i].nodeId)
                var oldfill = d3
                  .select(
                    `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  )
                  .select('rect')
                  .attr('oldfill')
                if (oldfill) {
                  // oldfill = d3
                  //   .select(
                  //     `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  //   )
                  //   .select('rect')
                  //   .attr('oracle')

                  d3.select(
                    `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  )
                    .select('rect')
                    .style('fill', oldfill)
                    .attr('dir', null)
                  d3.select(
                    `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  )
                    .select('rect')
                    .attr('oldfill', undefined)
                  colour(`#del__${idTransformerFrontend(tmp[i].nodeId)}`)
                } else {
                  const fill = d3
                    .select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                    .select('rect')
                    .attr('fill')
                  d3.select(
                    `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  )
                    .select('rect')
                    .style('fill', 'red')
                    .attr('dir', 'out')
                  d3.select(
                    `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                  )
                    .select('rect')
                    .attr('oldfill', fill)
                }
              }
            }
          }
          getInfo(JSON.stringify(info))
        })
        // 功能：为每个节点添加动画
        svg.selectAll('.node')._groups[0].forEach((nodeKey) => {
          let nodeName = nodeKey.id
          const nodes = g.node(nodeKey.id)
          const edges = g.nodeEdges(nodeKey.id)
          nodeName = nodeName.split('/')
          nodeName = nodeName[nodeName.length - 1]
          nodeName = nodeName.slice(0, nodeName.length)
          const nodeId = idTransformerFrontend(nodeKey.id)
          const nodeThis = d3.select(nodeKey)
          let currName = ''
          let nodeFromID = ''
          let nodeToID = ''
          nodeThis.append('text')
          nodeThis.style('cursor', 'context-menu')
          const width = parseInt(
            d3
              .select(`#${nodeId}`)
              .select('rect')
              .style('width'),
            10
          )
          const height = parseInt(
            d3
              .select(`#${nodeId}`)
              .select('rect')
              .style('height'),
            10
          )
          if (nodes.sub_net.length > 0) {
            let isexpand = false
            for (let i = 0; i < expandNode.length; i += 1) {
              if (nodeId === expandNode[i].uid) {
                isexpand = true
              }
            }
            const size = d3
              .select(`#${nodeId}`)
              .selectAll('text.expand')
              .size()
            if (size <= 0) {
              d3.select(`#${nodeId}`)
                .append('text')
                .attr('class', 'expand')
                .attr('x', width / 2 - 15)
                .attr('y', -height / 2 + 12)
                .style('font-size', '14px')
                .style('fill', 'white')
                .attr('font-weight', 'bold')
            }
            if (!isexpand) {
              d3.select(`#${nodeId}`)
                .selectAll('text.expand')
                .text('+')
            }
          }
          nodeThis.on('mouseover', () => {
            const tag = Number(d3.select(`#${nodeId}`).attr('flag'))
            if (tag) {
              return
            }
            // 快速预览悬浮窗
            d3.select(`#${nodeId}`).attr('flag', 1)
            const oldLength = d3
              .select(`#${nodeId}`)
              .select('.label')
              .select('g')
              .select('text')
              .select('tspan')._groups[0][0].textLength.baseVal.value
            const newLength = d3
              .select(`#${nodeId}`)
              .select('.label')
              .select('g')
              .select('text')
              .select('tspan')._groups[0][0].textLength.baseVal.value
            const gap = (newLength - oldLength) / 2
            const nodeTransform = d3.select(`#${nodeId}`).attr('transform')
            const messageBox = d3
              .select('.nodes')
              .append('g')
              .attr('id', 'messageBox')
              .attr('transform', nodeTransform)
            const boxComponent = messageBox.append('g').attr('id', 'boxComponent')
            const nodeWidth = d3.select(`#${nodeId}`).attr('width')
            const nodeHeight = d3.select(`#${nodeId}`).attr('height')
            const nodeheight = parseInt(
              d3
                .select(`#${nodeId}`)
                .select('rect')
                .style('height'),
              10
            )
            let obj
            for (let i = 0; i < nodeInfo.length; i += 1) {
              if (nodeInfo[i].uid === nodeKey.id) {
                obj = nodeInfo[i]
                break
              }
            }
            const info = {}
            info['NODE PROPERTIES'] = {}
            const index = obj.uid.lastIndexOf('/')
            info['NODE PROPERTIES'].name = obj.uid.substring(index + 1, obj.uid.length)
            if (obj.op) {
              info['NODE PROPERTIES'].op = obj.op
            }
            const TEXT = boxComponent
              .append('text')
              .attr('font-size', '14px')
              .attr('fill', 'white')
            let count = 0
            let maxLength = 0
            let Count = 0
            for (const i in info) {
              const length = TEXT.append('tspan')
                .attr('x', '0')
                .attr('y', count * 14 + Count * 10)
                .text(i)._groups[0][0].textLength.baseVal.value
              if (length > maxLength) {
                maxLength = length
              }
              count += 1
              for (const j in info[i]) {
                const message = `● ${j}:${info[i][j]}`
                const length = TEXT.append('tspan')
                  .attr('x', '0')
                  .attr('y', count * 20 + Count * 10)
                  .text(message)._groups[0][0].textLength.baseVal.value
                if (length > maxLength) {
                  maxLength = length
                }
                count += 1
              }
              Count += 1
            }
            boxComponent
              .insert('rect', 'text')
              .attr('height', count * 20 + 15 + Count * 10)
              .attr('width', maxLength + 50)
              .attr('fill', 'white')
              .attr('transform', 'translate(-25,-24)')
              .attr('rx', 3)
              .attr('ry', 3)
              .attr('fill', '#004986')
              .style('opacity', '0.40')
            const boxComponentX = nodeWidth / 2
            let boxComponentY = -nodeHeight / 2 - (count * 14 + 20 + Count * 10) - 15
            if (nodeheight === 70) {
              boxComponentY = -nodeHeight / 2 - (count * 14 + 20 + Count * 10) - 30
            }
            boxComponent.attr('transform', `translate(${boxComponentX},${boxComponentY})`)
            d3.select(`#${nodeId}`)
              .select('.label')
              .select('g')
              .select('text')
              .attr('transform', `translate(${-gap},0)`)
            if (
              d3
                .select(`#${nodeId}`)
                .select('rect')
                .style('fill') === 'rgb(102, 102, 102)'
            ) {
              d3.select(`#${nodeId}`)
                .select('rect')
                .style('fill', 'rgb(102, 102, 102)')
            } else {
              d3.select(`#${nodeId}`)
                .select('rect')
                .style('opacity', '1')
            }
            if (
              d3
                .select(`#${nodeId}`)
                .select('rect')
                .style('stroke') === 'red'
            ) {
              d3.select(`#${nodeId}`)
                .select('rect')
                .style('stroke-width', '2.5')
                .style('stroke', 'red')
            } else {
              d3.select(`#${nodeId}`)
                .select('rect')
                .style('stroke-width', '2.5')
                .style('stroke', '#e4007f')
            }
          })
          nodeThis.on('mouseleave', () => {
            if (nodeName.length > 12) {
              currName = `${nodeName.slice(0, 12)}...`
            } else {
              currName = nodeName
            }
            d3.select(`#${nodeId}`).attr('flag', 0)
            d3.select(`#${nodeId}`)
              .select('.label')
              .select('g')
              .select('text')
              .select('tspan')
              .text(currName)
            d3.select(`#${nodeId}`)
              .select('.label')
              .select('g')
              .select('text')
              .attr('transform', 'translate(0,0)')
            d3.select('#messageBox').remove()
            if (
              d3
                .select(`#${nodeId}`)
                .select('rect')
                .style('fill') === 'rgb(102, 102, 102)'
            ) {
              d3.select(`#${nodeId}`)
                .select('rect')
                .style('fill', 'rgb(102, 102, 102)')
            } else if (
              d3
                .select(`#${nodeId}`)
                .select('rect')
                .style('fill') === 'blue'
            ) {
              d3.select(`#${nodeId}`)
                .select('rect')
                .style('fill', 'blue')
            } else if (
              d3
                .select(`#${nodeId}`)
                .select('rect')
                .style('fill') === 'red'
            ) {
              d3.select(`#${nodeId}`)
                .select('rect')
                .style('fill', 'red')
            } else {
              d3.select(`#${nodeId}`)
                .select('rect')
                .style('fill', GetColorByNode(g, nodes))
              // 1:卷积层,2:全连接层，3：池化层，4：归一化
              const nodeColor = { 1: '#e8c5df', 2: '#b7d4ae', 3: '#d7dafb', 4: '#daf4cc' }
              const nodeType = IsSpecialNode(nodes) || IsDoubleNode(nodes)
              if (nodeType in nodeColor) {
                d3.select(`#${nodeId}`)
                  .select('rect')
                  .style('fill', nodeColor[nodeType])
              }
            }
            if (
              d3
                .select(`#${nodeId}`)
                .select('rect')
                .style('stroke') === 'red'
            ) {
              d3.select(`#${nodeId}`)
                .select('rect')
                .style('stroke-width', '1')
                .style('stroke', 'red')
            } else {
              d3.select(`#${nodeId}`)
                .select('rect')
                .style('stroke-width', '1')
                .style('stroke', '#696969')
            }
          })
          nodeThis.on('click', () => {
            const reserverStageNode = self.reserve
            if (!g.node(nodeKey.id).clicked) {
              if (self.lastClick) {
                self.restoreLastClick()
              }
              if (self.lastAssistClick) {
                self.restoreLastClickRight()
              }
              self.lastAssistClick = ''
              self.lastClick = nodeKey.id
              g.node(nodeKey.id).clicked = true
              edges.forEach((v) => {
                const edgeID = `${v.v}__${v.w}`
                const edgeGroup = Array.from(d3.selectAll('.edgePath')._groups[0])
                // const edgeLabelGroup = d3.selectAll('.edgeLabel')._groups[0]
                let index
                for (let i = 0; i < edgeGroup.length; i += 1) {
                  if (edgeGroup[i].id === edgeID) {
                    index = i
                    break
                  }
                }
                const dEdgeID = `#${idTransformerFrontend(edgeID)}`
                d3.select(dEdgeID)
                  .select('.path')
                  .style('stroke', 'red')
                  .style('stroke-width', '1.5')
                // d3.select(edgeLabelGroup[index])
                //   .select('g')
                //   .select('text')
                //   .attr('fill', 'red')
                nodeFromID = `#${idTransformerFrontend(v.v)}`
                nodeToID = `#${idTransformerFrontend(v.w)}`
                d3.select(nodeFromID)
                  .select('rect')
                  .style('stroke', 'red')
                d3.select(nodeToID)
                  .select('rect')
                  .style('stroke', 'red')
              })
              var coldfill = d3.select(`#${idTransformerFrontend(nodeKey.id)}`)
                .select('rect')
                .style('fill')
              d3.select(`#${idTransformerFrontend(nodeKey.id)}`)
                .select('rect')
                .style('stroke', 'red')
                .style('fill', 'rgb(102, 102, 102)')
                .attr('coldfill', coldfill)
                .attr('clicked', 'clicked')

              let info
              if (reserverStageNode.length) {
                const cur = reserverStageNode[reserverStageNode.length - 1]
                const curNodeInfo = cur.nodeInfo
                for (let i = 0; i < curNodeInfo.length; i += 1) {
                  if (curNodeInfo[i].uid === nodeKey.id) {
                    info = JSON.parse(JSON.stringify(curNodeInfo[i]))
                    break
                  }
                }
              }
              let initInfo
              for (let i = 0; i < nodeInfo.length; i += 1) {
                if (nodeInfo[i].uid === nodeKey.id) {
                  initInfo = nodeInfo[i]
                  break
                }
              }
              for (let i = 0; i < tmp.length; i += 1) {
                if (initInfo.inNode.indexOf(tmp[i].nodeId) >= 0) {
                  info.inNode.push(tmp[i].nodeId)
                  var oldfill = d3
                    .select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                    .select('rect')
                    .attr('oldfill')
                  if (oldfill) {
                    // oldfill = d3
                    //   .select(
                    //     `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    //   )
                    //   .select('rect')
                    //   .attr('oracle')

                    d3.select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                      .select('rect')
                      // .style('fill', oldfill)
                      .attr('dir', null)
                    d3.select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                      .select('rect')
                      .attr('oldfill', undefined)
                    colour(`#del__${idTransformerFrontend(tmp[i].nodeId)}`)
                  } else {
                    const fill = d3
                      .select(
                        `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                      )
                      .select('rect')
                      .attr('fill')
                    d3.select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                      .select('rect')
                      .attr('dir', 'in')
                      .style('fill', 'blue')

                    d3.select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                      .select('rect')
                      .attr('oldfill', fill)
                  }
                }
                if (initInfo.outNode.indexOf(tmp[i].nodeId) >= 0) {
                  info.outNode.push(tmp[i].nodeId)
                  var oldfill = d3
                    .select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                    .select('rect')
                    .attr('oldfill')
                  if (oldfill) {
                    // oldfill = d3
                    //   .select(
                    //     `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    //   )
                    //   .select('rect')
                    //   .attr('oracle')

                    d3.select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                      .select('rect')
                      .attr('dir', null)
                      // .style('fill', oldfill)
                    d3.select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                      .select('rect')
                      .attr('oldfill', undefined)
                    colour(`#del__${idTransformerFrontend(tmp[i].nodeId)}`)
                  } else {
                    const fill = d3
                      .select(
                        `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                      )
                      .select('rect')
                      .attr('fill')
                    d3.select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                      .select('rect')
                      .attr('dir', 'out')
                      .style('fill', 'red')

                    d3.select(
                      `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                    )
                      .select('rect')
                      .attr('oldfill', fill)
                  }
                }
              }
              getInfo(JSON.stringify(info))
            } else {
              g.node(nodeKey.id).clicked = false
              self.restoreLastClick()
            }
          })
        })
        svg.selectAll('.cluster')._groups[0].forEach((nodeKey) => {
          const nodeId = idTransformerFrontend(nodeKey.id)
          const nodeThis = d3.select(nodeKey)
          nodeThis.append('text')
          const width = parseInt(
            d3
              .select(`#${nodeId}`)
              .select('rect')
              .style('width'),
            10
          )
          const height = parseInt(
            d3
              .select(`#${nodeId}`)
              .select('rect')
              .style('height'),
            10
          )
          const size = d3
            .select(`#${nodeId}`)
            .selectAll('text.expand')
            .size()
          if (size <= 0) {
            d3.select(`#${nodeId}`)
              .append('text')
              .attr('class', 'expand')
              .attr('x', width / 2 - 35)
              .attr('y', -height / 2 + 30)
              .style('font-weight', 'lighter')
              .style('font-size', '50px')
              .style('fill', 'white')
          }
          d3.select(`#${nodeId}`)
            .selectAll('text.expand')
            .text('-')
        })
        // 为控制边添加虚线
        g.edges().forEach((v) => {
          const edgeID = `${v.v}__${v.w}`
          const dEdgeID = `#${idTransformerFrontend(edgeID)}`
          if (isDashed[edgeID] === 'true') {
            d3.select(dEdgeID)
              .select('.path')
              .style('stroke-dasharray', '5,3')
          }
          if (Number(isLines[edgeID]) > 1) {
            d3.select(dEdgeID)
              .select('.path')
              .style('stroke-width', '2')
          }
        })
        colorCopy()
        $('#draw').contextMenu({
          selector: '.node',
          items: {
            invisible: {
              name: '隐藏相关边',
              icon: 'edit',
              callback() {
                const nodeId = this[0].id
                const edges = self.curg.nodeEdges(nodeId)
                var oldfill = d3
                  .select(`[id='${nodeId}']`)
                  .select('rect')
                  .attr('coldfill')
                if (oldfill === null) {
                  oldfill = d3
                    .select(`[id='${nodeId}']`)
                    .select('rect')
                    .style('fill')
                }

                if (
                  d3
                    .select(`[id='${nodeId}']`)
                    .select('rect')
                    .attr('oldfill')
                ) {
                  return
                }
                d3.select(`[id='${nodeId}']`)
                  .select('rect')
                  .attr('oldfill', oldfill)
                d3.select(`[id='${nodeId}']`)
                  .select('rect')
                  .style('fill', 'rgb(102, 102, 102)')
                  .attr('edit', 'edit')
                  .attr('clicked', null)
                // const edgeGroup = Array.from(d3.selectAll('.edgePath')._groups[0])
                // const edgeLabelGroup = d3.selectAll('.edgeLabel')._groups[0]
                edges.forEach((v) => {
                  const edgeId = idTransformerFrontend(`#${`${v.v}__${v.w}`}`)
                  d3.select(edgeId)
                    // .select('.path')
                    // .style('stroke', 'black')
                    .style('visibility', 'hidden')
                  // const edgeDom = document.getElementById(`${v.v}__${v.w}`)
                  // const index = edgeGroup.indexOf(edgeDom)
                  // edgeLabelGroup[index].attributes.style.value = 'opacity: 1;visibility:hidden'
                })
              }
            },
            visible: {
              name: '显示相关边',
              icon: 'cut',
              callback() {
                const nodeId = this[0].id
                const edges = self.curg.nodeEdges(nodeId)
                var oldfill = d3
                  .select(`[id='${nodeId}']`)
                  .select('rect')
                  .attr('oldfill')
                if (!oldfill) {
                  return
                }
                d3.select(`[id='${nodeId}']`)
                  .select('rect')
                  .attr('oldfill', null)
                // const dir = d3.select(`[id='${nodeId}']`)
                //   .select('rect')
                //   .attr('dir')
                // oldfill = d3
                //   .select(`[id='${nodeId}']`)
                //   .select('rect')
                //   .attr('oracle')
                d3.select(`[id='${nodeId}']`)
                  .select('rect')
                  // .style('fill', oldfill)
                  .attr('edit', null)
                  .attr('clicked', null)
                colour(`[id='${nodeId}']`)
                const edgeGroup = Array.from(d3.selectAll('.edgePath')._groups[0])
                // const edgeLabelGroup = d3.selectAll('.edgeLabel')._groups[0]
                edges.forEach((v) => {
                  const edgeId = idTransformerFrontend(`#${`${v.v}__${v.w}`}`)
                  d3.select(edgeId)
                    // .select('.path')
                    .style('visibility', 'visible')
                  const edgeDom = document.getElementById(`${v.v}__${v.w}`)
                  const index = edgeGroup.indexOf(edgeDom)
                  // edgeLabelGroup[index].attributes.style.value = 'opacity: 1;visibility:visible'
                })
              }
            },
            delete: {
              name: '隐藏节点',
              icon: 'delete',
              callback() {
                const { nodeInfo } = self
                // eslint-disable-next-line no-unused-vars
                const g = self.curg
                // eslint-disable-next-line no-unused-vars
                let delNode = []
                for (let i = 0; i < nodeInfo.length; i += 1) {
                  if (nodeInfo[i].uid === this[0].id) {
                    delNode = nodeInfo[i]
                  }
                }
                const nodeId = this[0].id
                const reserverStageNode = self.reserve
                if (self.lastClick) {
                  self.restoreLastClick()
                }
                if (self.lastAssistClick) {
                  self.restoreLastClickRight()
                }
                self.lastClick = ''
                self.lastAssistClick = ''
                var oldfill = d3
                  .select(`[id='${nodeId}']`)
                  .select('rect')
                  .attr('oracle')
                if (oldfill === null || oldfill === undefined) {
                  oldfill = d3
                    .select(`[id='${nodeId}']`)
                    .select('rect')
                    .style('fill')
                }
                for (let i = 0; i < reserverStageNode.length; i += 1) {
                  const curNodeInfo = reserverStageNode[i].nodeInfo
                  for (let j = curNodeInfo.length - 1; j >= 0; j -= 1) {
                    if (curNodeInfo[j].uid === nodeId) {
                      curNodeInfo.splice(j, 1)
                    } else {
                      const { inNode, outNode } = curNodeInfo[j]
                      for (let k = 0; k < inNode.length; k += 1) {
                        if (inNode[k] === nodeId) {
                          inNode.splice(k, 1)
                          break
                        }
                      }
                      for (let k = 0; k < outNode.length; k += 1) {
                        if (outNode[k] === nodeId) {
                          outNode.splice(k, 1)
                          break
                        }
                      }
                    }
                  }
                }
                tmp.push({ nodeId, color: oldfill })
                drawAssist(oldfill)
                // eslint-disable-next-line
                  d3.select('#assist').select('svg').selectAll('g').on('dblclick', function() {
                  const nodeId = this.id.split('__')[1]
                  const index = tmp.findIndex((item) => item.nodeId === nodeId)
                  self.restoreNode = nodeId
                  tmp.splice(index, 1)
                  drawAssist(oldfill)
                  getModifyClick(nodeId)
                  draw(self.copy[0], init)
                  // eslint-disable-next-line
                  }).on('click', function() {
                  if (self.lastClick) {
                    self.restoreLastClick()
                  }
                  self.lastClick = ''
                  if (self.lastAssistClick && self.lastAssistClick !== this.id) {
                    self.restoreLastClickRight()
                  }
                  const nodeId = this.id.split('__')[1]
                  if (self.lastAssistClick === this.id) {
                    self.lastAssistClick = ''
                  } else {
                    self.lastAssistClick = this.id
                  }
                  let info = getDelNodeInfo(nodeId, nodeInfo)
                  if (!info) {
                    info = { info: '无信息' }
                  } else {
                    const { inNode, outNode } = info
                    for (let i = 0; i < inNode.length; i += 1) {
                      const nodeId = `#${idTransformerFrontend(inNode[i])}`
                      if (
                        !d3
                          .select(nodeId)
                          .select('rect')
                          .attr('tag')
                      ) {
                        const old = d3
                          .select(nodeId)
                          .select('rect')
                          .style('fill')
                        d3.select(nodeId)
                          .select('rect')
                          .attr('tag', old)
                        d3.select(nodeId)
                          .select('rect')
                          .style('fill', 'blue')
                          .attr('dir', 'in')
                        drawCircleTag(nodeId, 'out', 1)
                      } else {
                        // const old = d3
                        //   .select(nodeId)
                        //   .select('rect')
                        //   .attr('tag')
                        d3.select(nodeId)
                          .select('rect')
                          // .style('fill', old)
                          .attr('dir', null)
                        d3.select(nodeId)
                          .select('rect')
                          .attr('tag', null)
                        colour(nodeId)
                        drawCircleTag(nodeId, 'out', 0)
                      }
                    }
                    for (let i = 0; i < outNode.length; i += 1) {
                      const nodeId = `#${idTransformerFrontend(outNode[i])}`
                      if (
                        !d3
                          .select(nodeId)
                          .select('rect')
                          .attr('tag')
                      ) {
                        const old = d3
                          .select(nodeId)
                          .select('rect')
                          .style('fill')
                        d3.select(nodeId)
                          .select('rect')
                          .attr('tag', old)
                        d3.select(nodeId)
                          .select('rect')
                          .style('fill', 'red')
                          .attr('dir', 'out')
                        drawCircleTag(nodeId, 'in', 1)
                      } else {
                        // const old = d3
                        //   .select(nodeId)
                        //   .select('rect')
                        //   .attr('tag')
                        d3.select(nodeId)
                          .select('rect')
                          // .style('fill', old)
                          .attr('dir', null)
                        d3.select(nodeId)
                          .select('rect')
                          .attr('tag', null)
                        colour(nodeId)
                        drawCircleTag(nodeId, 'in', 0)
                      }
                    }
                    let initInfo
                    for (let i = 0; i < nodeInfo.length; i += 1) {
                      if (nodeInfo[i].uid === info.uid) {
                        initInfo = nodeInfo[i]
                        break
                      }
                    }
                    for (let i = 0; i < tmp.length; i += 1) {
                      if (initInfo.inNode.indexOf(tmp[i].nodeId) >= 0) {
                        info.inNode.push(tmp[i].nodeId)
                        var oldfill = d3
                          .select(
                            `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          )
                          .select('rect')
                          .attr('oldfill')
                          // .attr('orcale')
                        if (oldfill) {
                          oldfill = d3
                            .select(
                              `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                            )
                            .select('rect')
                            .attr('orcale')

                          d3.select(
                            `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          )
                            .select('rect')
                            .style('fill', oldfill)
                            .attr('dir', null)
                          d3.select(
                            `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          )
                            .select('rect')
                            .attr('oldfill', undefined)
                        } else {
                          const fill = d3
                            .select(
                              `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                            )
                            .select('rect')
                            .attr('fill')
                          d3.select(
                            `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          )
                            .select('rect')
                            .style('fill', 'blue')
                            .attr('dir', 'in')
                          d3.select(
                            `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          )
                            .select('rect')
                            .attr('oldfill', fill)
                        }
                      }
                      if (initInfo.outNode.indexOf(tmp[i].nodeId) >= 0) {
                        info.outNode.push(tmp[i].nodeId)
                        var oldfill = d3
                          .select(
                            `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          )
                          .select('rect')
                          .attr('oldfill')
                        if (oldfill) {
                          // oldfill = d3
                          //   .select(
                          //     `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          //   )
                          //   .select('rect')
                          //   .attr('oracle')

                          d3.select(
                            `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          )
                            .select('rect')
                            // .style('fill', oldfill)
                            .attr('dir', null)
                          d3.select(
                            `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          )
                            .select('rect')
                            .attr('oldfill', undefined)
                          colour(`#del__${idTransformerFrontend(tmp[i].nodeId)}`)
                        } else {
                          const fill = d3
                            .select(
                              `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                            )
                            .select('rect')
                            .attr('fill')
                          d3.select(
                            `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          )
                            .select('rect')
                            .style('fill', 'red')
                            .attr('dir', 'out')
                          d3.select(
                            `#del__${idTransformerFrontend(tmp[i].nodeId)}`
                          )
                            .select('rect')
                            .attr('oldfill', fill)
                        }
                      }
                    }
                  }
                  getInfo(JSON.stringify(info))
                })
                const edges = d3.selectAll('.edgePath')._groups[0]
                const edgeLabel = d3.selectAll('.edgeLabel')._groups[0]
                for (let i = 0; i < edges.length; i += 1) {
                  const v2w = edges[i].id.split('__')
                  if (v2w[0] === nodeId) {
                    edgeLabel[i].getElementsByTagName('g')[0].style.opacity = '0'
                    edges[i].children[0].style = 'opacity: 1;visibility:hidden'
                  }
                  if (v2w[1] === nodeId) {
                    edgeLabel[i].getElementsByTagName('g')[0].style.opacity = '0'
                    edges[i].children[0].style = 'opacity: 1;visibility:hidden'
                  }
                }
                d3.select(
                  `#${idTransformerFrontend(nodeId)}`
                ).style('visibility', 'hidden')
                changeTag = 1
                self.curg.removeNode(nodeId)
              }
            }
          }
        })
      }
      const init = true

      draw(data, init)
    },
    getDelNodeInfo(nodeID) {
      function subSet(arr1, arr2) {
        const set1 = new Set(arr1)
        const set2 = new Set(arr2)
        const subset = []
        for (const item of set1) {
          if (!set2.has(item)) {
            subset.push(item)
          }
        }
        return subset
      }
      const reserverStageNode = this.reserve
      const { nodeInfo } = this
      const { length } = nodeInfo
      let node
      for (let i = 0; i < length; i += 1) {
        if (nodeInfo[i].uid === nodeID) {
          node = JSON.parse(JSON.stringify(nodeInfo[i]))
          break
        }
      }
      if (!node) {
        return
      }
      const { inNode, outNode } = node
      const lastStageNode = reserverStageNode[reserverStageNode.length - 1].nodeInfo
      const curNodes = []
      lastStageNode.forEach((v) => {
        curNodes.push(v.uid)
      })
      const inSub = subSet(inNode, curNodes)
      const outSub = subSet(outNode, curNodes)
      node.inNode = subSet(inNode, inSub)
      node.outNode = subSet(outNode, outSub)
      return node
    },
    drawAssist() {
      if (tmp.length) {
        d3.select('#assist').style('display', 'flex')
      } else {
        d3.select('#assist').style('display', 'none')
        return
      }
      d3.select('#assist')
        .select('svg')
        .selectAll('g')
        .remove()
      let maxlength = 0
      for (let i = 0; i < tmp.length; i += 1) {
        const item = tmp[i]
        let nodeName = item.nodeId
        // eslint-disable-next-line
        const index = nodeName.lastIndexOf('\/');
        nodeName = nodeName.substring(index + 1, nodeName.length)
        const rectWidth = 12 * nodeName.length + 20
        if (rectWidth > maxlength) {
          maxlength = rectWidth
        }
        const g = d3
          .select('#assist')
          .select('svg')
          .append('g')
          .attr('transform', `translate(${0},${50 * i + 20})`)
          .attr('id', `del__${item.nodeId}`)
        g.append('rect')
          .attr('width', rectWidth)
          .attr('height', 25)
          .attr('fill', item.color)
          .attr('stroke-width', '0.5px')
          .attr('rx', 12.5)
          .attr('ry', 12.5)
          .attr('stroke', '#696969')
          .attr('orcale', item.color)
        g.append('text')
          .text(nodeName)
          .attr('dy', '1em')
          .attr('text-anchor', 'middle')
          .attr('transform', `translate(${rectWidth / 2},0)`)
      }
      d3.select('#assist')
        .select('svg')
        .attr('width', maxlength)
        .attr('height', 50 * tmp.length + 50)
    },
    getModifyClick(val) {
      let ob
      const { nodeInfo } = this
      let obsec
      for (let i = 0; i < nodeInfo.length; i += 1) {
        if (nodeInfo[i].uid === val) {
          obsec = ob = nodeInfo[i]
          break
        }
      }
      if (!ob) {
        return
      }
      const reserverStageNode = this.reserve
      const { inNode, outNode } = ob
      for (let i = reserverStageNode.length - 1; i >= 0; i -= 1) {
        if (reserverStageNode[i].sign === 1) {
          reserverStageNode.splice(i + 1, reserverStageNode.length - i - 1)
          break
        }
      }
      for (let i = 0; i < reserverStageNode.length; i += 1) {
        obsec.inNode = []
        obsec.outNode = []
        for (let j = 0; j < reserverStageNode[i].nodeInfo.length; j += 1) {
          const curNode = reserverStageNode[i].nodeInfo[j]
          for (let z = 0; z < inNode.length; z += 1) {
            if (curNode.uid === inNode[z]) {
              curNode.outNode.push(ob.uid)
              obsec.inNode.push(curNode.uid)
              break
            }
          }
          for (let z = 0; z < outNode.length; z += 1) {
            if (curNode.uid === outNode[z]) {
              curNode.inNode.push(ob.uid)
              obsec.outNode.push(curNode.uid)
              break
            }
          }
        }
        reserverStageNode[i].nodeInfo.push(obsec)
      }
      for (let i = 0; i < clickDel.length; i += 1) {
        if (clickDel[i].uid === ob.uid) {
          clickDel.splice(i, 1)
        }
      }
    },
    glitter(val) {
      const { idTransformerFrontend, colorCopy } = this
      if (!val) {
        return
      }
      const nodeId = `#${idTransformerFrontend(val)}`
      const node = d3.select(nodeId)
      // eslint-disable-next-line
      if(!node["_groups"][0][0]) {
        this.restoreNode = ''
        return
      }
      this.restoreNode = ''
      if (node) {
        let old = ''
        old = d3
          .select(nodeId)
          .select('rect')
          .style('fill')
        d3.select(nodeId)
          .select('rect')
          .style('fill', 'red')
        setTimeout(() => {
          old &&
            d3
              .select(nodeId)
              .select('rect')
              .style('fill', old),
          colorCopy()
        }, 1000)
      }
    },
    drawCircleTag(nodeId, dir, flag) {
      const node = d3.select(nodeId)
      if (flag) {
        const cx = 0
        const nodeRect = node.select('rect')
        let cy = nodeRect._groups[0][0].attributes.height.value
        cy = Number(cy) / 2
        if (dir === 'out') {
          node
            .append('circle')
            .attr('cx', cx)
            .attr('cy', cy)
            .attr('r', 4)
            .attr('fill', 'blue')
        } else if (dir === 'in') {
          node
            .append('circle')
            .attr('cx', cx)
            .attr('cy', -cy)
            .attr('r', 4)
            .attr('fill', 'red')
        }
      } else {
        node.select('circle').remove()
      }
    },
    hidden() {
      const { idTransformerFrontend } = this
      const reserverStageNode = this.reserve
      const stages = reserverStageNode.length
      let curStage
      const waiting = []
      if (stages === 0) {
        curStage = { sign: 0 }
        curStage.nodeInfo = JSON.parse(JSON.stringify(this.nodeInfo))
      } else if (reserverStageNode[stages - 1].sign === 0) {
        this.pre()
        curStage = JSON.parse(JSON.stringify(reserverStageNode[stages - 2]))
        curStage.sign = 0
      } else {
        curStage = JSON.parse(JSON.stringify(reserverStageNode[stages - 1]))
        curStage.sign = 0
      }
      const cNodeInfo = curStage.nodeInfo
      for (let i = 0; i < cNodeInfo.length; i += 1) {
        // eslint-disable-next-line
        let input = cNodeInfo[i].inNode.length
        // eslint-disable-next-line
        let output = cNodeInfo[i].outNode.length
        // eslint-disable-next-line
        let res = eval(this.reg)
        if (res) {
          waiting.push(cNodeInfo[i].uid)
        }
      }
      if (waiting.length === 0) {
        return
      }
      const edgeGroup = Array.from(d3.selectAll('.edgePath')._groups[0])
      // const edgeLabelGroup = d3.selectAll('.edgeLabel')._groups[0]
      for (let i = 0; i < waiting.length; i += 1) {
        const edges = this.curg.nodeEdges(waiting[i])
        edges.forEach((v) => {
          const edgeId = idTransformerFrontend(`#${`${v.v}__${v.w}`}`)
          d3.select(edgeId)
            // .select('.path')
            .style('visibility', 'hidden')
          const edgeDom = document.getElementById(`${v.v}__${v.w}`)
          const index = edgeGroup.indexOf(edgeDom)
          // edgeLabelGroup[index].attributes.style.value = 'opacity: 1;visibility:hidden'
        })
        const nodeId = idTransformerFrontend(`#${waiting[i]}`)
        d3.select(nodeId).style('visibility', 'hidden')
      }
      for (let i = cNodeInfo.length - 1; i >= 0; i -= 1) {
        let tag = 1
        for (let j = 0; j < waiting.length; j += 1) {
          if (cNodeInfo[i].uid === waiting[j]) {
            tag = 0
            cNodeInfo.splice(i, 1)
            break
          }
        }
        if (tag) {
          const { inNode, outNode } = cNodeInfo[i]
          for (let j = outNode.length - 1; j >= 0; j -= 1) {
            for (let k = 0; k < waiting.length; k += 1) {
              if (outNode[j] === waiting[k]) {
                outNode.splice(j, 1)
              }
            }
          }
          for (let j = inNode.length - 1; j >= 0; j -= 1) {
            for (let k = 0; k < waiting.length; k += 1) {
              if (inNode[j] === waiting[k]) {
                inNode.splice(j, 1)
              }
            }
          }
        }
      }
      reserverStageNode.push(curStage)
      delStageNode.push(waiting)
    },
    run() {
      const stages = reserverStageNode.length
      const curStage = JSON.parse(JSON.stringify(reserverStageNode[stages - 1]))
      curStage.sign = 1
      let hiddenLayer = 0
      let tag = 1
      for (let i = stages - 1; i >= 0; i -= 1) {
        if (reserverStageNode[i].sign === 1) {
          tag = 0
          hiddenLayer = stages - 1 - i
          if (hiddenLayer === 0 && changeTag === 0) {
            return
          }
          reserverStageNode.splice(i + 1, hiddenLayer)
          break
        }
      }
      if (tag) {
        hiddenLayer = reserverStageNode.length
        reserverStageNode.splice(0, hiddenLayer)
      }
      reserverStageNode.push(curStage)
      let delNode = []
      const len = delStageNode.length
      for (let i = 0; i < hiddenLayer; i += 1) {
        delNode = delNode.concat(delStageNode[len - 1 - i])
      }
      delStageNode.splice(len - hiddenLayer, hiddenLayer)
      changeTag = 0
      delStageNode.push(delNode)
      this.drawGraph()
    },
    pre() {
      const { length } = reserverStageNode
      const { idTransformerFrontend } = this
      let lastSign = -1
      if (length === 1) {
        return
      }
      for (let i = reserverStageNode.length - 1; i >= 1; i -= 1) {
        if (reserverStageNode[i].sign === 1) {
          lastSign = i
          break
        }
      }
      if (lastSign === length - 1) {
        reserverStageNode.splice(lastSign, 1)
        delStageNode.splice(delStageNode.length - 1, 1)
        this.drawGraph()
      } else {
        reserverStageNode.splice(length - 1, 1)
        const waiting = delStageNode.splice(-1, 1)[0]
        for (let i = 0; i < waiting.length; i += 1) {
          const tNodeInfo = this.getDelNodeInfo(waiting[i])
          const edges = []
          for (let j = 0; j < tNodeInfo.inNode.length; j += 1) {
            edges.push(`${tNodeInfo.inNode[j]}__${waiting[i]}`)
          }
          for (let j = 0; j < tNodeInfo.outNode.length; j += 1) {
            edges.push(`${waiting[i]}__${tNodeInfo.outNode[j]}`)
          }
          d3.select(idTransformerFrontend(`#${waiting[i]}`)).style('visibility', 'visible')
          const edgeGroup = Array.from(d3.selectAll('.edgePath')._groups[0])
          // const edgeLabelGroup = d3.selectAll('.edgeLabel')._groups[0]
          edges.forEach((v) => {
            const edgeId = `#${idTransformerFrontend(v)}`
            d3.select(edgeId)
              // .select('.path')
              .style('visibility', 'visible')
            const edgeDom = document.getElementById(v)
            const index = edgeGroup.indexOf(edgeDom)
            // edgeLabelGroup[index].attributes.style.value = 'opacity: 1;visibility:visible'
          })
        }
      }
    },
    restoreLastClick() {
      const { nodeInfo, idTransformerFrontend, colour } = this
      const g = this.curg
      g.node(this.lastClick).clicked = false
      const lastEdges = g.nodeEdges(this.lastClick)
      lastEdges.forEach((v) => {
        const edgeID = `${v.v}__${v.w}`
        const edgeGroup = Array.from(d3.selectAll('.edgePath')._groups[0])
        // const edgeLabelGroup = d3.selectAll('.edgeLabel')._groups[0]
        let index
        for (let i = 0; i < edgeGroup.length; i += 1) {
          if (edgeGroup[i].id === edgeID) {
            index = i
            break
          }
        }
        const dEdgeID = `#${idTransformerFrontend(edgeID)}`
        d3.select(dEdgeID)
          .select('.path')
          .style('stroke', 'black')
          .style('stroke-width', '1')

        // d3.select(edgeLabelGroup[index])
        //   .select('g')
        //   .select('text')
        //   .attr('fill', 'black')
        const nodeFromID = idTransformerFrontend(`#${v.v}`)
        const nodeToID = idTransformerFrontend(`#${v.w}`)
        d3.select(nodeFromID)
          .select('rect')
          .style('stroke', '#696969')
        d3.select(nodeToID)
          .select('rect')
          .style('stroke', '#696969')
      })
      // var coldfill = d3.select(idTransformerFrontend(`#${this.lastClick}`)).select('rect').attr('coldfill')
      // console.log(coldfill)
      // d3.select(idTransformerFrontend(`#${this.lastClick}`)).select('rect').attr('coldfill', null).style('fill', coldfill).attr('clicked', null)
      d3.select(idTransformerFrontend(`#${this.lastClick}`)).select('rect').attr('clicked', null)
      colour(idTransformerFrontend(`#${this.lastClick}`))
      d3.select(
        idTransformerFrontend(`#${this.lastClick}`)
      )
        .select('rect')
        .style('stroke', '#c9c9c9')
      d3.select(`[id="${this.lastClick}"]`)
        .select('rect')
        .style('stroke-width', '1')
        .style('stroke', '#696969')
      let initInfo
      for (let i = 0; i < nodeInfo.length; i += 1) {
        if (nodeInfo[i].uid === this.lastClick) {
          initInfo = nodeInfo[i]
          break
        }
      }
      for (let i = 0; i < tmp.length; i += 1) {
        if (initInfo.inNode.indexOf(tmp[i].nodeId) >= 0) {
          // const oldfill = d3
          //   .select(
          //     idTransformerFrontend(`#del__${tmp[i].nodeId}`)
          //   )
          //   .select('rect')
          //   // .attr('oldfill')
          //   .attr('oracle')
          d3.select(
            idTransformerFrontend(`#del__${tmp[i].nodeId}`)
          )
            .select('rect')
            // .style('fill', oldfill)
            .attr('dir', null)
          d3.select(
            idTransformerFrontend(`#del__${tmp[i].nodeId}`)
          )
            .select('rect')
            .attr('oldfill', undefined)
          colour(idTransformerFrontend(`#del__${tmp[i].nodeId}`))
        }
        if (initInfo.outNode.indexOf(tmp[i].nodeId) >= 0) {
          // const oldfill = d3
          //   .select(
          //     idTransformerFrontend(`#del__${tmp[i].nodeId}`)
          //   )
          //   .select('rect')
          //   // .attr('oldfill')
          //   .attr('oracle')
          d3.select(
            idTransformerFrontend(`#del__${tmp[i].nodeId}`)
          )
            .select('rect')
            // .style('fill', oldfill)
            .attr('dir', null)
          d3.select(
            idTransformerFrontend(`#del__${tmp[i].nodeId}`)
          )
            .select('rect')
            .attr('oldfill', undefined)

          colour(idTransformerFrontend(`#del__${tmp[i].nodeId}`))
        }
      }
      this.lastClick = ''
    },
    restoreLastClickRight() {
      const { nodeInfo, idTransformerFrontend, colour } = this
      const nodeId = this.lastAssistClick.split('__')[1]
      const info = this.getDelNodeInfo(nodeId, nodeInfo)
      const { inNode, outNode } = info
      for (let i = 0; i < inNode.length; i += 1) {
        const nodeId = idTransformerFrontend(`#${inNode[i]}`)
        // const old = d3
        //   .select(nodeId)
        //   .select('rect')
        //   .attr('tag')
        d3.select(nodeId)
          .select('rect')
          // .style('fill', old)
          .attr('dir', null)
        d3.select(nodeId)
          .select('rect')
          .attr('tag', null)
        colour(nodeId)
        this.drawCircleTag(nodeId, 'out', 0)
      }
      for (let i = 0; i < outNode.length; i += 1) {
        const nodeId = idTransformerFrontend(`#${outNode[i]}`)
        // const old = d3
        //   .select(nodeId)
        //   .select('rect')
        //   .attr('tag')
        d3.select(nodeId)
          .select('rect')
          // .style('fill', old)
          .attr('dir', null)
        d3.select(nodeId)
          .select('rect')
          .attr('tag', null)
        colour(nodeId)
        this.drawCircleTag(nodeId, 'in', 0)
      }
      let initInfo
      for (let i = 0; i < nodeInfo.length; i += 1) {
        if (nodeInfo[i].uid === info.uid) {
          initInfo = nodeInfo[i]
          break
        }
      }
      for (let i = 0; i < tmp.length; i += 1) {
        if (initInfo.inNode.indexOf(tmp[i].nodeId) >= 0) {
          info.inNode.push(tmp[i].nodeId)
          var oldfill = d3
            .select(
              idTransformerFrontend(`#del__${tmp[i].nodeId}`)
            )
            .select('rect')
            .attr('oldfill')
          if (oldfill) {
            // oldfill = d3
            //   .select(
            //     idTransformerFrontend(`#del__${tmp[i].nodeId}`)
            //   )
            //   .select('rect')
            //   .attr('oracle')

            d3.select(
              idTransformerFrontend(`#del__${tmp[i].nodeId}`)
            )
              .select('rect')
              .style('fill', oldfill)
              .attr('dir', null)
            d3.select(
              idTransformerFrontend(`#del__${tmp[i].nodeId}`)
            )
              .select('rect')
              .attr('oldfill', undefined)

            colour(idTransformerFrontend(`#del__${tmp[i].nodeId}`))
          }
        }
        if (initInfo.outNode.indexOf(tmp[i].nodeId) >= 0) {
          info.outNode.push(tmp[i].nodeId)
          var oldfill = d3
            .select(
              idTransformerFrontend(`#del__${tmp[i].nodeId}`)
            )
            .select('rect')
            .attr('oldfill')
          if (oldfill) {
            // oldfill = d3
            //   .select(
            //     idTransformerFrontend(`#del__${tmp[i].nodeId}`)
            //   )
            //   .select('rect')
            //   .attr('oracle')

            d3.select(
              idTransformerFrontend(`#del__${tmp[i].nodeId}`)
            )
              .select('rect')
              .style('fill', oldfill)
              .attr('dir', null)
            d3.select(
              idTransformerFrontend(`#del__${tmp[i].nodeId}`)
            )
              .select('rect')
              .attr('oldfill', undefined)

            colour(idTransformerFrontend(`#del__${tmp[i].nodeId}`))
          }
        }
      }
      this.lastAssistClick = ''
    },
    idTransformerFrontend(id) {
      var id = id.replace(/\//g, '\\/').replace(/\(/g, '\\(').replace(/\)/g, '\\)').replace(/\]/g, '\\]').replace(/\[/g, '\\[').replace(/\./g, '\\.')
      return id
    },
    edgeLabelAnimation() {
      const edgeGroup = Array.from(d3.selectAll('.edgePath')._groups[0])
      const edgeLabelGroup = d3.selectAll('.edgeLabel')._groups[0]
      edgeGroup.forEach((edge, index) => {
        const oraclePath = d3.select(edge).select('path')
        var newPath = d3.select(edge).append('path')
        newPath.attr('d', oraclePath.attr('d')).style('opacity', 0).style('stroke', 'white').style('stroke-width', '20px').attr('marker-end', 'url(http://localhost:8080/#arrowhead146)')
          .attr('marker-start', 'url(#dot)').style('fill', 'none')
        newPath
          .on('mouseover', () => {
            d3.select(edge).select('path').style('stroke', 'red')
            d3.select(edgeLabelGroup[index]).style('visibility', 'visible')
          }).on('mouseleave', () => {
            d3.select(edge).select('path').style('stroke', 'black')
            d3.select(edgeLabelGroup[index]).style('visibility', 'hidden')
          })
      })
    },
    colorCopy() {
      Array.from(d3.selectAll('.node')._groups[0]).forEach((v) => {
        var color = d3.select(v).select('rect').style('fill')
        // console.log(d3.select(v))
        d3.select(v).select('rect').attr('oracle', color)
      })
    },
    colour(id) {
      // console.log(id)
      const clicked = d3.select(id).select('rect').attr('clicked')
      const edit = d3.select(id).select('rect').attr('edit')
      const dir = d3.select(id).select('rect').attr('dir')
      if (clicked === 'clicked' || edit === 'edit') {
        // console.log(id)
        d3.select(id).select('rect').style('fill', 'rgb(102, 102, 102)')
      } else if (dir === 'in') {
        d3.select(id).select('rect').style('fill', 'blue')
      } else if (dir === 'out') {
        d3.select(id).select('rect').style('fill', 'red')
      } else {
        // console.log(id)
        var oldcolor = d3.select(id).select('rect').attr('oracle')
        d3.select(id).select('rect').style('fill', oldcolor)
      }
    }
  }
}
</script>
<style lang="less" scoped>
.temp {
  position: absolute;
  width: calc(100% - 290px);
  height: 100%;
  background-color: white;
}

/deep/ .Graph {
  position: relative;
  height: 97.5%;
  margin: 1% 1% 0 1%;
  overflow-y: auto;
  background-color: white;
  border-radius: 5px 5px 0 0;
  box-shadow: rgba(0, 0, 0, 0.3) 0 0 10px;

  svg {
    position: relative;
  }
}

.assist {
  position: absolute;
  width: 100%;
  height: 100%;
  margin: 0% 0% 0 1%;
  overflow-y: auto;
  box-shadow: #8f8fb4 0 0 10px;
}

.clusters rect {
  opacity: 0.1;
  fill: #646464;
  stroke: #fff;
  stroke-width: 1.5px;
}

.node rect {
  opacity: 0.85;
  fill: #fff;
  stroke: #646464;
  stroke-width: 2.5px;
}

g.type-current > rect {
  fill: #1e9fff;
}

g.type-success > rect {
  fill: green;
}

g.type-fail > rect {
  fill: red;
}

text {
  font-size: 16px;
  fill: #000;
}

.edgeLabel text {
  font-family:
    -apple-system,
    BlinkMacSystemFont,
    'Segoe WPC',
    'Segoe UI',
    'Ubuntu',
    'Droid Sans',
    sans-serif,
    'PingFang SC';
  font-size: 1px;
}

.edgePath path {
  stroke: #333;
  stroke-width: 1.5px;
}

line {
  stroke: red;
  stroke-width: 2px;
}

.special-layer-1,
.special-layer-2 {
  fill: #fff !important;
}

.icon {
  font-size: 80px;
  color: #004986;
  opacity: 0.4;
}
</style>
