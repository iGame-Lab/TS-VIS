/** Copyright 2021 Tianshu AI Platform. All Rights Reserved.
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
    <div class="transformer-panel" v-if="reload">
      <div v-show="isText" class="transformer-text-panel">
        <el-card>
          <div class="info">
            <div class="info-title">
              <span i class="iconfont icon-ziyuan40">&nbsp;&nbsp;控制面板</span>
            </div>
            <div class="info-content">
              <span>请选择要可视化注意力的语句:</span>
              <el-select class="text-select" v-model="getValue">
                <el-option v-for="item in options" :key="item.id"
                  :value="item.value">
                  <el-popover placement="top-start" width="350" trigger="hover">
                    <span>{{ item.value }}</span>
                    <span slot="reference">{{
                      item.value.slice(0, 22) + "..."
                    }}</span>
                  </el-popover>
                </el-option>
              </el-select>
            </div>
          </div>
        </el-card>
        <el-card>
          <div class="info">
            <div class="info-title">
              <span i class="iconfont icon-ziyuan41">&nbsp;&nbsp;数据信息栏</span>
            </div>
            <div class="info-content">
              <div v-if="!isShowAttentionInfo">
                <span>暂无信息</span>
              </div>
              <div v-if="isShowAttentionInfo">
                <div>
                  <el-row>
                    <el-col :span="10">Head：</el-col>
                    <el-col :span="14">{{ getAttentionInfoData[0] }}</el-col>
                  </el-row>
                </div>
                <div>
                  <el-row>
                    <el-col :span="10">Max：</el-col>
                    <el-col :span="14">{{ getAttentionInfoData[1] }}</el-col>
                  </el-row>
                </div>
                <div>
                  <el-row>
                    <el-col :span="10">Min：</el-col>
                    <el-col :span="14">{{ getAttentionInfoData[2] }}</el-col>
                  </el-row>
                </div>
                <div>
                  <el-row>
                    <el-col :span="10">Quar：</el-col>
                    <el-col :span="14">{{ getAttentionInfoData[3] }}</el-col>
                  </el-row>
                </div>
                <div>
                  <el-row>
                    <el-col :span="10">Vari：</el-col>
                    <el-col :span="14">{{ getAttentionInfoData[4] }}</el-col>
                  </el-row>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
      <div v-show="!isText" class="transformer-image-panel">
        <el-card>
          <div class="info">
            <div class="info-title">
              <span i class="iconfont icon-ziyuan40">&nbsp;&nbsp;控制面板</span>
            </div>
            <div class="info-content">
              <div class="info-content-item">
                <span class="select-tip">选择图片：</span>
                <el-select v-model="selectImg" placeholder="请选择">
                  <el-option v-for="(item, i) in imgList" :key="i" :label="item"
                    :value="item">
                  </el-option>
                </el-select>
              </div>
              <div class="info-content-item">
                <span class="select-tip">选择层：</span>
                <el-select v-model="selectLayer" multiple>
                  <el-checkbox v-model="allLayerChecked"
                    style="text-align: right; width: 95%"
                    @change="allLayerCheckedChange" :indeterminate="
                      layerList.length !== selectLayer.length &&
                      selectLayer.length > 0
                    ">全选</el-checkbox>
                  <el-checkbox-group v-model="selectLayer">
                    <el-option v-for="item in layerList" :key="item"
                      :value="'layer-' + (Number(item) + 1)">
                      <el-checkbox style="pointer-events: none"
                        :label="'layer-' + (Number(item) + 1)"></el-checkbox>
                    </el-option>
                  </el-checkbox-group>
                </el-select>
              </div>
              <div class="info-content-item">
                <span class="select-tip">选择归一化方式：</span>
                <el-switch style="display: block; margin: 0 auto"
                  v-model="normalize_type" active-color="#625eb3"
                  inactive-color="#625eb3" active-text="局部" inactive-text="全局">
                </el-switch>
              </div>
              <div class="info-content-item" v-show="!normalize_type">
                <span class="select-tip">比例：</span>
                <el-slider v-model="ratio" :step="5" :format-tooltip="
                    (el) => {
                      return parseInt(el / 11) + 1;
                    }
                  " @change="ratioChange($event)">
                </el-slider>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { createNamespacedHelpers } from "vuex";

const {
  mapGetters: mapTransformerGetters,
  mapActions: mapTransformerActions,
  mapMutations: mapTransformerMutations,
} = createNamespacedHelpers("transformer");

const { mapState: mapLayoutStates } = createNamespacedHelpers("layout");
export default {
  name: "TransformerPanel",
  data () {
    return {
      isText: true,
      isShowAttentionInfo: false,
      userTag: "",
      getValue: "",
      options: [],
      allData: {},
      textList: [],
      reload: true,
      selectImg: "",
      imgList: [],
      layerList: [],
      selectLayer: [],
      normalize_type: false,
      ratio: 0,
    };
  },
  computed: {
    ...mapTransformerGetters([
      "getSentences",
      "getAllData",
      "getCategoryInfo",
      "getAttentionInfoData",
      "getLayerNumber",
      "getAttnMap",
      "getSelectX",
      "getSelectY",
    ]),
    ...mapLayoutStates(["userSelectRunFile"]),
    allLayerChecked: {
      get () {
        if (this.layerList.length === this.selectLayer.length) {
          return true;
        } else {
          return false;
        }
      },
      set () { },
    },
  },
  created () {
    if (this.getCategoryInfo[0]) {
      let index = this.getCategoryInfo[0].indexOf(this.userSelectRunFile);
      if (index > -1) {
        let arr = this.getCategoryInfo[1][index][0].split("-");
        if (arr[1] == "transformertext") {
          this.userTag = arr[0];
        }
      }
    }

    if (this.userSelectRunFile) {
      const param = {
        run: this.userSelectRunFile,
        tag: this.userTag + "-transformertext-sentence"
      };
      this.getSentencesData(param);
    }
  },
  mounted () {
    if (this.getCategoryInfo[0]) {
      let index = this.getCategoryInfo[0].indexOf(this.userSelectRunFile);
      if (index > -1) {
        let arr = this.getCategoryInfo[1][index][0].split("-");
        if (arr[1] == "transformertext") {
          this.isText = true;
        } else {
          this.isText = false;
          this.getImgList();
          this.selectLayer = [];
          this.normalize_type = false;
          let param = {
            run: this.userSelectRunFile,
            tag: this.userTag + "-" + this.selectImg,
            l: "None",
            x: "None",
            y: "None",
            g: "0",
            r: parseInt(this.ratio / 11) + 1,
          };
          this.setSelectImgTag(this.userTag + "-" + this.selectImg);
          this.fetchAttentionMap(param);

          this.layerList = [];
          for (let i = 0; i < this.getLayerNumber; i++) {
            this.layerList.push(i);
          }
        }
      }
    }
  },
  watch: {
    userSelectRunFile (val) {
      let index = this.getCategoryInfo[0].indexOf(val);
      if (index > -1) {
        this.reload = false;
        let arr = this.getCategoryInfo[1][index][0].split("-");
        if (arr[1] == "transformertext") {
          this.isText = true;
          this.userTag = arr[0];
          if (val) {
            const param = {
              run: val,
              tag: this.userTag + "-transformertext-sentence"
            };
            this.getSentencesData(param);
          }
        } else {
          this.isText = false;
          this.getImgList();
          this.selectLayer = [];
          this.normalize_type = false;
          let param = {
            run: this.userSelectRunFile,
            tag: this.userTag + "-" + this.selectImg,
            l: "None",
            x: "None",
            y: "None",
            g: "0",
            r: parseInt(this.ratio / 11) + 1,
          };
          this.setSelectImgTag(this.userTag + "-" + this.selectImg);
          this.fetchAttentionMap(param);
          
          this.layerList = [];
          for (let i = 0; i < this.getLayerNumber; i++) {
            this.layerList.push(i);
          }
        }
      }

      this.$nextTick(() => {
        this.reload = true;
      });
    },
    getSentences (val) {
      this.options = [];
      this.textList = val;
      if (this.textList.length > 2) {
        for (let i = 0; i < this.textList.length; i++) {
          let text = { id: i, value: this.textList[i] };
          this.options.push(text);
        }
      } else {
        for (let i = 0; i < this.textList.length; i++) {
          let text = {
            id: i,
            value: this.textList[i][0] + " " + this.textList[i][1],
          };
          this.options.push(text);
        }
      }

      this.getValue = this.options[0].value;

      const param = {
        run: this.userSelectRunFile,
        tag: this.userTag + "-transformertext-" + 0
      };
      this.getTransformerTextData(param);
      this.setSelectedLH("00-00");
    },
    // 监听下拉框选择变化，请求不同数据进行渲染
    getValue (val) {
      let index = 0;
      for (let i = 0; i < this.options.length; i++) {
        if (val === this.options[i].value) {
          index = i;
        }
      }

      const param = {
        run: this.userSelectRunFile,
        tag: this.userTag + "-transformertext-" + index
      };
      this.getTransformerTextData(param);
      this.setSelectedLH("00-00");
    },
    getAttentionInfoData (val) {
      if (val.length) {
        this.isShowAttentionInfo = true;
      } else {
        this.isShowAttentionInfo = false;
      }
    },
    getLayerNumber (val) {
      this.layerList = [];
      for (let i = 0; i < val; i++) {
        this.layerList.push(i);
      }
    },
    selectImg (val) {
      this.emptyAttnData();
      if (this.selectLayer.length > 0) {
        this.getAttentionMap();
      } else {
        let param = {
          run: this.userSelectRunFile,
          tag: this.userTag + "-" + this.selectImg,
          l: 0,
          x: "None",
          y: "None",
          g: this.normalize_type ? 0 : 1,
          r: 0,
        };
        this.fetchAttentionMap(param);
      }
      this.setSelectImgTag(this.userTag + "-" + this.selectImg);
    },
    selectLayer (val) {
      if (val.length === this.layerList.length) {
        this.allLayerChecked = true;
      } else {
        this.allLayerChecked = false;
      }

      this.getAttentionMap();
      let temp = [];
      val.forEach((el) => {
        let arr = el.split("-");
        temp.push(Number(arr[1]) - 1);
      });
      this.setSelectLayer(temp);
    },
    normalize_type (val) {
      this.emptyAttnData();
      this.getAttentionMap();
      this.setSelectG(this.normalize_type ? 0 : 1);
    },
  },
  methods: {
    ...mapTransformerActions([
      "getSentencesData",
      "getTransformerTextData",
      "fetchAttentionMap",
    ]),
    ...mapTransformerMutations([
      "setSelectedLH",
      "setSelectImgTag",
      "setSelectLayer",
      "setSelectG",
      "setSelectR",
      "emptyAttnData",
    ]),
    getImgList () {
      let index = this.getCategoryInfo[0].indexOf(this.userSelectRunFile);
      if (index > -1) {
        let afterImgList = new Set();
        this.getCategoryInfo[1][index].forEach((element) => {
          let temp = element.split("-");
          this.userTag = temp[0];
          if (temp.length == 3) {
            afterImgList.add(temp[1]);
          }
        });
        this.imgList = [...afterImgList];
        if (this.imgList.length > 0) {
          this.selectImg = this.imgList[0];
        }
      }
    },
    allLayerCheckedChange (checked) {
      this.selectLayer = [];
      if (checked) {
        this.layerList.map((item) => {
          this.selectLayer.push("layer-" + (Number(item) + 1));
        });
      } else {
        this.selectedArray = [];
      }
    },
    getAttentionMap () {
      this.selectLayer.forEach((el) => {
        let arr = el.split("-");
        let layer = String(Number(arr[1]) - 1);
        if (!Object.keys(this.getAttnMap).includes(layer)) {
          let param = {
            run: this.userSelectRunFile,
            tag: this.userTag + "-" + this.selectImg,
            l: layer,
            x: this.getSelectX,
            y: this.getSelectY,
            g: this.normalize_type ? 0 : 1,
            r: parseInt(this.ratio / 11) + 1,
          };
          this.fetchAttentionMap(param);
        }
      });
    },
    ratioChange (e) {
      this.emptyAttnData();
      this.getAttentionMap();
      this.setSelectR(parseInt(e / 11) + 1);
    },
  },
};
</script>
<style lang="less" scoped>
.transformer-panel {
  /deep/.el-card {
    margin: 3.5% 5% 4% 0%;
    border-top: 0px;
  }

  /deep/.el-card__body {
    border-radius: 0 0 3px 3px;
    padding: 0px;
  }

  .info {
    .info-title {
      span {
        font-size: 12px;
      }
      background-color: #625eb3;
      color: white;
      text-align: left;
      border-bottom: 1px solid #8f8ad7;
      padding: 2% 2% 2% 5%;
      .iconfont {
        margin-right: 7px;
        font-size: 12px;
        font-style: normal;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }
    }
    .info-content {
      font-size: 11px;
      padding: 5% 10% 3% 10%;
      text-align: left;

      div {
        margin-bottom: 3%;
      }

      .text-select {
        margin-top: 5%;
      }
    }
  }

  /deep/.el-icon-circle-close {
    color: white;
  }

  /deep/.el-image-viewer__img {
    height: 100%;
  }
}
.info-content-item {
  width: 100%;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
}
.select-tip {
  margin: 20px 0 10px;
}
</style>
