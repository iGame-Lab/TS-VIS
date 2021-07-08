/* eslint-disable no-unused-vars */
/*
 * @Description: state.custom
 * @version: 1.0
 * @Author: xds
 * @Date: 2020-05-02 07:11:04
 * @LastEditors: xds
 * @LastEditTime: 2020-05-23 11:05:13
 */
// dubhe-web\src\utils\VisualUtils\api.js
import http from '@/utils/request'
import port from '@/utils/api'

const state = {
  categoryInfo: '', // 存放自己的类目信息
  detailData: '', // 具体数据
  clickState: false,
  // xxxData存放定制最终数据,xxx存放当前页面勾选数据
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
  // statisticBinNumber: 30, // 要修改桶数还要保存最原始的数据
  lastRouter: -1
}

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
  // getStatisticBinNumber: (state) => state.statisticBinNumber,
  getStatisticShowNumber: (state) => state.statisticShowNumber
}

const actions = {
  async getSelfCategoryInfo(context, param) {

    // let initDetailData = {}
    // console.log(Object.keys(param[1]))
    // Object.keys(param[1]).forEach(value => {
    //   initDetailData[value] = []
    // })

    // context.commit('setSelfCategoryInfo', param)

    // context.commit('setInitDetailDataInfo', initDetailData)
    // console.log(initDetailData)
    // if (param[2]['initStateFlag']) { // 判断是否为页面加载后需显示的模块
    //   console.log('我是初始显示界面')
    //   console.log(param[1])
    //   if (typeof (param[1]) === 'object') {
    //     console.log('I am Object!')
    //     let firstFloor = Object.keys(param[1])[0]
    //     // console.log(firstFloor)
    //     context.dispatch('getData', [firstFloor, param[1][firstFloor]])
    //   } else if (param[1][0] === 'true') {
    //     // 处理需要数据请求
    //     console.log('I am array!')
    //   }
    // }

  },
  async getData(context, param) {
    if (context.state.detailData[param[0]].length === 0) {

      // console.log(param[1])
      // let allDataTemp = []
      // for (let i = 0; i < context.state.categoryInfo[0].length; i++) {
      //   for (let j = 0; j < param[1].length; j++) {
      //     let parameter = {
      //       run: context.state.categoryInfo[0][i],
      //       tag: param[1][j]
      //     }
      //     // console.log(parameter)
      //     await http.useGet(port.category.custom, parameter).then(res => { // port.category.scalar 'scalar' 换成你需要的接口
      //       console.log(res)
      //       allDataTemp.push([context.state.categoryInfo[0][i], param[j], res.data])
      //     })
      //   }
      // }
      // // 可在此处处理数据
      // console.log(allDataTemp)
      // // 处理完调用mutation中的方法保存到状态中
      // // context.commit('setDetailData', allDataTemp)

    }
  },
  async dynamicGetData(context) {
    // {} {} 特定的url/参数
    await http.useGet({}, {}).then(res => {
      // 对获取到的结果进行判断1.是否需更新数据， 2.时间戳(保存到状态中，下次发送请求作为标志)
    })
  }
}

