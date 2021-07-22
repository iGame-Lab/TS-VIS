<style lang="less" scoped>
    /deep/.el-icon-circle-close{
      color: white;
    }
    .imagecontainer{
      width: 100%;
      height: 100%;
      background-color: rgb(255, 255, 255);
      /deep/.el-slider__runway {
        width: 95%;
        margin: 16px auto;
      }
      /deep/.el-slider__button{
        border-color: #625EB3
      }
      /deep/.el-slider__bar{
        background-color: #625EB3;
      }
    }
    .imagecontent{
      width:100%;
      height:auto;
    }
    .scroll{
      width:100%;
      height:auto;
    }
    /deep/.el-image{
      width: 100%;
      height: 400px;
    }
    /deep/.el-image__preview{
      width: 100%;
      height: 400px;
    }
    /deep/.el-image-viewer__img{
      height: 100%;
    }
    .titleRight{
      float:right;
      right:1%;
      .iconfont {
        font-size: 12px;
      }
    }
    .leftItem{
      margin-left: auto;
      margin-right: 1%;
      /deep/.checked{
        width: 20px;
        height: 20px;
      }
      /deep/.el-checkbox__inner:hover{
        border-color: #8F8BD9;
      }
      /deep/.el-checkbox__inner{
        font-size: 20px;
      }
      /deep/.el-checkbox{
        font-size:20px;
      }
      /deep/.el-checkbox__input.is-checked .el-checkbox__inner{
        background-color:#8F8BD9;
        border-color:#8F8BD9;
      }
      /deep/.el-checkbox__input.is-focus .el-checkbox__inner{
        border-color:gray;
      }
    }
    input{
      width:100%;
      height:auto;
    }
    .temp{
      padding: 2%;
      background-color: #8f8bd8;
    }
    .image-container-title{
      height: auto;
      width: 100%;
      background-color: #8f8bd8;
      color: white;
      font-size: 12px;
      /deep/.el-col {
        margin-bottom: 10px;
      }
    }
    .el-col {
      margin-bottom: 20px;
    }
    .imagetext{
      margin-left: 1%;
      text-align: left;
    }
    p{
      font-size: 10px;
    }
    .checkedBox {
      cursor: pointer;
    }
  </style>
