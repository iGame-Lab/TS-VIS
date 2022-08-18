<style lang="less">
.audiocontent .el-slider__bar {
  background-color: #8f8ad7;
}
.audiocontent .el-slider__button {
  border-color: #8f8ad7;
}
audio::-webkit-media-controls-play-button {
  font-size: 25px;
  color: #8f8ad7 !important;
}
audio::-webkit-media-controls-mute-button {
  color: #8f8ad7;
}
audio {
  background-color: white;
}
audio::-webkit-media-controls-panel {
  border: 1px solid #ebeef5;
  color: #8f8ad7;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
<template>
  <div class="audiocontainer">
    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="8">
      <el-card class="box-card">
        <el-row>
          <el-col :span="6">
            <el-tag class="top">RUN</el-tag>
          </el-col>
          <el-col :span="16" class="center"><span>{{ content.run }}</span>
          </el-col>
          <el-col :span="2" class="center">
            <div class="leftItem">
              <el-tooltip class="item" effect="dark"
                content="勾选后，点击定制按钮会跳转到用户定制界面" placement="top">
                <el-checkbox v-if="parentComponent" v-model="checked"
                  @change="ischeckedLocal" />
              </el-tooltip>
              <span v-if="!parentComponent" @click="ischecked"><i
                  class="close-i el-icon-circle-close" /></span>
            </div>
          </el-col>
        </el-row>
        <el-divider />
        <el-row>
          <el-col :span="6">
            <el-tag class="top">TAG</el-tag>
          </el-col>
          <el-col :span="18" class="center">
            <span>{{ Object.keys(content.value)[0] }}</span></el-col>
        </el-row>
        <el-divider />
        <el-row>
          <el-col :span="6">
            <el-tag class="bottom">STEP</el-tag>
          </el-col>
          <el-col :span="18" class="center">
            <span>{{ audiocontent[scrollvalue].step}}</span></el-col>
        </el-row>
        <el-divider />
        <el-row>
          <el-col :span="6">
            <el-tag class="bottom">WALL_TIME</el-tag>
          </el-col>
          <el-col :span="18" class="center"><span>{{ normalTime }}</span>
          </el-col>
        </el-row>
        <el-divider />
        <el-row>
          <el-col :span="6">
            <el-tag class="bottom">LABEL</el-tag>
          </el-col>
          <el-col :span="18" class="center">
            <span>{{ audiocontent[scrollvalue].label }}</span></el-col>
        </el-row>
      </el-card>

      <div class="audiocontent">
        <customAudio :theUrl="audiourl" :index="index"
          theControlList="noSpeed onlyOnePlaying" />
        <el-slider v-model="scrollvalue" :max="audiocontent.length - 1"
          :disabled="audiocontent.length - 1===0"
          :format-tooltip="formatTooltip" class="slider" />
      </div>
    </el-col>
  </div>
</template>

<script>
import http from '@/utils/request'
import port from '@/utils/api'
import customAudio from './CustomAudio'
import { unixTimestamp2Normal } from '@/utils/utils'
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
  components: {
    customAudio
  },
  props: {
    content: Object,
    index: Number,
    parentComponent: Boolean
  },
  data () {
    return {
      scrollvalue: 0,
      audiocontent: [],
      audiourl: '',
      size: 8,
      checked: false,
      normalTime: ''
    }
  },
  computed: {
    ...mapCustomGetters(['getAudio']),
    ...mapLayoutGetters(['getParams', 'getTimer'])
  },
  watch: {
    getTimer: function () {
      this.audiocontent = this.content.value[Object.keys(this.content.value)[0]]
    },
    async scrollvalue (val) {
      this.normalTime = unixTimestamp2Normal(this.audiocontent[this.scrollvalue].wall_time)
      const params = {
        step: this.audiocontent[val].step.toString(),
        run: this.content.run,
        tag: Object.keys(this.content.value)[0],
      }
      await http.useGet(port.category.audio_raw, params)
        .then(res => {
          if (+res.data.code !== 200) {
            this.setErrorMessage(res.data.msg + '_' + new Date().getTime())
            return
          }
          this.audiourl = res.data.data
        })
    }
  },
  mounted: function () {
    const paramStringIndex = this.content.run + '/' + Object.keys(this.content.value)[0]
    for (let i = 0; i < this.getAudio.length; i++) {
      if (paramStringIndex === this.getAudio[i].stringIndex) {
        this.checked = true
        break
      }
    }
    this.normalTime = unixTimestamp2Normal(this.audiocontent[this.scrollvalue].wall_time)
  },
  async created () {
    this.audiocontent = this.content.value[Object.keys(this.content.value)[0]]
    const params = {
      step: this.audiocontent[0].step.toString(),
      run: this.content.run,
      tag: Object.keys(this.content.value)[0],
    }
    await http.useGet(port.category.audio_raw, params)
      .then(res => {
        if (+res.data.code !== 200) {
          this.setErrorMessage(res.data.msg + '_' + new Date().getTime())
          return
        }
        this.audiourl = res.data.data
      })
  },
  methods: {
    ...mapCustomMutations(['setAudioData']),
    ...mapMediaMutations(['setErrorMessage']),
    sizebig () {
      this.size = 24
    },
    sizesmall () {
      this.size = 8
    },
    ischecked () {
      const param = {}
      param['content'] = this.content
      param['index'] = this.index
      param['checked'] = false
      param['copyToData'] = true
      this.setAudioData(param)
    },
    ischeckedLocal () {
      const param = {}
      param['content'] = this.content
      param['index'] = this.index
      param['checked'] = this.checked
      param['copyToData'] = false
      this.setAudioData(param)
    },
    formatTooltip (val) {
      if (val === null) {
        return 0
      }
      return this.audiocontent[val]['step']
    },
  }
}
</script>