const mutations = {
  setSelfCategoryInfo: (state, param) => {
    state.categoryInfo = param
  },
  setInitDetailDataInfo: (state, param) => {
    state.detailData = param
  },
  setDetailData: (state, param) => {
    state.detailData.push(param)
  },
  setClickState: (state, param) => {
    state.clickState = param
  },
  setAudioData: (state, param) => { // param 是一个json对象 且只包含第一个数据
    const paramStringIndex = param.content.run + '/' + Object.keys(param.content.value)[0] // Ex: train/bisine_wave_1/audio_summary
    let flag = true
    for (let i = 0; i < state.audio.length; i++) {
      if (paramStringIndex === state.audio[i].stringIndex) {
        flag = false
        state.audio.splice(i, 1)
        if (param.copyToData) {
          state.audioData = JSON.parse(JSON.stringify(state.audio))
        }
        break
      }
    }
    if (flag) {
      state.audio.push({ stringIndex: paramStringIndex, checked: param.checked, content: param.content })
    }
  },
  setTextData: (state, param) => {
    const paramStringIndex = param.content.run + '/' + Object.keys(param.content.value)[0] // Ex: train/bisine_wave_1/audio_summary
    let flag = true
    for (let i = 0; i < state.text.length; i++) {
      if (paramStringIndex === state.text[i].stringIndex) {
        flag = false
        state.text.splice(i, 1)
        if (param.copyToData) {
          state.textData = JSON.parse(JSON.stringify(state.text))
        }
        break
      }
    }
    if (flag) {
      state.text.push({ stringIndex: paramStringIndex, checked: param.checked, content: param.content })
    }
  },
  setImageData: (state, param) => { // param 是一个json对象 且只包含第一个数据
    const paramStringIndex = param.content.run + '/' + Object.keys(param.content.value)[0] // Ex: train/bisine_wave_1/audio_summary
    let flag = true
    for (let i = 0; i < state.image.length; i++) {
      if (paramStringIndex === state.image[i].stringIndex) {
        flag = false
        state.image.splice(i, 1)
        if (param.copyToData) {
          state.imageData = JSON.parse(JSON.stringify(state.image))
        }
        break
      }
    }
    if (flag) {
      state.image.push({ stringIndex: paramStringIndex, checked: param.checked, content: param.content })
    }
  },
  setStatisticData: (state, param) => {
    // 先查看当前custom里有没有这个数据
    let flag = -1
    for (let i = 0; i < state.statistic.length; i++) {
      if (state.statistic[i].ttlabel === param.ttlabel && state.statistic[i].tag === param.tag &&
       (state.statistic[i].componentName === param.componentName || param.componentName === 'threed' || param.componentName === 'orthographic')) {
        // 存在这个数据
        // delete为false表示是原父组件调用，把checked标记为false
        if (!param.delete) {
          // state.statistic[i].checked = param.checked
          state.statistic.splice(i, 1) // 只删除statistic中的数据，statisticData等到定制时再赋值
        } else { // 如果是custom组件调用的删除直接更新statisticData
          state.statistic.splice(i, 1) // 直接删除
          state.statisticData = state.statistic
        }
        if (!state.statisticData.length) { // 为空了，恢复默认值
          state.statisticMode = '三维'
          state.statisticShowNumber = 10
        }
        flag = 1
        break
      }
    }
    if (flag === -1) {
      // 不存在，添加这个数据
      if (param.itemp < 1000) param.itemp = 1000 + param.itemp
      param.divId = 'custom' + param.componentName + param.itemp
      // 根据控制面板修改
      if (state.statisticMode === '三维' && param.componentName === 'orthographic') {
        param.componentName = 'threed'
      } else if (state.statisticMode === '二维' && param.componentName === 'threed') {
        param.componentName = 'orthographic'
      }
      state.statistic.push(param)
    }
    // console.log(state.statistic)
  },
  setData: (state, param) => {
    // console.log('setData', param)
    switch (param) {
      case 'scalar':
        Object.assign(state.scalarmid, JSON.parse(JSON.stringify(state.scalar)))
        Object.assign(state.scalarData, JSON.parse(JSON.stringify(state.scalar)))
        state.scalar = {}
        break
      case 'media':
        state.imageData = JSON.parse(JSON.stringify(state.image))
        state.audioData = JSON.parse(JSON.stringify(state.audio))
        state.textData = JSON.parse(JSON.stringify(state.text))
        break
      case 'statistic':
        /*
        state.statisticData = []
        for (let i = 0; i < state.statistic.length; i++) {
          if (state.statistic[i].checked) {
            state.statisticData.push(state.statistic[i])
          }
        }
        state.statistic = JSON.parse(JSON.stringify(state.statisticData))
        */
        state.statisticData = JSON.parse(JSON.stringify(state.statistic))
        break
      case 'custom':
        // state.scalarData = JSON.parse(JSON.stringify(state.scalar))
        // state.statisticData = JSON.parse(JSON.stringify(state.statistic))
        // state.image = JSON.parse(JSON.stringify(state.imageData))
        // state.audio = JSON.parse(JSON.stringify(state.audioData))
        // state.text = JSON.parse(JSON.stringify(state.textData))
        state.imageData = JSON.parse(JSON.stringify(state.image))
        state.audioData = JSON.parse(JSON.stringify(state.audio))
        state.textData = JSON.parse(JSON.stringify(state.text))
        state.statisticData = JSON.parse(JSON.stringify(state.statistic))
        break
    }
  },
  // 页面跳转时,将定制勾选的最终数据复制给勾选数据
  setRouter: (state, param) => {
    // console.log('setRouter', param)
    switch (param) {
      case 1:
        break
      case 2:
        // state.image = JSON.parse(JSON.stringify(state.imageData))
        // state.audio = JSON.parse(JSON.stringify(state.audioData))
        // state.text = JSON.parse(JSON.stringify(state.textData))
        break
      case 3:
        break
      case 7:
        // for (let i = 0; i < state.imageData.data.length; i++) {
        //   const paramStringIndex = state.imageData.data[i].content.run + '/' + Object.keys(state.imageData.data[i].content.value)[0]
        //   state.imageData.checked[paramStringIndex] = state.imageData.checked[paramStringIndex] = true
        //   state.image = JSON.parse(JSON.stringify(state.imageData))
        // }
        // for (let i = 0; i < state.audioData.data.length; i++) {
        //   const paramStringIndex = state.audioData.data[i].content.run + '/' + Object.keys(state.audioData.data[i].content.value)[0]
        //   state.audioData.checked[paramStringIndex] = state.audio.checked[paramStringIndex] = true
        //   state.audio = JSON.parse(JSON.stringify(state.audioData))
        // }
        // for (let i = 0; i < state.textData.data.length; i++) {
        //   const paramStringIndex = state.textData.data[i].content.run + '/' + Object.keys(state.textData.data[i].content.value)[0]
        //   state.textData.checked[paramStringIndex] = state.text.checked[paramStringIndex] = true
        //   state.text = JSON.parse(JSON.stringify(state.textData))
        // }
    }
  },
  setStatisticMode: (state, param) => {
    state.statisticMode = param
    if (param === '三维') {
      for (let i = 0; i < state.statistic.length; i++) {
        if (state.statistic[i].componentName === 'orthographic') {
          state.statistic[i].componentName = 'threed'
        }
      }
    } else {
      for (let i = 0; i < state.statistic.length; i++) {
        if (state.statistic[i].componentName === 'threed') {
          state.statistic[i].componentName = 'orthographic'
        }
      }
    }
    state.statisticData = JSON.parse(JSON.stringify(state.statistic))
  },
  // setStatisticBinNumber: (state, param) => {
  //   state.statisticBinNumber = param
  // },
  setStatisticShowNumber: (state, param) => {
    state.statisticShowNumber = param
  },
  setScalar: (state, param) => {
    state.scalar[param[0]] = param[1]
    console.log(state.scalar)
  },
  deleteScalar: (state, param) => {
    delete state.scalar[param]
    console.log(state.scalar)
  },
  deleteScalarData: (state, param) => {
    delete state.scalarmid[param]
    state.scalarData = JSON.parse(JSON.stringify(state.scalarmid))
    console.log(state.scalarData)
  },
  cleanScalar: (state) => {
    state.scalar = {}
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
