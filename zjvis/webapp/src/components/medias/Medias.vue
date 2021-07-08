<style lang="less" scoped>
  .medias{
      // position: absolute;
      height: 100%;
      overflow-y: auto;
      width: 100%;
      background-color:white;
  }
  .testDiv{
      margin: 1% 1% 0 1%;
      height: 97.5%;
      border-radius: 5px 5px 0 0;
      background-color: white;
      overflow-y: auto;
  }
  .display-panel{
      margin: 1% 1% 0 1%;
      height: 97.5%;
      border-radius: 5px 5px 0 0;
      box-shadow: rgba(0,0,0,.3) 0px 0px 10px;
      background-color: white;
      overflow-y: auto;
      min-width: 400px;
    }
  .content{
    margin-bottom: 0.5%;
  }
</style>
<template>
  <div>
    <div class="medias">
      <!-- v-if="totaltag != ''" -->
      <div :class="['display-panel']">
        <div v-for="(value, name, index) in totaltag" :key="index">
          <component :is="type[name]" :value="value" :subname="name" :index="index" class="content" />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { images } from './image'
import { audios } from './audio'
import { texts } from './text'
import { createNamespacedHelpers } from 'vuex'
const {
  mapMutations: mapCustomMutations
} = createNamespacedHelpers('custom')
const { mapGetters: mapMediaGetters, mapMutations: mapMediaMutations, mapActions: mapMediaActions } = createNamespacedHelpers('media')
export default {
  components: {
    images, audios, texts
  },
  data() {
    return {
      type: {
        'audio': 'audios',
        'image': 'images',
        'text': 'texts'
      },
      data: [],
      totaltag: ''
    }
  },
  beforeRouteLeave(to, from, next) {
    this.setRouter(2)
    next()
  },
  computed: {
    ...mapMediaGetters([
      'categoryInfo',
      'getTotaltag',
      'getFreshInfo',
      'getErrorMessage'
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
    }
  },
  mounted() {
    if (this.getTotaltag !== '') {
      this.totaltag = this.getTotaltag
    } else {
      this.settotaltag()
    }
  },
  methods: {
    ...mapCustomMutations(['setRouter']),
    ...mapMediaMutations(['setTotaltag']),
    ...mapMediaActions([
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
