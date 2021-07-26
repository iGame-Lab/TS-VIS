<template>
  <div class="embeddingpanel">
    <div class="panel">
      <el-card class="father">
        <div class="info">
          <div class="infoTitle">
            <span i class="iconfont icon-ziyuan40">&nbsp;&nbsp;控制面板</span>
          </div>
          <div class="infoContent">
            <div class="infoItem">
              <el-row type="flex" justify="space-between">
                <el-col :span="8">
                  <div>
                    <span class="midFont">标&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;签</span>
                  </div>
                </el-col>
                <el-col :span="16">
                  <div class="center">
                    <el-select
                      v-model="curTag"
                      class="tagSelect histmodeselect"
                      size="small"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(item,index) in curTags"
                        :key="index"
                        :value="item"
                        :label="item"
                      />
                    </el-select>
                  </div>
                </el-col>
              </el-row>
            </div>
            <div class="infoItem">
              <el-row type="flex" justify="space-between">
                <el-col :span="8">
                  <div>
                    <span>降维方法</span>
                  </div>
                </el-col>
                <el-col :span="16">
                  <div class="center">
                    <el-select
                      v-model="curMethod"
                      class="tagSelect histmodeselect"
                      size="small"
                    >
                      <el-option
                        v-for="item in allMethods"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                      />
                    </el-select>
                  </div>
                </el-col>
              </el-row>
            </div>
            <div class="infoItem">
              <el-row type="flex" justify="space-between">
                <el-col :span="8">
                  <div>
                    <span>维度选择</span>
                  </div>
                </el-col>
                <el-col :span="16">
                  <div class="center">
                    <el-select
                      v-model="curDim"
                      class="tagSelect histmodeselect"
                      size="small"
                    >
                      <el-option
                        v-for="(item,index) in allDims"
                        :key="index"
                        :value="item"
                        :label="item"
                      />
                    </el-select>
                  </div>
                </el-col>
              </el-row>
            </div>
            <div v-if="getReceivedQuestionInfo && getReceivedCurInfo" class="infoItem">
              <el-row type="flex" justify="space-around" class="row-bg">
                <el-col :span="6">
                  <el-button
                    :icon="playAction ? 'iconfont icon-zanting':'iconfont icon-ziyuan74'"
                    background-color="#736FBC"
                    type="primary"
                    size="medium"
                    @click="playActionClick()"
                  />
                </el-col>
                <el-col :span="12">
                  <el-slider
                    v-model="curStep"
                    :min="curMin"
                    :max="curMapMax"
                    :disabled="curMapMax===0"
                    :show-tooltip="false"
                    input-size="small"
                    class="rangeNumber"
                  />
                </el-col>
                <el-col :span="6">
                  <div class="grid-content">
                    <span text-align="center" class="midFont">{{ curMapStep }}/{{ curMax }}</span>
                  </div>
                </el-col>
              </el-row>
            </div>
            <div v-if="parseInt(curDim) > 3" class="infoItem ProbabilityDensitySec">
              <span class="ProbabilityDensity">概率密度</span>
              <hr>
              <el-checkbox-group v-model="checkedLabels" :max="2" class="leftInline-block">
                <el-checkbox v-for="(item,index) in lableTypes" :key="item" :label="item" :class="'checkboxx'+index">{{ item }}</el-checkbox>
              </el-checkbox-group>
            </div>
            <div v-if="parseInt(curDim) > 3" class="infoItem">
              <el-row type="flex" justify="space-around" class="row-bg">
                <el-col :span="6">
                  <span style="line-height:38px">线条宽度</span>
                </el-col>
                <el-col :span="12">
                  <el-slider
                    v-model="curLineWidth"
                    :min="0.4"
                    :max="2.0"
                    :show-tooltip="false"
                    :step="0.1"
                    input-size="small"
                    class="rangeNumber"
                  />
                </el-col>
                <el-col :span="6">
                  <div class="grid-content">
                    <span text-align="center" class="midFont">{{ curLineWidth.toFixed(1) }} / 2.0</span>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>
        </div>
      </el-card>
      <el-card class="father">
        <div class="info">
          <div class="infoTitle">
            <span i class="iconfont icon-ziyuan41">&nbsp;&nbsp;数据信息栏</span>
          </div>
          <div class="infoContent">
            <div class="infoItem">
              <div v-if="getMessage == ''">
                <span>暂无信息</span>
              </div>
              <el-card v-if="getMessage != ''" :body-style="{ padding: '0px' }" class="infoCard" display="none">
                <div v-if="getQuestionInfo[userSelectRunFile][getCurInfo.curTag]['sample']" class="showBox">
                  <!-- <img v-if="getQuestionInfo[userSelectRunFile][getCurInfo.curTag]['sample_type'] == 'image' && getMessage != ''" :src="getMessage[0]+'&trainJobName='+getParams.trainJobName" class="image"> -->
                  <!-- <AudioContainer v-if="getQuestionInfo[userSelectRunFile][getCurInfo.curTag]['sample_type'] == 'audio' && getMessage != ''" :theUrl="getMessage[0]+'&trainJobName='+getParams.trainJobName" theControlList="noMuted noSpeed onlyOnePlaying" :index="1000" /> -->
                  <div v-if="getQuestionInfo[userSelectRunFile][getCurInfo.curTag]['sample_type'] == 'text' && getMessage != ''" class="image">
                    <el-scrollbar style="height: 100%">
                      <p>{{ getPanelSampleData["url"] }}</p>
                    </el-scrollbar>
                  </div>
                  <div v-if="getQuestionInfo[userSelectRunFile][getCurInfo.curTag]['sample_type'] == 'image' && getMessage != ''" class="image">
                    <!-- <el-scrollbar style="height: 100%"> -->
                      <el-image
                        :src="getPanelSampleData['url']"
                        :preview-src-list="[getPanelSampleData['url']]"
                        class="image"
                      />
                    <!-- </el-scrollbar> -->
                  </div>
                  <div v-if="getQuestionInfo[userSelectRunFile][getCurInfo.curTag]['sample_type'] == 'audio' && getMessage != ''" class="image">
                    <el-scrollbar style="height: 100%">
                      <AudioContainer
                        v-if="getQuestionInfo[userSelectRunFile][getCurInfo.curTag]['sample_type'] == 'audio' && getMessage != ''"
                        :theUrl="getPanelSampleData['url']"
                        :index="1000"
                        theControlList="noMuted noSpeed onlyOnePlaying"
                      />
                    </el-scrollbar>
                  </div>
                </div>
                <div style="padding: 14px;" class="imageSpan">
                  <span>{{ getMessage[1] }}</span>
                </div>
              </el-card>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
