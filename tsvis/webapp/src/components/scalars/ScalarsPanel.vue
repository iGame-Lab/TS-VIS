<style lang="less" scoped>
.information {
  font-size: 11px;
  text-align: left;
  margin-bottom: 6%;
}
.infoTitle {
  padding: 2% 2% 2% 5%;
  border-bottom: 1px solid #8f8ad7;
  font-size: 12px;
  color: white;
  background-color: rgb(96, 97, 173);
  text-align: left;
}
.infoContent {
  padding: 2% 5% 5% 5%;
}
.el-select-dropdown__item.selected {
  color: #8f8ad7;
}
.select {
  display: flex;
  align-items: center;
}
.select,
.scroll,
.action {
  margin: 5% 0 8% 0;
}
.select .el-select {
  margin-left: 20px;
  flex: 1;
}
.infoItem {
  margin-top: 5%;
}
.infoItemLeft {
  display: flex;
}
.display {
  margin: 3.5% 1% 5% 1%;
  border-radius: 2px 2px 0 0;
  box-shadow: rgba(0, 0, 0, 0.2) 0px 0px 5px;
  background-color: white;
  overflow-y: auto;
}
.iconfont {
  font-family: 'iconfont' !important;
  margin-right: 7px;
  font-size: 13px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.action {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.modeselect {
  margin-left: 5%;
  width: 75%;
}
</style>
<template>
  <div class="temp">
    <div class="information">
      <el-card>
        <div class="infoTitle">
          <div><span class="icon iconfont">&#xe634;</span>控制面板</div>
        </div>
        <div class="infoContent">
          <div class="scroll">
            <span>Smooth({{ smooth }})</span>
            <el-slider v-model="smooth" :max="0.9" :step="0.1"
              class="rangeNumber" />
          </div>
          <div class="select">
            <span>Y-axis:</span>
            <el-select v-model="yselect" class="modeselect">
              <el-option value="linear" label="linear" />
              <el-option value="log-linear" label="log-linear" />
            </el-select>
          </div>
          <div class="action">
            <span>视图操作</span>
            <el-button class="button" round size="small" @click="startmerge()">
              合并</el-button>
            <el-button class="button" round size="small" @click="startback()">还原
            </el-button>
          </div>
        </div>
      </el-card>
    </div>
    <div class="information">
      <el-card>
        <div class="infoTitle">
          <div><span class="icon iconfont">&#xe636;</span>数据信息栏</div>
        </div>
        <div class="infoContent">
          <div class="infoItem">暂无信息</div>
        </div>
      </el-card>
    </div>
  </div>
</template>
<script>
import { createNamespacedHelpers } from 'vuex'
const { mapMutations: mapScalarMutations, mapGetters: mapScalarGetters } = createNamespacedHelpers('scalar')
const { mapMutations: mapCustomMutations } = createNamespacedHelpers('custom')
export default {
  data () {
    return {
      checked: true,
      xradio: 0
    }
  },
  computed: {
    ...mapScalarGetters([
      'categoryInfo', 'smoothvalue', 'yaxis', 'checkeditem', 'checkedorder', 'backednumber'
    ]),
    smooth: {
      get () {
        return this.smoothvalue
      },
      set (value) {
        this.setsmoothvalue(value)
      }
    },
    yselect: {
      get () {
        return this.yaxis
      },
      set (value) {
        this.setyaxis(value)
      }
    }
  },
  created () {
  },
  methods: {
    ...mapScalarMutations([
      'setsmoothvalue', 'setyaxis', 'merge', 'back'
    ]),
    ...mapCustomMutations([
      'cleanScalar'
    ]),
    startmerge () {
      if (Object.keys(this.checkeditem).length > 2) {
        this.$alert('选择种类超出限制', '警告', {
          confirmButtonText: '确定'
        })
      } else if (this.checkedorder.length > 6) {
        this.$alert('选择数量超出限制', '警告', {
          confirmButtonText: '确定'
        })
      } else if (Object.keys(this.checkeditem).length === 1 && this.checkeditem[Object.keys(this.checkeditem)[0]].length > 1) {
        this.merge()
      } else if (Object.keys(this.checkeditem).length === 2) {
        this.merge()
      }
    },
    startback () {
      if (this.backednumber.length > 0) {
        this.back()
      }
    }
  }
}
</script>
<style scoped>
.rangeNumber .el-slider__bar {
  background-color: #625eb3;
}
.rangeNumber .el-slider__button {
  border-color: #625eb3;
}

.el-button {
  background-color: #dfe7fd;
  width: 30%;
  color: #270089;
  font-size: 10px;
}
.el-button:hover {
  background-color: #8f8bd8;
  color: #ffffff;
}
.el-button:focus {
  background-color: #8f8bd8;
  color: #ffffff;
}
.information .el-input__inner {
  border-radius: 50px;
  height: 30px;
  line-height: 30px;
  font-size: 11px;
  border-color: #8c89c7;
  color: #b8bbc9;
}
.information .el-input.is-focus .el-input__inner {
  border-color: #8c89c7;
}
.information .el-input__inner:focus {
  border-color: #8c89c7;
}
.information .el-input__icon {
  line-height: 30px;
}
.information .el-select:hover .el-input__inner {
  border-color: #625eb3;
}

.information .el-card__body {
  border-radius: 0 0 3px 3px;
  padding: 0px;
}
.information .el-card {
  margin: 3.5% 5% 4% 0%;
  border-top: 0px;
}
.information .el-input .el-select__caret {
  /* color:#625eb3; */
  color: #9492cb;
  font-size: 20px;
}
.information [class*=' el-icon-'],
[class^='el-icon-'] {
  font-weight: 900;
}
</style>
