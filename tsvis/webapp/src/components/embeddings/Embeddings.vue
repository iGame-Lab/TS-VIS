<template>
  <div>
    <div class="temp">
      <div :class="['display-panel']">
        <embeddingDraw />
      </div>
    </div>
  </div>
</template>
<script>
import embeddingDraw from './EmbeddingDraw'
import { createNamespacedHelpers } from 'vuex'
const {
  mapGetters: mapEmbeddingGetters,
  mapActions: mapEmbeddingActions
} = createNamespacedHelpers('embedding')
const { mapState: mapLayoutStates } = createNamespacedHelpers('layout')
export default {
  components: {
    embeddingDraw: embeddingDraw
  },
  data() {
    return {
    }
  },
  computed: {
    ...mapEmbeddingGetters([
    ]),
    ...mapLayoutStates([
      'userSelectRunFile'
    ])
  },
  watch: {
  },
  created() {
  },
  methods: {
    ...mapEmbeddingActions([
    ])
  }
}
</script>
<style lang="less" scoped>
  .temp{
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