<style lang="less" scoped>
.audiocontainer {
  width: 100%;
  height: 100%;
  background-color: rgb(255, 255, 255);
}
.audiocontent {
  margin-top: 20px;
  width: 100%;
  height: 20%;
}
audio {
  width: 100%;
}
.close-i {
  font-size: 19px;
}
.leftItem {
  margin-left: auto;
  margin-right: 1%;
  /deep/.checked {
    width: 20px;
    height: 20px;
  }
  /deep/.el-checkbox__inner:hover {
    border-color: #8f8bd9;
  }
  /deep/.el-checkbox__inner {
    font-size: 20px;
  }
  /deep/.el-checkbox {
    font-size: 20px;
  }
  /deep/.el-checkbox__input.is-checked .el-checkbox__inner {
    background-color: #8f8bd9;
    border-color: #8f8bd9;
  }
  /deep/.el-checkbox__input.is-focus .el-checkbox__inner {
    border-color: gray;
  }
  /deep/.el-checkbox__input span {
    height: 14px !important;
  }
}
/deep/.box-card {
  height: 100%;
  width: 100%;
  text-align: left;
  .el-divider--horizontal {
    margin: 6px 0;
  }
  .top {
    background-color: #e5fcff;
    color: #66cbd7;
    border-color: #e5fcff;
    font-size: 9px;
  }
  .bottom {
    background-color: #def8fb;
    color: #48d994;
    border-color: #def8fb;
    font-size: 9px;
  }
  .center {
    align-items: center;
    font-size: 10px;
    color: #333333;
    vertical-align: middle;
  }
  span {
    font-weight: bold;
    line-height: 30px;
    height: 30px;
  }
  .el-row {
    margin-bottom: 0;
  }
  .el-col {
    margin-bottom: 0;
  }
}
.el-col {
  margin-bottom: 20px;
}
.audiotext {
  margin-left: 2%;
  text-align: left;
}
.button {
  align-self: flex-start;
}
p {
  font-size: 10px;
}
/deep/.el-slider__runway {
  width: 95%;
  margin: 16px auto;
}
/deep/.el-slider__button {
  border-color: #625eb3;
}
/deep/.el-slider__bar {
  background-color: #625eb3;
}
</style>
