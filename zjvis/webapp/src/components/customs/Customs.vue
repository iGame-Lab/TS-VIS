<!--
 * @Descripttion: Customs content panel
 * @version: 1.0
 * @Author: xds
 * @Date: 2020-04-22 00:56:46
 * @LastEditors: xds
 * @LastEditTime: 2020-06-05 19:25:13
 -->
<style lang="less" scoped>
    .temp{
        // position: absolute;
        height: 100%;
        overflow-y: hidden;
        width: 100%;
        background-color:white;
    }
    .display-panel{
      margin: 1% 1% 0 1%;
      height: 97.5%;
      border-radius: 5px 5px 0 0;
      box-shadow: rgba(0,0,0,.3) 0px 0px 10px;
      background-color: white;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      .test1{
        .test1-title{
          height: 30px;
          background-color: burlywood;
        }
        .test1-content{
          height: 100%;
          // background-color: hotpink;
          border: 2px solid #e8eaec;
          border-width: 0 2px 2px 2px;
          border-radius: 0 0 5px 5px;
          overflow-y: auto;
          .test1-detail-content{
            background-color: #ffffff;
            height: 700px;
          }
        }
      }
      .scalar{
        display: flex;
        flex-direction: row;
        height: auto;
        display: flex;
        align-items: center;
        color: white;
        background-color: white;
        span{
          line-height: 30px;
          font-weight: 700;
        }
      }
      .media{
        display: flex;
        flex-direction: row;
        height: auto;
        display: flex;
        align-items: center;
        color: white;
        background-color: white;
        span{
          line-height: 30px;
          font-weight: 700;
        }
      }
      .statistic{
        display: flex;
        flex-direction: row;
        height: auto;
        display: flex;
        align-items: center;
        color: white;
        background-color: white;
        span{
          line-height: 30px;
          font-weight: 700;
        }
      }
    }
    .noneData {
      display: 'none';
    }
    .line1 {
      height: 1px;
      width: 88%;
      background-color: #F4F6FF;
    }
    .line2 {
      height: 5px;
      width:2.5%;
      background-color: #625EB3;
    }
    .linestyle{
      background-color: #b9c6ff;
    }
    // .sub1{
    //   background: url(../../assets/tag1.png);
    //   background-size: 100% 100%;
    //   width: 9.5%;
    //   height:30px;
    //   display: flex;
    //   flex-direction: row;
    //   align-items: center;
    //   justify-content: center;
    //   font-family: sans-serif;
    //   font-size: 12px;
    //   color: #FFF;
    // }

    // .sub{
    //   background: url(../../assets/tag2.png);
    //   background-size: 100% 100%;
    //   width: 9.5%;
    //   height:30px;
    //   display: flex;
    //   flex-direction: row;
    //   justify-content: center;
    //   align-items: center;
    //   font-family: sans-serif;
    //   font-size: 12px;
    //   color: #FFF;
    // }
    .linestyle{
      background-color: #b9c6ff;
    }
    .scalarcontainer{
      width: 100%;
      height: 100%;
      background-color: white;
    }
    .scalarscontent {
      padding: 1% 2% 0 2%;
      background-color: white;
    }
    .content{
      margin-bottom: 0.5%;
    }
    .statistics-container {
      // border: 1px solid #EBEEF5;
      background-color: #FFF;
      // box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
      margin-bottom:0.5%;
      .statistics-title {
      // height: 30px;
      // // background-color: #8F8AD7;
      // color:#625eb3;
      // text-align:center;
      // display: flex;
      // cursor:pointer;
      height: auto;
      display: flex;
      align-items: center;
      color: white;
      background-color: white;
      // margin:0.5%;
      // span {
      //   line-height: 30px;
      //   // font-weight: 700;
      //   color:white;
      //   // margin-left:-14%;
      // }
      // .icon-tag{
      //   font-size:35px;
      // }
  }
  .statistics-content {
    margin-left: 1%;
    position: relative;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
    height: 100%;
    .allStatisticContainer{
      // width: 24%; // 一行放四个
      width: 31%; // 一行放三个
      height: 100%;
      margin: 0.8%;
      background-color:white;
      .statisticContaierContent{
        width: 100%;
        // height: 80%
        .runTag{
          width:100%;
        }
      }
    }
  }
}
.showClass {
  display: none;
}
</style>
<template>
  <div>
    <div class="temp">
      <div :class="['display-panel']">
        <div id="scalar">
          <!-- <div :class="[hasScalar.hasData?'scalar':'noneData']"  @click="showContent('hasScalar')" :style="hasScalar.hasData?'':'display:none'">
            <div :class="[hasScalar.showFlag?'sub1':'sub']">
              <span class='subtitle'>标量</span>
            </div>
            <div :class="['line1']"></div>
            <div :class="['line2', hasScalar.showFlag?'':'linestyle']"></div>
          </div> -->
          <!-- <div :style="hasScalar.hasData && hasScalar.showFlag?'':'display:none'"> -->
          <div>
            <div class="scalarscontent">
              <el-row :gutter="20">
                <ScalarContainer v-for="(val, name) in scalarData" :key="name" :content="val" :chartname="name" />
              </el-row>
            </div>
          </div>
        </div>

        <div id="audio">
          <!-- <div :class="[hasAudio.hasData?'media':'noneData']"  @click="showContent('hasAudio')" :style="hasAudio.hasData?'':'display:none'">
            <div :class="[hasAudio.showFlag?'sub1':'sub']">
              <span class='subtitle'>音频</span>
            </div>
            <div :class="['line1']"></div>
            <div :class="['line2', hasAudio.showFlag?'':'linestyle']"></div>
          </div>
          <div :style="hasAudio.hasData && hasAudio.showFlag?'':'display:none'"> -->
          <div :style="hasAudio.hasData?'':'display:none'">
            <div class="scalarscontent">
              <el-row :gutter="20">
                <AudioContainer v-for="item in audioData" ref="AudioContainer" :key="item.index" :content="item.content" :index="item.index" />
              </el-row>
            </div>
          </div>
        </div>

        <div id="image">
          <!-- <div :class="[hasImage.hasData?'media':'noneData']"  @click="showContent('hasImage')" :style="hasImage.hasData?'':'display:none'">
            <div :class="[hasImage.showFlag?'sub1':'sub']">
              <span class='subtitle'>图像</span>
            </div>
            <div :class="['line1']"></div>
            <div :class="['line2', hasImage.showFlag?'':'linestyle']"></div>
          </div> -->
          <div :style="hasImage.hasData?'':'display:none'">
            <div class="scalarscontent">
              <el-row :gutter="20">
                <ImageContainer v-for="item in imageData" ref="ImageContainer" :key="item.content.run + '/' + Object.keys(item.content.value)[0]" :content="item.content" />
              </el-row>
            </div>
          </div>
        </div>

        <div id="text">
          <!-- <div :class="[hasText.hasData?'media':'noneData']"  @click="showContent('hasText')" :style="hasText.hasData?'':'display:none'">
            <div :class="[hasText.showFlag?'sub1':'sub']">
              <span class='subtitle'>文本</span>
            </div>
            <div :class="['line1']"></div>
            <div :class="['line2', hasText.showFlag?'':'linestyle']"></div>
          </div> -->
          <!-- <div :style="hasText.hasData && hasText.showFlag?'':'display:none'"> -->
          <div :style="hasText.hasData?'':'display:none'">
            <div class="scalarscontent">
              <el-row :gutter="20">
                <!-- :style="getTextChecked[item.content.run + '/' + Object.keys(item.content.value)[0]] ? '' : 'display: none'" -->
                <TextContainer v-for="item in textData" ref="TextContainer" :key="item.content.run + '/' + Object.keys(item.content.value)[0]" :content="item.content" />
                <!-- <TextContainer ref='TextContainer' v-for="(item) in textData" :key="item.id" :content="item.content" ></TextContainer>                 -->
              </el-row>
            </div>
          </div>
        </div>

        <div id="histogram">
          <div class="statistics-container">
            <div :class="['statistics-content']">
              <div v-for="item in statisticData" :id="item.divId" :key="item.divId" class="allStatisticContainer">

                <statisticContainer
                  ref="histoContainer"
                  :key="item.ttlabel"
                  :data="item.data"
                  :ttlabel="item.ttlabel"
                  :tag="item.tag"
                  :itemp="item.itemp"
                  :componentName="item.componentName"
                  :runColor="item.runColor"
                  :divId="item.divId"
                  :parentComponent="parentComponent"
                  class="statisticContaierContent"
                />
              </div>
            </div>
          </div>
        </div>
        <div v-if="!hasData">
          <p>本页面支持将其他页面的数据通过“定制”按钮  <i class="iconfont icon-ziyuan104" />  导入到本页面</p>
          <p>支持将媒体数据、统计分析和标量数据导入到本页面</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
