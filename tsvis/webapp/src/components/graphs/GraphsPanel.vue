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
  <div class="temp">
    <div class="graphPanel">
      <div class="graphPanelHead">
        <div
          id="c-graph"
          :class="[cGraph ? 'graphhead2' : 'graphhead1']"
          @click="changeTag('c_graph')"
        >
          计算图
        </div>
        <div
          id="s-graph"
          :class="[cGraph ? 'graphhead1' : 'graphhead2']"
          @click="changeTag('s_graph')"
        >
          结构图
        </div>
      </div>
      <el-card>
        <div class="graphPanelContent">
          <div v-show="cGraph" class="cGraphPanel">
            <el-row style="margin-bottom: 7%; font-size: 15px;">条件过滤</el-row>

            <template v-for="(item1, index1) in item">
              <template v-if="index1">
                <el-row :key="index1 + 'orRow'" class="orRow">
                  <el-link disabled>OR</el-link>
                </el-row>
              </template>

              <el-row :key="index1 + 'mainSection'" class="mainSection">
                <el-row style="height: 5%;">
                  <div style="float: right;">
                    <el-button
                      :icon="0 ? 'iconfont icon-zise' : 'iconfont icon-zise-'"
                      style="color: #662d91;"
                      size="mini"
                      class="choose"
                      @click="delOr(index1)"
                    />
                  </div>
                </el-row>

                <template v-for="(item2, index2) in item1">
                  <template v-if="index2">
                    <el-row :key="index1 + '-' + index2 + '-seg'" class="andRow">
                      <el-link disabled>AND</el-link>
                    </el-row>
                  </template>

                  <div
                    :key="index1 + '-' + index2 + '-section'"
                    style=" margin-right: 2%; margin-left: 4%;"
                  >
                    <el-row :key="index1 + '-' + index2 + '-condition'" class="coloredRow">
                      <el-col :span="22">
                        <el-row :gutter="7">
                          <el-col :span="8">
                            <el-select
                              v-model="item2.type"
                              placeholder="入(出)度"
                              size="mini"
                              class="selection1"
                            >
                              <el-option
                                v-for="item0 in options"
                                :key="item0.value"
                                :label="item0.label"
                                :value="item0.value"
                              />
                            </el-select>
                          </el-col>

                          <el-col :span="8">
                            <el-select
                              v-model="item2.tag"
                              placeholder="符号"
                              size="mini"
                              class="selection2"
                            >
                              <el-option
                                v-for="item5 in tags"
                                :key="item5.value"
                                :label="item5.label"
                                :value="item5.value"
                              />
                            </el-select>
                          </el-col>

                          <el-col :span="8">
                            <el-input
                              v-model="item2.num"
                              placeholder=""
                              size="mini"
                              class="selection"
                            />
                          </el-col>
                        </el-row>
                      </el-col>
                      <el-col :span="2" style="padding: 0;">
                        <div style="margin-top: 20%;">
                          <el-button
                            :icon="0 ? 'iconfont icon-huangse' : 'iconfont icon-huangse-'"
                            style="color: #fbb03b;"
                            size="mini"
                            class="choose"
                            @click="delAnd(item1, item2, index1, index2)"
                          />
                        </div>
                      </el-col>
                    </el-row>
                  </div>
                </template>
                <el-row>
                  <div style=" margin-top: 2%; margin-bottom: 2%; margin-left: 47%;">
                    AND
                    <el-button
                      :icon="1 ? 'iconfont icon-huangse' : 'iconfont icon-huangse-'"
                      style="color: #fbb03b;"
                      size="mini"
                      class="choose"
                      @click="addAnd(item1)"
                    />
                  </div>
                </el-row>
              </el-row>
            </template>

            <el-row>
              <div style=" margin-top: 3%; margin-bottom: 3%; margin-left: 47%;">
                OR
                <el-button
                  :icon="1 ? 'iconfont icon-zise' : 'iconfont icon-zise-'"
                  class="choose"
                  style="color: #662d91;"
                  size="mini"
                  @click="addOr()"
                />
              </div>
            </el-row>
          </div>
          <div v-show="!cGraph" class="sGraphPanel">
            <div>
              <el-select v-model="value1" placeholder="请选择" style="width: 100%;">
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
      <el-tooltip
        class="item"
        effect="dark"
        content="条件过滤后点击该按钮隐藏节点"
        placement="top-start"
      >
        <el-button v-show="cGraph" class="buttonOption1" round size="mini" @click="hidde()"
          >隐藏</el-button
        >
      </el-tooltip>
      <el-tooltip class="item" effect="dark" content="隐藏节点后点击该按钮" placement="top-start">
        <el-button v-if="cGraph" class="buttonOption1" round size="mini" @click="Run()"
          >布局</el-button
        >
        <el-button
          v-else
          class="buttonOption1"
          style="margin-left: 40%;"
          round
          size="mini"
          @click="Run()"
          >布局</el-button
        >
      </el-tooltip>
      <el-button v-show="cGraph" class="buttonOption2" round size="mini" @click="Pre()"
        >上一步</el-button
      >
      <el-button v-show="cGraph" class="buttonOption2" round size="mini" @click="Clear()"
        >初始化</el-button
      >
    </div>

    <div class="info">
      <div class="infoTitle"><i class="el-icon-chat-line-round dot" />数据信息栏</div>
      <el-card>
        <div class="infoContent">
          <template v-for="(item3, index) in obj">
            <div
              :key="index + '-control'"
              class="information"
              style="float: left; width: 100%; clear: both;"
            >
              <el-card class="cardStyle">
                <el-col :span="24">
                  <el-col :span="3">
                    <div style="float: left; margin-bottom: 10px;">
                      <el-button
                        :icon="tag[index] == 0 ? 'iconfont icon-suohui' : 'iconfont icon-zhankai1'"
                        style="color: #6f6bd8;"
                        size="mini"
                        @click="switchTag(index)"
                      />
                    </div>
                  </el-col>

                  <el-col :span="21">
                    <div style="float: left; margin-bottom: 5%;">
                      {{ index }}
                    </div>
                  </el-col>
                </el-col>
              </el-card>
            </div>

            <div :id="index" :key="index + '-box'" class="flag" style='display:&quot;inline&quot;;clear:both'>
              <ul>
                <template v-for="(name, value4) in item3">
                  <div :key="value4" style="padding: 1%; clear: both;">
                    <li>
                      <el-col :span="12">
                        <div style="float: left;"><span class="ddot" />{{ value4 }}</div>
                      </el-col>

                      <div style="float: left; word-break:break-all; ">{{ name }}</div>
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
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import { createNamespacedHelpers } from 'vuex';
import * as d3 from 'd3';

