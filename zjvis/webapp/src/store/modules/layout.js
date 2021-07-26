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
import constants from '@/utils/constants'

const state = {
  stateStore: {},
  category: [],
  initShowPanel: '',
  initSidebarId: '',
  categoryIndex: '',
  runFileCategory: '',
  userSelectRunFile: '',
  runCategoryDetail: '',
  multipleFlag: '',
  svgDownloadList: [],
  subCategoryTimerId: null,
  initWaitingMessage: '',
  timeSyncInterval: false,
  errorMessage: '',
  params: {
    id: '',
    trainJobName: ''
  }
}

const getters = {
  allCategoryInform: (state) => state.category,
  initShowPanelInfo: (state) => state.initShowPanel,
  initRunFile: (state) => state.runFileCategory,
  initWaitingMessage: (state) => state.initWaitingMessage,
  getParams: (state) => state.params,
  getErrorMessage: (state) => state.errorMessage,
  setDownloadSvgClass: (state) => state.svgDownloadList,
  getStateStore: (state) => state.stateStore,
  getTimer: (state) => state.timeSyncInterval
}

const actions = {
  async initWaitingPage(context, params) {
    await http.useGet('/api/init', params)
      .then((res) => {
        context.commit('setCookie', 'session_id', res.data.data['session_id'])
        context.commit('setWaitingMessage', res.data.data['msg'])
      })
  },
  async initFeatchCategory(context, path) {
    const splitArray = path.split('/')
    const cate = splitArray[splitArray.length - 1]
    await http.useGet(port.manage.initCategory, {}).then((res) => {
      const dataCategoryInfo = res.data.data
      let categorys = []
      const runFile = []
      const categoryToRunFile = {} // 根据所选类目显示run信息
      Object.keys(dataCategoryInfo).forEach((val) => {
        categorys = categorys.concat(
          Object.keys(dataCategoryInfo[val]).filter((v) => !categorys.includes(v))
        )
        runFile.push(val)
      })
      const categoryOrder = []
      categorys.forEach((val) => {
        categoryOrder.push(constants.CATEGORYORDER.indexOf(val))
      })
      categoryOrder.sort()
      let newIndex = 0
      if (cate === 'index') {
        newIndex = 0
      } else {
        newIndex = categoryOrder.indexOf(constants.CATEGORYORDER.indexOf(cate))
      }
      if (categorys.length !== 0) {
        categorys.forEach((ce) => {
          const detailTag = []
          const tempRunFile = []
          const temp = []
          runFile.forEach((res) => {
            if (dataCategoryInfo[res].hasOwnProperty(ce)) {
              tempRunFile.push(res)
              detailTag.push(dataCategoryInfo[res][ce])
              temp.push(res)
            }
            categoryToRunFile[ce] = temp
          })
          if (ce === constants.CATEGORYORDER[categoryOrder[0]] && cate === 'index') {
            context.dispatch(
              `${ce}/getSelfCategoryInfo`,
              [tempRunFile, detailTag, { initStateFlag: true }],
              { root: true }
            )
          } else if (ce === cate) {
            context.dispatch(
              `${ce}/getSelfCategoryInfo`,
              [tempRunFile, detailTag, { initStateFlag: true }],
              { root: true }
            )
          } else {
            context.dispatch(
              `${ce}/getSelfCategoryInfo`,
              [tempRunFile, detailTag, { initStateFlag: false }],
              { root: true }
            )
          }
        })
      } else {
        context.commit(
          'setErrorMessage',
          `${'日志文件中尚未发现可展示信息！_'}${new Date().getTime()}`
        )
      }
      context.commit('setRunCategoryDetail', categoryToRunFile)
      context.commit('setCategory', [categoryOrder, newIndex])
      context.commit('setRunCategory', constants.CATEGORYORDER[categoryOrder[newIndex]])
    })
  },
  async featchCategory(context, path) {
    const splitArray = path.split('/')
    const cate = splitArray[splitArray.length - 1]
    await http.useGet(port.manage.initCategory, {}).then((res) => {
      const dataCategoryInfo = res.data.data
      let categorys = []
      const runFile = []
      const categoryToRunFile = {} // 根据所选类目显示run信息
      Object.keys(dataCategoryInfo).forEach((val) => {
        categorys = categorys.concat(
          Object.keys(dataCategoryInfo[val]).filter((v) => !categorys.includes(v))
        )
        runFile.push(val)
      })
      const categoryOrder = []
      categorys.forEach((val) => {
        categoryOrder.push(constants.CATEGORYORDER.indexOf(val))
      })
      categoryOrder.sort()
      let newIndex = 0
      if (cate === 'index') {
        newIndex = 0
      } else {
        newIndex = categoryOrder.indexOf(constants.CATEGORYORDER.indexOf(cate))
      }
      if (categorys.length !== 0) {
        categorys.forEach((ce) => {
          const detailTag = []
          const tempRunFile = []
          const temp = []
          runFile.forEach((res) => {
            if (dataCategoryInfo[res].hasOwnProperty(ce)) {
              tempRunFile.push(res)
              detailTag.push(dataCategoryInfo[res][ce])
              temp.push(res)
            }
            categoryToRunFile[ce] = temp
          })
          // if (ce === constants.CATEGORYORDER[categoryOrder[0]] && cate === 'index') {
          //   context.dispatch(
          //     `${ce}/getSelfCategoryInfo`,
          //     [tempRunFile, detailTag, { initStateFlag: true }],
          //     { root: true }
          //   )
          // } else if (ce === cate) {
          //   context.dispatch(
          //     `${ce}/getSelfCategoryInfo`,
          //     [tempRunFile, detailTag, { initStateFlag: true }],
          //     { root: true }
          //   )
          // } else {
          //   context.dispatch(
          //     `${ce}/getSelfCategoryInfo`,
          //     [tempRunFile, detailTag, { initStateFlag: false }],
          //     { root: true }
          //   )
          // }
        })
      } else {
        context.commit(
          'setErrorMessage',
          `${'日志文件中尚未发现可展示信息！_'}${new Date().getTime()}`
        )
      }
      context.commit('setRunCategoryDetail', categoryToRunFile)
      context.commit('setCategory', [categoryOrder, newIndex])
      context.commit('setRunCategory', constants.CATEGORYORDER[categoryOrder[newIndex]])
    })
  },
  async timingFeatchCategory(context, parm) {
    // parm 存储间隔时间
    const splitArray = parm[1].split('/')
    const cate = splitArray[splitArray.length - 1]
    const t = setInterval(async() => {
      http.useGet(port.manage.initCategory, { test: 1 }).then((res) => {
        const dataCategoryInfo = res.data.data
        let categorys = []
        const runFile = []
        const categoryToRunFile = {}
        Object.keys(dataCategoryInfo).forEach((val) => {
          categorys = categorys.concat(
            Object.keys(dataCategoryInfo[val]).filter((v) => !categorys.includes(v))
          )
          runFile.push(val)
        })
        const categoryOrder = []
        categorys.forEach((val) => {
          categoryOrder.push(constants.CATEGORYORDER.indexOf(val))
        })
        categoryOrder.sort()
        let newIndex = 0
        if (cate === 'index') {
          newIndex = 0
        } else {
          newIndex = categoryOrder.indexOf(constants.CATEGORYORDER.indexOf(cate))
        }
        if (categorys.length !== 0) {
          categorys.forEach((ce) => {
            const detailTag = []
            const tempRunFile = []
            const temp = []
            runFile.forEach((res) => {
              if (dataCategoryInfo[res].hasOwnProperty(ce)) {
                tempRunFile.push(res)
                detailTag.push(dataCategoryInfo[res][ce])
                temp.push(res)
              }
              categoryToRunFile[ce] = temp
            })
            if (ce === constants.CATEGORYORDER[categoryOrder[0]] && cate === 'index') {
              context.dispatch(
                `${ce}/getSelfCategoryInfo`,
                [tempRunFile, detailTag, { initStateFlag: true }],
                { root: true }
              )
            } else if (ce === cate) {
              context.dispatch(
                `${ce}/getSelfCategoryInfo`,
                [tempRunFile, detailTag, { initStateFlag: true }],
                { root: true }
              )
            } else {
              context.dispatch(
                `${ce}/getSelfCategoryInfo`,
                [tempRunFile, detailTag, { initStateFlag: false }],
                { root: true }
              )
            }
          })
        } else {
          context.commit(
            'setErrorMessage',
            `${'日志文件中尚未发现可展示信息！_'}${new Date().getTime()}`
          )
        }
        context.commit('setRunCategoryDetail', categoryToRunFile)
        context.commit('setCategory', [categoryOrder, newIndex])
        context.commit('setRunCategory', constants.CATEGORYORDER[categoryOrder[newIndex]])
      })
    }, parm[0])
    context.commit('setSyncTime', t)
  },
  async timingFeatchCategoryOnce(context, parm) {
    const splitArray = parm.split('/')
    const cate = splitArray[splitArray.length - 1]
    await http.useGet(port.manage.initCategory, {}).then((res) => {
      const dataCategoryInfo = res.data.data
      let categorys = []
      const runFile = []
      const categoryToRunFile = {}
      Object.keys(dataCategoryInfo).forEach((val) => {
        categorys = categorys.concat(
          Object.keys(dataCategoryInfo[val]).filter((v) => !categorys.includes(v))
        )
        runFile.push(val)
      })
      const categoryOrder = []
      categorys.forEach((val) => {
        categoryOrder.push(constants.CATEGORYORDER.indexOf(val))
      })
      categoryOrder.sort()
      let newIndex = 0
      if (cate === 'index') {
        newIndex = 0
      } else {
        newIndex = categoryOrder.indexOf(constants.CATEGORYORDER.indexOf(cate))
      }
      if (categorys.length !== 0) {
        categorys.forEach((ce) => {
          const detailTag = []
          const tempRunFile = []
          const temp = []
          runFile.forEach((res) => {
            if (dataCategoryInfo[res].hasOwnProperty(ce)) {
              tempRunFile.push(res)
              detailTag.push(dataCategoryInfo[res][ce])
              temp.push(res)
            }
            categoryToRunFile[ce] = temp
          })
          if (ce === constants.CATEGORYORDER[categoryOrder[0]] && cate === 'index') {
            context.dispatch(
              `${ce}/getSelfCategoryInfo`,
              [tempRunFile, detailTag, { initStateFlag: true }],
              { root: true }
            )
          } else if (ce === cate) {
            context.dispatch(
              `${ce}/getSelfCategoryInfo`,
              [tempRunFile, detailTag, { initStateFlag: true }],
              { root: true }
            )
          } else {
            context.dispatch(
              `${ce}/getSelfCategoryInfo`,
              [tempRunFile, detailTag, { initStateFlag: false }],
              { root: true }
            )
          }
        })
      } else {
        context.commit(
          'setErrorMessage',
          `${'日志文件中尚未发现可展示信息！_'}${new Date().getTime()}`
        )
      }
      context.commit('setRunCategoryDetail', categoryToRunFile)
      context.commit('setCategory', [categoryOrder, newIndex])
      context.commit('setRunCategory', constants.CATEGORYORDER[categoryOrder[newIndex]])
    })
  },
  async getClickState(context, parm) {
    context.state.categoryIndex.forEach((value) => {
      const el = constants.CATEGORYORDER[value]
      if (value === parm) {
        context.commit(`${el}/setClickState`, true, { root: true })
      } else {
        context.commit(`${el}/setClickState`, false, { root: true })
      }
    })
  }
}

