<style lang="scss" scoped>
.test {
  position: relative;
  background-color: #2c2d2f;
  opacity: 0.5;
  width: 80%;
  margin: 0 0 0 10%;
  padding: 2% 0 2% 0;
  color: white;
  p {
    padding: 1% 0 1% 0;
    margin: 0;
    position: relative;
  }
  .test-title {
    text-align: left;
    span {
      margin: 0 0 0 5%;
      font-size: 16px;
      font-weight: 600;
    }
  }
  .test-content {
    text-align: left;
    display: flex;
    font-size: 15px;
    .span-key {
      flex: 3;
      text-align: right;
      font-weight: 500;
    }
    .span-content {
      margin: 0 0 0 2%;
      text-align: left;
      flex: 7;
      font-weight: 500;
      white-space: pre-wrap;
      word-wrap: break-word;
      overflow: hidden;
      background-color: black;
    }
  }
}
</style>
<template>
  <div class="test">
    <p :class="['test-title']">
      <span>{{ name }}</span>
    </p>
    <p v-for="(item, key, i) in content" :key="i" :class="['test-content']">
      <span :class="['span-key']">{{ key }}:</span>
      <span :class="['span-content']">{{ item }}</span>
    </p>
  </div>
</template>
<script>
export default {
  props: {
    content: {
      type: Object
    },
    name: {
      type: String
    }
  },
  mounted () {
  }
}
</script>
