<!--
 * @Descripttion: loss
 * @version: 1.0
 * @Author: xds
 * @Date: 2020-04-24 15:23:44
 * @LastEditors: xds
 * @LastEditTime: 2020-05-20 11:53:07
 -->
 <style lang="less" scoped>
  .scalarcontainer{
    width: 100%;
    height: 100%;
    background-color: white;
  }
  .scalarContainerTitle, .scalarContainerTitleLarge{
    color: white;
    background-color: #9FA5FA;
    text-align: left;
    padding: 0% 2% 0 2%;
    border-radius:2px;
    display:flex;
    height: 30px;
    line-height: 30px;
    .scale:hover{
      cursor: pointer;
    }
    .titleRight{
      margin-left: auto;
      margin-right: 1%;
    }
  }
  .scalarContainerTitle{
    font-size: 11px;
    .iconfont{
      font-size: 11px;
    }
  }
  .scalarContainerTitleLarge {
    font-size: 16px;
    .iconfont{
      font-size: 16px;
    }
  }
  .el-col {
    margin-bottom: 20px;
  }
</style>
<template>
  <div v-show="isshow[chartgrade]" class="scalarcontainer">
    <el-col :span="size">
      <el-card :body-style="{ padding: '0px' }" class="box-card">
        <div :class="[scaleLargeSmall?'scalarContainerTitleLarge':'scalarContainerTitle']">
          <div>
            <span class="tagShow">{{ info }}</span>
          </div>
          <div class="titleRight">
            <el-tooltip class="item" effect="dark" content="点击可放大此图表" placement="top">
              <span class="scale" @click="sizebig()"><i class="iconfont icon-fangda" /></span>
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="点击可缩小此图表" placement="top">
              <span class="scale" @click="sizesmall()"><i class="iconfont icon-suoxiao1" /></span>
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="勾选图表参与合并，或选中后点击定制按钮会跳转到用户定制界面" placement="top">
              <span class="scale"><i :class="['iconfont',chartchecked?'icon-xuanzhong1':'icon-weixuanzhong1']" @click="ischecked()" /></span>
            </el-tooltip>
          </div>
        </div>
        <scalarchart
          :chartdata="chartdata"
          :start="start"
          :end="end"
          :ytext="ytext"
          :scaleLargeSmall="scaleLargeSmall"
          :classname="classname"
          :isaddmain="isaddmain"
          :title="id"
        />
      </el-card>
    </el-col>
  </div>
