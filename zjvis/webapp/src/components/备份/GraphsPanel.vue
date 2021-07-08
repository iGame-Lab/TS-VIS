<style lang="less" scoped>
  .temp{
      height: 100px
  }
  .mainSection{
    box-shadow: 0 0 4px 0 rgba(143, 143, 180, 0.24)
  }
  .buttonOption1{
    padding: 7px 10px;
  }
  .buttonOption2{
    padding: 7px 7px;
  }
  .buttons{
    margin-top: 6%;
    margin-left: 4%;
    margin-right: 4%;
    .el-button{
      background-color: #dfe7fd;
      width:20%;
      color:#270089;
      font-size: 10px;
    }
    .el-button:hover{
      background-color: #8f8bd8;
      color:#ffffff;
    }
    .el-button:focus{
      background-color: #8f8bd8;
      color:#ffffff;
    }
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .graphPanel {
    width:94%;
    margin:5% 3% 0 3%;
  }
  // .datasetsHead,
  .graphPanelHead{
    width:100%;
    height:30px;
    display: inline-flex;
    font-size:13px;
  }
  .graphhead1, .graphhead2{
    height: 30px;
    color: white;
    font-weight: 700;
    line-height: 30px;
    width: 49%;
  }
  .graphhead1 {
    // border: 1px solid white;
    background-color: #b8c6ff;
  }
  .graphhead2 {
    // border: 1px solid rgb(84, 116, 223);
    background-color: #625eb3;
  }
  #c-graph{
    border-radius: 3px;
    margin-right:2%;
  }
  #s-graph{
    border-radius: 3px;
  }
  .graphPanelContent{
    border-radius: 0 0 3px 3px;
    text-align: left;
    font-size:12px;
  }
  .andRow, .orRow{
    text-align: center;
    margin-top: 2%;
    margin-bottom: 2%;
  }
  .el-link.el-link--default.is-disabled{
    color: #000000;
    font-size: 20%;
  }
  .info{
    width:94%;
    margin:8% 3% 0 3%;
  }
  .infoTitle{
    background-color:#625eb3;
    border-radius: 3px;
    color:white;
    text-align:left;
    font-weight: 700;
    height:30px;
    line-height: 30px;
    padding-left:5%;
    font-size: 13px;
    .dot{
      margin-right:2%;
    }
  }
  .infoContent{
    font-size: 13px;
  }
  .el-select-dropdown__item.selected{
    color:#8F8AD7;
  }
  .information .el-button--mini{
    padding:0
  }
  .choose{
    border: none;
    padding:0
  }
  .cardStyle{
    margin-bottom: 2%;
    margin-top: 2%;
  }
  .infoTitle .el_card_body{
    padding-bottom: 20px
  }
  .ddot{
  display: inline-block;
  width: 5px;
  height: 5px;
  margin-right: 5px;
  background: blue;
  vertical-align: middle;
  overflow: hidden;
  }

  li{list-style:none}
  .information .el-button{
    border:none;
  }
  /deep/ .information .el-card__body{
    padding: 10px 20px 20px 10px;
  }
  /deep/ .el-input__inner{
    border: #FFFFFF;
    box-shadow: 0 0 4px 0 rgba(143, 143, 180, 0.24);
    font-size: xx-small;
    text-align: center;
    padding: 0 12px;
  }
  /deep/ .selection1 .el-input__inner{
    padding: 0 1px;
  }
  /deep/ .el-input__suffix{
    right: 0;
  }
  /deep/ .el-input--suffix .el-input__inner {
    padding-right: 16px;
  }
  /deep/ .el-select .el-input .el-select__caret{
    color: #662d91;
    font-size: 10px;
  }
  /deep/ .el-input__icon {
    width: 20px;
  }
  /deep/ .iconfont {
     font-family: "iconfont" !important;
     -webkit-font-smoothing: antialiased;
     font-size: 20px;
   }
  .el-button--mini, .el-button--mini.is-round {

  }
  /deep/ ul{
    padding:0;
    margin:0 0 0 7%;
    text-align:left;
    list-style-type:none;
  }
</style>