// import * as d3 from 'd3'
import { createNamespacedHelpers } from 'vuex'
const {
  mapGetters: mapEmbeddingGetters,
  mapMutations: mapEmbeddingMutations,
  mapActions: mapEmbeddingActions
} = createNamespacedHelpers('embedding')
const { mapState: mapLayoutStates, mapGetters: mapLayoutGetters } = createNamespacedHelpers('layout')
export default {
  components: {
  },
  data() {
    return {
      // ----------------------------- Tag选择 -----------------------------
      curTag: '',
      curTags: [],
      // ----------------------------- method选择 -----------------------------
      curMethod: '',
      allMethods: [{
        value: 'PCA',
        label: 'PCA'
      },
      {
        value: 'TSNE',
        label: 'TSNE'
      }
      ],
      // ----------------------------- 维度信息选择选择 ---------------------
      curDim: '',
      allDims: ['2维', '3维'],
      // ----------------------------- 播放动作 -----------------------------
      playAction: false,
      curStep: 0,
      curMapStep: 0,
      curMin: 0, // 可能稍后赋值同步信息
      curMax: 100,
      curMapMax: 100,
      // ----------------------------- 概率密度 -----------------------------
      checkedLabels: [],
      lableTypes: [],
      curLineWidth: 1
    }
  },
  computed: {
    ...mapEmbeddingGetters([
      'getCurInfo',
      'getCategoryInfo',
      'getQuestionInfo',
      'getReceivedCategoryInfo',
      'getReceivedCurInfo',
      'getReceivedQuestionInfo',
      'getCurData',
      'getReceivedCurData',
      'getPanelSampleData',
      'getMessage',
      'getInitStateFlag',
      'getErrorMessage',
      'getLineWidth'
    ]),
    ...mapLayoutStates([
      'userSelectRunFile'
    ]),
    ...mapLayoutGetters(['getParams', 'getTimer'])
  },
  watch: {
    curLineWidth: function() {
      this.setLineWidth(this.curLineWidth)
    },
    getReceivedCurInfo: function() { // 只触发一次第一次
      console.log(269)
      if(this.getReceivedCurInfo == false) return
      if (this.userSelectRunFile === '') {
        return
      }
      this.setCurInfo(['received', false]) // 屏蔽别的请求
      for (let i = 0; i < this.getCategoryInfo.curRuns.length; i++) {
        if (this.userSelectRunFile === this.getCategoryInfo.curRuns[i]) {
          this.curTags = this.getCategoryInfo.curTags[i].slice(0)
        }
      }
      let index = this.curTags.indexOf(this.curTag);
      if(index < 0 || this.curTag == '')  {
        this.curTag = this.curTags[0]
        this.curStep = this.getCurInfo.curStep
      }
      this.curMethod = this.getCurInfo.curMethod
      this.curDim = this.getCurInfo.curDim
      
      this.curMax = this.getQuestionInfo[this.userSelectRunFile][this.curTag].allSteps[this.getQuestionInfo[this.userSelectRunFile][this.curTag].curMax]
      this.curMapMax = this.getQuestionInfo[this.userSelectRunFile][this.curTag].curMax
      this.curMin = 0
      this.curMapStep = this.getQuestionInfo[this.userSelectRunFile][this.curTag].allSteps[this.curStep]
      const param = {
        run: this.userSelectRunFile,
        tag: this.curTag,
        step: this.curMapStep,
        method: this.curMethod.toLowerCase(),
        dims: parseInt(this.curDim)
      }
      this.fetchDataPower(param)
    },
    curTag: function() {
      console.log(297)
      this.setCurInfo(['curTag', this.curTag])
      this.fetchData()
    },
    curMethod: function() {
      console.log(302)
      this.setCurInfo(['curMethod', this.curMethod])
      this.fetchData()
    },
    curDim: function() {
      console.log(307)
      this.setCurInfo(['curDim', this.curDim])
      this.fetchData()
    },
    curStep: function() {
      this.setCurInfo(['curStep', this.curStep])
      this.curMapStep = this.getQuestionInfo[this.userSelectRunFile][this.curTag].allSteps[this.curStep]
    },
    curMapStep: function() {
      console.log(316)
      this.setCurInfo(['curMapStep', this.curMapStep])
      this.fetchData()
    },
    getReceivedQuestionInfo: function() {
      for (let i = 0; i < this.getCategoryInfo.curRuns.length; i++) {
        if (this.userSelectRunFile === this.getCategoryInfo.curRuns[i]) {
          this.curTags = this.getCategoryInfo.curTags[i].slice(0)
        }
      }
    },
    checkedLabels: function(val) {
      this.setCheckLabels(val)
    },
    getMessage() {
      if (this.getQuestionInfo[this.userSelectRunFile][this.getCurInfo.curTag]['sample'] && this.getMessage.length > 0) {
        this.fetchSampleData(this.getMessage[0])
      }
    },
    getReceivedCurData: function() {
      if (parseInt(this.curDim) > 3) {
        this.lableTypes = this.getCurData.labelType.slice(0)
      }
      const vm = this
      if (this.playAction) {
        setTimeout(function() {
          if (vm.playAction) {
            let curSteptmp = vm.curStep
            curSteptmp++
            if (curSteptmp > vm.curMapMax) {
              vm.playAction = false
            } else {
              vm.curStep++
            }
          }
        }, 2000)
      }
    },
    getTimer: function() {
      this.setMessage('')
      console.log("383")
      if (!this.getReceivedQuestionInfo) {
        // console.log('数据还没有整理好')
        return
      }
      this.setCurInfo(['received', false]) // 屏蔽别的请求
      this.fetchOneStep(this.userSelectRunFile);
      // console.log(this.getTimer)
      // console.log("352")
      // if(this.getReceivedCurInfo == false) return
      // if (this.userSelectRunFile === '') {
      //   return
      // }
      // this.setCurInfo(['received', false]) // 屏蔽别的请求
      // for (let i = 0; i < this.getCategoryInfo.curRuns.length; i++) {
      //   if (this.userSelectRunFile === this.getCategoryInfo.curRuns[i]) {
      //     this.curTags = this.getCategoryInfo.curTags[i].slice(0)
      //   }
      // }
      // if(this.curTag.length == 0) this.curTag = this.curTags[0];
      // this.curMethod = this.getCurInfo.curMethod
      // this.curDim = this.getCurInfo.curDim
      // this.curStep = this.getCurInfo.curStep
      // this.curMax = this.getQuestionInfo[this.userSelectRunFile][this.curTag].allSteps[this.getQuestionInfo[this.userSelectRunFile][this.curTag].curMax]
      // this.curMapMax = this.getQuestionInfo[this.userSelectRunFile][this.curTag].curMax
      // this.curMin = 0
      // this.curMapStep = this.getQuestionInfo[this.userSelectRunFile][this.curTag].allSteps[this.curStep]
      // const param = {
      //   run: this.userSelectRunFile,
      //   tag: this.curTag,
      //   step: this.curMapStep,
      //   method: this.curMethod.toLowerCase(),
      //   dims: parseInt(this.curDim)
      // }
      // this.fetchDataPower(param)
    },
    userSelectRunFile: function() {
      this.setMessage('')
      console.log("383")
      if (!this.getReceivedQuestionInfo) {
        // console.log('数据还没有整理好')
        return
      }
      this.setCurInfo(['received', false]) // 屏蔽别的请求
      this.fetchOneStep(this.userSelectRunFile);
    },
    getErrorMessage(val) {
      this.$message({
        message: val.split('_')[0],
        type: 'error'
      })
    }
  },
  // mounted() {
  // },
  created() { // 每次加载的时候都会触发
    if (!this.getInitStateFlag) {
      if (this.getReceivedCategoryInfo) {
        // console.log('mounted fetchAllStep')
        this.fetchOneStep()
      }
    } else {
      this.setInitStateFlag(false)
    }
    if (this.getReceivedQuestionInfo) {
      this.setCurInfo(['received', false]) // 屏蔽别的请求
      for (let i = 0; i < this.getCategoryInfo.curRuns.length; i++) {
        if (this.userSelectRunFile === this.getCategoryInfo.curRuns[i]) {
          this.curTags = this.getCategoryInfo.curTags[i].slice(0)
        }
      }
      this.curTag = this.curTags[0]
      this.curMethod = this.getCurInfo.curMethod
      this.curDim = this.getCurInfo.curDim
      this.curStep = this.getCurInfo.curStep
      this.curMax = this.getQuestionInfo[this.userSelectRunFile][this.curTag].allSteps[this.getQuestionInfo[this.userSelectRunFile][this.curTag].curMax]
      this.curMapMax = this.getQuestionInfo[this.userSelectRunFile][this.curTag].curMax
      // this.curMin = this.getQuestionInfo[this.userSelectRunFile][this.curTag].allSteps[0]
      this.curMin = 0
      this.curMapStep = this.getQuestionInfo[this.userSelectRunFile][this.curTag].allSteps[this.curStep]
      const param = {
        run: this.userSelectRunFile,
        tag: this.curTag,
        step: this.curMapStep,
        method: this.curMethod.toLowerCase(),
        dims: parseInt(this.curDim)
      }
      this.fetchDataPower(param)
    }
    this.curLineWidth = this.getLineWidth
  },
  methods: {
    ...mapEmbeddingMutations([
      'setCheckLabels',
      'setCurInfo',
      'setMessage',
      'setInitStateFlag',
      'setLineWidth'
    ]),
    ...mapEmbeddingActions(['fetchSampleData', 'featchData', 'fetchAllStep', 'fetchOneStep']),
    playActionClick() {
      this.playAction = !this.playAction // 取非
      if (this.playAction) {
        if (this.curStep === 0) {
          this.fetchData()
        } else {
          this.curStep = 0
        }
      }
    },
    fetchData() {
      if (!this.getReceivedCurInfo || !this.getCurInfo.received) { // 只要数据未准备好就不触发请求
        return
      }
      // console.log('this.getCurInfo.curMethod', this.getCurInfo.curMethod)
      const param = {
        run: this.userSelectRunFile,
        tag: this.getCurInfo.curTag,
        step: this.getCurInfo.curMapStep,
        method: this.getCurInfo.curMethod.toLowerCase(),
        dims: parseInt(this.getCurInfo.curDim)
      }
      this.featchData(param)
    },
    fetchDataPower(param) {
      this.featchData(param)
    }
  }
}
</script>
<style lang="less" scoped>
  .typeselect{
    height: 30%;
  }
  select{
    width:70%;
    height:30%;
    margin-top: 20%;
  }
  .panel{
    /deep/.el-card{
      margin:3.5% 5% 4% 0%;
      border-top: 0px;
    }
    /deep/.el-card__body{
      border-radius: 0 0 3px 3px;
      padding: 0px;
    }
    .info{
      .infoTitle{
        span{
          font-size: 12px;
        }
        background-color: #625eb3;
        color: white;
        text-align:left;
        border-bottom:1px solid #8F8AD7;
        padding:2% 2% 2% 5%;
        .iconfont{
          margin-right: 7px;
          font-size: 12px;
          font-style: normal;
          -webkit-font-smoothing: antialiased;
          -moz-osx-font-smoothing: grayscale;
        }
      }
    }
    /deep/.el-icon-circle-close{
      color: white;
    }
    /deep/.el-image-viewer__img{
      height: 100%;
    }
    /deep/.infoContent{
      @backgroundColorList: #EF6F38, #EFDD79 ,#C5507A, #9359B0, #525C99,#47C1D6, #B5D4E8, #15746C, #81c19c, #A08983;
      .backgroundcard(@className, @backgroundColorList,@i){
        .@{className}@{i} .el-checkbox__inner{ //属性名称 可以直接拼接属性
            background: @backgroundColorList;
            opacity: 0.5;
        }
      }
      @checkboxClass: checkboxx;
      .loop(@i) when(@i < 10){ // extract 是取出列表中的对应元素
        .backgroundcard(@checkboxClass,extract(@backgroundColorList, @i+1), @i);
        .loop(@i+1);
      }
      .loop(0);
      // 选中状态下的透明度得更改
      .backgroundchecked(@className, @backgroundColorList,@i){
        .@{className}@{i}.is-checked .el-checkbox__inner{ //属性名称 可以直接拼接属性
            opacity: 1;
        }
      }
      .loop(@i) when(@i < 10){ // extract 是取出列表中的对应元素
        .backgroundchecked(@checkboxClass,extract(@backgroundColorList, @i+1), @i);
        .loop(@i+1);
      }
      .loop(0);
      padding: 2% 10% 2% 10%;
      .image {
        width: 100%;
        height: 300px;
        display: block;
        p{
          margin-left: 2%;
          margin-right: 2%;
          margin-top: 2%;
          margin-bottom: 2%;
        }
      }
      .infoItem{
        margin:5% 0 5% 0;
        text-align: left;
        font-size: 11px;
        justify-content: center;
        .center{
          text-align:center;
        }
        span{
          display: flex;
          align-items: center; /*定义body的元素垂直居中*/
          text-align: center;
          line-height: 30px;
        }
      }
      .infoItem .el-select{
        width:100%;
      }
      .el-slider__bar{
        background-color: #625eb3;
      }
      .el-input__inner{
        border-radius: 50px;
        height: 30px;
        line-height: 30px;
        font-size:11px;
        border-color: #8f95ad;
        color:#625eb3;
      }
      // .el-input{
      //   border-color:#8f95ad;
      // }
      .el-input.is-focus{
        border-color:#7f7cc1;
      }
      .el-select{
        border-color:#8f95ad;
      }
      .el-select:hover .el-input__inner{
        border-color:#7f7cc1;
      }
      .el-select__caret{
        font-weight: 900;
        color: #7f7cc1;
        font-size:20px;
      }
      .ProbabilityDensitySec{
        width: 93%;
        .ProbabilityDensity{
          color: #8F8AD7;
          margin-bottom: -10px;
        }
        .el-checkbox__label {
          color: #8F8AD7;
        }
        .el-checkbox {
          color: #8F8AD7;
        }
        .leftInline-block{
          display: -webkit-flex; /* Safari */
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          justify-content: flex-start;
          .el-checkbox{
            display: inline-block;
            span{
              display: inline-block;
            }
          }
          .el-checkbox__inner:hover{
            border-color: #DCDFE6;
          }
          .el-checkbox__inner{
            border-color: #DCDFE6;
          }
          .el-checkbox__input.is_focus .el-checkbox__inner{
            border-color: #DCDFE6;
          }
          .el-checkbox__input.is-checked .el-checkbox__inner{
            border-color: #DCDFE6;
          }
        }
        hr{
          background-color: #8F8AD7;
          border-color: #8F8AD7;
          border-width: 0.1;
          opacity: 0.6;
        }
        .el-checkbox__inner{
          border-radius: 50%;
        }
      }

      .row-bg{
        button{
          background-color:white;
          border-color: white;
          color: #7f7cc1;
        }
        .el-slider__button{
          border-color: #7f7cc1;
        }
        .el-slider__runway{
          height: 4px;
        }
        .el-slider__bar{
          height: 4px;
        }
        .iconfont{
          font-size: 11px;
        }
        .el-slider__button{
          width: 12px;
          height: 12px;
        }
        .grid-content{
          line-height: 38px;
          height: 38px;
          span{
            line-height: 38px;
            text-align: center;
            margin: 0 auto;
            display: block;
          }
        }
      }
      .imageSpan{
          span{
            display: block !important;
            text-align: center;
            margin: 0 auto;
          }
        }
    }
  }
  .el-select-dropdown__item.selected{
    color: #625eb3;
  }
  .el-select-dropdown__item {
    font-size: 11px;
  }
</style>
