import http from '@/utils/request'
import port from '@/utils/api'
import { param2Obj } from '@/utils/utils'
import layout from './layout'
/*
{ questionInfo存储结构
  "run": {
    "tag": {
      "shape": 0,
      "allSteps": [],
      "curMin": 0,
      "curMax": 0,
      "sample": [] // 记录index
      "sample_type" : 'image'
    }
  }
}
*/
const state = {
  categoryInfo: {
    curRuns: [], // 类目信息中的所有的Run
    curTags: [], // 类目信息中的所有的Tag[][]
    initFlag: false, // 是否是初始化页面
    received: false // 当所有的信息填充之后改变
  },
  questionInfo: { // 请求每个点需要存储的数据结构
    received: false // 当所有的信息填充之后改变
  },
  curInfo: { // 当前所处于的信息节点
    curTag: '',
    curStep: 0,
    curMapStep: 0,
    curMethod: 'PCA',
    curDim: '3维',
    received: false // 当当前的信息都被填充结束后改变
  },
  curData: {
    data: [],
    label: [],
    labelType: [],
    labelTypeColor: {},
    echaLabelNumber: {},
    received: false
  },
  checkLabels: [],
  receivedCategoryInfo: false, // 作为别的部分的监听信息
  receivedQuestionInfo: false, // 作为别的部分的监听信息
  receivedCurInfo: false, // 作为别的部分的监听信息
  receivedCurData: false,
  legendColor: [ // 颜色条因为很多地方都会用到直接放在这里
    '#EF6F38',
    '#EFDD79',
    '#C5507A',
    '#9359B0',
    '#525C99',
    '#47C1D6',
    '#B5D4E8',
    '#15746C',
    '#81c19c',
    '#A08983'
  ],
  panelSampleData: {
    type: '',
    url: ''
  },
  message: '', // 放在info中的信息
  initStateFlag: false,
  errorMessage: '',
  lineWidth: 0.4
}

const getters = {
  getCurInfo: (state) => state.curInfo,
  getCategoryInfo: (state) => state.categoryInfo,
  getQuestionInfo: (state) => state.questionInfo,
  getReceivedCategoryInfo: (state) => state.receivedCategoryInfo,
  getReceivedQuestionInfo: (state) => state.receivedQuestionInfo,
  getReceivedCurInfo: (state) => state.receivedCurInfo,
  getReceivedCurData: (state) => state.receivedCurData,
  getCurData: (state) => state.curData,
  getCheckLabels: (state) => state.checkLabels,
  getLegendColor: (state) => state.legendColor,
  getPanelSampleData: (state) => state.panelSampleData,
  getMessage: (state) => state.message,
  getInitStateFlag: (state) => state.initStateFlag,
  getErrorMessage: (state) => state.errorMessage,
  getLineWidth: (state) => state.lineWidth
}

