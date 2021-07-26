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

// dubhe-web\src\utils\VisualUtils\api.js
// import port from '@/utils/VisualUtils/api';

const state = {
  categoryInfo: '',
  detailData: '',
  clickState: false,
  scalarData: {},
  scalar: {},
  scalarmid: {},
  audioData: [],
  imageData: [],
  textData: [],
  statisticData: [],
  audio: [],
  text: [],
  image: [],
  statistic: [],
  statisticMode: '三维',
  statisticShowNumber: 30,
  lastRouter: -1,
};

const getters = {
  getAudioData: (state) => state.audioData,
  getAudio: (state) => state.audio,

  getTextData: (state) => state.textData,
  getText: (state) => state.text,

  getImageData: (state) => state.imageData,
  getImage: (state) => state.image,

  getScalarData: (state) => state.scalarData,
  getScalar: (state) => state.scalar,

  getStatisticData: (state) => state.statisticData,
  getStatisticMode: (state) => state.statisticMode,
  getStatisticShowNumber: (state) => state.statisticShowNumber,
};

const actions = {
  // eslint-disable-next-line
  async getSelfCategoryInfo(context, param) {
  },
  async getIntervalSelfCategoryInfo(context, param) {

  },
  // eslint-disable-next-line
  async getData(context, param) {
  },
  // eslint-disable-next-line
  async dynamicGetData(context) {
  },
};

const mutations = {
  setSelfCategoryInfo: (state, param) => {
    state.categoryInfo = param;
  },
  setInitDetailDataInfo: (state, param) => {
    state.detailData = param;
  },
  setDetailData: (state, param) => {
    state.detailData.push(param);
  },
  setClickState: (state, param) => {
    state.clickState = param;
  },
  setAudioData: (state, param) => {
    const paramStringIndex = `${param.content.run}/${Object.keys(param.content.value)[0]}`;
    let flag = true;
    for (let i = 0; i < state.audio.length; i += 1) {
      if (paramStringIndex === state.audio[i].stringIndex) {
        flag = false;
        state.audio.splice(i, 1);
        if (param.copyToData) {
          state.audioData = JSON.parse(JSON.stringify(state.audio));
        }
        break;
      }
    }
    if (flag) {
      state.audio.push({
        stringIndex: paramStringIndex,
        checked: param.checked,
        content: param.content,
      });
    }
  },
  setTextData: (state, param) => {
    const paramStringIndex = `${param.content.run}/${Object.keys(param.content.value)[0]}`;
    let flag = true;
    for (let i = 0; i < state.text.length; i += 1) {
      if (paramStringIndex === state.text[i].stringIndex) {
        flag = false;
        state.text.splice(i, 1);
        if (param.copyToData) {
          state.textData = JSON.parse(JSON.stringify(state.text));
        }
        break;
      }
    }
    if (flag) {
      state.text.push({
        stringIndex: paramStringIndex,
        checked: param.checked,
        content: param.content,
      });
    }
  },
  setImageData: (state, param) => {
    const paramStringIndex = `${param.content.run}/${Object.keys(param.content.value)[0]}`;
    let flag = true;
    for (let i = 0; i < state.image.length; i += 1) {
      if (paramStringIndex === state.image[i].stringIndex) {
        flag = false;
        state.image.splice(i, 1);
        if (param.copyToData) {
          state.imageData = JSON.parse(JSON.stringify(state.image));
        }
        break;
      }
    }
    if (flag) {
      state.image.push({
        stringIndex: paramStringIndex,
        checked: param.checked,
        content: param.content,
      });
    }
  },
  setStatisticData: (state, param) => {
    let flag = -1;
    for (let i = 0; i < state.statistic.length; i += 1) {
      if (
        state.statistic[i].ttlabel === param.ttlabel &&
        state.statistic[i].tag === param.tag &&
        (state.statistic[i].componentName === param.componentName ||
          param.componentName === 'threed' ||
          param.componentName === 'orthographic')
      ) {
        if (!param.delete) {
          state.statistic.splice(i, 1);
        } else {
          state.statistic.splice(i, 1);
          state.statisticData = state.statistic;
        }
        if (!state.statisticData.length) {
          state.statisticMode = '三维';
          state.statisticShowNumber = 10;
        }
        flag = 1;
        break;
      }
    }
    if (flag === -1) {
      if (param.itemp < 1000) param.itemp = 1000 + param.itemp;
      param.divId = `custom${param.componentName}${param.itemp}`;
      if (state.statisticMode === '三维' && param.componentName === 'orthographic') {
        param.componentName = 'threed';
      } else if (state.statisticMode === '二维' && param.componentName === 'threed') {
        param.componentName = 'orthographic';
      }
      state.statistic.push(param);
    }
  },
  setData: (state, param) => {
    // eslint-disable-next-line
    switch (param) {
      case 'scalar':
        Object.assign(state.scalarmid, JSON.parse(JSON.stringify(state.scalar)));
        Object.assign(state.scalarData, JSON.parse(JSON.stringify(state.scalar)));
        state.scalar = {};
        break;
      case 'media':
        state.imageData = JSON.parse(JSON.stringify(state.image));
        state.audioData = JSON.parse(JSON.stringify(state.audio));
        state.textData = JSON.parse(JSON.stringify(state.text));
        break;
      case 'statistic':
        state.statisticData = JSON.parse(JSON.stringify(state.statistic));
        break;
      case 'custom':
        state.imageData = JSON.parse(JSON.stringify(state.image));
        state.audioData = JSON.parse(JSON.stringify(state.audio));
        state.textData = JSON.parse(JSON.stringify(state.text));
        state.statisticData = JSON.parse(JSON.stringify(state.statistic));
        break;
    }
  },
  setRouter: (state, param) => {
    // eslint-disable-next-line
    switch (param) {
      case 1:
        break;
      case 2:
        break;
      case 3:
        break;
      case 7:
    }
  },
  setStatisticMode: (state, param) => {
    state.statisticMode = param;
    if (param === '三维') {
      for (let i = 0; i < state.statistic.length; i += 1) {
        if (state.statistic[i].componentName === 'orthographic') {
          state.statistic[i].componentName = 'threed';
        }
      }
    } else {
      for (let i = 0; i < state.statistic.length; i += 1) {
        // eslint-disable-next-line
        if (state.statistic[i].componentName === 'threed') {
          // eslint-disable-next-line
          state.statistic[i].componentName = 'orthographic';
        }
      }
    }
    state.statisticData = JSON.parse(JSON.stringify(state.statistic));
  },
  setStatisticShowNumber: (state, param) => {
    state.statisticShowNumber = param;
  },
  setScalar: (state, param) => {
    // eslint-disable-next-line
    state.scalar[param[0]] = param[1];
  },
  deleteScalar: (state, param) => {
    delete state.scalar[param];
  },
  deleteScalarData: (state, param) => {
    delete state.scalarmid[param];
    state.scalarData = JSON.parse(JSON.stringify(state.scalarmid));
  },
  cleanScalar: (state) => {
    state.scalar = {};
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