Vue.use(ElementUI);

const { mapGetters: mapGraphGetters, mapMutations: mapGraphMutations } = createNamespacedHelpers(
  'graph'
);
const { mapState: mapLayoutStates } = createNamespacedHelpers('layout');
export default {
  name: 'GraphsPanel',
  data() {
    return {
      value1: '',
      option: [],
      tag: {
        NODE_PROPERTIES: 0,
        INPUTS: 0,
        OUTPUTS: 0,
        ATTRIBUTES: 0,
      },
      graphDegree: 100,
      reg: '',
      clickNode: [],
      value: '',
      min: '',
      max: '',
      text1: '',
      text2: '',
      obj: '',
      options: [
        {
          value: 'input',
          label: '入度',
        },
        {
          value: 'output',
          label: '出度',
        },
      ],
      tags: [
        {
          value: '<',
          label: '<',
        },
        {
          value: '<=',
          label: '<=',
        },
        {
          value: '==',
          label: '=',
        },
        {
          value: '>',
          label: '>',
        },
        {
          value: '>=',
          label: '>=',
        },
      ],
      item: [[{ type: '', tag: '', num: '' }]],
      Reg: '',
      tagRadioFlag: true,
      cGraph: true,
    };
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
      'getInitOption',
    ]),
    ...mapLayoutStates(['userSelectRunFile']),
  },
  watch: {
    getInitOption(val) {
      this.value1 = val;
    },
    getSList(val) {
      this.option = val;
    },
    value1(val) {
      this.setData(val);
    },
    getCurTag(val) {
      this.obj = '';
      if (val === 'c_graph') {
        this.cGraph = true;
      } else {
        this.cGraph = false;
      }
    },
    userSelectRunFile() {
      if (this.getCurTag === 'c_graph') {
        this.cGraph = true;
      } else {
        this.cGraph = false;
      }
    },
    getInfo(val) {
      d3.selectAll('.flag').style('display', '');
      this.tag.ATTRIBUTES = 1;
      this.tag.INPUTS = 1;
      this.tag.OUTPUTS = 1;
      this.tag.NODE_PROPERTIES = 1;
      const obj = JSON.parse(val);
      const info = {};

      if (obj.info) {
        if (obj.info === 'init') {
          this.obj = '';
        }
        return;
      }
      info.NODE_PROPERTIES = {};
      info.NODE_PROPERTIES.name = obj.uid;
      if (obj.op) {
        info.NODE_PROPERTIES.op = obj.op;
      }

      if (obj.attr) {
        info.ATTRIBUTES = {};
        for (const i in obj.attr) {
          if (i === '_output_shapes') {
            if (obj.attr[i].length === 1) {
              if (obj.attr[i][0] !== '') {
                // eslint-disable-next-line
                info.ATTRIBUTES[i] = obj.attr[i][0];
              }
            } else {
              info.ATTRIBUTES[i] = obj.attr[i];
            }
          } else if (i === 'shape') {
            if (obj.attr[i] !== '') {
              info.ATTRIBUTES[i] = obj.attr[i];
            }
          } else {
            info.ATTRIBUTES[i] = obj.attr[i];
          }
        }
      }

      if (obj.inNode.length > 0) {
        info.INPUTS = {};
        const name = 'input';
        if (obj.inNode.length === 1) {
          // eslint-disable-next-line
          info.INPUTS[name] = obj.inNode[0];
        } else {
          let curname = '';
          for (const i in obj.inNode) {
            curname = name + i.toString();
            info.INPUTS[curname] = obj.inNode[i];
          }
        }
      }

      if (obj.outNode.length > 0) {
        info.OUTPUTS = {};
        const name = 'output';
        if (obj.outNode.length === 1) {
          // eslint-disable-next-line
          info.OUTPUTS[name] = obj.outNode[0];
        } else {
          let curname = '';
          for (const i in obj.outNode) {
            curname = name + i.toString();
            info.OUTPUTS[curname] = obj.outNode[i];
          }
        }
      }

      this.obj = info;
    },
    getClick(val) {
      this.clickNode.push(val);
    },
  },
  mounted() {
    if (this.getCurTag === 'c_graph') {
      this.cGraph = true;
    } else {
      this.cGraph = false;
    }
    this.option = this.getSList;
    this.value1 = this.getInitOption;
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
      'setData',
    ]),
    changeTag(param) {
      if (!this.getRunChangeTag && !this.getIsDrawing) {
        let k = 0;
        for (let i = 0; i < this.getRunName.length; i += 1) {
          if (this.userSelectRunFile === this.getRunName[i]) {
            k = i;
            break;
          }
        }
        if (this.getTagName[k].length !== 1) {
          this.setCurTag(param);
        }
      }
    },
    addAnd(val) {
      val.push({
        type: '',
        tag: '',
        num: '',
      });
    },
    delAnd(val1, val2, index1, index2) {
      if (index1 === 0 && index2 === 0 && this.item.length === 1 && val1.length === 1) {
        return;
      }
      const index = val1.indexOf(val2);
      val1.splice(index, 1);
      if (val1.length === 0) {
        this.item.splice(index1, 1);
      }
    },
    addOr() {
      this.item.splice(this.item.length, 0, [{ type: '', tag: '', num: '' }]);
    },
    delOr(index1) {
      if (index1 === 0 && this.item.length === 1) {
        return;
      }
      this.item.splice(index1, 1);
    },
    to_Reg() {
      let outStr = '';
      for (let i = 0; i < this.item.length; i += 1) {
        let inStr = '';
        for (let j = 0; j < this.item[i].length; j += 1) {
          let childStr = '';
          if (
            this.item[i][j].type === '' ||
            this.item[i][j].tag === '' ||
            this.item[i][j].num === '' ||
            isNaN(Number(this.item[i][j].num))
          ) {
            childStr = '';
          } else {
            childStr = childStr + this.item[i][j].type + this.item[i][j].tag + this.item[i][j].num;
          }
          if (childStr) {
            inStr = `${inStr + childStr}&&`;
          }
        }
        if (inStr.slice(-2) === '&&') {
          inStr = inStr.substring(0, inStr.length - 2);
        }
        if (inStr) {
          inStr = `(${inStr})`;
          if (i > 0 && outStr !== '') {
            inStr = `||${inStr}`;
          }

          outStr += inStr;
        }
      }
      this.Reg = outStr;
    },
    hidde() {
      this.to_Reg();
      this.regularEx(this.Reg);
      this.Hidden();
    },
    switchTag(id) {
      id = id.replace(/\s/, '');
      const val = d3.select(`#${id}`)._groups[0][0].style.display;
      if (val === 'none') {
        d3.select(`#${id}`).style('display', '');
        this.tag[id] = 1;
      } else {
        d3.select(`#${id}`).style('display', 'none');
        this.tag[id] = 0;
      }
    },
  },
};
</script>
<style lang="less" scoped>
.temp {
  height: 100px;
}