const actions = {
  // 当系统初始化的时候，layout会给embedding 发起动作
  async getSelfCategoryInfo(context, param) {
    context.commit('setSelfCategoryInfo', param)
    
    
    if (param[2]['initStateFlag'] === true) {
      // context.dispatch('fetchAllStep')
      context.dispatch('fetchOneStep', context.state.categoryInfo.curRuns[0])
      
    }
  },
  async getSelfCategoryInfoNotInit(context, param) {
    context.commit('setSelfCategoryInfo', param)
    console.log("here")
    if (param[2]['initStateFlag'] === true) {
      // context.dispatch('fetchAllStep')
      context.dispatch('fetchOneStep', context.state.categoryInfo.curRuns[0])
    }
  },
  async getIntervalSelfCategoryInfo(context, param) {
    
  },
  async fetchOneStep(context, param) {
    state.questionInfo.received = false // 当需要请求信息的时候所有的数据已经完备
    state.receivedQuestionInfo = false
    state.receivedCurInfo = false // 临时测试
    const allStepTemp = {'data':[], 'index':0}
    // console.log('[context.state.categoryInfo]', context.state.categoryInfo)
    if(param == undefined) {
      param = context.state.categoryInfo.curRuns[0];
    }
    for (let i = 0; i < context.state.categoryInfo.curRuns.length; i++) {
      const oneRunStep = []
      if(param == context.state.categoryInfo.curRuns[i]) {
        for (let j = 0; j < context.state.categoryInfo.curTags[i].length; j++) {
          const param = { run: context.state.categoryInfo.curRuns[i], tag: context.state.categoryInfo.curTags[i][j] }
          await http.useGet(port.category.projector, param)
            .then(res => {
              if (+res.data.code !== 200) {
                context.commit('setErrorMessage', res.data.msg + '_' + new Date().getTime())
                return
              }
              const res1 = res.data.data[context.state.categoryInfo.curTags[i][j]]
              const res2 = res.data.data['shape']
              const res3 = res.data.data['sample']
              const res4 = res.data.data['sample_type']
              oneRunStep.push([res1, res2, res3, res4])
            })
        }
        allStepTemp['data'].push(oneRunStep)
        allStepTemp['index'] = i
      } else {
        const res1 = []
        const res2 = []
        const res3 = []
        const res4 = []
        oneRunStep.push([res1, res2, res3, res4])
        allStepTemp['data'].push(oneRunStep)
      }
      
    }
      let i = allStepTemp['index'];
      let params = [];
      params = allStepTemp['data'];
      
      for (let j = 0; j < state.categoryInfo.curTags[i].length; j++) {
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]] = {}
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['allSteps'] = params[i][j][0]
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['curMin'] = params[i][j][0][0]
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['curMax'] = params[i][j][0].length - 1
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['shape'] = params[i][j][1][1]
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['sample'] = params[i][j][2]
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['sample_type'] = params[i][j][3]
      }
    state.questionInfo.received = true // 当需要请求信息的时候所有的数据已经完备
    state.receivedQuestionInfo = true
    state.receivedCurInfo = true // 临时测试
  },
  async fetchAllStep(context) { // 数据链的第一步
    const allStepTemp = []
    // console.log('[context.state.categoryInfo]', context.state.categoryInfo)
    for (let i = 0; i < context.state.categoryInfo.curRuns.length; i++) {
      const oneRunStep = []
      for (let j = 0; j < context.state.categoryInfo.curTags[i].length; j++) {
        const param = { run: context.state.categoryInfo.curRuns[i], tag: context.state.categoryInfo.curTags[i][j] }
        await http.useGet(port.category.projector, param)
          .then(res => {
            if (+res.data.code !== 200) {
              context.commit('setErrorMessage', res.data.msg + '_' + new Date().getTime())
              return
            }
            const res1 = res.data.data[context.state.categoryInfo.curTags[i][j]]
            const res2 = res.data.data['shape']
            const res3 = res.data.data['sample']
            const res4 = res.data.data['sample_type']
            oneRunStep.push([res1, res2, res3, res4])
          })
      }
      allStepTemp.push(oneRunStep)
    }
    context.commit('setAllStep', allStepTemp)
  },
  async featchData(context, param) {
    await http.useGet(port.category.projector_data, param)
      .then(res => {
        if (+res.data.code !== 200) {
          context.commit('setErrorMessage', res.data.msg + '_' + new Date().getTime())
          return
        }
        context.commit('setCurData', res.data.data[param.step])
        context.commit('setCurInfo', ['received', true])
      })
  },
  async fetchSampleData(context, param) {
    param = param2Obj(param)
    console.log(layout.state.userSelectRunFile + "1111")
    await http.useGet(port.category.projector_sample, param)
      .then(res => {
        if (+res.data.code !== 200) {
          context.commit('setErrorMessage', res.data.msg + '_' + new Date().getTime())
          return
        }
        context.commit('setPanelSampleData', ['sampData', res.data.data])
      })
  }
}

