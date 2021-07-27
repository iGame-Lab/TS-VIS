<style lang="less" scoped>
    .scalars{
        height: 100%;
        overflow-y: auto;
        width: 100%;
        background-color: white;
    }
    .display-panel{
      margin: 1% 1% 0 1%;
      height: 97.5%;
      border-radius: 5px 5px 0 0;
      box-shadow: rgba(0,0,0,.3) 0px 0px 10px;
      background-color: white;
      overflow-y: auto;
    }
</style>
<template>
  <div>
    <div class="scalars">
      <div class="display-panel">
        <subScalars v-for="(value, name, index) in totaltag" :key="name" :subname="name" :value="value" :index="index" />
      </div>
    </div>
  </div>
</template>
<script>
import { subScalars } from './subscalar'
import { createNamespacedHelpers } from 'vuex'
const { mapGetters: mapScalarGetters, mapMutations: mapScalarMutations, mapActions: mapScalarActions } = createNamespacedHelpers('scalar')
const { mapState: mapLayoutStates, mapGetters: mapLayoutGetters } = createNamespacedHelpers('layout')
export default {
  components: {
    subScalars
  },

  data() {
    return {
      data: [],
      totaltag: {}
    }
  },
  computed: {
    ...mapScalarGetters([
      'categoryInfo', 'getTotaltag', 'getErrorMessage', 'getFreshInfo', 'getIntervalChange'
    ]),
    ...mapLayoutStates([
      'userSelectRunFile'
    ]),
    ...mapLayoutGetters([
      'getTimer'
    ])
  },
  watch: {
    categoryInfo() {
      this.settotaltag()
    },
    getErrorMessage(val) {
      this.$message({
        message: val.split('_')[0],
        type: 'error'
      })
    },
    // 定时请求数据
    getIntervalChange() {
      // console.log("scalar_time")
      if (!this.settotaltag) {
        // console.log('数据还没有整理好')
        return
      }
      
      this.settotaltag()
    }
  },
  created() {
    if (Object.keys(this.getTotaltag).length !== 0) {
      this.totaltag = this.getTotaltag
    } else {
      this.settotaltag()
      
    }
  },
  mounted() {

  },
  methods: {
    ...mapScalarMutations([
      'setTotaltag'
    ]),
    ...mapScalarActions([
      'getData'
    ]),
    settotaltag() {
      if (this.categoryInfo === '') {
        return
      }
      this.data = [].concat(JSON.parse(JSON.stringify(this.categoryInfo)))
      this.totaltag = {}
      let param = {}
      for (let i = 0; i < this.data[1].length; i++) {
        param = JSON.parse(JSON.stringify(this.data[1][i]))
        for (let j = 0; j < Object.keys(param).length; j++) {
          if (this.totaltag[Object.keys(param)[j]] === undefined) {
            this.totaltag[Object.keys(param)[j]] = []
          }
          const arr = this.totaltag[Object.keys(param)[j]].concat(param[Object.keys(param)[j]])
          this.totaltag[Object.keys(param)[j]] = Array.from(new Set(arr))
        }
      }
      this.setTotaltag(this.totaltag)
      // 谁打开就重新获取谁的数据
      for (const i in this.getFreshInfo) {
        if (this.getFreshInfo[i] === false) {
          this.getData([i, this.totaltag[i]])
        }
      }
    }
  }
}
</script>
