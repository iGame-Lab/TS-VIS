<template>
  <div class="temp">
    <component v-if="reload" :is="currentView" />
  </div>
</template>

<script>
import { createNamespacedHelpers } from "vuex";
import TransformerText from "./text/TransformerText";
import TransformerImage from "./image/TransformerImage";
const { mapState: mapLayoutStates } = createNamespacedHelpers("layout");
const { mapGetters: maptransformerGetters } =
  createNamespacedHelpers("transformer");

export default {
  components: {
    TransformerText,
    TransformerImage,
  },
  data() {
    return {
      currentView: "TransformerText",
      reload: "true",
    };
  },
  computed: {
    ...mapLayoutStates(["userSelectRunFile"]),
    ...maptransformerGetters(["getCategoryInfo"]),
  },
  created() {},
  mounted() {
    if (this.getCategoryInfo[0]) {
      let index = this.getCategoryInfo[0].indexOf(this.userSelectRunFile);
      if (index > -1) {
        let arr = this.getCategoryInfo[1][index][0].split("-");
        if (arr[1] == "transformertext") {
          this.currentView = "TransformerText";
        } else {
          this.currentView = "TransformerImage";
        }
      }
    }
  },
  watch: {
    userSelectRunFile(val) {
      let index = this.getCategoryInfo[0].indexOf(val);
      if (index > -1) {
        this.reload = false;
        let arr = this.getCategoryInfo[1][index][0].split("-");
        if (arr[1] == "transformertext") {
          this.currentView = "TransformerText";
        } else {
          this.currentView = "TransformerImage";
        }
      }
      this.$nextTick(() => {
        this.reload = true;
      });
    },
  },
  methods: {},
};
</script>
<style scoped>
</style>