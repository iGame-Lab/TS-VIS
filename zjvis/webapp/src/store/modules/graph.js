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
/* eslint-disable */
import http from '@/utils/request'
import port from '@/utils/api'

const state = {
  copy: [0],
  sInitState: 0,
  srcData: [],
  graphData: '',
  runName: [],
  tagName: [],
  retList: '',
  clear: 0,
  info: '',
  reg: '',
  run: 0,
  hidden_: 0,
  pre: 0,
  clickDel: [],
  modifyClick: '',
  curTag: '',
  runChangeTag: false,
  isDrawing: false,
  list: [],
};

const getters = {
  getGraphData: (state) => state.graphData,
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
};

const actions = {
  async getSelfCategoryInfo(context, param) {
    context.commit('setSelgCategoryInfo', param);
  },
  async getFullData(context, param) {
    if (!param.run) {
      return;
    }
    state.sInitState = 0;
    if (param.tag === 'c_graph') {
      http.useGet(port.category.graph, param).then(res => {
        const data = JSON.parse(res.data.data);
        context.commit('setGraphData', data.net);
        context.commit('setRetList', data.operator);
      });
    } else {
      http.useGet(port.category.graph, param).then(res => {
        const data = JSON.parse(res.data.data);
        context.commit('setSrcData', data.net);
        context.commit('setGraphData', data.net[0]);
        context.commit('setOptionList', data.net.length);
        context.commit('setRetList', data.operator);
      });
    }
  },
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
    state.tagName = param[1];
    // eslint-disable-next-line
    state.curTag = state.tagName[0][0];
  },
  setGraphData: (state, param) => {
    state.graphData = param;
    state.copy[0] = param;
  },
  setRetList: (state, param) => {
    state.retList = param;
  },
  Clear: (state) => {
    state.clear += 1;
  },
  getNodeInfo: (state, param) => {
    state.info = param;
  },
  regularEx: (state, param) => {
    state.reg = param;
  },
  Run: (state) => {
    state.run += 1;
  },
  Hidden: (state) => {
    state.hidden_ += 1;
  },
  Pre: (state) => {
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
    if (state.curTag === 's_graph') {
      state.graphData = state.srcData[param];
      state.copy[0] = state.srcData[param];
      state.sInitState = param;
    } else if (state.curTag === 'c_graph') {
      state.copy[0] = state.graphData;
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
