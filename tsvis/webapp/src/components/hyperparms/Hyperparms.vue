<style lang="less" scoped>
.temp {
  height: 100%;
  overflow-y: hidden;
  width: 100%;
  background-color: white;
}
.display-panel {
  margin: 1% 1% 0 1%;
  height: 97.5%;
  border-radius: 5px 5px 0 0;
  box-shadow: rgba(0, 0, 0, 0.3) 0px 0px 10px;
  background-color: white;
  overflow-y: auto;
}
</style>
<template>
  <div class="temp">
    <div :class="['display-panel']">
      <HyperPara />
    </div>
  </div>
</template>
<script>
import HyperPara from './HyperPara'
import { createNamespacedHelpers } from 'vuex'
const { mapActions: maphyperparmActions, mapGetters: maphyperparmGetters, mapMutations: maphyperparmMutations } = createNamespacedHelpers('hyperparm')
const { mapState: mapLayoutStates, mapGetters: mapLayoutGetters } = createNamespacedHelpers('layout')
export default {
  components: {
    HyperPara
  },
  computed: {
    ...maphyperparmGetters(['getAllData', 'getCategoryInfo', 'getRequestState', 'getErrorMessage', 'getIntervalChange']),
    ...mapLayoutStates(['userSelectRunFile']),
    ...mapLayoutGetters(['getTimer'])
  },
  watch: {
    userSelectRunFile (val) {
      if (val === '') {
        this.setAllData('null')
        this.setHypEmpty(true)
      } else {
        const param = { run: val }
        this.featchAllData(param)
        this.setHypEmpty(false)
      }
    },
    getErrorMessage (val) {
      this.$message({
        message: val.split('_')[0],
        type: 'error'
      })
    },
    getIntervalChange: function () {
      if (this.userSelectRunFile) {
        const param = { run: this.userSelectRunFile }
        this.featchAllData(param)
      }
    }
  },
  mounted () {
    if (this.userSelectRunFile) {
      const param = { run: this.userSelectRunFile }
      this.featchAllData(param)
    }
  },
  destroyed () {
    this.setAllData('null')
  },
  methods: {
    ...maphyperparmActions(['featchAllData']),
    ...maphyperparmMutations(['setAllData', 'setHypEmpty', 'setSelfCategoryInfo'])
  }
}
</script>
