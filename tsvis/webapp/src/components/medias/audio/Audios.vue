<template>
  <div class="audioscontainer">
    <div :class="['audios-title', showFlag?'titleStyle':'']"
      @click="showContent()">
      <div :class="[showFlag?'sub':'sub1']">
        <div class="my-label">
          <div class="my-text"><span>音频</span></div>
          <div class="circle-father">
            <div class="circle" />
          </div>
          <div class="triangle-father">
            <div class="triangle" />
          </div>
        </div>
      </div>
      <div class="line1" />
      <div :class="['line2', showFlag?'linestyle':'']" />
    </div>
    <div :class="[showFlag?'showClass':'']">
      <div class="audioscontent">
        <el-row :gutter="20">
          <audio-container v-for="(item,i) in detailData[subname]"
            v-show="showrun[item.run]" :key="item.index" :content="item"
            :index="i" :parentComponent="parentComponent" />
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import { audioContainer } from './audioContainer'
import { createNamespacedHelpers } from 'vuex'
const { mapGetters: mapMediaGetters, mapActions: mapMediaActions, mapMutations: mapMediaMutations } = createNamespacedHelpers('media')
const { mapState: mapLayoutStates } = createNamespacedHelpers('layout')
export default {
  components: {
    audioContainer
  },
  props: {
    subname: String,
    index: Number,
    value: Array
  },
  data () {
    return {
      showFlag: true, // 刚开始 都先不显示 点击之后 请求数据 再显示
      parentComponent: true
    }
  },
  computed: {
    ...mapMediaGetters([
      'detailData', 'categoryInfo', 'showrun', 'getShowFlag'
    ]),
    ...mapLayoutStates([
      'userSelectRunFile'
    ])
  },
  watch: {
    userSelectRunFile: function (val) {
      this.setshowrun(val)
      if (this.showFlag === false) {
        this.showFlag = true
        this.showFlag = false
      }
    },
    showFlag: function (val) {
      this.setShowFlag([this.subname, this.showFlag])
    }
  },
  created () {
    this.setshowrun(this.userSelectRunFile)
    if (this.index === 0 && this.getShowFlag.firstTime) {
      this.showFlag = false
      this.setFreshInfo([this.subname, false])
      this.getData([this.subname, this.value])
      this.setShowFlag(['firstTime', false])
    }
    if (!this.getShowFlag.firstTime) {
      if (typeof (this.getShowFlag[this.subname]) !== 'undefined') {
        this.showFlag = this.getShowFlag[this.subname]
      }
    }
  },
  methods: {
    ...mapMediaActions([
      'getData'
    ]),
    ...mapMediaMutations([
      'setDetailData', 'setshowrun', 'setFreshInfo', 'setShowFlag'
    ]),
    showContent () {
      if (this.showFlag) {
        this.showFlag = false
        this.setFreshInfo([this.subname, false])
        if (this.index !== 0) {
          this.getData([this.subname, this.value])
        }
      } else {
        this.showFlag = true
        this.setFreshInfo([this.subname, true])
      }
    }
  }
}
</script>

<style lang="less" scoped>
.audioscontainer {
  .audios-title {
    height: auto;
    display: flex;
    align-items: center;
    color: white;
    background-color: white;
    span {
      line-height: 30px;
      font-weight: 700;
    }
  }
}
.audioscontent {
  padding: 2%;
}
.showClass {
  display: none;
}
.my-label {
  cursor: pointer;
  display: flex;
  width: 100%;
  .triangle {
    position: absolute;
    width: 0px;
    height: 0px;
    overflow: hidden;
    border-top-width: 15px;
    border-bottom-width: 15px;
    border-left-width: 18px;
    border-right-width: 18px;
    border-style: dashed dashed dashed solid;
    border-color: transparent transparent transparent #7f7cc1;
  }
  .triangle-father {
    position: relative;
  }
  .circle-father {
    height: 30px;
    width: 15%;
    position: relative;
    background-color: #7f7cc1;
  }
  .circle {
    position: absolute;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: white;
    left: 50%;
    top: 50%;
    transform: translateX(-50%) translateY(-50%);
  }
  .my-text {
    width: 70%;
    height: 30px;
    text-align: center;
    vertical-align: center;
    background-color: #7f7cc1;
  }
  span {
    align-items: center;
    line-height: 30px;
    color: white;
  }
}
.sub .triangle {
  border-color: transparent transparent transparent #b8c6ff;
}
.sub .circle-father {
  background-color: #b8c6ff;
}
.sub .my-text {
  background-color: #b8c6ff;
}
.sub {
  background-size: 100% 100%;
  width: 9.5%;
  height: 30px;
  display: flex;
  align-items: center;
  font-family: sans-serif;
  font-size: 12px;
  color: #fff;
}
.sub1 {
  background-size: 100% 100%;
  width: 9.5%;
  height: 30px;
  display: flex;
  align-items: center;
  font-family: sans-serif;
  font-size: 12px;
  color: #fff;
}
.line1 {
  height: 1px;
  width: 88%;
  background-color: #f4f6ff;
}
.line2 {
  height: 5px;
  width: 2.5%;
  background-color: #625eb3;
}
.linestyle {
  background-color: #b9c6ff;
}
</style>
