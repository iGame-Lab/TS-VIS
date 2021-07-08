import http from '@/utils/request'
import port from '@/utils/api'

const state = {
  run: [],
  tag: [],
  initStateFlag: false,
  allStep: [], // {step, box}
  allData: [], // {run, tag, rectData, histData}
  curNewData: [], // 记录点击step后获取的新数据
  curNewExcepBox: [],
  rectCurInfo: {},
  curIqrTimes: ['', '', '', 1.50, 1.50], // 当前选中的盒线图的一些数据 {run, tag, step, box}
  linkChecked: false,
  excepBoxStatistic: [], // 异常点数据统计
  errorMessage: '',
  freshFlag: true,
  dq0Show: true, // 如果dq是0，控制面板显示需要切换
  upDownValue: [0, 0] // 控制面板不显示倍数，而是直接显示数值
}

const getters = {
  getInitStateFlag: (state) => state.initStateFlag,
  getRun: (state) => state.run,
  getTag: (state) => state.tag,
  getAllStep: (state) => state.allStep,
  getAllData: (state) => state.allData,
  getCurNewData: (state) => state.curNewData,
  getCurNewExcepBox: (state) => state.curNewExcepBox,
  getRectCurInfo: (state) => state.rectCurInfo,
  getCurIqrTimes: (state) => state.curIqrTimes,
  getLinkChecked: (state) => state.linkChecked,
  getExcepBoxStatistic: (state) => state.excepBoxStatistic,
  getErrorMessage: (state) => state.errorMessage,
  getFreshFlag: (state) => state.freshFlag,
  getDq0Show: (state) => state.dq0Show,
  getUpDownValue: (state) => state.upDownValue
}

const actions = {
  async getSelfCategoryInfo(context, param) {
    if (context.state.freshFlag) { // 连类目信息都要等到这一次全部数据获取后再更新
      context.commit('setFreshFlag', false)
      context.commit('setSelfCategoryInfo', param)
      if (param[2]['initStateFlag']) {
        context.dispatch('fetchAllStep')
        // 初始先执行created再执行这里的函数
        context.commit('setInitStateFlag', false)
      }
    }
  },
  async fetchAllStep(context) {
    const run = context.state.run
    if (run.length === 0) return
    const tag = context.state.tag
    const allStepTemp = []
    for (let i = 0; i < run.length; i++) {
      for (let j = 0; j < tag[i].length; j++) {
        const param = { run: run[i], tag: tag[i][j] }
        await http.useGet(port.category.exception, param).then(res => {
          if (Number(res.data.code) !== 200) {
            context.commit('setErrorMessage', run[i] + ',' + tag[i][j] + ',' + res.data.msg)
            return
          }
          allStepTemp.push([run[i], tag[i][j], res.data.data[tag[i][j]]])
        })
      }
    }
    context.commit('setAllStep', allStepTemp)
  },
  async fetchAllData(context) { // 获得初始数据,step均为step[0]
    context.commit('clearAllData')
    const run = context.state.run
    const tag = context.state.tag
    let count = 0
    for (let i = 0; i < run.length && count < context.state.allStep.length; i++) {
      for (let j = 0; j < tag[i].length && count < context.state.allStep.length; j++) {
        const initStep = context.state.allStep[count][2]['step'][0]
        const param = { run: run[i], tag: tag[i][j], step: initStep }
        const oneDataTemp = []
        let successFlag = true
        await http.useGet(port.category.exception_data, param).then(res => {
          if (Number(res.data.code) !== 200) {
            successFlag = false
            context.commit('setErrorMessage', run[i] + ',' + tag[i][j] + ',' + res.data.msg)
            return
          }
          oneDataTemp.push(param.run)
          oneDataTemp.push(param.tag)
          oneDataTemp.push(0)
          const rectDataTemp = res.data.data[initStep]
          if (rectDataTemp[0].length === 1) { // 处理一维数据
            const rectLenTemp = rectDataTemp[0][0]
            rectDataTemp[0][0] = 1
            rectDataTemp[0].push(rectLenTemp)
            const rectData = rectDataTemp[4]
            rectDataTemp[4] = []
            rectDataTemp[4].push(rectData)
          }
          oneDataTemp.push(rectDataTemp)
        })
        if (successFlag) { // 默认上一个请求到了，这个也可以请求到，嵌套好像不行
          await http.useGet(port.category.exception_hist, param).then(res => {
            oneDataTemp.push(res.data.data[initStep][0])
          })
          context.commit('setAllData', oneDataTemp)
        }
        count++
      }
    }
    // 取完step后立马取出颜色矩阵和直方图，需要这些数据都取到后再刷新
    context.commit('setFreshFlag', true)
  },
  // 双击盒线图调用这个获取一个step的三个数据：直方图、颜色矩阵
  async fetchOneData(context, param) { // {run: param.run, tag: param.tag, step: param.step, down: param.down, up: param.up}
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
      if (rectDataTemp[0].length === 1) { // 处理一维数据
        const rectLenTemp = rectDataTemp[0][0]
        rectDataTemp[0][0] = 1
        rectDataTemp[0].push(rectLenTemp)
        const rectData = rectDataTemp[4]
        rectDataTemp[4] = []
        rectDataTemp[4].push(rectData)
      }
      oneDataTemp.push(rectDataTemp)
    })
    if (successFlag) {
      // 上一个请求成功了再进行下一个请求
      await http.useGet(port.category.exception_hist, param).then(res => {
        oneDataTemp.push(res.data.data[param.step][0])
      })
      oneDataTemp.push(param.index) // index确定当前（run,tag）的数据在allData数组中的下标
      context.commit('setOneData', oneDataTemp)
    }
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
    state.allData.push(param)
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
  setFreshFlag(state, param) {
    state.freshFlag = param
  },
  setDq0Show(state, param) {
    state.dq0Show = param
  },
  setUpDownValue(state, param) {
    state.upDownValue = param
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