<template>
  <div class="imagecontainer">
    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="8">
      <div class="temp">
        <div class="image-container-title">
          <el-row>
            <el-col :span="12">
              <div class="imagetext" style="margin-left:2%">
                <span>run: {{ content.run }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="titleRight">
                <!-- <span class="scale" @click="scaleLarge()">
                  <i class="iconfont icon-fangda" />
                </span>
                <span class="scale" @click="scaleSmall()">
                  <i class="iconfont icon-suoxiao1" />
                </span> -->
                <el-tooltip class="item" effect="dark" content="勾选后，点击定制按钮会跳转到用户定制界面" placement="top">
                  <span v-if="parentComponent" v-show="!checked" class="checkedBox" @click="ischeckedLocal()">
                    <i class="iconfont icon-weixuanzhong1" />
                  </span>
                </el-tooltip>
                <el-tooltip class="item" effect="dark" content="勾选后，点击定制按钮会跳转到用户定制界面" placement="top">
                  <span v-if="parentComponent" v-show="checked" class="checkedBox" @click="ischeckedLocal()">
                    <i class="iconfont icon-xuanzhong1" />
                  </span>
                </el-tooltip>
                <span v-if="!parentComponent" class="checkedBox" @click="ischecked()"><i class="close-i el-icon-circle-close" /></span>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div class="imagetext">
                <span>step: {{ imagecontent[scrollvalue].step }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div class="imagetext">
                <span>tag: {{ Object.keys(content.value)[0] }}</span>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
      <div class="imagecontent demo-image__placeholder">
        <div class="block">
          <!-- <span class="demonstration">默认</span> -->
          <el-image
            :src="imgurl"
            :preview-src-list="[imgurl]"
          >
            <div slot="placeholder" class="image-slot">
              加载中<span class="dot">...</span>
            </div>
          </el-image>
        </div>
      </div>
      <el-slider
        v-model="scrollvalue"
        :max="imagecontent.length - 1"
        :disabled="imagecontent.length - 1===0"
        :format-tooltip="formatTooltip"
        class="slider" />
    </el-col>
  </div>
</template>
<script>
import http from '@/utils/request'
import port from '@/utils/api'
import 'element-ui/lib/theme-chalk/display.css'
import { createNamespacedHelpers } from 'vuex'
const {
  mapMutations: mapCustomMutations,
  mapGetters: mapCustomGetters
} = createNamespacedHelpers('custom')
const { mapGetters: mapLayoutGetters } = createNamespacedHelpers('layout')
const {
  mapMutations: mapMediaMutations
} = createNamespacedHelpers('media')
export default {
  props: {
    content: Object,
    parentComponent: Boolean
  },
  data() {
    return {
      scrollvalue: 0,
      imagecontent: [],
      imgurl: '',
      size: 8,
      scaleLargeSmall: false,
      checked: false
    }
  },
  computed: {
    ...mapCustomGetters(['getImage']),
    ...mapLayoutGetters(['getParams'])
  },
  watch: {
    async scrollvalue(val) {
      const params = {
        step: this.imagecontent[val].step.toString(),
        run: this.content.run,
        tag: Object.keys(this.content.value)[0],
        // trainJobName: this.getParams.trainJobName
      }
      await http.useGet(port.category.image_raw, params)
        .then(res => {
          if (+res.data.code !== 200) {
            this.setErrorMessage(res.data.msg + '_' + new Date().getTime())
            return
          }
          this.imgurl = res.data.data
        })
      // this.imgurl = constant.DJANGOHOSTNAME + '/api/image_raw?step=' + this.imagecontent[val].step.toString() + '&run=' + this.content.run + '&tag=' + Object.keys(this.content.value)[0] + '&trainJobName=' + this.getParams.trainJobName
    }
  },
  async created() {
    this.imagecontent = this.content.value[Object.keys(this.content.value)[0]]
    const params = {
      step: this.imagecontent[0].step.toString(),
      run: this.content.run,
      tag: Object.keys(this.content.value)[0]
      // trainJobName: this.getParams.trainJobName
    }
    await http.useGet(port.category.image_raw, params)
      .then(res => {
        if (+res.data.code !== 200) {
          this.setErrorMessage(res.data.msg + '_' + new Date().getTime())
          return
        }
        this.imgurl = res.data.data
      })
    // this.imgurl = constant.DJANGOHOSTNAME + '/api/image_raw?step=' + this.imagecontent[0].step.toString() + '&run=' + this.content.run + '&tag=' + Object.keys(this.content.value)[0] + '&trainJobName=' + this.getParams.trainJobName
  },
  mounted: function() {
    const paramStringIndex = this.content.run + '/' + Object.keys(this.content.value)[0]
    for (let i = 0; i < this.getImage.length; i++) {
      if (paramStringIndex === this.getImage[i].stringIndex) {
        this.checked = true
        break
      }
    }
  },
  methods: {
    ...mapCustomMutations(['setImageData']),
    ...mapMediaMutations(['setErrorMessage']),
    ischecked() {
      const param = {}
      param['content'] = this.content
      param['checked'] = false
      param['copyToData'] = true
      this.setImageData(param)
    },
    ischeckedLocal() {
      this.checked = !this.checked
      const param = {}
      param['checked'] = this.checked
      param['copyToData'] = false
      param['content'] = this.content
      this.setImageData(param)
    },
    scaleLarge() {
      this.scaleLargeSmall = true
      this.size = 24
    },
    scaleSmall() {
      this.size = 8
      this.scaleLargeSmall = false
    },
    formatTooltip(val) {
      if (val === null) {
        return 0
      }
      return this.imagecontent[val]['step']
    },
  }

}
</script>
