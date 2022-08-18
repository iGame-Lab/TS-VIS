<template>
  <div class="transformer-text">
    <div class="visualization">
      <text-attention-vis :allAttentionData="allData.data" :key="allData.id">
      </text-attention-vis>
    </div>
  </div>
</template>

<script>
import { createNamespacedHelpers } from "vuex";
import TextAttentionVis from "./TextAttentionVis";

const {
  mapGetters: mapTransformerGetters,
} = createNamespacedHelpers("transformer");

export default {
  components: {
    TextAttentionVis,
  },
  data () {
    return {
      allData: {},
    };
  },
  computed: {
    ...mapTransformerGetters([
      "getAllData",
    ]),
  },
  watch: {
    getAllData (val) {
      let textdata = {
        id: Object.keys(val)[0],
        data: val[Object.keys(val)[0]].data,
      };
      this.allData = textdata;
    }
  }
};
</script>
<style scoped>
.transformer-text {
  width: 100%;
  height: 100%;
  background-color: white;
}

.visualization {
  height: 97.5%;
  margin: 1% 1% 0 1%;
  overflow-y: auto;
  background-color: white;
  border-radius: 5px 5px 0 0;
  box-shadow: rgba(0, 0, 0, 0.3) 0 0 10px;
}
</style>