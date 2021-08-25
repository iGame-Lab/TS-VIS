<style lang="less" scoped>
.temp {
  height: 100%;
  overflow-y: auto;
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
}
</style>
<template>
  <div>
    <div class="temp">
      <div :class="['display-panel']">
        <subStatistics
          v-for="(item,index) in getCategoryInfo"
          :key="index"
          :categoryInfo="item"
        >{{ item }}</subStatistics>
      </div>
    </div>
  </div>
</template>
<script>
import { subStatistics } from './substatistic'
import { createNamespacedHelpers } from 'vuex'
const { mapGetters: mapStatisticGatters } = createNamespacedHelpers('statistic')

export default {
  components: {
    subStatistics
  },
  computed: {
    ...mapStatisticGatters([
      'getCategoryInfo',
      'getErrorMessage'
    ])
  },
  watch: {
    getErrorMessage(val) {
      this.$message({
        message: val,
        type: 'error'
      })
    }
  }
}
</script>
