<template>
  <div class="attention-metric-list">
    <div class="title">
      <div class="square"></div>
      <span>统计信息表</span>
    </div>
    <el-table border ref="infoTable"
      :default-sort="{prop: 'head', order: 'ascending'}" :data="infoData"
      style="width: 95%" :height="tableHeight"
      :row-class-name="tableRowClassName" @row-click="rowClick">
      <el-table-column prop="head" label="L-H" sortable>
      </el-table-column>
      <el-table-column prop="max" label="max" sortable>
      </el-table-column>
      <el-table-column prop="min" label="min" sortable>
      </el-table-column>
      <el-table-column prop="quar" label="quar" sortable>
      </el-table-column>
      <el-table-column prop="vari" label="vari" sortable>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { createNamespacedHelpers } from "vuex";

const {
  mapGetters: mapTransformerGetters,
  mapActions: mapTransformerActions,
  mapMutations: mapTransformerMutations,
} = createNamespacedHelpers("transformer");
export default {
  name: '',
  components: {
  },
  props: {
    infoData: Array
  },
  data () {
    return {
      attentionInfoTitle: "统计信息表",
      screenHeight: 0,
      screenWidth: 0,
      tableHeight: null,
    }
  },
  computed: {
    ...mapTransformerGetters([
      "getSelectedLH"
    ]),
  },
  watch: {
    screenHeight: {
      handler (newVal, oldVal) {
        if (newVal) {
          this.tableHeight = newVal * 0.6 + "px";
        }

        if (newVal && oldVal != 0) {
          this.setChartHeightScale((newVal / oldVal).toFixed(4));
        }
      },
      immediate: true,
      deep: true
    },
    screenWidth: {
      handler (newVal, oldVal) {
        if (newVal && oldVal != 0) {
          this.setChartWidthScale((newVal / oldVal).toFixed(4));
        }
      },
      immediate: true,
      deep: true
    }
  },
  created () {
  },
  mounted () {
    this.screenHeight = window.innerHeight;
  },
  updated () {
    window.onresize = () => {
      return (() => {
        this.screenHeight = window.innerHeight;
        this.screenWidth = window.innerWidth;
      })();
    };
  },
  methods: {
    ...mapTransformerMutations([
      "setSelectedLH",
      "setChartWidthScale",
      "setChartHeightScale"
    ]),
    tableRowClassName ({ row, rowIndex }) {
      if (row["head"] == this.getSelectedLH) {
        this.tableScrollMove("infoTable", rowIndex);
        return 'active-row';
      }
    },
    tableScrollMove (refName, index = 0) {
      //不存在表格的ref vm 则返回
      if (!refName || !this.$refs[refName]) {
        return;
      }

      let vmEl = this.$refs[refName].$el;

      if (!vmEl) {
        return;
      }

      //计算滚动条的位置
      const targetTop = vmEl.querySelectorAll('.el-table__body tr')[index].getBoundingClientRect().top;
      const containerTop = vmEl.querySelector('.el-table__body').getBoundingClientRect().top;
      const scrollParent = vmEl.querySelector('.el-table__body-wrapper');
      scrollParent.scrollTop = targetTop - containerTop;
    },
    rowClick (e) {
      this.setSelectedLH(e.head);
    }
  }
}
</script>

<style scoped lang="less">
/deep/ .attention-metric-list {
  height: 100%;
}

/deep/ .title {
  margin-bottom: 20px;
  display: flex;
  flex-direction: row;

  .square {
    width: 20px;
    height: 20px;
    border-radius: 5px;
    background: #625eb3;
    margin-right: 5px;
  }
  span {
    font-weight: bold;
    font-size: 20px;
    line-height: 20px;
    font-family: 'Times New Roman', Times, serif;
  }
}

/deep/ .el-table {
  .el-table__header-wrapper {
    .el-table__header {
      thead {
        th {
          padding: 2px 0 2px 0;
          border-left: none;
          border-right: none;
        }
      }
    }
  }

  .el-table__body-wrapper {
    .el-table__body {
      tbody {
        tr,
        td {
          border: none;
        }
      }
    }
  }
}

/deep/ .el-table th.gutter {
  display: table-cell !important;
}

/deep/ .active-row {
  background: #cfd8ff;
}
</style>
