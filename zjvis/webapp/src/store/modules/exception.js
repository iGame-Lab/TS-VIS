import http from '@/utils/request'
import port from '@/utils/api'

const state = {
  run: [],
  tag: [],
  initStateFlag: false,
  allStep: [], // {step, box}
  allData: [], // [[run, tag, rectData, histData]]
  exceptionShow: false,
  curRunTag: null,
  curNewData: [], // 记录点击step后获取的新数据
  curNewExcepBox: [],
  rectCurInfo: [],
  curIqrTimes: ['', '', '', 1.50, 1.50], // 当前选中的盒线图的一些数据 {run, tag, step, box}
  linkChecked: false,
  excepBoxStatistic: [], // 异常点数据统计
  errorMessage: '',
  dq0Show: true, // 如果dq是0，控制面板显示需要切换
  upDownValue: [0, 0], // 控制面板不显示倍数，而是直接显示数值
  // 临时存储请求的数据和标志
  oneDataTemp: [],
  successFlag: false,
  // 定时刷新
  updateFlag: false, // run和tag是否有变化，如果有变化，判断当前数据是否存在，如果存在就重新请求，否则请求一个新数据
  // 如果run、tag、step变化，值为'run...', 'tag...', 'setp...', 否则就为'none'
  updateHistMatrixDataFlag: 'run', // 如果run、tag或step有变化，需要重新请求颜色矩阵和直方图的数据，run/tag变化，用fetchAllData请求；step变化就用fetchOneData请求
  fetchAllStepNotify: true
}

const getters = {
  getInitStateFlag: (state) => state.initStateFlag,
  getRun: (state) => state.run,
  getTag: (state) => state.tag,
  getAllStep: (state) => state.allStep,
  getAllData: (state) => state.allData,
  getExceptionShow: (state) => state.exceptionShow,
  getCurRunTag: (state) => state.curRunTag,
  getCurNewData: (state) => state.curNewData,
  getCurNewExcepBox: (state) => state.curNewExcepBox,
  getRectCurInfo: (state) => state.rectCurInfo,
  getCurIqrTimes: (state) => state.curIqrTimes,
  getLinkChecked: (state) => state.linkChecked,
  getExcepBoxStatistic: (state) => state.excepBoxStatistic,
  getErrorMessage: (state) => state.errorMessage,
  getDq0Show: (state) => state.dq0Show,
  getUpDownValue: (state) => state.upDownValue,
  getUpdateFlag: (state) => state.updateFlag,
  getUpdateHistMatrixDataFlag: (state) => state.updateHistMatrixDataFlag,
  getFetchAllStepNotify: (state) => state.fetchAllStepNotify
}

const actions = {
  async getSelfCategoryInfo(context, param) {
    context.commit('setSelfCategoryInfo', param)
    const param2 = { run: param[0][0], tag: param[1][0][0], index: 0, step: '' }
    context.commit('setCurRunTag', param2)
    if (param[2]['initStateFlag']) {
      context.dispatch('fetchAllStep')
    }
  },
  async getIntervalSelfCategoryInfo(context, param) {
    // 不能在这里发起请求，得在vue组件中判断请求，否则不在本页面也会请求新数据
    context.commit('setIntervalSelfCategoryInfo', param)
  },
  // 初始请求，改变run、改变tag时需要重新请求数据step数据，定时刷新也需要重新请求数据
  async fetchAllStep(context) { // param={run, tag}
    const param = {}
    param['run'] = context.state.curRunTag.run
    param['tag'] = context.state.curRunTag.tag
    const run = context.state.run
    if (run.length === 0) return
    const allStepTemp = []
    await http.useGet(port.category.exception, param).then(res => {
      if (Number(res.data.code) !== 200) {
        context.commit('setErrorMessage', param.run + ',' + param.tag + ',' + res.data.msg)
        return
      }
      allStepTemp.push([param.run, param.tag, res.data.data[param.tag]])
    })
    if (context.state.curRunTag.step === '' || allStepTemp[0][2].step.indexOf(context.state.curRunTag.step) === -1) {
      await context.commit('setCurStep', allStepTemp[0][2].step[0])
      if (context.state.updateHistMatrixDataFlag === 'none') {
        await context.commit('setUpdateHistMatrixDataFlag', 'step' + new Date().getTime())
      }
    }
    context.commit('setAllStep', allStepTemp)
    context.commit('setFetchAllStepNotify')
  },
  async fetchData(context) {
    const param = {
      run: context.state.curRunTag.run,
      tag: context.state.curRunTag.tag,
      step: context.state.curRunTag.step
    }
    const oneDataTemp = []
    let successFlag = true
    await http.useGet(port.category.exception_data, param).then(res => {
      if (Number(res.data.code) !== 200) {
        successFlag = false
        context.commit('setErrorMessage', param.run + ',' + param.tag + ',' + res.data.msg)
        return
      }
      oneDataTemp.push(param.run)
      oneDataTemp.push(param.tag)
      oneDataTemp.push(param.step)
      const rectDataTemp = res.data.data[param.step]
      if (!(rectDataTemp[4][0] instanceof Array)) { // 处理一维数据
        const rectData = rectDataTemp[4]
        rectDataTemp[4] = []
        rectDataTemp[4].push(rectData)
      }
      rectDataTemp[0][0] = rectDataTemp[4].length
      rectDataTemp[0][1] = rectDataTemp[4][0].length
      oneDataTemp.push(rectDataTemp)
    })
    if (successFlag) { // 默认上一个请求到了，这个也可以请求到，嵌套好像不行
      await http.useGet(port.category.exception_hist, param).then(res => {
        if (Number(res.data.code) !== 200) {
          successFlag = false
          context.commit('setErrorMessage', param.run + ',' + param.tag + ',' + res.data.msg)
          return
        }
        oneDataTemp.push(res.data.data[param.step][0])
      })
    }
    oneDataTemp.push(context.state.curRunTag.index)
    context.commit('setTempData', { 'data': oneDataTemp, 'flag': successFlag })
  },
  async fetchAllData(context) { // 获得初始数据,step均为step[0], param={run, tag, step}，run、tag发生变化
    context.commit('setExceptionShow', false)
    // context.commit('clearAllData')
    await context.dispatch('fetchData')
    let exceptionShow = true
    if (!context.state.successFlag) {
      context.state.oneDataTemp = []
      exceptionShow = false
    }
    context.commit('setAllData', context.state.oneDataTemp)
    context.commit('setExceptionShow', exceptionShow)
  },
  // 双击盒线图调用这个获取一个step的三个数据：直方图、颜色矩阵
  async fetchOneData(context, param) { // {run: param.run, tag: param.tag, step: param.step, index}，step发生变化
    await context.commit('setCurStep', param.step)
    await context.dispatch('fetchData')
    if (!context.state.successFlag) {
      context.state.oneDataTemp = []
    }
    context.commit('setOneData', context.state.oneDataTemp)
  },
  // 移动盒线图上下边界时获取异常点
  async fetchExcepBox(context, param) { // param={run:, tag:,step:,down:,up:},异常点数据
    await http.useGet(port.category.exception_box, param).then(res => {
      if (Number(res.data.code) !== 200) {
        context.commit('setErrorMessage', param.run + ',' + param.tag + ',' + res.data.msg)
        return
      }
      context.commit('setExcepBox', [param.run, param.tag, res.data.data[param.step]])
    })
  }
}

