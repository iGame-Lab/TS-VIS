<template>
  <div class="highlight-item">
    {{ index }}
  </div>
</template>

<script>
export default {
  name: '',
  components: {},
  props: {
    index: {
      type: [String, Number]
    },
  },
  data () {
    return {}
  },
  computed: {},
  watch: {},
  created () { },
  mounted () { },
  methods: {}
}
</script>

<style scoped lang="less">
.highlight-item {
  width: 30px;
  height: 20px;
  border-radius: 5px;
  background-color: #e6ebff;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
