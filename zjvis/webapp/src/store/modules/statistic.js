import http from '@/utils/request'
import port from '@/utils/api'

const state = {
  categoryInfo: '',
  initStateFlag: false,
  dataSets: [], // 所有数据集是相同的tag
  dataSetsState: [], // 数据集的显示状态，监听layout.js的userSelectRunFile，是一个数组，里面是数据集的下标
  histTags: [],
  oldHistData: [],
  histData: [], // 直接存储处理后的数据
  oldDistData: [],
  distData: [],
  binNum: 30,
  clickState: false, // 有没有被点击,没用
  histMode: '三维', // threed和orthographic切换
  showNumber: 100,
  histShow: true,
  distShow: false,
  // 控制面板信息栏显示
  histCheckedArray: [], // 用户定制选中
  distCheckedArray: [],
  // 不同run不同颜色
  statisticColor: ['#9FA5FA', '#6dd2f0', '#c06f98', '#f07c82', '#57c3c2', '#9359b1', '#8cc269', '#ffa60f', '#de5991', '#EA7E53', '#cc95c0'], // #6464FF
  // 控制面板信息
  statisticInfo: [],
  errorMessage: '',
  freshFlag: true, // 上一步刷新的请求全部结束后再进行这一步的请求
  downLoadArray: [], // 下载svg图暂存id
  // 在加载数据和渲染时不允许用户操作控制面板
  featchDataFinished: false
}

const getters = {
  getInitStateFlag: (state) => state.initStateFlag,
  getShowNumber: (state) => state.showNumber,
  getMode: (state) => state.histMode,
  getDistData: (state) => state.distData,
  getHistData: (state) => state.histData,
  getBinNum: (state) => state.binNum,
  getShowStatisticFlag: (state) => state.showStatisticFlag,
  getDataSets: (state) => state.dataSets,
  getCategoryInfo: (state) => state.categoryInfo,
  getClickState: (state) => state.clickState,
  getDataSetsState: (state) => state.dataSetsState,
  getStatisticColor: (state) => state.statisticColor,
  getHistCheckedArray: (state) => state.histCheckedArray,
  getDistCheckedArray: (state) => state.distCheckedArray,
  getStatisticInfo: (state) => state.statisticInfo,
  getErrorMessage: (state) => state.errorMessage,
  getHistShow: (state) => state.histShow,
  getDistShow: (state) => state.distShow,
  getDownLoadArray: (state) => state.downLoadArray,
  getFeatchDataFinished: (state) => state.featchDataFinished
}

const actions = {
  async getSelfCategoryInfo(context, param) {
    if (context.state.freshFlag) {
      context.commit('setFreshFlag', false)
      context.commit('setSelfCategoryInfo', param)
      // 如果是第一个，直接获取数据
      if (param[2]['initStateFlag']) {
        context.dispatch('featchAllHistData')
      }
    }
  },

  async featchAllDistData(context) {
    context.commit('clearDistData')
    context.commit('setFeatchDataFinished', false)
    for (let k = 0; k < context.state.dataSets.length; k++) {
      for (let i = 0; i < context.state.histTags[k].length; i++) {
        await http.useGet(port.category.distribution,
          { run: context.state.dataSets[k], tag: context.state.histTags[k][i] })
          .then(res => {
            if (Number(res.data.code) !== 200) {
              context.commit('setErrorMessage', context.state.dataSets[k] + ',' + context.state.histTags[k][i] + ',' + res.data.msg)
              return
            }
            context.commit('storeDistData', [context.state.dataSets[k], context.state.histTags[k][i], res.data.data[context.state.histTags[k][i]], k])
            context.commit('manageDistData')
            if (k === context.state.dataSets.length - 1 && i === context.state.histTags[k].length - 1) {
              context.commit('setFeatchDataFinished', true)
            }
          })
      }
    }
  },
  async featchAllHistData(context) {
    context.commit('clearHistData')
    context.commit('setFeatchDataFinished', false)
    for (let k = 0; k < context.state.dataSets.length; k++) {
      for (let i = 0; i < context.state.histTags[k].length; i++) {
        await http.useGet(port.category.histogram,
          { run: context.state.dataSets[k], tag: context.state.histTags[k][i] })
          .then(res => {
            if (Number(res.data.code) !== 200) {
              context.commit('setErrorMessage', context.state.dataSets[k] + ',' + context.state.histTags[k][i] + ',' + res.data.msg)
              return
            }
            // 根据数据step个数确定显示比例
            const dataLen = res.data.data[context.state.histTags[k][i]].length
            if ((dataLen > 50) && (5000.0 / dataLen < context.state.showNumber)) {
              context.commit('changeShownumber', Math.round(5000.0 / dataLen))
            }
            // 根据上面也可以确定桶个数的最大值
            context.commit('storeHistData', [context.state.dataSets[k], context.state.histTags[k][i], res.data.data[context.state.histTags[k][i]], k])
            context.commit('manageHistData', false)
            if (k === context.state.dataSets.length - 1 && i === context.state.histTags[k].length - 1) {
              context.commit('setFeatchDataFinished', true)
            }
          })
      }
    }
    context.commit('setFreshFlag', true)
  }
}