const mutations = {
  setSelfCategoryInfo: (state, param) => {
    state.run = param[0]
    state.tag = param[1]
    state.initStateFlag = param[2]['initStateFlag']
    state.allData = [] // 刷新时需要
  },
  setInitStateFlag: (state, param) => {
    state.initStateFlag = param
  },
  clearAllData: (state) => {
    state.allData = []
  },
  setAllStep: (state, param) => {
    state.allStep = param
  },
  setAllData: (state, param) => {
    const temp = []
    temp.push(param)
    state.allData = temp
  },
  setExceptionShow(state, param) {
    state.exceptionShow = param
  },
  setOneData: (state, param) => {
    state.curNewData = param
    for (let i = 2; i <= 4; i++) {
      state.allData[0][i] = param[i]
    }
  },
  setExcepBox(state, param) {
    state.curNewExcepBox = param
  },
  // 调整box中上下两条线，根据这个来计算筛选异常点
  setAllStepBoxDown(state, param) { // param={index:,step:,down}，index:是run\tag对应的下标
    state.allStep[param.index][2]['box'][param.step][0][4] = param.down
  },
  setAllStepBoxUp(state, param) {
    state.allStep[param.index][2]['box'][param.step][0][0] = param.up
  },
  setCurRunTag(state, param) {
    state.curRunTag = param
  },
  setRectCurInfo(state, param) {
    state.rectCurInfo = param
  },
  setCurIqrTimes(state, param) {
    // 还是要存储run, tag, step的
    param[3] = Number(param[3])
    param[4] = Number(param[4])
    if (state.curIqrTimes[0] === param[0] && state.curIqrTimes[1] === param[1] && state.curIqrTimes[2] === param[2] &&
      state.curIqrTimes[3] === param[3] && state.curIqrTimes[4] === param[4]) { // 数据没有变化就不存进去
      return
    }
    state.curIqrTimes = param
  },
  setLinkChecked(state, param) {
    state.linkChecked = param
  },
  setExcepBoxStatistic(state, param) {
    state.excepBoxStatistic = param
  },
  setErrorMessage(state, param) {
    state.errorMessage = param
  },
  setDq0Show(state, param) {
    state.dq0Show = param
  },
  setUpDownValue(state, param) {
    state.upDownValue = param
  },
  setTempData(state, param) {
    state.oneDataTemp = param.data
    state.successFlag = param.flag
  },
  setIntervalSelfCategoryInfo(state, param) {
    state.run = param[0]
    state.tag = param[1]
    state.updateFlag = !state.updateFlag // 不管值如何，只监听变化
    // 如果run、tag发生变化，修改curRun、curTag
    if (state.curRunTag === null || state.run.indexOf(state.curRunTag.run) === -1) {
      state.curRunTag = { run: state.run[0], tag: state.tag[0], index: 0, step: '' }
      state.updateHistMatrixDataFlag = 'run' + state.run[0]
    } else if (state.tag[state.curRunTag['index']].indexOf(state.curRunTag.tag) === -1) {
      state.curRunTag['tag'] = state.tag[state.curRunTag['index']][0]
      state.updateHistMatrixDataFlag = 'tag' + state.curRunTag['tag']
    } else {
      state.updateHistMatrixDataFlag = 'none'
    }
  },
  setCurStep(state, param) {
    state.curRunTag.step = param
  },
  setUpdateHistMatrixDataFlag(state, param) {
    state.updateHistMatrixDataFlag = param
  },
  setFetchAllStepNotify(state) {
    state.fetchAllStepNotify = !state.fetchAllStepNotify
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
