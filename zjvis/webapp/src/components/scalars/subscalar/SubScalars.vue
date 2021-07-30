/** Copyright 2020 Zhejiang Lab. All Rights Reserved.
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

<style lang="less" scoped>
.scalars-container {
  background-color: #FFF;
  margin-bottom:0.5%;
  .scalars-title {
    height: auto;
    display: flex;
    align-items: center;
    color: white;
    background-color: white;
  }
}
.showClass {
  display: none;
}
.scalarscontent {
  padding: 1% 2% 0 2%;
  background-color: white;
}
    .my-label{
      display:flex;
      width: 100%;
      .triangle{
        position: absolute;
        width: 0px;
        height: 0px;
        overflow: hidden;
        border-top-width: 15px;
        border-bottom-width: 15px;
        border-left-width: 18px;
        border-right-width: 18px;
        border-style: dashed  dashed  dashed solid;
        border-color: transparent transparent   transparent #7f7cc1;
      }
      .triangle-father{
        position: relative;
      }
      .circle-father{
        height: 30px;
        width: 15%;
        position: relative;
        background-color:#7f7cc1;
      }
      .circle{
        position: absolute;
        width:8px;
        height: 8px;
        border-radius: 50%;
        background-color: white;
        left: 50%;
        top: 50%;
        transform: translateX(-50%) translateY(-50%);
      }
      .my-text{
        width: 70%;
        height: 30px;
        text-align: left;
        vertical-align: center;
        background-color:#7f7cc1;
      }
      span{
        align-items: left;
        margin-left: 10%;
        line-height: 30px;
        color:white;
      }
    }
    .sub .triangle{
      border-color: transparent transparent   transparent #b8c6ff;
    }
    .sub .circle-father{
      background-color:#b8c6ff;
    }
    .sub .my-text{
      background-color:#b8c6ff;
    }
    .sub{
      background-size: 100% 100%;
      width: 9.5%;
      height:30px;
      display: flex;
      align-items: center;
      font-family: sans-serif;
      font-size: 12px;
      color: #FFF;
    }
    .sub1{
      background-size: 100% 100%;
      width: 9.5%;
      height:30px;
      display: flex;
      align-items: center;
      font-family: sans-serif;
      font-size: 12px;
      color: #FFF;
    }
.line1 {
  height: 2px;
  width: 88%;
  background-color: #f4f5ff;
}
.line2 {
  height: 5px;
  width:2.5%;
  background-color: #625eb3;
}
.linestyle{
  background-color: #bac6ff;
}
.scalars-title:hover{
  cursor: pointer;
}
</style>
<template>
  <div v-show="subshow" class="scalars-container">
    <div class="scalars-title" @click="showContent()">
      <div :class="[show?'sub':'sub1']">
        <div class="my-label">
          <div class="my-text"><span>{{ info }}</span></div>
          <div class="circle-father"><div class="circle" /></div>
          <div class="triangle-father">
            <div class="triangle" />
          </div>
        </div>
      </div>
      <div class="line1" />
      <div :class="['line2', show?'linestyle':'']" />
    </div>
    <div :class="[show?'showClass':'']">
      <div class="scalarscontent">
        <el-row :gutter="20">
          <scalar-container v-for="item in data" v-show="isshow[item.run]" :key="item.index" :content="item" :subname="subname" />
        </el-row>
      </div>
    </div>
  </div>
</template>
<script>
import { createNamespacedHelpers } from 'vuex'
import { ScalarContainer } from '../scalarcontainer'

const { mapGetters: mapScalarGetters, mapActions: mapScalarActions, mapMutations: mapScalarMutations } = createNamespacedHelpers('scalar')
const { mapGetters: mapLayoutGetters,mapState: mapLayoutStates } = createNamespacedHelpers('layout')
export default {
  components: {
    ScalarContainer
  },
  props: {
    subname: String,
    index: Number,
    value: Array
  },
  data() {
    return {
      data: {},
      show: true,
      isshow: {},
      subshow: true,
      info: ''
    }
  },
  computed: {
    ...mapScalarGetters([
      'detailData', 'categoryInfo', 'initshowrun', 'showFlag', 'subisshow'
    ]),
    ...mapLayoutStates([
      'userSelectRunFile'
    ]),
    ...mapLayoutGetters([
      'getTimer'
    ])
  },
  watch: {
    userSelectRunFile(val) {
      let flag = 1
      for (let i = 0; i < Object.keys(this.isshow).length; i += 1) {
        if (val.indexOf(Object.keys(this.isshow)[i]) > -1) {
          this.isshow[Object.keys(this.isshow)[i]] = true
          flag -= 1
        } else {
          this.isshow[Object.keys(this.isshow)[i]] = false
        }
      }
      if (flag === 1) {
        this.setsubisshow([this.subname, false])
        this.subshow = this.subisshow[this.subname]
      } else {
        this.setsubisshow([this.subname, true])
        this.subshow = this.subisshow[this.subname]
      }
    },
    getTimer: function () {
      this.data = this.detailData[this.subname]
    }
  },
  created() {
    this.info = this.subname
    if (this.info.length > 10) {
      this.info = `${this.info.slice(0, 7)}...`
    }
    this.isshow = this.initshowrun[this.subname]
    if (!(this.subname in this.showFlag)) {
      if (this.index === 0) {
        this.setshowFlag([this.subname, false])
        this.show = this.showFlag[this.subname]
      } else {
        this.setshowFlag([this.subname, true])
        this.show = this.showFlag[this.subname]
      }
    } else {
      this.show = this.showFlag[this.subname]
    }

    if (!this.showFlag[this.subname]) {
      this.getData([this.subname, this.value])
      this.setFreshInfo([this.subname, this.showFlag[this.subname]])
      this.data = this.detailData[this.subname]
    }

    if (!(this.subname in this.subisshow)) {
      this.setsubisshow([this.subname, true])
    } else {
      this.subshow = this.subisshow[this.subname]
    }
  },
  methods: {
    ...mapScalarActions([
      'getData'
    ]),
    ...mapScalarMutations([
      'setDetailData', 'setshowrun', 'back', 'setFreshInfo', 'setshowFlag', 'setsubisshow'
    ]),
    showContent() {
      if (this.showFlag[this.subname]) {
        this.setshowFlag([this.subname, false])
        this.show = this.showFlag[this.subname]
        this.setFreshInfo([this.subname, this.showFlag[this.subname]])
        this.getData([this.subname, this.value])
        this.data = this.detailData[this.subname]
      } else {
        this.setshowFlag([this.subname, true])
        this.show = this.showFlag[this.subname]
        this.setFreshInfo([this.subname, this.showFlag[this.subname]])
      }
    }
    
  }
}
</script>
