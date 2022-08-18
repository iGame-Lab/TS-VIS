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
.hypPanelSelect {
  margin: 5% 0 8% 0;
}
.hypPanelSelect .el-select {
  margin-left: 10%;
  width: 60%;
}
.hypScale {
  margin: 5% 0 0 12%;
}
.infoItem {
  margin-top: 5%;
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
.el-select-dropdown__item.selected {
  color: #625eb3;
}
.el-select-dropdown__item {
  font-size: 11px;
}
</style>
<template>
  <div class="temp">
    <div class="information">
      <el-card>
        <div class="infoTitle">
          <div class="statistichead1"><span
              class="icon iconfont">&#xe634;</span>控制面板</div>
        </div>
        <div>
          <div v-show="!panelShow" class="infoContent infoItem">暂无信息</div>
          <div v-show="panelShow" class="infoContent">
            <div class="hypPanelSelect">
              <span>主参数：</span>
              <el-select v-model="selected" placeholder="请选择">
                <el-option v-for="(item, index) in getMainParams" :key="index"
                  :label="item" :value="item" />
              </el-select>
            </div>
            <div>
              <span>坐标尺度:</span>
              <el-row>
                <div v-for="(item, index) in getAxisParms" :key="index">
                  <div class="hypScale" style="align:left">
                    <el-col :span="8">
                      <div>{{ item }}:</div>
                    </el-col>
                    <el-col :span="8">
                      <div>
                        <el-radio v-model="getAxisType[item]" label="linear"
                          @change="changeData('linear', item)">Linear</el-radio>
                      </div>
                    </el-col>
                    <el-col :span="8">
                      <div>
                        <el-radio v-model="getAxisType[item]" label="log"
                          @change="changeData('log', item)">Log</el-radio>
                      </div>
                    </el-col>
                  </div>
                  <br>
                </div>
              </el-row>
            </div>
          </div>
        </div>
      </el-card>
    </div>
    <div class="information">
      <el-card>
        <div class="infoTitle">
          <div class="statistichead1"><span
              class="icon iconfont">&#xe633;</span>统计信息栏</div>
        </div>
        <div v-show="!panelShow" class="infoContent infoItem">暂无信息</div>
        <div v-show="panelShow" class="infoContent hypTable">
          <el-table :data="localSelectedDatas"
            :header-cell-style="{color:'rgb(96, 97, 174)'}">
            <el-table-column v-for="(item, index) in localKeys" :key="index"
              :prop="item" :label="item" :min-width="columnWidth[index]"
              align="left" />
          </el-table>
        </div>
      </el-card>
    </div>
    <div class="information">
      <el-card>
        <div class="infoTitle">
          <div class="statistichead1"><span
              class="icon iconfont">&#xe636;</span>数据信息栏</div>
        </div>
        <div class="infoContent">
          <div v-show="!infoControl" class="infoItem">暂无信息</div>
          <div v-show="infoControl">
            <div v-for="(item, index) in keys" :key="index">
              <div class="infoItem">
                <el-row>
                  <el-col :span="10">{{ item }}:</el-col>
                  <el-col :span="14">{{ getFocusData[item] }}</el-col>
                </el-row>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>
<script>
import { createNamespacedHelpers } from 'vuex'
import * as d3 from 'd3'
const { mapMutations: mapHyperparmMutations, mapGetters: mapHyperparmGatters } = createNamespacedHelpers('hyperparm')
export default {
  data () {
    return {
      selected: '',
      focusData: [],
      keys: [],
      localSelectedDatas: [],
      localKeys: [],
      localAxisType: {},
      infoControl: false,
      columnWidth: ['31%', '22%', '25%', '22%'],
      panelShow: false
    }
  },
  computed: {
    ...mapHyperparmGatters(['getAllData', 'getSelected', 'getFocusData', 'getGlobalSelectedDatas', 'getAxisType', 'getHypEmpty', 'getKey', 'getAxisParms', 'getMainParams'])
  },
  watch: {
    getHypEmpty (val) {
      this.panelShow = val
    },
    selected: function (newValue) {
      this.setSelected(newValue)
    },
    getSelected (val) {
      this.selected = val
    },
    getFocusData: function (newValue) {
      this.focusData = JSON.parse(JSON.stringify(newValue))
      if (this.focusData.length !== 0) {
        this.infoControl = true
      } else {
        this.infoControl = false
      }
      if (this.getAllData.length !== 0) {
        this.keys = Object.keys(this.getAllData[0])
      }
    },
    getGlobalSelectedDatas: function (newValue) {
      if (newValue === []) {
        newValue = this.getAllData
      }
      this.calcData(newValue)
    }
  },
  mounted () {
    this.selected = this.getSelected
    this.localAxisType = this.getAxisType
    this.calcData(this.getAllData)
  },
  methods: {
    ...mapHyperparmMutations(['setSelected', 'setGlobalSelectedDatas', 'setAxisType']),
    changeData (label, item) {
      this.setAxisType(label, item)
    },
    calcData (newValue) {
      const data = JSON.parse(JSON.stringify(newValue))
      const calcItems = this.getMainParams
      const format = d3.format('.2f')
      let res = []
      calcItems.forEach(function (d) {
        const maxData = d3.max(data, function (i) { return +i[d] })
        const minData = d3.min(data, function (i) { return +i[d] })
        const meanData = d3.mean(data, function (i) { return +i[d] })
        const temp = {
          'Items': d,
          'Min': format(minData),
          'Mean': format(meanData),
          'Max': format(maxData)
        }
        res.push(temp)
      })
      res = JSON.parse(JSON.stringify(res))
      this.localSelectedDatas = res
      this.localKeys = d3.keys(res[0])
    }
  }
}
</script>
<style>
.information .el-input__inner {
  border-radius: 50px;
  height: 30px;
  line-height: 30px;
  font-size: 11px;
  border-color: #8c89c7;
  color: #8c89c7;
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
.hypScale .el-radio__input.is-checked .el-radio__inner {
  border-color: #8f8ad7;
  background: #8f8ad7;
}
.hypScale .el-radio__inner:hover {
  border-color: #8f8ad7;
}
.hypScale .el-radio__input.is-checked + .el-radio__label {
  color: #8f8ad7;
  font-size: 11px;
}
.hypTable .el-table {
  font-size: 11px;
}
.hypScale .el-radio__input + .el-radio__label {
  font-size: 11px;
}
.hypTable .el-table .cell {
  line-height: 14px;
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
  color: #9492cb;
  font-size: 20px;
}
.information [class*=' el-icon-'],
[class^='el-icon-'] {
  font-weight: 900;
}
</style>