<template>

  <div class="temp">

    <div class="graphPanel">

      <div class="graphPanelHead">
        <div
          id="c-graph"
          :class="[cGraph?'graphhead2':'graphhead1']"
          @click="changeTag('c_graph')"
        >计算图</div>
        <div
          id="s-graph"
          :class="[cGraph?'graphhead1':'graphhead2']"
          @click="changeTag('s_graph')"
        >结构图</div>
      </div>
      <el-card>
        <div class="graphPanelContent">
          <div v-show="cGraph" class="cGraphPanel">

            <el-row style="margin-bottom: 7%; font-size: 15px">条件过滤</el-row>

            <template v-for="(item1,index1) in item">

              <template v-if="index1">
                <el-row :key="index1+'orRow'" class="orRow">
                  <el-link disabled>OR</el-link>
                </el-row>
              </template>

              <el-row :key="index1+'mainSection'" class="mainSection">

                <el-row style="height: 5%">
                  <div style="float:right">
                    <el-button
                      :icon="0?'iconfont icon-zise':'iconfont icon-zise-'"
                      style="color:#662d91"
                      size="mini"
                      class="choose"
                      @click="delOr(index1)"
                    />
                  </div>
                </el-row>

                <template v-for="(item2,index2) in item1">

                  <template v-if="index2">
                    <el-row :key="index1+'-'+index2+'-seg'" class="andRow">
                      <el-link disabled>AND</el-link>
                    </el-row>
                  </template>

                  <div :key="index1+'-'+index2+'-section'" style="margin-left: 4%; margin-right: 2%">
                    <el-row :key="index1+'-'+index2+'-condition'" class="coloredRow">
                      <el-col :span="22">
                        <el-row :gutter="7">
                          <el-col :span="8">
                            <el-select v-model="item2.type" placeholder="入(出)度" size="mini" class="selection1">
                              <el-option
                                v-for="item0 in options"
                                :key="item0.value"
                                :label="item0.label"
                                :value="item0.value"
                              />
                            </el-select>
                          </el-col>

                          <el-col :span="8">
                            <el-select v-model="item2.tag" placeholder="符号" size="mini" class="selection2">
                              <el-option
                                v-for="item5 in tags"
                                :key="item5.value"
                                :label="item5.label"
                                :value="item5.value"
                              />
                            </el-select>
                          </el-col>

                          <el-col :span="8">
                            <el-input v-model="item2.num" placeholder="" size="mini" class="selection" />
                          </el-col>
                        </el-row>

                      </el-col>
                      <el-col :span="2" style="padding: 0">
                        <div style="margin-top:20%">
                          <el-button
                            :icon="0?'iconfont icon-huangse':'iconfont icon-huangse-'"
                            style="color:#fbb03b"
                            size="mini"
                            class="choose"
                            @click="delAnd(item1,item2,index1,index2)"
                          />
                        </div>
                      </el-col>
                    </el-row>
                  </div>

                </template>
                <el-row>
                  <div style="margin-left:47%; margin-top: 2%; margin-bottom: 2%">
                    AND
                    <el-button
                      :icon="1?'iconfont icon-huangse':'iconfont icon-huangse-'"
                      style="color:#fbb03b"
                      size="mini"
                      class="choose"
                      @click="addAnd(item1)"
                    />
                  </div>
                </el-row>
              </el-row>

            </template>

            <el-row>
              <div style="margin-left:47%; margin-top: 3%; margin-bottom: 3%">
                OR
                <el-button
                  :icon="1?'iconfont icon-zise':'iconfont icon-zise-'"
                  class="choose"
                  style="color:#662d91"
                  size="mini"
                  @click="addOr()"
                />
              </div>
            </el-row>

          </div>
          <div v-show="!cGraph" class="sGraphPanel">
            <div>
              <el-select v-model="value1" placeholder="请选择" style="width:100%">
                <el-option
                  v-for="item2 in option"
                  :key="item2.value"
                  :label="item2.label"
                  :value="item2.value"
                />
              </el-select>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <div class="buttons">
      <el-button v-show="cGraph" class="buttonOption1" round size="mini" @click="hidde()">隐藏</el-button>
      <el-button v-if="cGraph" class="buttonOption1" round size="mini" @click="Run()">布局</el-button>
      <el-button v-if="!cGraph" class="buttonOption1" style="margin-left: 40%" round size="mini" @click="Run()">布局</el-button>
      <el-button v-show="cGraph" class="buttonOption2" round size="mini" @click="Pre()">上一步</el-button>
      <el-button v-show="cGraph" class="buttonOption2" round size="mini" @click="Clear()">初始化</el-button>
    </div>

    <div class="info">
      <div class="infoTitle"><i class="el-icon-chat-line-round dot" />数据信息栏</div>
      <el-card>
        <div class="infoContent">
          <template v-for="(item3,index) in obj">
            <div :key="index+'-control'" class="information" style="float:left;clear:both;width:100%">
              <el-card class="cardStyle">
                <el-col :span="24">

                  <el-col :span="3">
                    <div style="float:left; margin-bottom:10px">
                      <el-button
                        :icon="tag[index] == 0?'iconfont icon-suohui':'iconfont icon-zhankai1'"
                        style="color:#6f6bd8"
                        size="mini"
                        @click="switchTag(index)"
                      />
                    </div>
                  </el-col>

                  <el-col :span="21">
                    <div style="float:left;margin-bottom:5%">
                      {{ index }}
                    </div>
                  </el-col>

                </el-col>
              </el-card>
            </div>

            <div :id="index" :key="index+'-box'" class="flag" style="display:&quot;inline&quot;;clear:both">
              <ul>
                <template v-for="(name,value4) in item3">
                  <div :key="value4" style="clear:both;padding:1%">
                    <li>
                      <el-col :span="12">
                        <div style="float:left"><span class="ddot" />{{ value4 }}</div>
                      </el-col>

                      <div style="float:left">{{ name }}</div>
                    </li>
                  </div>
                </template>
              </ul>
            </div>
          </template>

        </div>
      </el-card>
    </div>
  </div>