const mutations = {
  setSelfCategoryInfo: (state, param) => { // 处理分类
    state.categoryInfo.curRuns = param[0].slice(0)
    state.categoryInfo.curTags = param[1].slice(0) // 实现深度拷贝[][]
    state.categoryInfo.initFlag = param[2]['initStateFlag']
    for (let i = 0; i < state.categoryInfo.curRuns.length; i++) {
      state.questionInfo[state.categoryInfo.curRuns[i]] = {}
      for (let j = 0; j < state.categoryInfo.curTags[i].length; j++) {
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]] = {}
      }
    }
    state.curInfo.curRun = state.categoryInfo.curRuns[0]
    state.curInfo.curTags = state.categoryInfo.curTags[0]
    state.curInfo.curTag = state.categoryInfo.curTags[0][0]
    state.curInfo.curStep = 0
    state.curInfo.curMapStep = 0
    state.categoryInfo.received = true // 类目信息完备
    state.receivedCategoryInfo = true
    state.initStateFlag = param[2]['initStateFlag']
  },
  setAllStep: (state, param) => {
    for (let i = 0; i < state.categoryInfo.curRuns.length; i++) {
      for (let j = 0; j < state.categoryInfo.curTags[i].length; j++) {
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]] = {}
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['allSteps'] = param[i][j][0]
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['curMin'] = param[i][j][0][0]
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['curMax'] = param[i][j][0].length - 1
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['shape'] = param[i][j][1][1]
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['sample'] = param[i][j][2]
        state.questionInfo[state.categoryInfo.curRuns[i]][state.categoryInfo.curTags[i][j]]['sample_type'] = param[i][j][3]
      }
    }
    state.questionInfo.received = true // 当需要请求信息的时候所有的数据已经完备
    state.receivedQuestionInfo = true
    state.receivedCurInfo = true // 临时测试
  },
  setReceivedCategoryInfo: (state, param) => {
    state.receivedCategoryInfo = param
  },
  setReceivedQuestionInfo: (state, param) => {
    state.receivedquestionInfo = param
  },
  setReceivedCurInfo: (state, param) => {
    state.receivedCurInfo = param
  },
  setReceivedCurData: (state, param) => {
    state.receivedCurData = param
  },
  setPanelSampleData: (state, param) => {
    state.panelSampleData.type = param[0]
    state.panelSampleData.url = param[1]
  },
  setMessage: (state, param) => {
    state.message = param
  },
  setCurData: (state, param) => {
    state.curData.data = param[0].slice(0)
    if(param[1].slice(0).length == 0) { // 防止后端数据tag为空
      for(let i = 0; i < param[0].length; i++) {
        param[1].push('NULL');
      }
    }
    state.curData.label = param[1].slice(0)
    state.curData.labelType = []
    state.curData.echaLabelNumber = {}
    state.curData.labelTypeColor = {}
    const arr = Array.from(new Set(param[1])).sort(function(m, n) {
      if (m < n) return -1
      else if (m > n) return 1
      else return 0
    })
    for (let i = 0; i < arr.length && i < 10; i++) {
      state.curData.labelType.push(arr[i] + '')
    }
    if (arr.length > 10) {
      state.curData.labelType[9] = '其他'
    }
    for (let i = 0; i < state.curData.labelType.length; i++) {
      state.curData.labelTypeColor[state.curData.labelType[i]] = state.legendColor[i]
    }
    for (let i = 0; i < state.curData.labelType.length; i++) {
      state.curData.echaLabelNumber[state.curData.labelType[i]] = 0
    }
    // 统计每个labelType的个数
    for (let i = 0; i < param[1].length; i++) {
      if (state.curData.labelType.indexOf(param[1][i].toString()) !== -1) {
        state.curData.echaLabelNumber[param[1][i].toString()]++
      } else {
        state.curData.echaLabelNumber[state.curData.labelType[9]]++
      }
    }
    state.receivedCurData = !state.receivedCurData
  },
  setCheckLabels: (state, param) => {
    state.checkLabels = param
  },
  setCurInfo: (state, param) => {
    if (param[0] === 'curTag') {
      state.curInfo.curTag = param[1]
    } else if (param[0] === 'curStep') {
      state.curInfo.curStep = param[1]
    } else if (param[0] === 'curMethod') {
      state.curInfo.curMethod = param[1]
    } else if (param[0] === 'curDim') {
      state.curInfo.curDim = param[1]
    } else if (param[0] === 'received') {
      state.curInfo.received = param[1]
    } else if (param[0] === 'curMapStep') {
      state.curInfo.curMapStep = param[1]
    }
  },
  setInitStateFlag: (state, param) => {
    state.initStateFlag = param
  },
  setErrorMessage: (state, param) => {
    state.errorMessage = param
  },
  setLineWidth: (state, param) => {
    state.lineWidth = param
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