</template>
<script>
import { Scalarchart } from './scalarchart'
import { createNamespacedHelpers } from 'vuex'
const { mapMutations: mapScalarMutations, mapGetters: mapScalarGetters } = createNamespacedHelpers('scalar')
const { mapMutations: mapCustomMutations, mapGetters: mapCustomGetters } = createNamespacedHelpers('custom')
const { mapGetters: mapLayoutGetters } = createNamespacedHelpers('layout')
export default {
  components: {
    Scalarchart
  },
  props: {
    content: Object,
    subname: String
  },
  data() {
    return {
      scaleLargeSmall: false,
      size: 8,
      ytext: '',
      thisitem: {},
      isshow: { 'main': true, 'subordinate': false, 'general': true, 'undefined': true },
      start: false,
      end: false,
      chartchecked: false,
      chartgrade: 'general',
      info: '',
      id: '',
      chartdata: { 'run': '', 'value': {}},
      classname: '',
      isaddmain: false
    }
  },
  computed: {
    ...mapScalarGetters([
      'checkeditem',
      'startmerged',
      'endmerged',
      'mergestep',
      'checkedorder',
      'mergednumber',
      'backednumber',
      'getDownLoadArray',
      'grade',
      'mergedorder',
      'checked',
      'mergeditem'
    ]),
    ...mapCustomGetters([
      'getScalar'
    ]),
    ...mapLayoutGetters([
      'setDownloadSvgClass'
    ])
  },
  watch: {
    mergestep: function(val) {
      if (val === this.checkedorder.length && val !== 0 && this.mergedorder[this.classname] === this.mergednumber && this.grade[this.classname] === 'main') {
        this.setdatainit()
      }
    },
    startmerged: function(val) {
      if (val) {
        if (this.checkedorder.indexOf(this.classname) > 0) {
          this.setgrade([this.classname, 'subordinate'])
          this.chartgrade = this.grade[this.classname]
          this.setmergedorder([this.classname, this.mergednumber])
          this.setmergestep()
          this.setchecked([this.classname, false])
          this.deleteScalar(this.id)
          this.chartchecked = this.checked[this.classname]
        } else if (this.classname === this.checkedorder[0]) {
          this.setgrade([this.classname, 'main'])
          this.chartgrade = this.grade[this.classname]
          this.setmergedorder([this.classname, this.mergednumber])
          this.deleteScalar(this.id)
          this.start = val
          this.setchecked([this.classname, false])
          this.chartchecked = this.checked[this.classname]
        }
      }
    },
    endmerged: function(val) {
      if (val && this.backednumber.indexOf(this.mergedorder[this.classname]) > -1) {
        if (this.grade[this.classname] === 'main') {
          this.end = val
          this.reducemergeditem(this.classname)
        }
        this.setgrade([this.classname, 'general'])
        this.chartgrade = this.grade[this.classname]
        this.setmergedorder([this.classname, 1000])
        this.setchecked([this.classname, false])
        this.chartchecked = this.checked[this.classname]
      }
    }
  },
  created() {
    const content = this.content.value[Object.keys(this.content.value)[0]]
    this.chartdata.run = this.content.run
    this.chartdata.value[Object.keys(this.content.value)[0]] = []
    if (content.length > 1000) {
      const n = Math.ceil(content.length / 1000)
      for (let i = 0; i < content.length; i = i + n) {
        this.chartdata.value[Object.keys(this.content.value)[0]].push(content[i])
      }
    } else {
      this.chartdata.value = this.content.value
    }
    this.id = this.chartdata.run + ' ' + Object.keys(this.chartdata.value)[0]
    this.info = this.id
    if (this.info.length > 20) {
      this.info = this.info.slice(0, 17) + '...'
    }
    const arr = Object.keys(this.chartdata.value)[0].split('/')
    this.ytext = arr[arr.length - 1]
    this.classname = this.chartdata.run.replace(/\//g, '').replace(/\./g, '') + Object.keys(this.chartdata.value)[0].replace(/\//g, '').replace(/\./g, '')
    this.thisitem.run = this.chartdata.run
    this.thisitem.tag = Object.keys(this.chartdata.value)[0]
    this.thisitem.value = this.chartdata.value[Object.keys(this.chartdata.value)[0]]
    if (!(this.classname in this.checked)) {
      this.setchecked([this.classname, false])
    }
    this.chartchecked = this.checked[this.classname]
    if (!(this.classname in this.grade)) {
      this.setgrade([this.classname, 'general'])
    }
    if (!(this.classname in this.mergedorder)) {
      this.setmergedorder([this.classname, 1000])
    }
  },
  mounted: function() {
    this.chartgrade = this.grade[this.classname]
  },
  methods: {
    ...mapScalarMutations([
      'setcheckeditem',
      'deletecheckeditem',
      'setdatainit',
      'setmergestep',
      'addcheckedorder',
      'reducecheckedorder',
      'addbackednumber',
      'reducebackednumber',
      'deleteDownLoadArray',
      'setDownLoadArray',
      'setgrade',
      'setmergedorder',
      'setchecked',
      'reducemergeditem'
    ]),
    ...mapCustomMutations([
      'setScalar', 'deleteScalar'
    ]),
    sizebig() {
      this.size = 24
      this.info = this.id
      this.scaleLargeSmall = true
    },
    sizesmall() {
      this.size = 8
      this.scaleLargeSmall = false
      if (this.info.length > 20) {
        this.info = this.info.slice(0, 17) + '...'
      }
    },
    ischecked() {
      if (this.checked[this.classname]) {
        this.setchecked([this.classname, false])
        this.chartchecked = this.checked[this.classname]
        this.deleteDownLoadArray('#svg' + this.classname)
        this.setDownloadSvgClass['scalar'] = this.getDownLoadArray
        if (this.grade[this.classname] === 'general') {
          this.deleteScalar(this.id)
          this.reducecheckedorder(this.classname)
          this.deletecheckeditem([this.ytext, this.thisitem])
        } else if (this.grade[this.classname] === 'main') {
          this.reducebackednumber(this.mergedorder[this.classname])
          this.isaddmain = false
        }
      } else {
        this.setchecked([this.classname, true])
        this.chartchecked = this.checked[this.classname]
        this.start = false
        this.end = false
        this.setDownLoadArray('#svg' + this.classname)
        this.setDownloadSvgClass['scalar'] = this.getDownLoadArray
        if (this.grade[this.classname] === 'general') {
          this.setScalar([this.id, this.content])
          this.addcheckedorder(this.classname)
          this.setcheckeditem([this.ytext, this.thisitem])
        } else if (this.grade[this.classname] === 'main') {
          this.addbackednumber(this.mergedorder[this.classname])
          this.isaddmain = true
        }
      }
    }
  }
}
</script>
