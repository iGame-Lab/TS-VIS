<template>
  <div class="mediaspanel">
    <div class="panel">
      <el-card class="father">
        <div class="info">
          <div class="infoTitle">
            <!-- <i class='iconfont icon-ziyuan41'></i> -->
            <span i class="iconfont icon-ziyuan41">&nbsp;&nbsp;数据信息栏</span>
          </div>
          <div class="infoContent">
            <div class="infoItem">
              <span>暂无信息</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>
<script>
import { createNamespacedHelpers } from 'vuex'
const { mapMutations: mapMediaMutations, mapGetters: mapMediaGetters } = createNamespacedHelpers('media')
export default {
}
</script>

<style lang="less" scoped>
.typeselect {
  height: 30%;
}
select {
  width: 70%;
  height: 30%;
  margin-top: 20%;
}
.panel {
  /deep/.el-card {
    margin: 3.5% 5% 4% 0%;
    border-top: 0px;
  }
  /deep/.el-card__body {
    border-radius: 0 0 3px 3px;
    padding: 0px;
  }
  .info {
    .infoTitle {
      span {
        font-size: 12px;
      }
      background-color: #625eb3;
      color: white;
      text-align: left;
      border-bottom: 1px solid #8f8ad7;
      padding: 2% 2% 2% 5%;
      .iconfont {
        margin-right: 7px;
        font-size: 12px;
        font-style: normal;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }
    }
  }
  /deep/.infoContent {
    div {
      padding: 2% 5% 5% 5%;
    }
    .infoItem {
      margin-top: 5%;
      text-align: left;
      font-size: 11px;
    }
  }
}
</style>