</template>

<script>
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import { createNamespacedHelpers } from 'vuex'
import * as d3 from 'd3'
Vue.use(ElementUI)

const {
  // mapGetters: mapGraphGetters,
  mapGetters: mapGraphGetters,
  mapMutations: mapGraphMutations
} = createNamespacedHelpers('graph')
const { mapState: mapLayoutStates } = createNamespacedHelpers('layout')
export default {

  name: 'GraphsPanel',
  data() {
    return {
      initTag: 'y',
      value1: '',
      option: [],
      tag: {
        NODE_PROPERTIES: 0,
        INPUTS: 0,
        OUTPUTS: 0,
        ATTRIBUTES: 0 },
      graphDegree: 100,
      reg: '',
      clickNode: [],
      value: '',
      min: '',
      max: '',
      text1: '',
      text2: '',
      obj: '',
      options: [{
        value: 'input',
        label: '入度'
      }, {
        value: 'output',
        label: '出度'
      }],
      tags: [{
        value: '<',
        label: '<'
      }, {
        value: '<=',
        label: '<='
      }, {
        value: '==',
        label: '='
      }, {
        value: '>',
        label: '>'
      }, {
        value: '>=',
        label: '>='
      }],
      item: [[{ 'type': '', 'tag': '', 'num': '' }]],
      Reg: '',
      tagRadioFlag: true,
      cGraph: true
    }
  },
  computed: {
    ...mapGraphGetters([
      'getInfo',
      'getClick',
      'getRunName',
      'getTagName',
      'getCurTag',
      'getRunChangeTag',
      'getIsDrawing',
      'getSList',
      'getInitOption'
    ]),
    ...mapLayoutStates(['userSelectRunFile'])
  },
  watch: {
    getInitOption(val) {
      this.value1 = val
    },
    getSList(val) {
      this.option = val
    },
    value1(val) {
      this.setData(val)
    },
    getCurTag(val) {
      this.obj = ''
      if (val === 'c_graph') {
        this.cGraph = true
      } else {
        this.cGraph = false
      }
    },
    userSelectRunFile() {
      if (this.getCurTag === 'c_graph') {
        this.cGraph = true
      } else {
        this.cGraph = false
      }
    },
    getInfo(val) {
      d3.selectAll('.flag').style('display', '')
      this.tag.ATTRIBUTES = 1
      this.tag.INPUTS = 1
      this.tag.OUTPUTS = 1
      this.tag.NODE_PROPERTIES = 1
      const obj = JSON.parse(val)
      const info = {}

      if (obj['info']) {
        if (obj['info'] === 'init') {
          this.obj = ''
        }
        return
      }
      // 建立节点本身属性
      info['NODE_PROPERTIES'] = {}
      info['NODE_PROPERTIES'].name = obj.uid
      if (obj.op) {
        info['NODE_PROPERTIES'].op = obj.op
      }

      // 建立attrs属性
      if (obj.attr) {
        info['ATTRIBUTES'] = {}
        for (const i in obj.attr) {
          if (i === '_output_shapes') {
            if (obj.attr[i].length === 1) {
              if (obj.attr[i][0] !== '') {
                info['ATTRIBUTES'][i] = obj.attr[i][0]
              }
            } else {
              info['ATTRIBUTES'][i] = obj.attr[i]
            }
          } else if (i === 'shape') {
            if (obj.attr[i] !== '') {
              info['ATTRIBUTES'][i] = obj.attr[i]
            }
          } else {
            info['ATTRIBUTES'][i] = obj.attr[i]
          }
        }
      }

      if (obj.inNode.length > 0) {
        info['INPUTS'] = {}
        const name = 'input'
        if (obj.inNode.length === 1) {
          info['INPUTS'][name] = obj.inNode[0]
        } else {
          let curname = ''
          for (const i in obj.inNode) {
            curname = name + i.toString()
            info['INPUTS'][curname] = obj.inNode[i]
          }
        }
      }

      if (obj.outNode.length > 0) {
        info['OUTPUTS'] = {}
        const name = 'output'
        if (obj.outNode.length === 1) {
          info['OUTPUTS'][name] = obj.outNode[0]
        } else {
          let curname = ''
          for (const i in obj.outNode) {
            curname = name + i.toString()
            info['OUTPUTS'][curname] = obj.outNode[i]
          }
        }
      }

      this.obj = info
    },
    getClick(val) {
      this.clickNode.push(val)
    }
  },
  mounted() {
    if (this.getCurTag === 'c_graph') {
      this.cGraph = true
    } else {
      this.cGraph = false
    }
    this.option = this.getSList
    this.value1 = this.getInitOption
  },
  methods: {
    ...mapGraphMutations([
      'Clear',
      'regularEx',
      'Run',
      'Hidden',
      'Pre',
      'Modify',
      'regClear',
      'setCurTag',
      'setData'
    ]),
    changeTag(param) {
      // 保证不会在切换run时可以切换tag，保证不会在绘制过程中可以切换tag
      if (!this.getRunChangeTag && !this.getIsDrawing) {
        let k = 0
        for (let i = 0; i < this.getRunName.length; i++) {
          if (this.userSelectRunFile === this.getRunName[i]) {
            k = i
            break
          }
        }
        // 在多个图都有数据时才可以切换
        if (this.getTagName[k].length !== 1) {
          this.setCurTag(param)
        }
      }
    },
    addAnd(val) {
      val.push({
        'type': '',
        'tag': '',
        'num': ''
      })
    },
    delAnd(val1, val2, index1, index2) {
      if (index1 === 0 && index2 === 0 && this.item.length === 1 && val1.length === 1) {
        return
      }
      const index = val1.indexOf(val2)
      val1.splice(index, 1)
      if (val1.length === 0) {
        this.item.splice(index1, 1)
      }
    },
    addOr(val) {
      // let index = this.item.indexOf(val)

      this.item.splice(this.item.length, 0, [{ 'type': '',
        'tag': '',
        'num': '' }])
    },
    delOr(index1) {
      if (index1 === 0 && this.item.length === 1) {
        return
      }
      this.item.splice(index1, 1)
    },
    to_Reg() {
      let outStr = ''
      // () || () || () || ()
      for (let i = 0; i < this.item.length; i++) {
        let inStr = ''
        for (let j = 0; j < this.item[i].length; j++) {
          let childStr = ''
          if (this.item[i][j].type === '' || this.item[i][j].tag === '' || this.item[i][j].num === '' || isNaN(Number(this.item[i][j].num))) {
            childStr = ''
          } else {
            childStr = childStr + this.item[i][j].type + this.item[i][j].tag + this.item[i][j].num
          }
          if (childStr) {
            inStr = inStr + childStr + '&&'
          }
        }
        if (inStr.slice(-2) === '&&') {
          inStr = inStr.substring(0, inStr.length - 2)
        }
        if (inStr) {
          inStr = '(' + inStr + ')'
          if (i > 0 && outStr !== '') {
            inStr = '||' + inStr
          }

          outStr = outStr + inStr
        }
      }
      this.Reg = outStr
    },
    hidde() {
      this.to_Reg()
      this.regularEx(this.Reg)
      this.Hidden()
    },
    switchTag(id) {
      id = id.replace(/\s/, '')
      const val = d3.select('#' + id)['_groups'][0][0]['style']['display']
      if (val === 'none') {
        d3.select('#' + id).style('display', '')
        this.tag[id] = 1
      } else {
        d3.select('#' + id).style('display', 'none')
        this.tag[id] = 0
      }
    }
  }
}
</script>