const mutations = {
  setSelfCategoryInfo: (state, param) => {
    state.categoryInfo = ['histogram', 'distribution']
    state.dataSets = param[0]
    for (let i = 0; i < state.dataSets.length; i++) {
      state.histTags.push(param[1][i]['histogram'])
    }
    state.dataSetsState = []
    for (let i = 0; i < state.dataSets.length; i++) {
      state.dataSetsState[state.dataSets[i]] = true
    }
    state.initStateFlag = param[2]['initStateFlag']
  },
  setInitStateFlag: (state, param) => {
    state.initStateFlag = param
  },
  setClickState: (state, param) => {
    state.clickState = param
  },
  changeMode: (state, curMode) => {
    state.histMode = curMode
    state.isSwitchFlag = true
    // 在模型切换时需要替换掉downloadArray中的id
    const newDownLoadArray = []
    if (state.histMode === '三维') {
      for (let i = 0; i < state.downLoadArray.length; i++) {
        newDownLoadArray.push(state.downLoadArray[i].replace(/overlay/, 'offset'))
      }
      state.downLoadArray = newDownLoadArray
    } else {
      for (let i = 0; i < state.downLoadArray.length; i++) {
        newDownLoadArray.push(state.downLoadArray[i].replace(/offset/, 'overlay'))
      }
      state.downLoadArray = newDownLoadArray
    }
  },
  changeShownumber: (state, curNumber) => {
    state.showNumber = curNumber
  },
  storeDistData: (state, data) => {
    state.oldDistData.push(data)
  },
  manageDistData: (state) => {
    const k = state.oldDistData.length - 1 // 每次只处理最新获取到的数据
    const oneData = state.oldDistData[k][2]
    const newData = []
    for (let i = 0; i <= 8; i++) {
      // 每个图9条线
      const linedata = []
      for (let j = 0; j < oneData.length; j++) {
        const temp = []
        temp.push(oneData[j][1]) // step,x
        temp.push(oneData[j][2][i][1]) // value,y
        linedata.push(temp)
      }
      newData.push(linedata)
    }
    // 为了画area,需要再处理一下，除了第一步，其余都要加上上一条的y轴数据
    for (let i = 1; i < newData.length; i++) {
      for (let j = 0; j < newData[i - 1].length; j++) {
        newData[i][j].push(newData[i - 1][j][1])
      }
    }
    state.distData.push([state.oldDistData[k][0], state.oldDistData[k][1], newData, state.oldDistData[k][3], k])
    state.distCheckedArray.push(false)
  },
  clearHistData: (state) => {
    state.oldHistData = []
    state.histData = []
    state.histCheckedArray = []
    // 同时清空dist数据，因为页面刷新
    state.oldDistData = []
    state.distData = []
    state.distCheckedArray = []
  },
  clearDistData: (state) => {
    state.oldDistData = []
    state.distData = []
    state.distCheckedArray = []
  },
  storeHistData: (state, data) => {
    state.oldHistData.push(data)
  },
  manageHistData: (state, param) => {
    // 不仅在取出初始数据时调用，在修改桶数时也调用这个函数
    // 加个param，false表示是初始获取数据，处理最后一个；true表示是修改桶数，处理所有
    const histDataTemp = []
    let k = 0
    if (!param) k = state.oldHistData.length - 1
    for (; k < state.oldHistData.length; k++) {
      const data = state.oldHistData[k][2]
      const newdata = []
      let min = 1000
      let max = -1000
      for (let i = 0; i < data.length; i++) {
        if (min > data[i][2]) min = data[i][2]
        if (max < data[i][3]) max = data[i][3]
      }
      const binWidth = (max - min) / state.binNum
      for (let i = 0; i < data.length; i++) { // 遍历step
        const onedata = data[i][4]
        // 处理一下首尾
        onedata[0][0] = onedata[0][1] - binWidth / 2
        onedata[onedata.length - 1][1] = onedata[onedata.length - 1][0] + binWidth / 2
        const newOneData = []
        let binleft = min
        let binright = binleft
        let curbucket = 0
        // 让首尾为0
        newOneData.push([min - binWidth / 2, 0, data[i][1]])
        for (let j = 0; j < state.binNum; j++) {
          binleft = binright
          binright = binleft + binWidth
          let count = 0
          for (; curbucket < onedata.length - 1; curbucket++) {
            if (binright < onedata[curbucket][0]) break
            const maxleft = Math.max(binleft, onedata[curbucket][0])
            const curBinWidth = onedata[curbucket][1] - onedata[curbucket][0]
            if (binright <= onedata[curbucket][1]) {
              if (curBinWidth !== 0) count += (binright - maxleft) / curBinWidth * onedata[curbucket][2]
              break
            } else {
              if (curBinWidth !== 0) count += (onedata[curbucket][1] - maxleft) / curBinWidth * onedata[curbucket][2]
            }
          }
          newOneData.push([(binleft + binright) / 2, count, data[i][1]])
        }
        newOneData.push([max + binWidth / 2, 0, data[i][1]])
        newdata.push(newOneData)
      }
      histDataTemp.push([state.oldHistData[k][0], state.oldHistData[k][1], newdata, state.oldHistData[k][3], k])
    }
    if (!param) {
      state.histData.push(histDataTemp[0])
      state.histCheckedArray.push(false)
    } else { // 修改桶数
      state.histData = histDataTemp
    }
  },
  setBinNum: (state, binNum) => {
    state.binNum = binNum
  },
  setDataSetsState: (state, param) => {
    state.dataSetsState = param
  },
  setHistShow: (state, param) => {
    state.histShow = param
  },
  setDistShow: (state, param) => {
    state.distShow = param
  },
  setStatisticInfo: (state, param) => {
    state.statisticInfo = param
  },
  setHistCheckedArray(state, param) {
    state.histCheckedArray[param.idx] = param.value
  },
  setDistCheckedArray(state, param) {
    state.distCheckedArray[param.idx] = param.value
  },
  setErrorMessage(state, param) {
    state.errorMessage = param
  },
  setFreshFlag(state, param) {
    state.freshFlag = param
  },
  setDownLoadArray(state, param) {
    if (param[0]) {
      state.downLoadArray.push(param[1])
    } else {
      const i = state.downLoadArray.indexOf(param[1])
      if (i !== -1) {
        state.downLoadArray.splice(i, 1)
      }
    }
  },
  setFeatchDataFinished(state, param) {
    state.featchDataFinished = param
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
