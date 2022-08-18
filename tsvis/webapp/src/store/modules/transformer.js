import http from "@/utils/request";
import port from "@/utils/api";

const state = {
  categoryInfo: "", // 存放自己的类目信息
  sentences: [],
  allData: {},
  attention: {},
  defaultFilter: "all",
  bidirectional: true,
  displayMode: "light",
  defaultLayer: 0,
  defaultHead: 0,
  errorMessage: "",
  attentionInfoData: [],
  attentionLayers: [],
  selectedLH: "00-00",
  selectImgTag: "",
  selectLayer: [],
  selectX: "0",
  selectY: "0",
  selectG: "1",
  selectR: "1",
  originImg: "",
  attnMap: {},
  layerNumber: 0,
  chartWidthScale: 1,
  chartHeightScale: 1
};

const getters = {
  getCategoryInfo: state => state.categoryInfo,
  getSentences: state => state.sentences,
  getAllData: state => state.allData,
  getAttention: state => state.attention,
  getDefaultFilter: state => state.defaultFilter,
  getBidirctional: state => state.bidirectional,
  getDisplayMode: state => state.displayMode,
  getDefaultLayer: state => state.defaultLayer,
  getDefaultHead: state => state.defaultHead,
  getErrorMessage: state => state.errorMessage,
  getAttentionInfoData: state => state.attentionInfoData,
  getAttentionLayers: state => state.attentionLayers,
  getSelectedLH: state => state.selectedLH,
  getOriginImg: state => state.originImg,
  getAttnMap: state => state.attnMap,
  getLayerNumber: state => state.layerNumber,
  getSelectImgTag: state => state.selectImgTag,
  getSelectLayer: state => state.selectLayer,
  getSelectX: state => state.selectX,
  getSelectY: state => state.selectY,
  getSelectG: state => state.selectG,
  getSelectR: state => state.selectR,
  getChartWidthScale: state => state.chartWidthScale,
  getChartHeightScale: state => state.chartHeightScale
};

const actions = {
  async getSelfCategoryInfo(context, param) {
    context.commit("setSelfCategoryInfo", param);
  },
  // 获取所选文本对应的注意力数据
  async getTransformerTextData(context, param) {
    await http.useGet(port.category.transformer_text, param).then(res => {
      if (Number(res.data.code) !== 200) {
        context.commit(
          "setErrorMessage",
          param.run + "," + param.tag + "," + res.data.msg
        );
        return;
      }
      context.commit("setTransformerTextData", [param.tag, res.data.data]);
    });
  },
  // 获取日志中的文本列表
  async getSentencesData(context, param) {
    await http.useGet(port.category.transformer_text, param).then(res => {
      if (Number(res.data.code) !== 200) {
        context.commit(
          "setErrorMessage",
          param.run + "," + param.tag + "," + res.data.msg
        );
        return;
      }
      context.commit("setSentencesData", [param.tag, res.data.data]);
    });
  },
  //获取attention图
  async fetchAttentionMap(context, param) {
    if (param !== undefined) {
      let res = await http.useGet(port.category.transformer_image, param);
      if (res.data.code === 200) {
        context.commit("setAttnData", res.data.data);
      }
    }
  }
};

const mutations = {
  setSelfCategoryInfo(state, param) {
    state.categoryInfo = param;
  },
  setTransformerTextData: (state, param) => {
    state.allData = param[1];

    state.attentionLayers = [];
    let layersLength =
      param[1][param[0]]["data"]["attention"]["all"]["attn"].length;
    for (let i = 0; i < layersLength; i++) {
      state.attentionLayers.push(i);
    }
  },
  setSentencesData: (state, param) => {
    state.sentences = param[1][param[0]];
  },
  setAttentionInfoData: (state, param) => {
    state.attentionInfoData = param;
  },
  setSelectedLH: (state, param) => {
    state.selectedLH = param;
  },
  setErrorMessage(state, param) {
    state.errorMessage = param;
  },
  setSelectImgTag(state, param) {
    state.selectImgTag = param;
  },
  setSelectLayer(state, param) {
    state.selectLayer = param;
  },
  setSelectX(state, param) {
    state.selectX = param;
  },
  setSelectY(state, param) {
    state.selectY = param;
  },
  setSelectG(state, param) {
    state.selectG = param;
  },
  setSelectR(state, param) {
    state.selectR = param;
  },
  setAttnData(state, param) {
    if (Object.keys(param).includes("num_layers")) {
      state.originImg = param["img"];
      state.layerNumber = param["num_layers"];
    } else {
      state.originImg = param[Object.keys(param)]["img"];
      state.attnMap[param[Object.keys(param)]["layer"]] =
        param[Object.keys(param)]["attn_map"];
      // this.$set(state.attnMap, param[Object.keys(param)]["layer"], param[Object.keys(param)]['attn_map']);
      let newAttnMap = {};
      Object.assign(newAttnMap, state.attnMap);
      state.attnMap = newAttnMap;
    }
  },
  emptyAttnData(state, param) {
    state.attnMap = {};
  },
  setChartWidthScale(state, param) {
    state.chartWidthScale = param;
  },
  setChartHeightScale(state, param) {
    state.chartHeightScale = param;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
