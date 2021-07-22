import http from '@/utils/request'
import port from '@/utils/api'

const state = {
  run: [],
  tag: [],
  initStateFlag: false,
  allStep: [], // {step, box}
  allData: [], // {run, tag, rectData, histData}
  exceptionShow: false,
  curRunTag: null,
  curNewData: [], // 记录点击step后获取的新数据
  curNewExcepBox: [],
  rectCurInfo: {},
  curIqrTimes: ['', '', '', 1.50, 1.50], // 当前选中的盒线图的一些数据 {run, tag, step, box}
  linkChecked: false,
  excepBoxStatistic: [], // 异常点数据统计
  errorMessage: '',
  dq0Show: true, // 如果dq是0，控制面板显示需要切换
  upDownValue: [0, 0], // 控制面板不显示倍数，而是直接显示数值
  // 临时存储请求的数据和标志
  oneDataTemp: [],
  successFlag: false
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
  getUpDownValue: (state) => state.upDownValue
}

const actions = {
  async getSelfCategoryInfo(context, param) {
    context.commit('setSelfCategoryInfo', param)
    const param2 = { run: param[0][0], tag: param[1][0][0], index: 0 }
    context.commit('setCurRunTag', param2)
    if (param[2]['initStateFlag']) {
      context.dispatch('fetchAllStep')
    }
  },
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
    context.commit('setAllStep', allStepTemp)
    context.dispatch('fetchAllData', { step: allStepTemp[0][2].step[0] })
  },
  async fetchData(context, param) {
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
    oneDataTemp.push(param.index)
    context.commit('setTempData', { 'data': oneDataTemp, 'flag': successFlag })
  },
  async fetchAllData(context, param) { // 获得初始数据,step均为step[0], param={run, tag, step}
    param['run'] = context.state.curRunTag.run
    param['tag'] = context.state.curRunTag.tag
    context.commit('setExceptionShow', false)
    // context.commit('clearAllData')
    await context.dispatch('fetchData', param)
    let exceptionShow = true
    if (!context.state.successFlag) {
      context.state.oneDataTemp = []
      exceptionShow = false
    }
    context.commit('setAllData', context.state.oneDataTemp)
    context.commit('setExceptionShow', exceptionShow)
  },
  // 双击盒线图调用这个获取一个step的三个数据：直方图、颜色矩阵
  async fetchOneData(context, param) { // {run: param.run, tag: param.tag, step: param.step, index}
    await context.dispatch('fetchData', param)
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
      state.allData[param[5]][i] = param[i]
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
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
