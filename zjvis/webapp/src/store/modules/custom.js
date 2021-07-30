/** Copyright 2020 Tianshu AI Platform. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =============================================================
 */

import http from '@/utils/request'
import port from '@/utils/api'
//  import { param2Obj } from '@/utils/utils'

const state = {
  categoryInfo: '',
  detailData: '',
  clickState: false,
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
  getStatisticShowNumber: (state) => state.statisticShowNumber
}

const actions = {
  // eslint-disable-next-line
  async getSelfCategoryInfo(context, param) {
  },
  async getIntervalSelfCategoryInfo(context, param) {

  },
  // eslint-disable-next-line
  async getData(context, param) {
  },
  // eslint-disable-next-line
  async dynamicGetData(context) {
  },
  async getAudioDataInterval(context, param) {
    await http.useGet(param[1]['content']['port'], param[1]['content']['parameter']).then(res => {
      if (+res.data.code !== 200) {
        context.commit('setErrorMessage', res.data.msg + '_' + new Date().getTime())
        return
      }
      context.commit('setAudioDataInterval', [param[0], param[1], res.data.data])
    })
  },
  async getImageDataInterval(context, param) {
    await http.useGet(param[1]['content']['port'], param[1]['content']['parameter']).then(res => {
      if (+res.data.code !== 200) {
        context.commit('setErrorMessage', res.data.msg + '_' + new Date().getTime())
        return
      }
      context.commit('setImageDataInterval', [param[0], param[1], res.data.data])
    })
  },
  async getTextDataInterval(context, param) {
    await http.useGet(param[1]['content']['port'], param[1]['content']['parameter']).then(res => {
      if (+res.data.code !== 200) {
        context.commit('setErrorMessage', res.data.msg + '_' + new Date().getTime())
        return
      }
      context.commit('setTextDataInterval', [param[0], param[1], res.data.data])
    })
  },
  async getHistDataInterval(context, param) {
    await http.useGet(port.category.histogram, { run: param.run, tag: param.tag })
      .then(res => {
        if (Number(res.data.code) !== 200) {
          context.commit('setErrorMessage', param.run + ',' + param.tag + ',' + res.data.msg)
          return
        }
        context.commit('manageHistData', { data: res.data.data[param.tag], index: param.index })
      })
  },
  async getDistDataInterval(context, param) {
    await http.useGet(port.category.distribution,
      { run: param.run, tag: param.tag })
      .then(res => {
        if (Number(res.data.code) !== 200) {
          context.commit('setErrorMessage', param.run + ',' + param.tag + ',' + res.data.msg)
          return
        }
        context.commit('manageDistData', { data: res.data.data[param.tag], index: param.index }) // 处理，然后存储下来
      })
  },
  async getStatisticDataInterval(context, param) {
    const featchParam = { run: param[1].ttlabel, tag: param[1].tag, index: param[0] }
    if (param[1].componentName === 'threed' || param[1].componentName === 'orthographic') {
      context.dispatch('getHistDataInterval', featchParam)
    } else {
      context.dispatch('getDistDataInterval', featchParam)
    }
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
  setAudioDataInterval: (state, param) => {
    param[1]['content']['value'] = param[2]
    state.audio[param[0]] = param[1]
  },
  setImageDataInterval: (state, param) => {
    param[1]['content']['value'] = param[2]
    state.image[param[0]] = param[1]
  },
  setTextDataInterval: (state, param) => {
    param[1]['content']['value'] = param[2]
    state.text[param[0]] = param[1]
  },
  setAudioData: (state, param) => {
    const paramStringIndex = `${param.content.run}/${Object.keys(param.content.value)[0]}`
    let flag = true
    for (let i = 0; i < state.audio.length; i += 1) {
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
      state.audio.push({
        stringIndex: paramStringIndex,
        checked: param.checked,
        content: param.content
      })
    }
  },
  setTextData: (state, param) => {
    const paramStringIndex = `${param.content.run}/${Object.keys(param.content.value)[0]}`
    let flag = true
    for (let i = 0; i < state.text.length; i += 1) {
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
      state.text.push({
        stringIndex: paramStringIndex,
        checked: param.checked,
        content: param.content
      })
    }
  },
  setImageData: (state, param) => {
    const paramStringIndex = `${param.content.run}/${Object.keys(param.content.value)[0]}`
    let flag = true
    for (let i = 0; i < state.image.length; i += 1) {
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
      state.image.push({
        stringIndex: paramStringIndex,
        checked: param.checked,
        content: param.content
      })
    }
  },
  setStatisticData: (state, param) => {
    let flag = -1
    for (let i = 0; i < state.statistic.length; i += 1) {
      if (
        state.statistic[i].ttlabel === param.ttlabel &&
        state.statistic[i].tag === param.tag &&
        (state.statistic[i].componentName === param.componentName ||
          param.componentName === 'threed' ||
          param.componentName === 'orthographic')
      ) {
        if (!param.delete) {
          state.statistic.splice(i, 1)
        } else {
          state.statistic.splice(i, 1)
          state.statisticData = state.statistic
        }
        if (!state.statisticData.length) {
          state.statisticMode = '三维'
          state.statisticShowNumber = 10
        }
        flag = 1
        break
      }
    }
    if (flag === -1) {
      if (param.itemp < 1000) param.itemp = 1000 + param.itemp
      param.divId = `custom${param.componentName}${param.itemp}`
      if (state.statisticMode === '三维' && param.componentName === 'orthographic') {
        param.componentName = 'threed'
      } else if (state.statisticMode === '二维' && param.componentName === 'threed') {
        param.componentName = 'orthographic'
      }
      state.statistic.push(param)
    }
  },
  setData: (state, param) => {
    // eslint-disable-next-line
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
        state.statisticData = JSON.parse(JSON.stringify(state.statistic))
        break
      case 'custom':
        state.imageData = JSON.parse(JSON.stringify(state.image))
        state.audioData = JSON.parse(JSON.stringify(state.audio))
        state.textData = JSON.parse(JSON.stringify(state.text))
        state.statisticData = JSON.parse(JSON.stringify(state.statistic))
        break
    }
  },
  setRouter: (state, param) => {
    // eslint-disable-next-line
    switch (param) {
      case 1:
        break
      case 2:
        break
      case 3:
        break
      case 7:
    }
  },
  setStatisticMode: (state, param) => {
    state.statisticMode = param
    if (param === '三维') {
      for (let i = 0; i < state.statistic.length; i += 1) {
        if (state.statistic[i].componentName === 'orthographic') {
          state.statistic[i].componentName = 'threed'
        }
      }
    } else {
      for (let i = 0; i < state.statistic.length; i += 1) {
        // eslint-disable-next-line
        if (state.statistic[i].componentName === 'threed') {
          // eslint-disable-next-line
          state.statistic[i].componentName = 'orthographic';
        }
      }
    }
    state.statisticData = JSON.parse(JSON.stringify(state.statistic))
  },
  setStatisticShowNumber: (state, param) => {
    state.statisticShowNumber = param
  },
  setScalar: (state, param) => {
    // eslint-disable-next-line
    state.scalar[param[0]] = param[1]
  },
  deleteScalar: (state, param) => {
    delete state.scalar[param]
  },
  deleteScalarData: (state, param) => {
    delete state.scalarmid[param]
    state.scalarData = JSON.parse(JSON.stringify(state.scalarmid))
  },
  cleanScalar: (state) => {
    state.scalar = {}
  },
  manageDistData: (state, param) => {
    const oneData = param.data
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
    const newStatisticData = JSON.parse(JSON.stringify(state.statisticData[param.index]))
    newStatisticData.data = newData
    state.statisticData.splice(param.index, 1, newStatisticData)
  },
  manageHistData: (state, param) => {
    const data = param.data
    const newdata = []
    let min = 1000
    let max = -1000
    for (let i = 0; i < data.length; i++) {
      if (min > data[i][2]) min = data[i][2]
      if (max < data[i][3]) max = data[i][3]
    }
    // 默认
    const binNum = 30
    const binWidth = (max - min) / binNum
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
      for (let j = 0; j < binNum; j++) {
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
    const newStatisticData = JSON.parse(JSON.stringify(state.statisticData[param.index]))
    newStatisticData.data = newdata
    state.statisticData.splice(param.index, 1, newStatisticData)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
