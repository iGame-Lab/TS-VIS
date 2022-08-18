import http from "@/utils/request";
import port from "@/utils/api";

const state = {
  errorMessage: "",
  stateRun: "",
  stateTag: "",
  sentenceTag: "hidden_state_word",
  stateData: null,
  sentence: [],
  rightWordsLength: 0,
  maxValue: 1,
  minValue: -1,
  pos: 0,
  range: 27,
  threshold: 0,
  selectedLineIndexs: [],
  selectedRange: [],
  signature: "",
  stateMatchData: []
};

const getters = {
  getStateRun: state => state.stateRun,
  getStateTag: state => state.stateTag,
  getSentenceTag: state => state.sentenceTag,
  getStateData: state => state.stateData,
  getSentence: state => state.sentence,
  getRightWordsLength: state => state.rightWordsLength,
  getMaxValue: state => state.maxValue,
  getMinValue: state => state.minValue,
  getPos: state => state.pos,
  getRange: state => state.range,
  getThreshold: state => state.threshold,
  getSelectedLineIndexs: state => state.selectedLineIndexs,
  getSelectedRange: state => state.selectedRange,
  getSignature: state => state.signature,
  getStateMatchData: state => state.stateMatchData
};

const actions = {
  async getSelfCategoryInfo(context, param) {
    context.commit("setSelfCategoryInfo", param);
  },
  async getHiddenStateData(context, param) {
    if (param.run && param.tag) {
      await http.useGet(port.category.state, param).then(res => {
        if (Number(res.data.code) !== 200) {
          context.commit(
            "setErrorMessage",
            param.run + "," + param.tag + "," + res.data.msg
          );
          return;
        }
        context.commit("setHiddenStateData", res.data.data);
        context.commit("setSentence", res.data.data);
        context.commit("setRightWordsLength", res.data.data);
        context.commit("setMaxValue", res.data.data["max"]);
        context.commit("setMinValue", res.data.data["min"]);
      });
    } else {
      return;
    }
  },
  async fetchStateMatchData(context, param) {
    if (param.run && param.tag) {
      await http.useGet(port.category.state_select, param).then(res => {
        if (Number(res.data.code) !== 200) {
          context.commit(
            "setErrorMessage",
            param.run + "," + param.tag + "," + res.data.msg
          );
          return;
        }
        context.commit("setStateMatchData", res.data.data);
      });
    } else {
      return;
    }
  }
};

const mutations = {
  setSelfCategoryInfo(state, param) {
    state.stateRun = param[0][0];

    for (let i = 0; i < param[1][0].length; i++) {
      if (param[1][0][i] !== state.sentenceTag) {
        state.stateTag = param[1][0][i];
      }
    }
  },
  setStateRun(state, param) {
    state.stateRun = param;
  },
  setStateTag(state, param) {
    state.stateTag = param;
  },
  setHiddenStateData(state, param) {
    state.stateData = param["data"];
  },
  setSentence(state, param) {
    let pattern = new RegExp("[\u4E00-\u9FA5]+");
    if (pattern.test(param["word"])) {
      state.sentence = param["word"].trim().split("");
    } else {
      state.sentence = param["word"].trim().split(" ");
    }
  },
  setRightWordsLength(state, param) {
    state.rightWordsLength = param["right"];
  },
  setPos(state, param) {
    state.pos = param;
  },
  setRange(state, param) {
    state.range = param;
  },
  setThreshold(state, param) {
    state.threshold = param.toFixed(4);
  },
  setMaxValue(state, param) {
    state.maxValue = param;
  },
  setMinValue(state, param) {
    state.minValue = param;
  },
  setSelectedLineIndexs(state, param) {
    state.selectedLineIndexs = param;
  },
  setSelectedRange(state, param) {
    state.selectedRange = param;
  },
  setSignature(state, param) {
    state.signature = param;
  },
  setStateMatchData(state, param) {
    state.stateMatchData = param;
  },
  setErrorMessage(state, param) {
    state.errorMessage = param;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
