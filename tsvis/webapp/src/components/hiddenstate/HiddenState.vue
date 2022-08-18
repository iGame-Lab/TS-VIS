<template>
  <div class="hidden-state">
    <div class="temp">
      <state-vis :stateData="getStateData" v-if="getStateData"></state-vis>
    </div>
  </div>
</template>

<script>
import StateVis from "./StateVis"
import { createNamespacedHelpers } from "vuex";
const {
  mapGetters: mapHiddenStateGetters,
  mapMutations: mapHiddenStateMutations,
  mapActions: mapHiddenStateActions
} = createNamespacedHelpers("hiddenstate");

const {
  mapState: mapLayoutStates
} = createNamespacedHelpers("layout");

export default {
  name: 'HiddenState',
  components: {
    StateVis
  },
  props: {},
  data () {
    return {
      screenWidth: 0,
      screenHeight: 0,
      userRun: "",
      userTag: "",
      range: 0
    }
  },
  computed: {
    ...mapHiddenStateGetters([
      "getStateData",
      "getStateRun",
      "getStateTag",
      "getPos",
      "getRange",
      "getSelectedLineIndexs"
    ]),
    ...mapLayoutStates([
      "userSelectRunFile"
    ]),
  },
  watch: {
    userSelectRunFile (val) {
      this.setSelectedLineIndexs([]);
      this.setSelectedRange([]);
      this.setStateMatchData([]);
      this.setThreshold(0);
      this.setPos(0);
      this.range = Math.floor(((this.screenWidth - 470) * 0.81 - 35) / 30);
      this.setRange(this.range);

      this.userRun = val;
      this.userTag = this.getStateTag;
      const param = {
        run: this.userRun,
        tag: this.userTag,
        pos: this.getPos,
        range: this.getRange,
      };
      this.getHiddenStateData(param);
      this.setStateRun(this.userRun);
      this.setStateTag(this.userTag);
    },
    screenWidth (val) {
      this.range = Math.floor(((val - 470) * 0.81 - 35) / 30);
      this.setRange(this.range);

      const param = {
        run: this.userRun,
        tag: this.userTag,
        pos: this.getPos,
        range: this.getRange,
      };
      this.getHiddenStateData(param);
    }
  },
  created () {
    this.setSelectedLineIndexs([]);
    this.setSelectedRange([]);
    this.setStateMatchData([]);

    this.screenHeight = window.innerHeight;
    this.screenWidth = window.innerWidth;

    this.userRun = this.getStateRun;
    this.userTag = this.getStateTag;
    const param = {
      run: this.userRun,
      tag: this.userTag,
      pos: this.getPos,
      range: this.getRange,
    }
    this.getHiddenStateData(param);
    this.setStateRun(this.userRun);
    this.setStateTag(this.userTag);
  },
  mounted () {
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
    ...mapHiddenStateActions([
      "getHiddenStateData"
    ]),
    ...mapHiddenStateMutations([
      "setThreshold",
      "setRange",
      "setPos",
      "setStateRun",
      "setStateTag",
      "setSelectedLineIndexs",
      "setSelectedRange",
      "setStateMatchData"
    ])
  },
}
</script>

<style scoped lang="less">
.hidden-state {
  width: 100%;
  height: 100%;
  background-color: white;
}

.temp {
  height: 97.5%;
  margin: 1% 1% 0 1%;
  overflow-y: auto;
  background-color: white;
  border-radius: 5px 5px 0 0;
  box-shadow: rgba(0, 0, 0, 0.3) 0 0 10px;
}
</style>
