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
/* eslint-disable */
import http from "@/utils/request";
import port from "@/utils/api";

const state = {
  copy: [0],
  sInitState: 0,
  srcData: [],
  graphData: "",
  structureGraphData: "",
  runName: [],
  tagName: [],
  retList: "",
  clear: 0,
  info: "",
  reg: "",
  run: 0,
  hidden_: 0,
  pre: 0,
  clickDel: [],
  modifyClick: "",
  curTag: "",
  runChangeTag: false,
  isDrawing: false,
  list: [],
  featureMapType: "GradCam",
  featureMapData: [],
  featureMapInfo: { "sorce_data": '', "label": '' },
  featureMapShow: false,
  fmType: {},
  selectFmType: "",
  taskType: {},
  foldTag: true
};

const getters = {
  getGraphData: (state) => state.graphData,
  getStructureGraphData: (state) => state.structureGraphData,
  getRetList: (state) => state.retList,
  getReg: (state) => state.reg,
  getClear: (state) => state.clear,
  getInfo: (state) => state.info,
  getHidden: (state) => state.hidden_,
  getRun: (state) => state.run,
  getPre: (state) => state.pre,
  getClick: (state) => state.clickDel,
  getModifyClick: (state) => state.modifyClick,
  getRunName: (state) => state.runName,
  getTagName: (state) => state.tagName,
  getCurTag: (state) => state.curTag,
  getRunChangeTag: (state) => state.runChangeTag,
  getIsDrawing: (state) => state.isDrawing,
  getSList: (state) => state.list,
  getInitOption: (state) => state.sInitState,
  getFeatureMapType: (state) => state.featureMapType,
  getFeatureMapData: (state) => state.featureMapData,
  getFeatureMapInfo: (state) => state.featureMapInfo,
  getFeatureMapShow: (state) => state.featureMapShow,
  getFmType: (state) => state.fmType,
  getSelectFmType: (state) => state.selectFmType,
  getTaskType: (state) => state.taskType,
  getFoldTag: (state) => state.foldTag
};

const actions = {
  async getSelfCategoryInfo(context, param) {
    context.commit("setSelgCategoryInfo", param);
  },
  async getIntervalSelfCategoryInfo(context, param) {
    context.commit("setIntervalSelgCategoryInfo", param);
  },
  async getFullData(context, param) {
    if (!param.run) {
      return;
    }
    state.sInitState = 0;
    if (param.tag === "c_graph") {
      http.useGet(port.category.graph, param).then(res => {
        const data = JSON.parse(res.data.data);
        context.commit("setGraphData", data.net);
        context.commit("setRetList", data.operator);
      });
    } else {
      http.useGet(port.category.graph, param).then(res => {
        const data = JSON.parse(res.data.data);
        context.commit("setStructureGraphData", data.net[0]);
      });
    }
  },
  async fetchFeatures(context, param) {
    await http.useGet(port.category.features, param).then(res => {
      if (Number(res.data.code) !== 200) {
        return;
      }
      context.commit("setFeaturesData", res.data.data);
    });
  }
};

