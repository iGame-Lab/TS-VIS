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
  },
  IntervalChange: false
}

const getters = {
  categoryInfo: (state) => state.categoryInfo,
  detailData: (state) => state.detailData,
  showrun: (state) => state.showrun,
  getTotaltag: (state) => state.totaltag,
  getFreshInfo: (state) => state.freshInfo,
  getErrorMessage: (state) => state.errorMessage,
  getShowFlag: (state) => state.showFlag,
  getIntervalChange: (state) => state.IntervalChange
}

const actions = {
  async getSelfCategoryInfo (context, param) {
    // console.log("param", param)
    let initDetailData = {}
    // 根据自己的类目增加相应的判断
    for (let i = 0; i < param[1].length; i++) {
      Object.keys(param[1][i]).forEach(value => {
        initDetailData[value] = []
      })
    }
    // console.log('initDetailData',  initDetailData)
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
  async getIntervalSelfCategoryInfo(context, param) {
    // console.log("param", param)
    let initDetailData = {}
    // 根据自己的类目增加相应的判断
    for (let i = 0; i < param[1].length; i++) {
      Object.keys(param[1][i]).forEach(value => {
        // console.log('value', value)
        initDetailData[value] = []
      })
    }
    // console.log('initDetailData',  initDetailData)
    context.commit('setSelfCategoryInfo', param)
    context.commit('setIntervalDetailDataInfo', initDetailData)
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
                context.commit('setDetailData', [param[0], { 'run': context.state.categoryInfo[0][i], 'value': res.data.data, 
                'port': port.category[param[0]], 'parameter':  parameter}])
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
  setIntervalDetailDataInfo: (state, param) => {
    // console.log("param", param, state.detailData)
    if(state.detailData == '') {
      state.detailData = param
    }else {
      Object.keys(param).forEach(value => {
        if(Object.keys(state.detailData).indexOf(value)==-1) {
          state.detailData[value] = []
        }
      })
    }
    // state.IntervalChange = !state.IntervalChange 母鸡为什么这个不更新也会去请求新数据
  },
  setDetailData: (state, param) => {
    // state.detailData[param[0]].push(param[1]) 

    // param分为两部分
    // param[0]为string，存储大tag标签，例如loss，mean，conv1等
    // param[1]为对象，param[1]['run']存储训练模型名称，param[1]['value']存储对应param[0]的标量数据类型
    let keys = [] // keys存储标量数据类型及模型名称，如loss-log

    for(let k in param[1]['value']) {
      keys.push(k + '-' + param[1]['run'])
    }
  
    let keys2 = [] // keys2存储第一次加载数据的存储标量数据类型及模型名称，用于和keys比较，判断替换下一次请求的数据
    let index = [] // 一个tag下多个模型编号
    for(let key in state.detailData[param[0]] ) {
        for(let kk in state.detailData[param[0]][key]['value']) {
          keys2.push(kk + '-' + state.detailData[param[0]][key]['run'])
          index.push(key)
        }
    }
    // console.log("index", index, "kyes2", keys2, 'keys',keys, 'state.detailData[param[0]]', state.detailData[param[0]], param[0])
    for(let i=0; i < keys.length; i++) {
      if(keys2.indexOf(keys[i]) != -1) {
        state.detailData[param[0]][index[keys2.indexOf(keys[i])]]['value'] = param[1]['value']
      }else{
        state.detailData[param[0]].push(param[1])
      }
    }

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
