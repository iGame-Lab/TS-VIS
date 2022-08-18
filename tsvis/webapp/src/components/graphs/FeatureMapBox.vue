<template>
  <div id="feature_map">
    <div class="fm_title">
      <el-tooltip
        effect="light"
        content="请选择特征图方法"
        placement="top-start"
      >
        <el-select v-model="selectType" size="mini">
          <el-option
            v-for="(type, i) in getFmType[userSelectRunFile]
              ? Object.keys(getFmType[userSelectRunFile])
              : ''"
            :key="i"
            :label="type.replace(type[0],type[0].toUpperCase())"
            :value="type"
          >
          </el-option>
        </el-select>
      </el-tooltip>

      <el-tooltip
        effect="light"
        content="展开显示特征图"
        placement="top-start"
        v-show="getFoldTag"
      >
        <img
          src="../../assets/featuremap_fold.svg"
          style="height: 50%"
          @click="setFoldTag"
        />
      </el-tooltip>
      <div style="width: 35%" v-show="!getFoldTag"></div>
      <div class="fm_op" @click="changeFmContent()" v-show="!getFoldTag">
        显示分类结果
      </div>
      <div class="fm_op" @click="resetGraphNode()" v-show="!getFoldTag">
        清空
      </div>
      <el-tooltip
        effect="light"
        content="缩小显示特征图"
        placement="top-start"
        v-show="!getFoldTag"
      >
        <img
          src="../../assets/featuremap_unfold.svg"
          style="height: 50%"
          @click="setFoldTag"
        />
      </el-tooltip>
    </div>
    <div :class="getFoldTag ? 'fm_content' : 'fm_content_unfold'">
      <div
        v-for="(fm, i) in featureMapData"
        :key="i"
        class="fm_box"
        :id="fm[0]"
      >
        <div class="fm_box_title">
          <div class="fm_box_title_circle"></div>
          <span style="margin-left: 10px; font-size: 12px; font-weight: bold">{{
            fm[0][0].slice(fm[0][0].indexOf("to") + 2, fm[0][0].indexOf("-"))
          }}</span>
        </div>
        <div
          :class="[
            'fm_box_content',
            getFoldTag ? 'fm_box_content_fold' : 'fm_box_content_unfold',
          ]"
        >
          <el-card
            :class="['fm-card', getFoldTag ? 'fm-card-fold' : 'fm-card-unfold']"
            v-for="(img, i) in fm[1]"
            :key="i"
          >
            <el-image
              class="fmShow"
              :tag="i"
              :src="img"
              :preview-src-list="[img]"
              :style="
                showLabel ? `box-shadow: 0 0 3px 2px ${setFmColor(i)};` : ''
              "
              @mouseenter="createFmInfo($event)"
              @mousemove="showFmInfo($event)"
              @mouseleave="removeFmInfo()"
            ></el-image>
          </el-card>
          <div style="width: 100%; height: 20px" v-show="!getFoldTag">
            <span class="more-btn" @click="loadMoreFm($event)">更多</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { createNamespacedHelpers } from "vuex";