const mutations = {
  setOptionList: (state, param) => {
    const optionList = [];
    for (let i = 0; i < param; i += 1) {
      const item = {};
      item.value = i;
      item.label = `结构图${i}`;
      optionList.push(item);
    }
    state.list = optionList;
  },
  setSrcData: (state, param) => {
    state.srcData = param;
  },
  setSelgCategoryInfo: (state, param) => {
    // eslint-disable-next-line
    state.runName = param[0];
    // eslint-disable-next-line

    for (let l = 0; l < param[1].length; l++) {
      let tempFmType = {};
      let tempTaskType = '';

      state.tagName.push([]);
      for (let i = 0; i < param[1][l].length; i++) {
        if (param[1][l][i] == "c_graph" || param[1][l][i] == "s_graph") {
          state.tagName[l].push(param[1][l][i]);
        } else {
          let arr = param[1][l][i].split('-');
          if (arr[1] == 'label') {
            tempTaskType = arr[0];
            state.taskType[param[0][l]] = arr[0];
          } else if (arr[0] !== tempTaskType) {
            if (tempFmType[arr[1]] == undefined) {
              tempFmType[arr[1]] = [];
            }
            tempFmType[arr[1]].push(arr[0]);
          }
        }
      }
      state.fmType[param[0][l]] = tempFmType;
    }
    // eslint-disable-next-line
    state.curTag = state.tagName[0][0];
    state.selectFmType = Object.keys(Object.values(state.fmType)[0])[0];
  },
  setIntervalSelgCategoryInfo: (state, param) => {
    // eslint-disable-next-line
    state.runName = param[0];
    // eslint-disable-next-line
    state.tagName = param[1];
  },
  setGraphData: (state, param) => {
    state.graphData = param;
    state.copy[0] = param;
  },
  setStructureGraphData: (state, param) => {
    state.structureGraphData = param;
  },
  setRetList: (state, param) => {
    state.retList = param;
  },
  Clear: state => {
    state.clear += 1;
  },
  getNodeInfo: (state, param) => {
    state.info = param;
  },
  regularEx: (state, param) => {
    state.reg = param;
  },
  Run: state => {
    state.run += 1;
  },
  Hidden: state => {
    state.hidden_ += 1;
  },
  Pre: state => {
    state.pre += 1;
  },
  getClickDel: (state, param) => {
    state.clickDel = param;
  },
  Modify: (state, param) => {
    state.modifyClick = param;
  },
  setCurTag: (state, param) => {
    state.curTag = param;
  },
  setRunChangeTag: (state, param) => {
    state.runChangeTag = param;
  },
  setIsDrawing: (state, param) => {
    state.isDrawing = param;
  },
  setData: (state, param) => {
    if (state.curTag === "s_graph") {
      state.graphData = state.srcData[param];
      state.copy[0] = state.srcData[param];
      state.sInitState = param;
    } else if (state.curTag === "c_graph") {
      state.copy[0] = state.graphData;
    }
  },
  setFeaturesData: (state, param) => {
    let flag = false;
    let key = Object.keys(param);
    let index = Number(
      String(key).substring(
        String(key).indexOf("[") + 1,
        String(key).indexOf("]")
      )
    );
    if (param[key][0] !== undefined) {
      for (let i in state.featureMapData) {
        let indexO = Number(
          String(state.featureMapData[i][0][0]).substring(
            String(state.featureMapData[i][0][0]).indexOf("[") + 1,
            String(state.featureMapData[i][0][0]).indexOf("]")
          )
        );
        if (index == indexO) {
          state.featureMapData[i][1].push(...param[key][0]["value"]);
          flag = true;
          break;
        } else if (indexO > index) {
          flag = true;
          let data = [key, param[key][0]["value"]];
          state.featureMapData.splice(i, 0, data);
          state.featureMapInfo["sorce_data"] = param[key][0]["sorce_data"];
          state.featureMapInfo["label"] = param[key][0]["label"];
          break;
        }
      }
      if (!flag) {
        let data = [key, param[key][0]["value"]];
        state.featureMapData.push(data);
        state.featureMapInfo["sorce_data"] = param[key][0]["sorce_data"];
        state.featureMapInfo["label"] = param[key][0]["label"];
      }
    }
  },
  setFeatureMapType: (state, para) => {
    state.featureMapType = para;
  },
  clearFeatureMap: (state, para) => {
    if (para === "all") {
      state.featureMapData = [];
    } else {
      for (let i in state.featureMapData) {
        if (state.featureMapData[i][0][0] == para) {
          state.featureMapData.splice(i, 1);
        }
      }
    }
  },
  setFeatureMapShow: (state, para) => {
    state.featureMapShow = !state.featureMapShow
  },
  setSelectFmType(state, param) {
    state.selectFmType = param;
  },
  setFoldTag(state, param) {
    if (param=='reset') {
      state.foldTag = true;
    } else {
      state.foldTag = !state.foldTag;
    }

  },
  clearGraphData(state, param) {
    state.graphData = '';
    state.structureGraphData = '';
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
