import http from '@/utils/request'
import port from '@/utils/api'

/* eslint-disable */

const state = {
  categoryInfo: '', // 存放自己的类目信息
  detailData: '', // 具体数据
  clickState: false,
  showrun: {},
  totaltag: '',
  freshInfo: {},
  errorMessage: '',
  showFlag: {
    firstTime: true
  }
}

const getters = {
  categoryInfo: (state) => state.categoryInfo,
  detailData: (state) => state.detailData,
  showrun: (state) => state.showrun,
  getTotaltag: (state) => state.totaltag,
  getFreshInfo: (state) => state.freshInfo,
  getErrorMessage: (state) => state.errorMessage,
  getShowFlag: (state) => state.showFlag
}

const actions = {
  async getSelfCategoryInfo (context, param) {
    let initDetailData = {}
    // 根据自己的类目增加相应的判断
    for (let i = 0; i < param[1].length; i++) {
      Object.keys(param[1][i]).forEach(value => {
        initDetailData[value] = []
      })
    }
    context.commit('setSelfCategoryInfo', param)
    context.commit('setInitDetailDataInfo', initDetailData)
    if (param[2]['initStateFlag']) {
      if (typeof (param[1]) === 'object') {
        // console.log('I am Object!')
        // let firstFloor = Object.keys(param[1])[0]
        // context.dispatch('getImageData', [firstFloor, param[1][firstFloor]]) // 没有真正的发出去因为没有承接函数
        // console.log('getImageData', [firstFloor, param[1][firstFloor]])
      } else if (param[1][0] === 'true') {
        // 处理需要数据请求
        // console.log('I am array!')
      }
    }
  },
  async getData (context, param) {
    // 类目  tags
    // console.log(param, context.state.detailData[param[0]])
    // if(context.state.detailData[param[0]].length === 0) {
      // console.log(param[1])
      for (let j = 0; j < param[1].length; j++) {
        // console.log(param[1][j])
        for (let i = 0; i < context.state.categoryInfo[0].length; i++) {
          if (Object.keys(context.state.categoryInfo[1][i]).indexOf(param[0]) > -1) {
            if (context.state.categoryInfo[1][i][param[0]].indexOf(param[1][j]) > -1) {
              let parameter = {
                run: context.state.categoryInfo[0][i],
                tag: param[1][j]
              }
              await http.useGet(port.category[param[0]], parameter).then(res => { // port.category.scalar 'scalar' 换成你需要的接口
                if (+res.data.code !== 200) {
                  context.commit('setErrorMessage', res.data.msg + '_' + new Date().getTime())
                  return
                }
                context.commit('setDetailData', [param[0], { 'run': context.state.categoryInfo[0][i], 'value': res.data.data }])
              })
            }
          }
        }
      }
    // }
  }
}

const mutations = {
  setShowFlag: (state, param) => {
    state.showFlag[param[0]] = param[1]
  },
  setSelfCategoryInfo: (state, param) => {
    // console.log('param', param) // param[0]:训练集 param[1] {audio:array, ...} param[2] 是否初始显示
    state.categoryInfo = param
  },
  setInitDetailDataInfo: (state, param) => {
    state.detailData = param
  },
  setDetailData: (state, param) => {
    state.detailData[param[0]].push(param[1])
  },
  setClickState: (state, param) => {
    state.clickState = param
  },
  setshowrun: (state, param) => {
    for (let i = 0; i < state.categoryInfo[0].length; i++) {
      if (param.indexOf(state.categoryInfo[0][i]) > -1) {
        state.showrun[state.categoryInfo[0][i]] = true
      } else {
        state.showrun[state.categoryInfo[0][i]] = false
      }
    }
  },
  setTotaltag: (state, param) => {
    state.totaltag = param
  },
  setFreshInfo: (state, param) => {
    state.freshInfo[param[0]] = param[1] // false表示类目被打开
  },
  setErrorMessage: (state, param) => {
    state.errorMessage = param
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