const {
  mapGetters: mapGraphGetters,
  mapActions: mapGraphActions,
  mapMutations: mapGraphMutations,
} = createNamespacedHelpers("graph");
const { mapState: mapLayoutStates } = createNamespacedHelpers("layout");
export default {
  name: "FeatureMapBox",
  data() {
    return {
      featureMapData: [],
      showLabel: false,
    };
  },
  computed: {
    ...mapGraphGetters([
      "getFeatureMapData",
      "getFeatureMapType",
      "getFeatureMapInfo",
      "getTaskType",
      "getFmType",
      "getSelectFmType",
      "getFoldTag",
    ]),
    ...mapLayoutStates(["userSelectRunFile"]),
    selectType: {
      get() {
        return this.getSelectFmType;
      },
      set(val) {
        this.setSelectFmType(val);
      },
    },
  },
  watch: {
    getFeatureMapData: {
      handler: function () {
        this.featureMapData = this.getFeatureMapData;
      },
    },
    selectType(val) {
      this.setFeatureMapType(val);
      this.resetGraphNode();
    },
  },
  mounted() {
  },
  methods: {
    ...mapGraphMutations([
      "setFeatureMapType",
      "clearFeatureMap",
      "setSelectFmType",
      "setFoldTag",
    ]),
    ...mapGraphActions(["fetchFeatures"]),
    loadMoreFm(event) {
      let node = event.currentTarget;
      let content = d3.select(node.parentNode.parentNode.parentNode);
      let imgNumber = content.selectAll("img")._groups[0].length;
      let fmType = this.getFeatureMapType;
      let tag = content.attr("id");
      if (fmType !== "") {
        let para = {
          run: this.userSelectRunFile,
          tag: tag,
          range: imgNumber,
          task: this.getTaskType[this.userSelectRunFile],
        };
        this.fetchFeatures(para);
      }
    },
    createFmInfo(event) {
      let fmBox = d3.select("#full-screen1");
      let x = event.x - 300;
      let y = event.y - 40;
      let fmInfo = fmBox
        .append("div")
        .attr("id", "fmInfo")
        .style("left", x + "px")
        .style("top", y + "px");
      let index = Number(d3.select(event.currentTarget).attr("tag"));

      let tempSocre = Object.assign(
        {},
        this.getFeatureMapInfo["sorce_data"][index]
      );
      let sorted = Object.keys(tempSocre).sort((a, b) => {
        return tempSocre[b] - tempSocre[a];
      });
      //如果是多分类任务，只取最高的十类
      if (sorted.length > 10) {
        sorted = sorted.splice(10);
      }
      sorted.forEach((index) => {
        fmInfo
          .append("p")
          .text(index + " : " + Number(tempSocre[index]).toFixed(4))
          .style("margin", "2px");
      });
    },
    showFmInfo(event) {
      let fmInfoBox = d3.select("#fmInfo");
      let x = event.x - 300;
      let y = event.y - 40;
      fmInfoBox.style("left", x + "px").style("top", y + "px");
    },
    removeFmInfo() {
      d3.select("#full-screen1").selectAll("#fmInfo").remove();
    },
    resetGraphNode() {
      this.clearFeatureMap("all");
      d3.selectAll(".node").select("#shadow").remove();
      let node = d3.selectAll(".node")._groups[0];
      for (let i = 0; i < node.length; i++) {
        let nodeId = node[i].id;
        let clicked = d3
          .select(this.idTransformerFrontend(`#${nodeId}`))
          .attr("clicked");
        if (clicked === "1") {
          d3.select(this.idTransformerFrontend(`#${nodeId}`)).attr(
            "clicked",
            "0"
          );
          let translate_str = d3
            .select(this.idTransformerFrontend(`#${nodeId}`))
            .attr("transform");
          let translate_x =
            parseFloat(
              translate_str.substring(
                translate_str.indexOf("(") + 1,
                translate_str.indexOf(",")
              )
            ) + 10;
          let translate_y =
            parseFloat(
              translate_str.substring(
                translate_str.indexOf(",") + 1,
                translate_str.indexOf(")")
              )
            ) + 10;
          d3.select(this.idTransformerFrontend(`#${nodeId}`)).attr(
            "transform",
            "translate(" + translate_x + "," + translate_y + ")"
          );
        }
      }
    },
    setFmColor(key) {
      let indexOfMax = this.getFeatureMapInfo["sorce_data"][key].indexOf(
        Math.max(...this.getFeatureMapInfo["sorce_data"][key])
      );
      if (this.getFeatureMapInfo["label"][key] == indexOfMax) {
        return "#00ff00";
      } else {
        return "#FF0000";
      }
    },
    changeFmContent() {
      this.showLabel = !this.showLabel;
    },
    idTransformerFrontend(id) {
      var index = 0;
      var id = id
        .replace(/\//g, "\\/")
        .replace(/\(/g, "\\(")
        .replace(/\)/g, "\\)")
        .replace(/\]/g, "\\]")
        .replace(/\[/g, "\\[")
        .replace(/\./g, "\\.");
      if (id[0] === "#") {
        index = 1;
      }
      var newId = "";
      while (!isNaN(parseInt(id[index])) && index < id.length) {
        newId = `${newId}\\3${id[index]}`;
        index += 1;
      }
      newId = `${newId}${id.substring(index)}`;
      if (id[0] === "#") {
        newId = `#${newId}`;
      }
      return newId;
    },
  },
};
</script>
<style>
#fm_select {
  height: 25px;
  width: 100px;
}
.fm_op {
  padding: 0px 5px;
  height: 20px;
  font-size: 13px;
  text-align: center;
  line-height: 20px;
  background-color: #625eb3;
  border-radius: 3px;
  color: #fff;
}
.fm_op:hover {
  background-color: #fff;
  color: #625eb3;
}
.fm_title {
  width: 100%;
  height: 40px;
  background-color: #d8dfff;
  border-radius: 3px 3px 0 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
}
.fm_content {
  height: calc(100% - 40px);
  overflow-y: auto;
  width: 100%;
  border-radius: 0 0 3px 3px;
}
.fm_content_unfold {
  height: calc(100% - 50px);
  overflow-y: auto;
  width: 100%;
  border-radius: 0 0 3px 3px;
  padding-top: 10px;
}
.fm_box_title {
  display: flex;
  align-items: center;
  width: 100%;
  height: 16px;
}
.fm_box_title_circle {
  width: 10px;
  height: 10px;
  border: #625eb3 3px solid;
  border-radius: 8px;
  background-color: #fff;
  margin-left: 20px;
}
.fm_box_content {
  margin-left: 27px;
  border-left: 2px solid #ccc;
  padding: 5px 0px 5px 20px;
  display: flex;
}
.fm_box_content_unfold {
  width: calc(100% - 30px);
  flex-wrap: wrap;
}
.fm_box_content_fold {
  width: auto;
  overflow-x: auto;
  overflow-y: hidden;
  white-space: nowrap;
}
.fm_box {
  width: 100%;
  background-color: #fff;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}
.fmTitle {
  margin-top: 0px;
  margin-bottom: 5px;
  width: 90%;
}
.fmCompareSelect {
  height: 100%;
  margin-left: 5px;
}
.fmShow {
  width: 95%;
}
.more-btn {
  line-height: 20px;
  color: #625eb3;
  
}
#fmInfo {
  width: 100px;
  background: rgba(216, 223, 255, 0.9);
  border-radius: 12px;
  position: absolute;
  z-index: 20;
}
.more-btn:hover {
  font-weight: bold;
}
.small-header {
  width: 100%;
  height: 20px;
  display: flex;
  align-items: center;
}
.small-label-container {
  background-color: #625eb3;
  width: 7%;
  height: 70%;
}
.small-triangle-container {
  width: 0;
  height: 0;
  border-top: 7px solid transparent;
  border-left: 10px solid #625eb3;
  border-bottom: 7px solid transparent;
}
.triangle-container {
  width: 90%;
  height: 2px;
  background-color: #f4f5ff;
}
.fm-card {
  margin-top: 1px;
  margin-left: 1px;
  margin-right: 1px;
}
.fm-card-unfold {
  width: 11.8%;
}
.fm-card-fold {
  width: 100px;
  flex: 0 0 auto;
}
.el-card__body {
  padding: 4px;
}
</style>