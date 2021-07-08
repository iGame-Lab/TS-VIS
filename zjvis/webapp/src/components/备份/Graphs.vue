<style lang="less" scoped>
    .temp{
      position: absolute;
      height: 100%;
      width: calc(100% - 290px);
      background-color: white;
    }
    /deep/.Graph{
      position: relative;
      margin: 1% 1% 0 1%;
      height: 97.5%;
      border-radius: 5px 5px 0 0;
      background-color: white;
      overflow-y: auto;
      box-shadow: rgba(0,0,0,.3) 0px 0px 10px;
      svg{
        position: relative;
      }
    }
    .assist{
      margin: 0% 0% 0 1%;
      position: absolute;
      height: 100%;
      width: 100%;
      overflow-y: auto;
      box-shadow:#8f8fb4 0px 0px 10px;
    }
    g.type-current>rect {
      fill: #1E9FFF;
    }

    g.type-success>rect {
      fill: green;
    }

    g.type-fail>rect {
      fill: red;
    }

    foreignObject{
      position: relative;
      x: 80%;
      width: 20%;
      opacity: 1;
      background-color: white;
      margin: 0% 1% 0 1%;
      box-shadow:#8f8fb4 0px 0px 10px;
    }

    /*#####调整字体#####*/
    text {
      font-size: 16px;
      fill: #000000;
    }
    .edgeLabel text {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe WPC", "Segoe UI", "Ubuntu", "Droid Sans", sans-serif, "PingFang SC";
      font-size: 1px;
    }
    .clusters rect {
      fill: #646464;
      stroke: #fff;
      stroke-width: 1.5px;
      opacity: 0.1;
    }

    /*#####修改节点边框、透明度#####*/
    .node rect {
      stroke: #646464;
      fill: #fff;
      stroke-width: 2.5px;
      opacity: 0.85;
    }

    .edgePath path {
      stroke: #333;
      stroke-width: 1.5px;
    }

    line{
      stroke:red;
      stroke-width:2px;
    }

    /* 设置特殊节点上下分层颜色 */
    .special-layer-1, .special-layer-2{
      fill: #fff !important;
    }

    .ass{
      stroke-width: 2.5px;
      stroke: #696969;
      opacity: 0.95;
      fill:white;
    }
    .icon {
      font-size: 80px;
      color: #004986;
      opacity: 0.4;
    }

</style>

<template>
  <div>
    <div class="temp">
      <!-- 可从这里加入你们的组件 -->
      <div id="test" class="Graph">
        <div style="position:absolute;top:50%;right:0%"><i class="icon iconfont">&#xe967;</i></div>
        <svg id="svg-canvas" style="float:left">
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
              <circle
                cx="10"
                cy="10"
                r="4"
                style="fill: black;"
              />
            </marker>
          </defs>
          <g id="draw" />
        </svg>
        <div id="assist" class="assist" style="height: 100%;right:0%;width:20%;display: none;flex-direction: column;background-color: white">
          <div style="height: 20px;padding: 10px 0 0 0"><span>删除节点</span></div>
          <div style="height: calc(100% - 20px);"><svg /></div>
          <div style="position:absolute;top:50%"><i class="icon iconfont">&#xe968;</i></div>
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

// 保存节点度数，及与该节点有关的边
let expandNode = []
let delStageNode = [] // 保存每步的删除节点
let reserverStageNode = [] // 保存每步的节点状态
let clickDel = [] // 保存右键删除节点
let changeTag = 0
let tmp = []

// 保存节点状态（隐藏）
let curg
const {
  mapGetters: mapGraphGetters,
  mapActions: mapGraphActions,
  mapMutations: mapGraphMutations

} = createNamespacedHelpers('graph')