.mainSection {
  box-shadow: 0 0 4px 0 rgba(143, 143, 180, 0.24);
}

.buttonOption1 {
  padding: 7px 10px;
}

.buttonOption2 {
  padding: 7px 7px;
}

.information .el-button {
  border: none;
}

.buttons {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 6%;
  margin-right: 4%;
  margin-left: 4%;

  .el-button {
    width: 20%;
    font-size: 10px;
    color: #270089;
    background-color: #dfe7fd;
  }

  .el-button:hover {
    color: #fff;
    background-color: #8f8bd8;
  }

  .el-button:focus {
    color: #fff;
    background-color: #8f8bd8;
  }
}

.graphPanel {
  width: 94%;
  margin: 5% 3% 0 3%;
}

.graphPanelHead {
  display: inline-flex;
  width: 100%;
  height: 30px;
  font-size: 13px;
}

.graphhead1,
.graphhead2 {
  width: 49%;
  height: 30px;
  font-weight: 700;
  line-height: 30px;
  color: white;
}

.graphhead1 {
  background-color: #b8c6ff;
}

.graphhead2 {
  background-color: #625eb3;
}

#c-graph {
  margin-right: 2%;
  border-radius: 3px;
}

#s-graph {
  border-radius: 3px;
}

.graphPanelContent {
  font-size: 12px;
  text-align: left;
  border-radius: 0 0 3px 3px;
}