const mutations = {
  setParams: (state, params) => {
    state.params = params
  },
  setCookie: (state, name, value) => {
    const days = 14
    const exp = new Date()
    exp.setTime(exp.getTime() + days * 24 * 60 * 60 * 1000)
    document.cookie = `${name}=${escape(value)};expires=${exp.toGMTString()}; path=/`
  },
  setCategory: (state, value) => {
    // eslint-disable-next-line
    state.categoryIndex = value[0];
    const CategoryInfomation = []
    Array.from(value[0]).forEach((order, index) => {
      CategoryInfomation.push({
        id: index,
        rawName: constants.CATEGORYORDER[order],
        routerName: '/index/' + constants.CATEGORYORDER[order],
        name: constants.CATEGORY[order][3],
        nameCopy: constants.CATEGORY[order][3],
        icon: constants.CATEGORY[order][4],
        iconCopy: constants.CATEGORY[order][4]
      })
    })
    state.category = CategoryInfomation
    // eslint-disable-next-line
    state.initSidebarId = value[1];
    if (state.initShowPanel !== CategoryInfomation[value[1]]) {
      state.initShowPanel = CategoryInfomation[value[1]]
    }
    const download = {}
    state.category.forEach((val) => {
      download[val.rawName] = []
      if (val.rawName === 'graph') {
        download.graph.push('#svg-canvas')
      }
    })
    // console.log(state.category)
    state.svgDownloadList = download
  },
  setSyncTime: (state) => {
    state.timeSyncInterval = !state.timeSyncInterval
  },
  clearSync: (state) => {
    clearInterval(state.timeSyncInterval)
  },
  setWaitingMessage: (state, value) => {
    state.initWaitingMessage = value
  },
  setRunCategory: (state, value) => {
    let detailInfo = []
    let initOption = []
    let temp = ''
    state.runCategoryDetail[value].forEach((val, i) => {
      detailInfo.push({
        value: val,
        label: val
      })
      if (constants.RUNFILESHOWFlAG[value] === 0) {
        temp = false
        if (i === 0) {
          initOption = val
        }
      } else {
        initOption.push(val)
        temp = true
      }
      if (constants.RUNFILESHOWFlAG[value] === 2) {
        detailInfo = []
        initOption = []
        temp = 2
      }
    })
    if (value in state.stateStore) {
      state.userSelectRunFile = state.stateStore[value]
    } else {
      state.stateStore[value] = initOption
      state.userSelectRunFile = initOption
    }
    state.runFileCategory = detailInfo
    // console.log(state.runFileCategory)
    state.multipleFlag = temp
  },
  setUserSelectRunFile: (state, value) => {
    state.userSelectRunFile = value
  },
  setRunCategoryDetail: (state, value) => {
    // console.log(value)
    state.runCategoryDetail = value
  },
  setTimer: (state) => {
    state.timeSyncInterval = !state.timeSyncInterval
    // console.log(state.timeSyncInterval)
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