// dubhe-web\src\components\Visual\statistics\drawStatistic\statisticContainer.vue
import statisticContainer from '@/components/statistics/drawStatistic/statisticContainer.vue'
import ImageContainer from '@/components/medias/image/imagecontainer/ImageContainer.vue'
import TextContainer from '@/components/medias/text/textContainer/TextContainer.vue'
import AudioContainer from '@/components/medias/audio/audioContainer/AudioContainer.vue'
import ScalarContainer from '@/components/scalars/scalarcontainer/ScalarCustom.vue'
import { createNamespacedHelpers } from 'vuex'
const {
  mapMutations: mapCustomMutations,
  mapGetters: mapCustomGetters
} = createNamespacedHelpers('custom')

// import Scalarchart from '@/components/scalars/scalarcontainer/scalarchart/Scalarchart.vue'
export default {
  components: {
    statisticContainer,
    ImageContainer,
    TextContainer,
    AudioContainer,
    ScalarContainer
  },
  data() {
    return {
      /* data要从定制页面删除的数据，
       *[0]:标量，
       *[1];音频
       *[2]:图像
       *[3]:文本
       *[4]:直方图
       *[5]:分布图
       */
      showFlag: false,
      parentComponent: false,
      data: [[], [], [], [], [], []],
      textChecked: [],
      hasScalar: {
        hasData: 0,
        showFlag: 0
      },
      hasAudio: {
        hasData: 0,
        showFlag: 0
      },
      hasImage: {
        hasData: 0,
        showFlag: 0
      },
      hasText: {
        hasData: 0,
        showFlag: 0
      },
      // hasHisto: {
      //   hasData: 0,
      //   showFlag: 0
      // },
      // hasDistri: {
      //   hasData: 0,
      //   showFlag: 0
      // },
      scalarData: {},
      // scalarData: [{
      //   'run': 'vgg',
      //   'value': {
      //     'accuracy': [{'wall_time': 1588930147.7661154, 'step': 400, 'value': 0.7639999985694885},
      //       {'wall_time': 1588930147.7661154, 'step': 900, 'value': 0.7639999985694885}]
      //   }
      // }, {
      //   'run': 'hparams',
      //   'value': {
      //     'accuracy': [{'wall_time': 1588930147.7661154, 'step': 400, 'value': 0.7639999985694885},
      //       {'wall_time': 1588930147.7661154, 'step': 900, 'value': 0.7639999985694885}]
      //   }
      // }, {
      //   'run': 'hpa',
      //   'value': {
      //     'accuracy': [{'wall_time': 1588930147.7661154, 'step': 400, 'value': 0.7639999985694885},
      //       {'wall_time': 1588930147.7661154, 'step': 900, 'value': 0.7639999985694885}]
      //   }
      // }, {
      //   'run': 'ams',
      //   'value': {
      //     'epoch-loss': [{'wall_time': 1588930147.7661154, 'step': 400, 'value': 0.7639999985694885},
      //       {'wall_time': 1588930147.7661154, 'step': 900, 'value': 0.7639999985694885}]
      //   }
      // }],
      audioData: [],
      imageData: [],
      textData: [],
      statisticData: [],
      hasData: false
    }
  },
  computed: {
    ...mapCustomGetters([
      'getAudioData',
      'getTextData',
      'getTextChecked',
      'getImageData',
      'getStatisticData',
      'getScalarData'
    ])
  },
  beforeRouteLeave(to, from, next) {
    this.setRouter(7)
    next()
  },
  watch: {
    getAudioData: function() {
      this.audioData = this.getAudioData
      // console.log(this.audioData)
      if (this.audioData.length === 0) {
        this.hasAudio.hasData = 0
        this.hasAudio.showFlag = 0
      }
      if (this.audioData.length || this.textData.length || this.imageData.length || this.statisticData.length || Object.keys(this.scalarData).length) {
        this.hasData = true
      } else {
        this.hasData = false
      }
    },
    getTextData: function() {
      this.textData = this.getTextData
      // console.log(this.textData)
      if (this.textData.length === 0) {
        this.hasText.hasData = 0
        this.hasText.showFlag = 0
      }
      if (this.audioData.length || this.textData.length || this.imageData.length || this.statisticData.length || Object.keys(this.scalarData).length) {
        this.hasData = true
      } else {
        this.hasData = false
      }
    },
    getImageData: function() {
      if (this.imageData.length === 0) {
        this.hasImage.hasData = 0
        this.hasImage.showFlag = 0
      }
      this.imageData = this.getImageData
      if (this.audioData.length || this.textData.length || this.imageData.length || this.statisticData.length || Object.keys(this.scalarData).length) {
        this.hasData = true
      } else {
        this.hasData = false
      }
    },
    getScalarData: function(val) {
      this.scalarData = val
      if (this.audioData.length || this.textData.length || this.imageData.length || this.statisticData.length || Object.keys(this.scalarData).length) {
        this.hasData = true
      } else {
        this.hasData = false
      }
    },
    getStatisticData(val) {
      // console.log(val)
      this.statisticData = val
      if (this.audioData.length || this.textData.length || this.imageData.length || this.statisticData.length || Object.keys(this.scalarData).length) {
        this.hasData = true
      } else {
        this.hasData = false
      }
    }
  },
  created() {
    this.audioData = this.getAudioData
    // this.textData = this.getTextData
    this.textData = this.getTextData
    // 猜测 可能 this.textData 是一个数组指针 直接指向了getTextData，所以就算不监听也没关系
    this.imageData = this.getImageData
    this.scalarData = this.getScalarData
    this.statisticData = this.getStatisticData
    // 如果存在数据那么就不显示信息提示
    if (this.audioData.length || this.textData.length || this.imageData.length || this.statisticData.length || Object.keys(this.scalarData).length) {
      this.hasData = true
    } else {
      this.hasData = false
    }
  },
  mounted() {
    // let that = this
    if (this.audioData.length) {
      this.hasAudio.hasData = 1
    }
    if (this.imageData.length) {
      this.hasImage.hasData = 1
    }
    if (this.textData.length) {
      this.hasText.hasData = 1
    }
  },
  methods: {
    ...mapCustomMutations(['setTextData', 'setRouter']),
    showContent(title) {
      this[title].showFlag = (this[title].showFlag + 1) % 2
    }
  }
}
</script>