.andRow,
.orRow {
  margin-top: 2%;
  margin-bottom: 2%;
  text-align: center;
}

.el-link.el-link--default.is-disabled {
  font-size: 20%;
  color: #000;
}

.info {
  width: 94%;
  margin: 8% 3% 0 3%;
}

.infoTitle {
  height: 30px;
  padding-left: 5%;
  font-size: 13px;
  font-weight: 700;
  line-height: 30px;
  color: white;
  text-align: left;
  background-color: #625eb3;
  border-radius: 3px;

  .dot {
    margin-right: 2%;
  }
}

.infoContent {
  font-size: 13px;
}

.el-select-dropdown__item.selected {
  color: #8f8ad7;
}

.information .el-button--mini {
  padding: 0;
}

.choose {
  padding: 0;
  border: none;
}

.cardStyle {
  margin-top: 2%;
  margin-bottom: 2%;
}

.infoTitle .el_card_body {
  padding-bottom: 20px;
}

.ddot {
  display: inline-block;
  width: 5px;
  height: 5px;
  margin-right: 5px;
  overflow: hidden;
  vertical-align: middle;
  background: blue;
}

li {
  list-style: none;
}

/deep/ .information .el-card__body {
  padding: 10px 20px 20px 10px;
}

/deep/ .el-input__inner {
  padding: 0 12px;
  font-size: xx-small;
  text-align: center;
  border: #fff;
  box-shadow: 0 0 4px 0 rgba(143, 143, 180, 0.24);
}

/deep/ .selection1 .el-input__inner {
  padding: 0 1px;
}

/deep/ .el-input__suffix {
  right: 0;
}

/deep/ .el-input--suffix .el-input__inner {
  padding-right: 16px;
}

/deep/ .el-select .el-input .el-select__caret {
  font-size: 10px;
  color: #662d91;
}

/deep/ .el-input__icon {
  width: 20px;
}

/deep/ .iconfont {
  font-family: 'iconfont' !important;
  -webkit-font-smoothing: antialiased;
  font-size: 20px;
}

/deep/ ul {
  padding: 0;
  margin: 0 0 0 7%;
  text-align: left;
  list-style-type: none;
}
</style>