const { mapState: mapLayoutStates } = createNamespacedHelpers('layout') // , mapMutations: mapLayoutMutations

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
    ...mapLayoutStates(['userSelectRunFile'])
  },
  watch: {
    getRetList(val) {
      this.retList = val
    },
    getGraphData(val) {
      this.graphData = val
      this.nodeInfo.splice(0, this.nodeInfo.length)
      expandNode = []
      delStageNode = [] // 保存每步的删除节点
      reserverStageNode = [] // 保存每步的节点状态
      clickDel = [] // 保存右键删除节点
      changeTag = 0
      tmp = []
      this.getNodeInfo(JSON.stringify({ 'info': 'init' }))
      this.drawGraph()
      // 在绘制完成后发送信号
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
    userSelectRunFile: function(val) {
      // 会自动获取一次run值
      this.setRunChangeTag(true)
      this.setIsDrawing(true)
      let k = 0
      for (let i = 0; i < this.getRunName.length; i++) {
        if (val === this.getRunName[i]) {
          k = i
          break
        }
      }
      this.setCurTag(this.getTagName[k][0])
      const param = { run: val, tag: this.getCurTag }
      this.getFullData(param)
    },
    getCurTag(val) { // 仅在通过panel修改tag时起作用
      // 在通过run获取数据时禁用panel的数据获取
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
    this.initDraw++
    // 若没有数据，就获取数据
    if (this.getGraphData.length === 0) {
      let k = 0
      for (let i = 0; i < this.getRunName.length; i++) {
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
    ...mapGraphActions([
      'getFullData'
    ]),
    ...mapGraphMutations([
      'getNodeInfo',
      'getClickDel',
      'setCurTag',
      'setRunChangeTag',
      'setIsDrawing'
    ]),
    drawGraph: function() {
      var self = this
      var nodeInfo = self.nodeInfo
      var drawCircleTag = this.drawCircleTag
      var glitter = this.glitter
      var getDelNodeInfo = this.getDelNodeInfo
      var getModifyClick = this.getModifyClick
      var drawAssist = this.drawAssist
      var getInfo = this.getNodeInfo
      var idTransform = this.idTransform
      // var getClick = this.getClickDel
      // nodeInfo = []
      // let clickInput = this.clickInput
      // let clickOutput = this.clickOutput
      // let degreeInput = this.degreeInput

      const data = this.graphData
      if (data === undefined) {
        return
      }

      var color = d3.scaleOrdinal()
        .range([
          '#e8c5df', // Convolution
          '#daf4cc', // Normalization
          '#d7dafb', // Math&Activation&Pooling
          '#b1cbe8', // Sparse Tensors&Tensor Transformations
          '#cdf6e8', // ControlFlow
          '#feedd3', // Losses&Metrics
          '#d2f5f9', // InputsandReaders
          '#dcdcdc', // empty
          '#dcdcdc', // empty
          '#dcdcdc', // empty
          '#dcdcdc' // empty
        ])
      // 存储是否为控制边
      var isDashed = {}
      // 存储是否为重边
      var isLines = {}
      // 特殊双层标题栏设置
      var titleHeight = 40 // 标题栏高度
      var cornerR = 5// 圆角大小
      var lineWidth = 1 // 边框线条宽度

      // 记录op分类信息，格式：{op1:大类,op2:大类},着色时找到op自己的大类
      var opdata = {}
      // 记录节点信息，防止.node(uid)和node.sub_net都找不到节点导致着色不对
      var nodedata = {}
      // 记录特殊节点label特征
      var SpecialNodeList = ['conv', 'dense', 'pool', 'norm']

      // ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
      // ！！！！！功能函数：                                                                                             //
      // 高炜哲                                                                                                        //
      // ---------------------------------------------------------------------------------------------------------------
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
      function DrawVirtualNodes(graph, parent) {
        d3.selectAll(`.nodes .node`)
          .attr('temp', function(uid) {
            if (!nodedata[uid] || !IsVirtualNode(nodedata[uid])) {
              return ''
            }
            var node = graph.node(uid)
            if (!node) {
              return ''
            }
            d3.select(this).select('rect').style('stroke-dasharray', '5,3').style('stroke', '#696969').style('stroke-width', '1.5px')
          })
      }

      // 判断是否为计算图特殊节点
      function IsSpecialNode(itemnode) {
        if (!itemnode) {
          return false
        }
        if (itemnode.sub_net.length > 0) {
          for (const n in itemnode.sub_net) {
            const size = d3.selectAll(`[id="${itemnode.sub_net[n].id}"]`).size()
            if (size > 0) {
              return false
            }
          }
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
      // 绘制计算图特殊节点
      function DrawSpecialNodes(graph, parent) {
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
        // 卷积层
        if (itemnode.op.toLowerCase().indexOf(SpecialNodeList[0].toLowerCase()) >= 0) {
          return 1
        }
        // 全连接层
        if (itemnode.op.toLowerCase().indexOf(SpecialNodeList[1].toLowerCase()) >= 0) {
          return 2
        }
        // 池化层
        if (itemnode.op.toLowerCase().indexOf(SpecialNodeList[2].toLowerCase()) >= 0) {
          return 3
        }
        // 归一化
        if (itemnode.op.toLowerCase().indexOf(SpecialNodeList[3].toLowerCase()) >= 0) {
          return 4
        }
        return false
      }

      // 绘制结构图双层节点
      // 绘制特殊节点
      function DrawDoubleNodes(graph, parent) {
        d3.selectAll(`.nodes .node`)
          .attr('temp', function(uid) {
            if (!nodedata[uid] || !IsDoubleNode(nodedata[uid])) {
              return ''
            }
            var node = graph.node(uid)
            if (!node) {
              return ''
            }
            // 全连接 修正着色
            d3.selectAll(`.nodes .node`)
              .attr('temp', function(uid) {
                if (!nodedata[uid] || IsDoubleNode(nodedata[uid]) !== 2) {
                  return ''
                }
                var node = graph.node(uid)
                if (!node) {
                  return ''
                }
                d3.select(this)
                  .select('rect').style('fill', '#b7d4ae')
              })

            // 池化层 修正着色
            d3.selectAll(`.nodes .node`)
              .attr('temp', function(uid) {
                if (!nodedata[uid] || IsDoubleNode(nodedata[uid]) !== 3) {
                  return ''
                }
                var node = graph.node(uid)
                if (!node) {
                  return ''
                }
                d3.select(this)
                  .select('rect').style('fill', '#d7dafb')
              })

            // 归一化 修正着色
            d3.selectAll(`.nodes .node`)
              .attr('temp', function(uid) {
                if (!nodedata[uid] || IsDoubleNode(nodedata[uid]) !== 4) {
                  return ''
                }
                var node = graph.node(uid)
                if (!node) {
                  return ''
                }
                d3.select(this)
                  .select('rect').style('fill', '#daf4cc')
              })

            // 信息栏大小
            var width = node.width + 20
            var height = node.height + 30

            if (IsDoubleNode(nodedata[uid]) !== 4) {
            /* ##### 分层的下层背景rect ##### */
              d3.select(this).select('.label').attr('transform', 'translate(0,-' + height / 4 + ')')
              d3.select(this).selectAll('.special-layer-2')
                .data([0])
                .enter()
                .append('rect')
                .attr('class', 'special-layer-2')
                .style('fill', '#ffffff')

              // 下层空白
              d3.select(this).selectAll('.special-layer-2')
              // position
                .attr('x', -width / 2 + lineWidth)
                .attr('y', -titleHeight + titleHeight / 2 - lineWidth + 20)
              // round
                .attr('rx', cornerR + 6)
                .attr('ry', cornerR + 6)
              // size
                .attr('width', width - lineWidth * 2)
                .attr('height', height - titleHeight - 5)
              // style
                .style('fill', '#fff')
                .style('opacity', 1)
                .style('stroke-width', 0)

              /* #####修复直角##### */
              d3.select(this).selectAll('.special-layer-1')
                .data([0])
                .enter()
                .append('rect')
                .attr('class', 'special-layer-1')
                .style('fill', '#fff')
              d3.select(this).selectAll('.special-layer-1')
              // position
                .attr('x', -width / 2 + lineWidth)
                .attr('y', -8)
              // size
                .attr('width', width - lineWidth * 2)
                .attr('height', 18)
              // style
                .style('opacity', 1)
                .style('fill', '#fff')
                .style('stroke-width', 0)

              // 卷积层 信息
              /* ##### 分层的下层内容1 kernel_size ##### */
              if (IsDoubleNode(nodedata[uid]) === 1) {
                const ATTR = nodedata[uid].attrs
                console.log('conv attrs:' + JSON.stringify(ATTR))
                /* ##### 分层的下层内容1 kernel_size ##### */
                d3.select(this).selectAll('.special-layer-text1')
                  .data([0])
                  .enter()
                  .append('text')
                  .attr('class', 'special-layer-text')
                  .attr('x', -width / 2 + 15)
                  .attr('y', 8)
                // 信息
                d3.select(this).selectAll('.special-layer-text')
                  .html(`● kernel size: ${JSON.stringify(ATTR.kernel_size)}`)
                  .style('font-size', '12px')
                /* ##### 分层的下层内容2 strides ##### */
                d3.select(this).selectAll('.special-layer-text2')
                  .data([0])
                  .enter()
                  .append('text')
                  .attr('class', 'special-layer-text')
                  .attr('x', -width / 2 + 15)
                  .attr('y', 26)
                  // 信息
                  .html(`● strides: : ${JSON.stringify(ATTR.strides)}`)
                  .style('font-size', '12px')
              }

              // 全连接层 信息
              if (IsDoubleNode(nodedata[uid]) === 2) {
                const ATTR = nodedata[uid].attrs
                /* ##### 分层的下层内容1 units ##### */
                d3.select(this).selectAll('.special-layer-text1')
                  .data([0])
                  .enter()
                  .append('text')
                  .attr('class', 'special-layer-text')
                  .attr('x', -width / 2 + 15)
                  .attr('y', 8)
                  // 信息
                d3.select(this).selectAll('.special-layer-text')
                  .html(`● units: ${JSON.stringify(ATTR.units)}`)
                  .style('font-size', '12px')

                /* ##### 分层的下层内容2 activation ##### */
                d3.select(this).selectAll('.special-layer-text2')
                  .data([0])
                  .enter()
                  .append('text')
                  .attr('class', 'special-layer-text')
                  .attr('x', -width / 2 + 15)
                  .attr('y', 26)
                  // 信息
                  .html(`● activation: : ${JSON.stringify(ATTR.activation)}`)
                  .style('font-size', '12px')
              }

              // 池化层 信息
              if (IsDoubleNode(nodedata[uid]) === 3) {
              /* ##### 分层的下层内容1pool_size ##### */
                const ATTR = nodedata[uid].attrs
                d3.select(this).selectAll('.special-layer-text1')
                  .data([0])
                  .enter()
                  .append('text')
                  .attr('class', 'special-layer-text')
                  .attr('x', -width / 2 + 15)
                  .attr('y', 8)
                  // 信息
                d3.select(this).selectAll('.special-layer-text')
                  .html(`● pool_size: ${JSON.stringify(ATTR.pool_size)}`)
                  .style('font-size', '12px')
                /* ##### 分层的下层内容2strides ##### */
                d3.select(this).selectAll('.special-layer-text2')
                  .data([0])
                  .enter()
                  .append('text')
                  .attr('class', 'special-layer-text')
                  .attr('x', -width / 2 + 15)
                  .attr('y', 26)
                  // 信息
                  .html(`● strides: ${JSON.stringify(ATTR.strides)}`)
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
        var op = ''
        var uid = node.uid
        // 根据uid从记录的节点信息中查找节点，如果找到，则取出op
        if (nodedata[uid]) {
          op = nodedata[uid].op
        } else { // 若在nodedata中未找到节点信息的话，则继续在dD.node(uid)中寻找
          if (g.node(uid)) {
            op = g.node(uid).op
            // 将找到的节点信息存入nodedata
            nodedata[uid] = g.node(uid)
          }
          if (g.node.sub_net) {
            // 从node.sub_net查找到节点信息
            var index = g.node.sub_net.findIndex(e => e.uid === uid)
            if (index >= 0) {
              op = g.node.sub_net[index].op
              // 将找到的节点信息存入nodedata
              nodedata[uid] = g.node.sub_net[index]
            }
          }
        }
        if (op === '') {
          op = 'empty'
        }
        return GetColorByOP(op)
      }
      // -------------------------------------------------------------------------------------------------------------

      // 从后台获取颜色数据并处理
      const retlist = this.retList

      retlist.forEach(function(d) {
        d.list.forEach(function(tk) {
          opdata[tk] = {
            op: tk, parent: d.op
          }
          if (tk.indexOf('_') >= 0) {
            opdata[tk] = {
              op: tk.replace(/_/g, ''), parent: d.op
            }
          }
        })
      })
      color.domain(retlist.map(function(d) { return d.op }))

      // 冒泡排序(扩展节点)
      const bubbleSortExpand = function(arr) {
        var len = arr.length
        for (var i = 0; i < len; i++) {
          for (var j = 0; j < len - 1 - i; j++) {
            // 相邻元素两两对比
            if (arr[j].layer > arr[j + 1].layer) {
              // 元素交换
              var temp = arr[j + 1]
              arr[j + 1] = arr[j]
              arr[j] = temp
            }
          }
        }
      }

      // 判断该节点是否可用
      const find = function(id) {
        const names = id.split('/')
        const namesLength = names.length
        if (namesLength === 1) {
          for (let i = 0; i < expandNode.length; i++) {
            if (id === expandNode[i].uid) {
              return false
            }
          }
          return true
        } else {
          let sign = 0
          const pre = names.slice(0, namesLength - 1).join('/')
          for (let i = 0; i < expandNode.length; i++) {
            if (pre === expandNode[i].uid) {
              sign = 1
              break
            }
          }

          for (let i = 0; i < expandNode.length; i++) {
            if (id === expandNode[i].uid) {
              sign = 0
              break
            }
          }

          if (sign) {
            return true
          } else {
            return false
          }
        }
      }

      // 保存节点及相关边,sign标记保存入边(0)或出边(1)
      const nodeHold = function(nodeUid, edgeUid, srcNode, sign, op, attrs) {
        // eslint-disable-next-line no-unused-vars
        let index = -1
        for (let i = 0; i < nodeInfo.length; i++) {
          if (nodeInfo[i].uid === nodeUid) {
            index = i
            if (sign) {
              if (srcNode) {
                nodeInfo[i].outNode.push(srcNode)
              }
              if (attrs && (JSON.stringify(attrs) !== '{}')) {
                nodeInfo[i].attr = attrs
              }
              nodeInfo[i].op = op
            } else {
              if (srcNode) {
                nodeInfo[i].inNode.push(srcNode)
              }
              if (attrs && (JSON.stringify(attrs) !== '{}')) {
                nodeInfo[i].attr = attrs
              }
            }
            return true
          }
        }

        const node = { 'uid': nodeUid, 'inNode': [], 'outNode': [], 'op': '' }
        if (sign) {
          if (srcNode) {
            node.outNode.push(srcNode)
          }
          node.op = op

          if (attrs && (JSON.stringify(attrs) !== '{}')) {
            node.attr = attrs
          }
          nodeInfo.push(node)
        } else {
          if (srcNode) {
            node.inNode.push(srcNode)
          }
          if (attrs && (JSON.stringify(attrs) !== '{}')) {
            node.attr = attrs
          }
          nodeInfo.push(node)
        }
      }

      // 画图--------------------------------------------------------------------------------------------
      var draw = function(data, init) {
        self.lastClick = ''
        self.lastAssistClick = ''
        nodeInfo.splice(0, nodeInfo.length)
        d3.select('#svg-canvas').select('g').selectAll('g').remove()
        var g = new dagreD3.graphlib.Graph({ compound: true })
          .setGraph({})
          .setDefaultEdgeLabel(function() {
            return {}
          })

        data.forEach(function(v) {
          v.id = v.uid
          v.clicked = false
          // 姜子敬
          // --------------------------------------------------------------------------------------------------------------
          // 功能：由于节点的名字是在setNode时根据其label确定了的，因此根据label长度判断书否修改label，并将label存入name中备用
          if (v.label) {
            if (v.label.length > 12) {
              v['name'] = v.label
              v.label = v.label.slice(0, 12) + '...'
            }
          }
          // ------------------------------------------------------------------------------------------------------------

          if (find(v.uid)) {
            g.setNode(v.uid, v)

            v.targets.forEach(function(u) {
              if (find(u.id)) {
                const edgeLabel = v.uid + '__' + u.id
                g.setEdge(v.uid, u.id, { 'id': edgeLabel, 'label': u.info, curve: d3.curveBasis })
                isDashed[edgeLabel] = u.control
                isLines[edgeLabel] = u.num
                nodeHold(v.uid, edgeLabel, u.id, 1, v.op, v.attrs)
                nodeHold(u.id, edgeLabel, v.uid, 0, undefined, u.attrs)
              }
            })
            nodeHold(v.uid, '', '', 1, v.op, v.attrs)
          } else {
            v.clusterLabelPos = 'top'
            g.setNode(v.uid, v)
          }
        })
        for (let i = 0; i < expandNode.length; i++) {
          const sub = expandNode[i].sub_net
          sub.forEach(function(v) {
            v.id = v.uid
            // 姜子敬
            // --------------------------------------------------------------------------------------------------------------
            // 功能：由于节点的名字是在setNode时根据其label确定了的，因此根据label长度判断书否修改label，并将label存入name中备用
            if (v.label) {
              if (v.label.length > 12) {
                v['name'] = v.label
                v.label = v.label.slice(0, 12) + '...'
              }
            }
            // ------------------------------------------------------------------------------------------------------------
            g.setParent(v.uid, expandNode[i].uid)
            if (find(v.uid)) {
              g.setNode(v.uid, v)
              v.targets.forEach(function(u) {
                if (find(u.id)) {
                  const edgeLabel = v.uid + '__' + u.id
                  g.setEdge(v.uid, u.id, { 'id': edgeLabel, 'label': u.info, curve: d3.curveBasis })
                  isDashed[edgeLabel] = u.control
                  isLines[edgeLabel] = u.num
                  nodeHold(v.uid, edgeLabel, u.id, 1, v.op, v.attrs)
                  nodeHold(u.id, edgeLabel, v.uid, 0, undefined)
                }
              })
              nodeHold(v.uid, '', '', 1, v.op, v.attrs)
            } else {
              v.clusterLabelPos = 'top'
              g.setNode(v.uid, v)
            }
          })
        }
        // 高炜哲
        // -------------------------------------------------------------------------------------------------------------
        // 设置节点样式
        g.nodes().forEach(function(v) {
          const node = g.node(v)
          if (node !== undefined) {
            // 获取节点的背景色
            let fill = GetColorByNode(g, v)
            // 获取当前节点对应的在扩展节点列表中的内容
            const expand = expandNode.find(item => item.uid === v)

            // 当前节点为扩展节点, 则背景色从对象中获取, 若没有则使用默认颜色
            if (expand !== void 0) {
              fill = expand.fill || fill
            }

            node.rx = node.ry = 10 // 圆角半径
            node.width = 125 // 节点长度
            node.height = 20 //  节点宽度
            node.style = 'fill:' + fill + ';rx:12.5px' + ';ry:12.5px' + ';stroke-width:1px' + ';stroke:' + '#696969'
            if (IsDoubleNode(node) && IsDoubleNode(node) !== 4 && self.getCurTag !== 'c_graph') {
              node.height = 50
            }
          }
        })
        // -------------------------------------------------------------------------------------------------------------

        // 节点过滤
        // -------------------------------------------------------------------------------------------------------------
        for (let i = 0; i < delStageNode.length; i++) {
          for (let j = 0; j < delStageNode[i].length; j++) {
            g.removeNode(delStageNode[i][j])
          }
        }
        for (let i = 0; i < tmp.length; i++) {
          g.removeNode(tmp[i].nodeId)
          // g.removeNode(tmp[i])
        }

        // -------------------------------------------------------------------------------------------------------------
        // eslint-disable-next-line new-cap
        const render = new dagreD3.render()
        const svg = d3.select('#svg-canvas')

        // 图渲染
        render(d3.select('#svg-canvas g'), g)

        // 调整画布大小
        d3.select('#svg-canvas')
          .attr('width', '100%')
          .attr('height', '100%')
        self.srcData = data
        if (!reserverStageNode.length) {
          const tmp1 = { 'sign': 1 }
          tmp1.nodeInfo = JSON.parse(JSON.stringify(nodeInfo))
          reserverStageNode.push(tmp1)
          const nnodeInfo = reserverStageNode[0].nodeInfo

          for (var i = 0; i < tmp.length; i++) {
            const tmpItem = tmp[i]
            for (var j = nnodeInfo.length - 1; j >= 0; j--) {
              if (nnodeInfo[j].uid === tmpItem.nodeId) {
                nnodeInfo.splice(j, 1)
              } else {
                const inNode = nnodeInfo[j].inNode
                const outNode = nnodeInfo[j].outNode
                for (let z = 0; z <= inNode.length; z++) {
                  if (inNode[z] === tmpItem.nodeId) {
                    inNode.splice(z, 1)
                    break
                  }
                }

                for (let z = 0; z <= outNode.length; z++) {
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
        curg = g
        // 姜子敬
        // 初次绘制中将图居中,并设置zoom的初始位置
        // -------------------------------------------------------------------------------------------------------------
        if (init) {
          init = false
          // 获取画布宽、高
          const canvas = d3.select('#svg-canvas')['_groups'][0][0]
          const canvasHeight = canvas.scrollHeight
          const canvasWidth = canvas.scrollWidth

          // 获取图宽、高
          const graph = d3.select('#svg-canvas g')['_groups'][0][0]
          const graphHeight = graph.getBBox().height
          const graphWidth = graph.getBBox().width

          d3.select('#svg-canvas g').attr('transform', 'translate(' + (canvasWidth - graphWidth) / 2 + ',' + (canvasHeight - graphHeight) / 2 + ')')

          // 设定zoom的初始位置
          const transform = d3.zoomTransform(0).translate((canvasWidth - graphWidth) / 2, (canvasHeight - graphHeight) / 2)
          d3.zoom().transform(svg, transform)
        }
        // 缩放 展开 保持颜色
        drawAssist('white')
        // -------------------------------------------------------------------------------------------------------------

        // 姜子敬
        // -------------------------------------------------------------------------------------------------------------
        // 鼠标滚动放大、缩小和移动
        const zoom = d3.zoom().on('zoom', function() {
          d3.select('#svg-canvas g').attr('transform', d3.event.transform)
        })
        svg.call(zoom).on('dblclick.zoom', null)
        // ----------------------------------------------------------------------------------------------------------------
        // 高炜哲
        // -----------------------------------------------------------------------------------------------------------------
        // 确定所有节点对应颜色
        d3.selectAll('.node rect')
          .style('fill', function(uid) {
            var op = ''

            // 根据uid从记录的节点信息中查找节点，如果找到，则取出op
            if (nodedata[uid] === 1) {
              op = nodedata[uid].op
            } else { // 若在nodedata中未找到节点信息的话，则继续在dD.node(uid)中寻找
              if (g.node(uid)) {
                op = g.node(uid).op
                // 将找到的节点信息存入nodedata
                nodedata[uid] = JSON.parse(JSON.stringify(g.node(uid)))
              }
              if (g.node.sub_net && g.node.sub_net.length) {
                // 从node.sub_net查找到节点信息
                const index = g.node.sub_net.findIndex(e => e.uid === uid)
                if (index !== -1) {
                  op = g.node.sub_net[index].op
                  // 将找到的节点信息存入nodedata
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
        // -------------------------------------------------------------------------------------------------------------

        // 绘制虚接节点样式
        DrawVirtualNodes(g, data)

        if (self.getCurTag === 'c_graph') {
          DrawSpecialNodes(g, data)
        }
        if (self.getCurTag === 's_graph') {
          DrawDoubleNodes(g, data)
        }
        glitter(self.restoreNode)
        // 为边添加实心
        d3.selectAll('.path').style('fill-opacity', 1).style('stroke', 'black').style('stroke-opacity', 1).attr('marker-start', 'url(#dot)')

        // 动作-----------------------------------------------------------------------------------------------------

        // 子节点动作：双击展开，自动调整位置，边框标红 -------------------------------------------------------------------------
        d3.selectAll('.node').on('dblclick', function(v) {
          // var index = -1
          // 先判断点击节点在不在扩展节点中
          // console.log('双击扩展节点: ', g.node(v).sub_net)
          if (g.node(v).sub_net.length !== 0) {
            const names = v.split('/')
            const layer = names.length
            // 扩展后的节点没有子节点, 无法通过计算获取颜色值, 在重新绘制之前获取
            const fillCurrent = d3.select(`[id="${v}"]`).select('rect').style('fill')
            expandNode.push({
              'uid': v,
              'layer': layer,
              'sub_net': g.node(v).sub_net,
              'label': g.node(v).label,
              fill: fillCurrent
            })

            bubbleSortExpand(expandNode)
            nodeInfo.splice(0, nodeInfo.length)
            reserverStageNode = []
            delStageNode = []
            // --------------------------------------------------------------------------------------------------------
            draw(data, init)

            // 保持展开后颜色不变+边框闪烁
            self.lastClick = ''
            d3.select(`[id="${v}"]`).select('rect').style('stroke-width', '2.5').style('stroke', 'red').style('fill', fillCurrent).style('opacity', '0.8')
            setTimeout(function() {
              d3.select(`[id="${v}"]`).select('rect').style('stroke-width', '1.5').style('stroke', '#696969')
            }, 1000)
            // 获取当前点击节点信息, 如果节点是最外层节点, 在 data 中查找, 否则在扩展节点中的 sub_net 中查找
            let currentNode = data.find(item => item.uid === v)

            if (!currentNode && expandNode && expandNode.length) {
              // eslint-disable-next-line no-labels
              loopExpandNode:
              for (const expand of expandNode) {
                for (const sub of expand.sub_net) {
                  if (sub.uid === v) {
                    currentNode = sub
                    // eslint-disable-next-line no-labels
                    break loopExpandNode
                  }
                }
              }
            }

            if (currentNode) {
              const str = d3.select('#svg-canvas g').attr('transform')
              // 获取 graph(g) 相对于画板 svg 的位置
              let [xCoor, yCoor] = str.substring(str.indexOf('(') + 1, str.indexOf(')')).split(',')
              // 获取当前节点相对于创建的 graph(g) 的位置
              const { x: xCurrent, y: yCurrent } = currentNode
              // 获取画板 svg 的宽高
              const svgWidth = d3.select('#svg-canvas').style('width').replace('px', '')
              const svgHeight = d3.select('#svg-canvas').style('height').replace('px', '')

              xCoor = Number(svgWidth) / 2 - xCurrent
              yCoor = Number(svgHeight) / 2 - yCurrent

              d3.select('#svg-canvas g').attr('transform', `translate(${xCoor}, ${yCoor})`)
              const transform = d3.zoomTransform(0).translate(xCoor, yCoor)
              d3.zoom().transform(svg, transform)
            }
          }
        })

        // 父节点动作：双击缩小，自动调整位置，边框标红 -------------------------------------------------------------------------
        d3.selectAll('.cluster').style('fill-opacity', '0.55').attr('font-weight', '600').on('dblclick', function(v) {
          const indexRecord = []
          const names = v.split('/')
          const namesLength = names.length
          for (let i = expandNode.length - 1; i >= 0; i--) {
            const uid = expandNode[i].uid
            const uids = uid.split('/')
            const uidLength = uids.length
            if (uidLength >= namesLength) {
              if (uids.slice(0, namesLength).join('/') === v) {
                indexRecord.push(i)
              }
            }
            for (let j = 0; j < indexRecord.length; j++) {
              expandNode.splice(indexRecord[j], 1)
            }
          }
          nodeInfo.splice(0, nodeInfo.length)
          reserverStageNode = []
          delStageNode = []
          // -----------------------------------------------------------------------------------------------------------

          draw(data, init)

          self.lastClick = ''
          d3.select(`[id="${v}"]`).select('rect').style('stroke-width', '1.5').style('stroke', 'red')
          setTimeout(function() {
            d3.select(`[id="${v}"]`).select('rect').style('stroke-width', '1.5').style('stroke', '#696969')
          }, 1000)
          // -----------------------------------------------------------------------------------------------------------

          // 获取当前点击节点信息, 如果节点是最外层节点, 在 data 中查找, 否则在扩展节点中的 sub_net 中查找
          let currentNode = data.find(item => item.uid === v)

          if (!currentNode && expandNode && expandNode.length) {
            // eslint-disable-next-line no-labels
            loopExpandNode:
            for (const expand of expandNode) {
              for (const sub of expand.sub_net) {
                if (sub.uid === v) {
                  currentNode = sub
                  // eslint-disable-next-line no-labels
                  break loopExpandNode
                }
              }
            }
          }

          if (currentNode) {
            const str = d3.select('#svg-canvas g').attr('transform')
            // 获取 graph(g) 相对于画板 svg 的位置
            let [xCoor, yCoor] = str.substring(str.indexOf('(') + 1, str.indexOf(')')).split(',')
            // 获取当前节点相对于创建的 graph(g) 的位置
            const { x: xCurrent, y: yCurrent } = currentNode
            // 获取画板 svg 的宽高
            const svgWidth = d3.select('#svg-canvas').style('width').replace('px', '')
            const svgHeight = d3.select('#svg-canvas').style('height').replace('px', '')

            xCoor = Number(svgWidth) / 2 - xCurrent
            yCoor = Number(svgHeight) / 2 - yCurrent

            d3.select('#svg-canvas g').attr('transform', `translate(${xCoor}, ${yCoor})`)
            const transform = d3.zoomTransform(0).translate(xCoor, yCoor)
            d3.zoom().transform(svg, transform)
          }
        })

        d3.selectAll('.path').on('click', function(v) {
          const edgeID = v.v + '__' + v.w
          const edgeGroup = Array.from(d3.selectAll('.edgePath')['_groups'][0])
          const edgeLabelGroup = d3.selectAll('.edgeLabel')['_groups'][0]
          let index
          for (let i = 0; i < edgeGroup.length; i++) {
            if (edgeGroup[i].id === edgeID) {
              index = i
              break
            }
          }
          const dEdgeID = '#' + idTransform(edgeID)
          const edgeDom = d3.select(dEdgeID)
          const tag = edgeDom.attr('tag')
          if (tag) {
            edgeDom.attr('tag', null)
            d3.select(dEdgeID).select('.path').style('stroke', 'black')
            d3.select(edgeLabelGroup[index]).select('g').select('text').attr('fill', 'black')
          } else {
            edgeDom.attr('tag', 1)
            d3.select(dEdgeID).select('.path').style('stroke', 'red')
            d3.select(edgeLabelGroup[index]).select('g').select('text').attr('fill', 'red')
          }
        })

        d3.select('#assist').select('svg').selectAll('g').on('dblclick', function() {
          const nodeId = this['id'].split('__')[1]
          self.restoreNode = nodeId
          const index = tmp.findIndex(item => item.nodeId === nodeId)

          drawAssist('white')
          tmp.splice(index, 1)

          getModifyClick(nodeId)
          draw(data, init)
        }).on('click', function() {
          const nodeId = this['id'].split('__')[1]
          let info = getDelNodeInfo(nodeId, nodeInfo)
          if (self.lastClick) {
            self.restoreLastClick()
          }
          if (self.lastAssistClick && self.lastAssistClick !== this['id']) {
            self.restoreLastClickRight()
          }
          if (!info) {
            info = { 'info': '无信息' }
          } else {
            const inNode = info.inNode
            const outNode = info.outNode
            // graph内的连接节点
            for (let i = 0; i < inNode.length; i++) {
              const nodeId = '#' + idTransform(inNode[i])
              if (!d3.select(nodeId).select('rect').attr('tag')) {
                const old = d3.select(nodeId).select('rect').style('fill')
                d3.select(nodeId).select('rect').attr('tag', old)
                d3.select(nodeId).select('rect').style('fill', 'blue')
                drawCircleTag(nodeId, 'out', 1)
              } else {
                const old = d3.select(nodeId).select('rect').attr('tag')
                d3.select(nodeId).select('rect').style('fill', old)
                d3.select(nodeId).select('rect').attr('tag', null)
                drawCircleTag(nodeId, 'out', 0)
              }
            }
            if (self.lastAssistClick === this['id']) {
              self.lastAssistClick = ''
            } else {
              self.lastAssistClick = this['id']
            }
            for (let i = 0; i < outNode.length; i++) {
              const nodeId = '#' + idTransform(outNode[i])
              if (!d3.select(nodeId).select('rect').attr('tag')) {
                const old = d3.select(nodeId).select('rect').style('fill')
                d3.select(nodeId).select('rect').attr('tag', old)
                d3.select(nodeId).select('rect').style('fill', 'red')
                drawCircleTag(nodeId, 'in', 1)
              } else {
                const old = d3.select(nodeId).select('rect').attr('tag')
                d3.select(nodeId).select('rect').style('fill', old)
                d3.select(nodeId).select('rect').attr('tag', null)
                drawCircleTag(nodeId, 'in', 0)
              }
            }
            let initInfo
            for (let i = 0; i < nodeInfo.length; i++) {
              if (nodeInfo[i].uid === info.uid) {
                initInfo = nodeInfo[i]
                break
              }
            }
            // foreign内的连接节点
            for (let i = 0; i < tmp.length; i++) {
              if (initInfo.inNode.indexOf(tmp[i].nodeId) >= 0) {
                info.inNode.push(tmp[i].nodeId)
                const oldfill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill')
                if (oldfill) {
                  d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', oldfill)
                  d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', undefined)
                } else {
                  const fill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('fill')
                  d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', 'blue')
                  d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', fill)
                }
              }
              if (initInfo.outNode.indexOf(tmp[i].nodeId) >= 0) {
                info.outNode.push(tmp[i].nodeId)
                const oldfill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill')
                if (oldfill) {
                  d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', oldfill)
                  d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', undefined)
                } else {
                  const fill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('fill')
                  d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', 'red')
                  d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', fill)
                }
              }
            }
          }
          getInfo(JSON.stringify(info))
        })

        // 姜子敬
        // -------------------------------------------------------------------------
        // 功能：为每个节点添加动画
        svg.selectAll('.node')['_groups'][0].forEach(function(nodeKey) {
          // nodeKey 当前用于动画的节点
          // 首先根据节点的id获得其简化的名称，用于文字动画
          let nodeName = nodeKey.id
          const nodes = g.node(nodeKey.id)
          const edges = g.nodeEdges(nodeKey.id)
          nodeName = nodeName.split('/')
          nodeName = nodeName[nodeName.length - 1]
          nodeName = nodeName.slice(0, nodeName.length)

          // 在/前加入转义字符，用于d3.select的搜索，防止报错
          const nodeId = idTransform(nodeKey.id)

          // 根据节点找到其对应的图的部分，根据事件对其中的text内容进行修改
          const nodeThis = d3.select(nodeKey)
          let currName = ''
          let nodeFromID = ''
          let nodeToID = ''

          nodeThis.append('text')
          nodeThis.style('cursor', 'context-menu')

          // 显示+号
          const width = parseInt(d3.select('#' + nodeId).select('rect').style('width'))
          const height = parseInt(d3.select('#' + nodeId).select('rect').style('height'))

          if (nodes.sub_net.length > 0) {
            let isexpand = false
            for (let i = 0; i < expandNode.length; i++) {
              if (nodeId === expandNode[i].uid) {
                isexpand = true
              }
            }
            const size = d3.select('#' + nodeId).selectAll('text.expand').size()
            if (size <= 0) {
              d3.select('#' + nodeId).append('text')
                .attr('class', 'expand')
                .attr('x', width / 2 - 15)
                .attr('y', -height / 2 + 12)
                .style('font-size', '14px')
                .style('fill', 'white')
                .attr('font-weight', 'bold')
            }
            if (!isexpand) {
              d3.select('#' + nodeId)
                .selectAll('text.expand')
                .text('+')
            }
          }

          // 添加鼠标悬浮事件
          nodeThis.on('mouseover', function() {
            const tag = Number(d3.select('#' + nodeId).attr('flag'))
            if (tag) {
              return
            }

            // 快速预览悬浮窗
            d3.select('#' + nodeId).attr('flag', 1)
            const oldLength = d3.select('#' + nodeId).select('.label').select('g').select('text').select('tspan')['_groups'][0][0]['textLength']['baseVal']['value']
            const newLength = d3.select('#' + nodeId).select('.label').select('g').select('text').select('tspan')['_groups'][0][0]['textLength']['baseVal']['value']
            const gap = (newLength - oldLength) / 2
            const nodeTransform = d3.select('#' + nodeId).attr('transform')
            const messageBox = d3.select('.nodes').append('g').attr('id', 'messageBox').attr('transform', nodeTransform)
            const boxComponent = messageBox.append('g').attr('id', 'boxComponent')
            const nodeWidth = d3.select('#' + nodeId).attr('width')
            const nodeHeight = d3.select('#' + nodeId).attr('height')
            const nodeheight = parseInt(d3.select('#' + nodeId).select('rect').style('height'))
            let obj
            for (let i = 0; i < nodeInfo.length; i++) {
              if (nodeInfo[i].uid === nodeKey.id) {
                obj = nodeInfo[i]
                break
              }
            }

            const info = {}
            // 建立节点本身属性
            info['NODE PROPERTIES'] = {}
            const index = obj.uid.lastIndexOf('/')
            info['NODE PROPERTIES'].name = obj.uid.substring(index + 1, obj.uid.length)
            if (obj.op) {
              info['NODE PROPERTIES'].op = obj.op
            }

            // 悬浮窗
            const TEXT = boxComponent.append('text').attr('font-size', '14px').attr('fill', 'white')
            let count = 0
            let maxLength = 0
            let Count = 0

            for (const i in info) {
              const length = TEXT.append('tspan').attr('x', '0').attr('y', count * 14 + Count * 10).text(i)['_groups'][0][0]['textLength']['baseVal']['value']
              if (length > maxLength) {
                maxLength = length
              }
              count++
              for (const j in info[i]) {
                const message = '● ' + j + ':' + info[i][j]

                const length = TEXT.append('tspan').attr('x', '0').attr('y', count * 20 + Count * 10).text(message)['_groups'][0][0]['textLength']['baseVal']['value']
                if (length > maxLength) {
                  maxLength = length
                }
                count++
              }
              Count++
            }

            boxComponent.insert('rect', 'text').attr('height', count * 20 + 15 + Count * 10)
              .attr('width', maxLength + 50).attr('fill', 'white')
              .attr('transform', 'translate(-25,-24)').attr('rx', 3)
              .attr('ry', 3).attr('fill', '#004986').style('opacity', '0.40')

            const boxComponentX = nodeWidth / 2
            let boxComponentY = -nodeHeight / 2 - (count * 14 + 20 + Count * 10) - 15
            if (nodeheight === 70) {
              boxComponentY = -nodeHeight / 2 - (count * 14 + 20 + Count * 10) - 30
            }

            boxComponent.attr('transform', 'translate(' + boxComponentX + ',' + boxComponentY + ')')

            d3.select('#' + nodeId).select('.label').select('g').select('text').attr('transform', 'translate(' + (-gap) + ',0)')

            //  改变节点颜色
            if (d3.select('#' + nodeId).select('rect').style('fill') === 'rgb(102, 102, 102)') {
              d3.select('#' + nodeId).select('rect').style('fill', 'rgb(102, 102, 102)')
            } else { // 若节点边没被隐藏，则正常恢复原来的颜色
              d3.select('#' + nodeId).select('rect').style('opacity', '1')
            }
            // 改变节点边框宽度
            if (d3.select('#' + nodeId).select('rect').style('stroke') === 'red') {
              d3.select('#' + nodeId).select('rect').style('stroke-width', '2.5').style('stroke', 'red')
            } else {
              d3.select('#' + nodeId).select('rect').style('stroke-width', '2.5').style('stroke', '#e4007f')
            }
          })

          // 添加鼠标移出事件
          nodeThis.on('mouseleave', function() {
            // 变回字体的原长
            if (nodeName.length > 12) {
              currName = nodeName.slice(0, 12) + '...'
            } else {
              currName = nodeName
            }
            d3.select('#' + nodeId).attr('flag', 0)
            d3.select('#' + nodeId).select('.label').select('g').select('text').select('tspan').text(currName)
            d3.select('#' + nodeId).select('.label').select('g').select('text').attr('transform', 'translate(0,0)')

            // 去除快速预览框
            d3.select('#messageBox').remove()

            //  若节点边被隐藏，则保持隐藏色不变
            if (d3.select('#' + nodeId).select('rect').style('fill') === 'rgb(102, 102, 102)') {
              d3.select('#' + nodeId).select('rect').style('fill', 'rgb(102, 102, 102)')
            } else if (d3.select('#' + nodeId).select('rect').style('fill') === 'blue') {
              d3.select('#' + nodeId).select('rect').style('fill', 'blue')
            } else if (d3.select('#' + nodeId).select('rect').style('fill') === 'red') {
              d3.select('#' + nodeId).select('rect').style('fill', 'red')
            } else { // 若节点边没被隐藏，则正常恢复原来的颜色
              d3.select('#' + nodeId).select('rect').style('fill', GetColorByNode(g, nodes))

              // 如果是 卷积层
              if (IsSpecialNode(nodes) === 1) {
                d3.select('#' + nodeId).select('rect').style('fill', '#e8c5df')
              }
              // 如果是 全连接层
              if (IsSpecialNode(nodes) === 2) {
                d3.select('#' + nodeId).select('rect').style('fill', '#b7d4ae')
              }
              if (IsDoubleNode(nodes) === 2) {
                d3.select('#' + nodeId).select('rect').style('fill', '#b7d4ae')
              }
              // 如果是 池化层
              if (IsSpecialNode(nodes) === 3) {
                d3.select('#' + nodeId).select('rect').style('fill', '#d7dafb')
              }
              if (IsDoubleNode(nodes) === 3) {
                d3.select('#' + nodeId).select('rect').style('fill', '#d7dafb')
              }
              // 如果是 归一化
              if (IsSpecialNode(nodes) === 4) {
                d3.select('#' + nodeId).select('rect').style('fill', '#daf4cc')
              }
              if (IsDoubleNode(nodes) === 4) {
                d3.select('#' + nodeId).select('rect').style('fill', '#daf4cc')
              }
            }
            // 恢复节点边框宽度和颜色
            if ((d3.select('#' + nodeId).select('rect').style('stroke')) === 'red') {
              d3.select('#' + nodeId).select('rect').style('stroke-width', '1').style('stroke', 'red')
            } else {
              d3.select('#' + nodeId).select('rect').style('stroke-width', '1').style('stroke', '#696969')
            }
          })

          nodeThis.on('click', function() {
            const reserverStageNode = self.reserve
            if (!g.node(nodeKey.id).clicked) {
              // 复原图内的点击节点
              if (self.lastClick) {
                self.restoreLastClick()
              }
              // 复原右侧栏点击节点
              if (self.lastAssistClick) {
                self.restoreLastClickRight()
              }
              self.lastAssistClick = ''
              self.lastClick = nodeKey.id
              g.node(nodeKey.id).clicked = true
              // 改变边颜色和相关节点外框的颜色
              edges.forEach(function(v) {
                // 让边变红
                const edgeID = v.v + '__' + v.w
                const edgeGroup = Array.from(d3.selectAll('.edgePath')['_groups'][0])
                const edgeLabelGroup = d3.selectAll('.edgeLabel')['_groups'][0]
                let index
                for (let i = 0; i < edgeGroup.length; i++) {
                  if (edgeGroup[i].id === edgeID) {
                    index = i
                    break
                  }
                }
                const dEdgeID = idTransform('#' + edgeID)
                d3.select(dEdgeID).select('.path').style('stroke', 'red').style('stroke-width', '1.5')
                d3.select(edgeLabelGroup[index]).select('g').select('text').attr('fill', 'red')
                // 让边的两个相关节点外框变红
                nodeFromID = idTransform('#' + v.v)
                nodeToID = idTransform('#' + v.w)
                d3.select(nodeFromID).select('rect').style('stroke', 'red')
                d3.select(nodeToID).select('rect').style('stroke', 'red')
              })
              d3.select(idTransform('#' + nodeKey.id)).select('rect').style('stroke', 'red')
              let info
              if (reserverStageNode.length) {
                const cur = reserverStageNode[reserverStageNode.length - 1]
                const curNodeInfo = cur.nodeInfo

                for (let i = 0; i < curNodeInfo.length; i++) {
                  if (curNodeInfo[i].uid === nodeKey.id) {
                    info = JSON.parse(JSON.stringify(curNodeInfo[i]))
                    break
                  }
                }
              }

              // 从右键隐藏节点中寻找连接节点改变颜色
              let initInfo
              for (let i = 0; i < nodeInfo.length; i++) {
                if (nodeInfo[i].uid === nodeKey.id) {
                  initInfo = nodeInfo[i]
                  break
                }
              }
              for (let i = 0; i < tmp.length; i++) {
                if (initInfo.inNode.indexOf(tmp[i].nodeId) >= 0) {
                  info.inNode.push(tmp[i].nodeId)
                  const oldfill = d3.select('#del__' + tmp[i].nodeId.replace(/\//g, '\\/').replace(/\(/g, '\\(').replace(/\)/g, '\\)').replace(/\]/g, '\\]').replace(/\[/g, '\\[')).select('rect').attr('oldfill')

                  if (oldfill) {
                    d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', oldfill)
                    d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', undefined)
                  } else {
                    const fill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('fill')
                    d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', 'blue')
                    d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', fill)
                  }
                }
                if (initInfo.outNode.indexOf(tmp[i].nodeId) >= 0) {
                  info.outNode.push(tmp[i].nodeId)
                  const oldfill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill')

                  if (oldfill) {
                    d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', oldfill)
                    d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', undefined)
                  } else {
                    const fill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('red')
                    d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', 'blue')
                    d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', fill)
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
        // -------------------------------------------------------------------------
        // 为每个父节点添加 - 号
        svg.selectAll('.cluster')['_groups'][0].forEach(function(nodeKey) {
          // nodeKey 当前用于动画的节点
          // 在/前加入转义字符，用于d3.select的搜索，防止报错
          const nodeId = idTransform(nodeKey.id)

          // 根据节点找到其对应的图的部分，根据事件对其中的text内容进行修改
          const nodeThis = d3.select(nodeKey)
          nodeThis.append('text')

          const width = parseInt(d3.select('#' + nodeId).select('rect').style('width'))
          const height = parseInt(d3.select('#' + nodeId).select('rect').style('height'))
          // 显示 - 号
          const size = d3.select('#' + nodeId).selectAll('text.expand').size()
          if (size <= 0) {
            d3.select('#' + nodeId).append('text')
              .attr('class', 'expand')
              .attr('x', width / 2 - 35)
              .attr('y', -height / 2 + 30)
              .style('font-weight', 'lighter')
              .style('font-size', '50px')
              .style('fill', 'white')
          }
          d3.select('#' + nodeId).selectAll('text.expand').text('-')
        })
        // -------------------------------------------------------------------------
        // 为控制边添加虚线
        g.edges().forEach(function(v) {
          const edgeID = v.v + '__' + v.w
          const dEdgeID = '#' + idTransform(edgeID)

          if (isDashed[edgeID] === 'true') {
            d3.select(dEdgeID).select('.path').style('stroke-dasharray', '5,3')
          }
          if (Number(isLines[edgeID]) > 1) {
            d3.select(dEdgeID).select('.path').style('stroke-width', '2')
          }
        })

        // 姜子敬
        // -------------------------------------------------------------------------------------------------------------
        // 右键菜单交互
        $('#draw').contextMenu({
          selector: '.node',
          items: {
            'invisible': {
              name: '隐藏相关边',
              icon: 'edit',
              callback: function() {
                const nodeId = this[0].id

                const edges = curg.nodeEdges(nodeId)
                // 改变节点样式
                // ----------------------------------------------------------------------------------------------------
                const oldfill = d3.select("[id='" + nodeId + "']").select('rect').style('fill')
                if (d3.select("[id='" + nodeId + "']").select('rect').attr('oldfill')) {
                  return
                }
                d3.select("[id='" + nodeId + "']").select('rect').attr('oldfill', oldfill)
                d3.select("[id='" + nodeId + "']").select('rect').style('fill', 'rgb(102, 102, 102)')
                // ----------------------------------------------------------------------------------------------------
                const edgeGroup = Array.from(d3.selectAll('.edgePath')['_groups'][0])
                const edgeLabelGroup = d3.selectAll('.edgeLabel')['_groups'][0]

                edges.forEach(function(v) {
                  // 边的选取和隐藏
                  const edgeId = '#' + idTransform(v.v + '__' + v.w)
                  d3.select(edgeId).select('.path').style('stroke', 'black').style('visibility', 'hidden')
                  const edgeDom = document.getElementById(v.v + '__' + v.w)
                  const index = edgeGroup.indexOf(edgeDom)

                  edgeLabelGroup[index]['attributes']['style']['value'] = 'opacity: 1;visibility:hidden'
                })
              }
            },
            'visible': {
              name: '显示相关边',
              icon: 'cut',
              callback: function() {
                const nodeId = this[0].id
                const edges = curg.nodeEdges(nodeId)
                // 恢复节点样式
                // ----------------------------------------------------------------------------------------------------
                const oldfill = d3.select("[id='" + nodeId + "']").select('rect').attr('oldfill')
                if (!oldfill) {
                  return
                }
                d3.select("[id='" + nodeId + "']").select('rect').attr('oldfill', null)
                d3.select("[id='" + nodeId + "']").select('rect').style('fill', oldfill)
                // ----------------------------------------------------------------------------------------------------
                const edgeGroup = Array.from(d3.selectAll('.edgePath')['_groups'][0])
                const edgeLabelGroup = d3.selectAll('.edgeLabel')['_groups'][0]
                edges.forEach(function(v) {
                  // 边的选取和显示
                  const edgeId = '#' + idTransform(v.v + '__' + v.w)
                  d3.select(edgeId).select('.path').style('visibility', 'visible')

                  const edgeDom = document.getElementById(v.v + '__' + v.w)
                  const index = edgeGroup.indexOf(edgeDom)
                  edgeLabelGroup[index]['attributes']['style']['value'] = 'opacity: 1;visibility:visible'
                })
              }
            },
            'delete': {
              name: '隐藏节点',
              icon: 'delete',
              callback: function() {
                const nodeInfo = self.nodeInfo
                // eslint-disable-next-line no-unused-vars
                const g = self.curg
                // eslint-disable-next-line no-unused-vars
                let delNode = []
                for (let i = 0; i < nodeInfo.length; i++) {
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
                const oldfill = d3.select("[id='" + nodeId + "']").select('rect').style('fill')

                // 遍历所有步骤删除节点及相关边
                for (let i = 0; i < reserverStageNode.length; i++) {
                  const curNodeInfo = reserverStageNode[i].nodeInfo
                  for (let j = curNodeInfo.length - 1; j >= 0; j--) {
                    if (curNodeInfo[j].uid === nodeId) {
                      curNodeInfo.splice(j, 1)
                    } else {
                      const inNode = curNodeInfo[j].inNode
                      const outNode = curNodeInfo[j].outNode
                      for (let k = 0; k < inNode.length; k++) {
                        if (inNode[k] === nodeId) {
                          inNode.splice(k, 1)

                          break
                        }
                      }
                      for (let k = 0; k < outNode.length; k++) {
                        if (outNode[k] === nodeId) {
                          outNode.splice(k, 1)
                          break
                        }
                      }
                    }
                  }
                }
                tmp.push({ nodeId, color: oldfill })
                // 双击移出去保持颜色
                drawAssist(oldfill)

                d3.select('#assist').select('svg').selectAll('g').on('dblclick', function() {
                  const nodeId = this['id'].split('__')[1]

                  const index = tmp.findIndex(item => item.nodeId === nodeId)
                  self.restoreNode = nodeId
                  tmp.splice(index, 1)

                  // 双击移持回来保颜色
                  drawAssist(oldfill)
                  getModifyClick(nodeId)
                  draw(self.srcData, init)
                }).on('click', function() {
                  // 复原图内的点击节点
                  if (self.lastClick) {
                    self.restoreLastClick()
                  }
                  self.lastClick = ''
                  // 复原上次点击节点的颜色
                  if (self.lastAssistClick && self.lastAssistClick !== this['id']) {
                    self.restoreLastClickRight()
                  }
                  const nodeId = this['id'].split('__')[1]
                  if (self.lastAssistClick === this['id']) {
                    self.lastAssistClick = ''
                  } else {
                    self.lastAssistClick = this['id']
                  }

                  let info = getDelNodeInfo(nodeId, nodeInfo)
                  if (!info) {
                    info = { 'info': '无信息' }
                  } else {
                    const inNode = info.inNode
                    const outNode = info.outNode
                    for (let i = 0; i < inNode.length; i++) {
                      const nodeId = '#' + idTransform(inNode[i])
                      if (!d3.select(nodeId).select('rect').attr('tag')) {
                        const old = d3.select(nodeId).select('rect').style('fill')
                        d3.select(nodeId).select('rect').attr('tag', old)
                        d3.select(nodeId).select('rect').style('fill', 'blue')
                        drawCircleTag(nodeId, 'out', 1)
                      } else {
                        const old = d3.select(nodeId).select('rect').attr('tag')
                        d3.select(nodeId).select('rect').style('fill', old)
                        d3.select(nodeId).select('rect').attr('tag', null)
                        drawCircleTag(nodeId, 'out', 0)
                      }
                    }

                    for (let i = 0; i < outNode.length; i++) {
                      const nodeId = '#' + idTransform(outNode[i])
                      if (!d3.select(nodeId).select('rect').attr('tag')) {
                        const old = d3.select(nodeId).select('rect').style('fill')
                        d3.select(nodeId).select('rect').attr('tag', old)
                        d3.select(nodeId).select('rect').style('fill', 'red')
                        drawCircleTag(nodeId, 'in', 1)
                      } else {
                        const old = d3.select(nodeId).select('rect').attr('tag')
                        d3.select(nodeId).select('rect').style('fill', old)
                        d3.select(nodeId).select('rect').attr('tag', null)
                        drawCircleTag(nodeId, 'in', 0)
                      }
                    }
                    // 获取隐藏节点中的连接节点
                    let initInfo
                    for (let i = 0; i < nodeInfo.length; i++) {
                      if (nodeInfo[i].uid === info.uid) {
                        initInfo = nodeInfo[i]
                        break
                      }
                    }
                    for (let i = 0; i < tmp.length; i++) {
                      if (initInfo.inNode.indexOf(tmp[i].nodeId) >= 0) {
                        info.inNode.push(tmp[i].nodeId)
                        const oldfill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill')
                        if (oldfill) {
                          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', oldfill)
                          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', undefined)
                        } else {
                          const fill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('fill')
                          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', 'blue')
                          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', fill)
                        }
                      }
                      if (initInfo.outNode.indexOf(tmp[i].nodeId) >= 0) {
                        info.outNode.push(tmp[i].nodeId)
                        const oldfill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill')
                        if (oldfill) {
                          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', oldfill)
                          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', undefined)
                        } else {
                          const fill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('fill')
                          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', 'red')
                          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', fill)
                        }
                      }
                    }
                  }

                  getInfo(JSON.stringify(info))
                })
                // 隐藏相关边及节点
                const edges = d3.selectAll('.edgePath')['_groups'][0]
                const edgeLabel = d3.selectAll('.edgeLabel')['_groups'][0]
                for (let i = 0; i < edges.length; i++) {
                  const v2w = edges[i]['id'].split('__')
                  if (v2w[0] === nodeId) {
                    edgeLabel[i].getElementsByTagName('g')[0]['style']['opacity'] = '0'
                    edges[i].children[0].style = 'opacity: 1;visibility:hidden'
                  }
                  if (v2w[1] === nodeId) {
                    edgeLabel[i].getElementsByTagName('g')[0]['style']['opacity'] = '0'
                    edges[i].children[0].style = 'opacity: 1;visibility:hidden'
                  }
                }
                d3.select('#' + idTransform(nodeId)).style('visibility', 'hidden')
                changeTag = 1
                curg.removeNode(nodeId)
              }
            }
          }
        })
        // -------------------------------------------------------------------------------------------------------------
      }
      // draw函数结束
      const init = true
      draw(data, init)
    },

    getDelNodeInfo(nodeID) {
      // 获取差集
      function subSet(arr1, arr2) {
        const set1 = new Set(arr1)
        const set2 = new Set(arr2)
        var subset = []

        for (const item of set1) {
          if (!set2.has(item)) {
            subset.push(item)
          }
        }
        return subset
      }
      const reserverStageNode = this.reserve
      const nodeInfo = this.nodeInfo
      const length = nodeInfo.length
      let node
      // 获取隐藏节点原始信息
      for (let i = 0; i < length; i++) {
        if (nodeInfo[i].uid === nodeID) {
          node = JSON.parse(JSON.stringify(nodeInfo[i]))
          break
        }
      }
      if (!node) {
        return
      }
      // 获取当前所有节点名
      const inNode = node.inNode
      const outNode = node.outNode
      const lastStageNode = reserverStageNode[reserverStageNode.length - 1].nodeInfo
      const curNodes = []
      lastStageNode.forEach(function(v) {
        curNodes.push(v.uid)
      })
      // 得到在图中的连接节点
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
      console.log(this.showTag)

      d3.select('#assist').select('svg').selectAll('g').remove()
      let maxlength = 0
      for (let i = 0; i < tmp.length; i++) {
        const item = tmp[i]
        let nodeName = item.nodeId
        const index = nodeName.lastIndexOf('\/')
        nodeName = nodeName.substring(index + 1, nodeName.length)
        const rectWidth = 12 * nodeName.length + 20
        if (rectWidth > maxlength) {
          maxlength = rectWidth
        }

        const g = d3.select('#assist').select('svg').append('g').attr('transform', 'translate(' + 0 + ',' + (50 * i + 20) + ')').attr('id', 'del__' + item.nodeId)
        g.append('rect')
          .attr('width', rectWidth)
          .attr('height', 25)
          .attr('fill', item.color)
          .attr('stroke-width', '0.5px')
          .attr('rx', 12.5).attr('ry', 12.5)
          .attr('stroke', '#696969')

        g.append('text').text(nodeName).attr('dy', '1em').attr('text-anchor', 'middle').attr('transform', 'translate(' + rectWidth / 2 + ',0)')
      }

      d3.select('#assist').select('svg').attr('width', maxlength).attr('height', 50 * tmp.length + 50)
    },
    getModifyClick(val) {
      let ob
      const nodeInfo = this.nodeInfo
      let obsec

      for (let i = 0; i < nodeInfo.length; i++) {
        if (nodeInfo[i].uid === val) {
          obsec = ob = nodeInfo[i]
          break
        }
      }
      if (!ob) {
        return
      }
      const reserverStageNode = this.reserve
      const innode = ob.inNode
      const outnode = ob.outNode
      for (let i = reserverStageNode.length - 1; i >= 0; i--) {
        if (reserverStageNode[i].sign === 1) {
          reserverStageNode.splice(i + 1, reserverStageNode.length - i - 1)
          break
        }
      }
      // 遍历所有stage加上节点
      for (let i = 0; i < reserverStageNode.length; i++) {
        obsec.inNode = []
        obsec.outNode = []

        for (let j = 0; j < reserverStageNode[i].nodeInfo.length; j++) {
          const curNode = reserverStageNode[i].nodeInfo[j]
          for (let z = 0; z < innode.length; z++) {
            if (curNode.uid === innode[z]) {
              curNode.outNode.push(ob.uid)
              obsec.inNode.push(curNode.uid)
              break
            }
          }
          for (let z = 0; z < outnode.length; z++) {
            if (curNode.uid === outnode[z]) {
              curNode.inNode.push(ob.uid)
              obsec.outNode.push(curNode.uid)
              break
            }
          }
        }
        reserverStageNode[i].nodeInfo.push(obsec)
      }

      for (let i = 0; i < clickDel.length; i++) {
        if (clickDel[i].uid === ob.uid) {
          clickDel.splice(i, 1)
        }
      }
    },
    glitter(val) {
      var idTransform = this.idTransform
      if (!val) {
        return
      }

      const nodeId = '#' + idTransform(val)
      const node = d3.select(nodeId)
      this.restoreNode = ''
      if (node) {
        let old = ''
        // 判断在隐藏内容中是否有当前选择标签，没有会抛出异常
        old = d3.select(nodeId).select('rect').style('fill')

        // 高亮样式设置
        d3.select(nodeId).select('rect').style('fill', 'red')

        setTimeout(function() {
          old && d3.select(nodeId).select('rect').style('fill', old)
        }, 1000)
      }
    },
    drawCircleTag(nodeId, dir, flag) {
      const node = d3.select(nodeId)
      if (flag) {
        const cx = 0
        const nodeRect = node.select('rect')
        let cy = nodeRect['_groups'][0][0]['attributes']['height']['value']
        cy = Number(cy) / 2
        if (dir === 'out') {
          node.append('circle').attr('cx', cx).attr('cy', cy).attr('r', 4).attr('fill', 'blue')
        } else if (dir === 'in') {
          node.append('circle').attr('cx', cx).attr('cy', -cy).attr('r', 4).attr('fill', 'red')
        }
      } else {
        node.select('circle').remove()
      }
    },
    hidden() {
      // 异常不做处理-------------------------------------------------------------
      const reserverStageNode = this.reserve
      var idTransform = this.idTransform
      // 对上个状态深拷贝--------------------------------------------------------------------------------
      const stages = reserverStageNode.length
      let curStage
      const waiting = []
      if (stages === 0) {
        curStage = { 'sign': 0 }
        curStage.nodeInfo = JSON.parse(JSON.stringify(this.nodeInfo))
      } else {
        if (reserverStageNode[stages - 1].sign === 0) {
          this.pre()
          curStage = JSON.parse(JSON.stringify(reserverStageNode[stages - 2]))
          curStage.sign = 0
        } else {
          curStage = JSON.parse(JSON.stringify(reserverStageNode[stages - 1]))
          curStage.sign = 0
        }
      }
      // 找出待处理点-----------------------------------------------------------------------------------------------

      const cNodeInfo = curStage.nodeInfo
      for (let i = 0; i < cNodeInfo.length; i++) {
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
      // 查找待处理点结束--------------------------------------------------------------------------------------------------------------------------------------------------------------
      // 隐藏相关边及节点----------------------------------------------------------------------------------------------------------------------------------------------------------------
      if (waiting.length === 0) {
        return
      } else {
        const edgeGroup = Array.from(d3.selectAll('.edgePath')['_groups'][0])
        const edgeLabelGroup = d3.selectAll('.edgeLabel')['_groups'][0]
        for (let i = 0; i < waiting.length; i++) {
          const edges = curg.nodeEdges(waiting[i])

          edges.forEach(function(v) {
            const edgeId = '#' + idTransform(v.v + '__' + v.w)
            d3.select(edgeId).select('.path').style('visibility', 'hidden')
            const edgeDom = document.getElementById(v.v + '__' + v.w)
            const index = edgeGroup.indexOf(edgeDom)
            edgeLabelGroup[index]['attributes']['style']['value'] = 'opacity: 1;visibility:hidden'
          })
          const nodeId = '#' + idTransform(waiting[i])
          d3.select(nodeId).style('visibility', 'hidden')
        }
      }
      // 结束----------------------------------------------------------------------------------------------
      // 对状态做修改----------------------------------------------------------------------------------------
      // 删除隐藏节点------------------------------------------------------------------------
      for (let i = cNodeInfo.length - 1; i >= 0; i--) {
        let tag = 1
        for (let j = 0; j < waiting.length; j++) {
          if (cNodeInfo[i].uid === waiting[j]) {
            tag = 0
            cNodeInfo.splice(i, 1)
            break
          }
        }
        // 删除隐藏边----------------------------------------------------------------------------
        if (tag) {
          const inNode = cNodeInfo[i].inNode
          const outNode = cNodeInfo[i].outNode
          for (let j = outNode.length - 1; j >= 0; j--) {
            for (let k = 0; k < waiting.length; k++) {
              if (outNode[j] === waiting[k]) {
                outNode.splice(j, 1)
              }
            }
          }
          for (let j = inNode.length - 1; j >= 0; j--) {
            for (let k = 0; k < waiting.length; k++) {
              if (inNode[j] === waiting[k]) {
                inNode.splice(j, 1)
              }
            }
          }
        }
      }
      // 结束-------------------------------------------------------------
      reserverStageNode.push(curStage)
      delStageNode.push(waiting)
    },
    run() {
      const stages = reserverStageNode.length
      let curStage
      if (stages === 0) {
        return
      } else {
        curStage = JSON.parse(JSON.stringify(reserverStageNode[stages - 1]))
        curStage.sign = 1
      }
      // 清除隐藏
      let hiddenLayer = 0
      let tag = 1
      for (let i = stages - 1; i >= 0; i--) {
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
      // 合并隐藏

      let delNode = []
      const len = delStageNode.length
      for (let i = 0; i < hiddenLayer; i++) {
        delNode = delNode.concat(delStageNode[len - 1 - i])
      }
      delStageNode.splice(len - hiddenLayer, hiddenLayer)
      changeTag = 0
      delStageNode.push(delNode)
      this.drawGraph()
    },
    pre() {
      var idTransform = this.idTransform
      const length = reserverStageNode.length
      let lastSign = -1
      if (length === 1) {
        return
      }

      for (let i = reserverStageNode.length - 1; i >= 1; i--) {
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

        for (let i = 0; i < waiting.length; i++) {
          const tNodeInfo = this.getDelNodeInfo(waiting[i])

          const edges = []
          for (let j = 0; j < tNodeInfo.inNode.length; j++) {
            edges.push(tNodeInfo.inNode[j] + '__' + waiting[i])
          }
          for (let j = 0; j < tNodeInfo.outNode.length; j++) {
            edges.push(waiting[i] + '__' + tNodeInfo.outNode[j])
          }

          d3.select('#' + idTransform(waiting[i])).style('visibility', 'visible')
          const edgeGroup = Array.from(d3.selectAll('.edgePath')['_groups'][0])
          const edgeLabelGroup = d3.selectAll('.edgeLabel')['_groups'][0]
          edges.forEach(function(v) {
            // 边的选取和隐藏
            const edgeId = '#' + idTransform(v)
            d3.select(edgeId).select('.path').style('visibility', 'visible')
            const edgeDom = document.getElementById(v)
            const index = edgeGroup.indexOf(edgeDom)
            edgeLabelGroup[index]['attributes']['style']['value'] = 'opacity: 1;visibility:visible'
          })
        }
      }
    },
    // 复原在图中点击的
    restoreLastClick() {
      const nodeInfo = this.nodeInfo
      const g = this.curg
      var idTransform = this.idTransform
      g.node(this.lastClick).clicked = false
      // 变回边的颜色
      const lastEdges = g.nodeEdges(this.lastClick)
      lastEdges.forEach(function(v) {
        // 让节点变回原色
        const edgeID = v.v + '__' + v.w
        const edgeGroup = Array.from(d3.selectAll('.edgePath')['_groups'][0])
        const edgeLabelGroup = d3.selectAll('.edgeLabel')['_groups'][0]
        let index
        for (let i = 0; i < edgeGroup.length; i++) {
          if (edgeGroup[i].id === edgeID) {
            index = i
            break
          }
        }
        const dEdgeID = idTransform('#' + edgeID)
        // let edgeDom=d3.select(dEdgeID)
        d3.select(dEdgeID).select('.path').style('stroke', 'black').style('stroke-width', '1')
        d3.select(edgeLabelGroup[index]).select('g').select('text').attr('fill', 'black')

        // 让边的两个相关节点外框变回原色
        const nodeFromID = idTransform('#' + v.v)
        const nodeToID = idTransform('#' + v.w)
        d3.select(nodeFromID).select('rect').style('stroke', '#696969')
        d3.select(nodeToID).select('rect').style('stroke', '#696969')
      })
      // 当上一次点击节点是扩展时高亮时，以上不能取消颜色
      d3.select('#' + idTransform(this.lastClick)).select('rect').style('stroke', '#c9c9c9')
      d3.select(`[id="${idTransform(this.lastClick)}"]`).select('rect').style('stroke-width', '1').style('stroke', '#696969')

      let initInfo

      for (let i = 0; i < nodeInfo.length; i++) {
        if (nodeInfo[i].uid === this.lastClick) {
          initInfo = nodeInfo[i]
          break
        }
      }
      // foreign内的连接节点
      for (let i = 0; i < tmp.length; i++) {
        if (initInfo.inNode.indexOf(tmp[i].nodeId) >= 0) {
          const oldfill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill')
          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', oldfill)
          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', undefined)
        }
        if (initInfo.outNode.indexOf(tmp[i].nodeId) >= 0) {
          const oldfill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill')

          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', oldfill)
          d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', undefined)
        }
      }
      this.lastClick = ''
    },
    // 复原在右侧栏点击
    restoreLastClickRight() {
      var idTransform = this.idTransform
      const nodeInfo = this.nodeInfo
      const nodeId = this.lastAssistClick.split('__')[1]
      const info = this.getDelNodeInfo(nodeId, nodeInfo)
      const inNode = info.inNode
      const outNode = info.outNode
      // 复原图中的节点颜色
      for (let i = 0; i < inNode.length; i++) {
        const nodeId = idTransform('#' + inNode[i])
        const old = d3.select(nodeId).select('rect').attr('tag')
        d3.select(nodeId).select('rect').style('fill', old)
        d3.select(nodeId).select('rect').attr('tag', null)
        this.drawCircleTag(nodeId, 'out', 0)
      }

      for (let i = 0; i < outNode.length; i++) {
        const nodeId = idTransform('#' + outNode[i])
        const old = d3.select(nodeId).select('rect').attr('tag')
        d3.select(nodeId).select('rect').style('fill', old)
        d3.select(nodeId).select('rect').attr('tag', null)
        this.drawCircleTag(nodeId, 'in', 0)
      }
      // 复原右侧栏内节点颜色
      let initInfo
      for (let i = 0; i < nodeInfo.length; i++) {
        if (nodeInfo[i].uid === info.uid) {
          initInfo = nodeInfo[i]
          break
        }
      }

      for (let i = 0; i < tmp.length; i++) {
        if (initInfo.inNode.indexOf(tmp[i].nodeId) >= 0) {
          info.inNode.push(tmp[i].nodeId)
          const oldfill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill')
          if (oldfill) {
            d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', oldfill)
            d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', undefined)
          }
        }
        if (initInfo.outNode.indexOf(tmp[i].nodeId) >= 0) {
          info.outNode.push(tmp[i].nodeId)
          const oldfill = d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill')
          if (oldfill) {
            d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').style('fill', oldfill)
            d3.select('#del__' + idTransform(tmp[i].nodeId)).select('rect').attr('oldfill', undefined)
          }
        }
      }
      this.lastAssistClick = ''
    },
    idTransform(id) {
      var id_ = id.replace(/\//g, '\\/').replace(/\(/g, '\\(').replace(/\)/g, '\\)').replace(/\]/g, '\\]').replace(/\[/g, '\\[').replace(/\./g, '\\.')
      return id_
    }
  }

}

</script>
