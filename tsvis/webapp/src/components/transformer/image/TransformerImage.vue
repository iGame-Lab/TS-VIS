<template>
  <div class="attentionmapBody">
    <div id="imgBox">
      <div id="leftBox">
        <div id="leftBoxTitle">
          <div class="titleIcon" style="margin-left: 30px"></div>
          <span class="titleText">图片展示</span>
        </div>
        <div id="originalImgBox">
          <div id="selectBox" :style="selectBoxStyle"></div>
          <img
            :src="getOriginImg"
            class="originalImg"
            @click.self="changeAttentionMap($event)"
          />
        </div>
        <div id="leftBoxBottom">
          <div id="leftBoxBottomIcon"></div>
          <span class="titleText" style="font-size: 12px">Selected Area</span>
        </div>
      </div>
      <div id="attentionMapBox">
        <div id="attentionMapBoxTitle">
          <div class="titleIcon"></div>
          <span class="titleText">Layer列表</span>
        </div>
        <div id="attentionMapBox-size-control">
          <div
            v-for="layer in Object.keys(attnMap).filter((el) => {
              if (getSelectLayer.includes(Number(el))) {
                return el;
              }
            })"
            :key="layer"
            class="layerBox"
          >
            <div style="width: 100%; height: 16px">
              <div class="am_box_title_circle"></div>
              <span class="layerBoxText"
                >Layer{{((Number(layer)+1) &lt; 10 ? '0':'')+ (Number(layer) + 1) }}</span
              >
            </div>

            <div class="img_box_content">
              <div
                class="attentionMap"
                v-for="(img, i) in attnMap[layer]"
                :key="i"
              >
                <el-image
                  :src="img"
                  :preview-src-list="[img]"
                  style="display: block"
                ></el-image>
                <div class="headTextBox">
                  <span class="headText"
                    >Head {{ ((Number(i)+1)&lt;10? '0':'')+(i + 1) }}</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { createNamespacedHelpers } from "vuex";
const { mapState: mapLayoutStates } = createNamespacedHelpers("layout");
const {
  mapActions: mapTransformerActions,
  mapGetters: mapTransformerGetters,
  mapMutations: mapTransformerMutations,
} = createNamespacedHelpers("transformer");
export default {
  data() {
    return {
      //markX,markY是当前标记点在图片上时所在的位置
      markX: 0,
      markY: 0,
      layer: "",
      originImgSize: 255,
      attnMap: {},
      selectBoxStyle: {
        top: "0px",
        left: "0px",
      },
    };
  },

  mounted() {
    this.setSelectX("0");
    this.setSelectY("0");
    this.emptyAttnData();
  },
  watch: {
    getAttnMap: {
      handler: function (e) {
        Object.keys(e).filter((el) => {
          if (this.getSelectLayer.includes(Number(el))) {
            this.$set(this.attnMap, el, e[el]);
          }
        });
      },
    },
  },
  computed: {
    ...mapLayoutStates(["userSelectRunFile"]),
    ...mapTransformerGetters([
      "getCategoryInfo",
      "getOriginImg",
      "getAttnMap",
      "getSelectImgTag",
      "getSelectLayer",
      "getSelectG",
      "getSelectR",
    ]),
  },
  methods: {
    ...mapTransformerActions(["fetchAttentionMap"]),
    ...mapTransformerMutations(["setSelectX", "setSelectY", "emptyAttnData"]),
    //鼠标移动时，记录位置
    markImg(e) {
      //offsetX,offsetY 鼠标坐标到元素的左侧，顶部的距离
      //target.offsetHeight,target.offsetWidth 目标的绝对尺寸
      //targrt.offsetTop,target.offsetLeft 目标的坐标
      this.markX = Math.min(
        Math.max(
          parseInt(
            (Number(e.offsetX) / Number(e.target.offsetWidth)) *
              this.originImgSize
          ),
          0
        ),
        249
      );
      this.markY = Math.min(
        Math.max(
          parseInt(
            (Number(e.offsetY) / Number(e.target.offsetHeight)) *
              this.originImgSize
          ),
          0
        ),
        249
      );
      if (e.offsetY <= 10) {
        this.selectBoxStyle.top = 0 + "px";
      } else if (e.offsetY >= e.target.offsetHeight - 10) {
        this.selectBoxStyle.top = e.target.offsetHeight - 21 + "px";
      } else {
        this.selectBoxStyle.top = e.offsetY - 10 + "px";
      }

      if (e.offsetX <= 10) {
        this.selectBoxStyle.left = 0 + "px";
      } else if (e.offsetX >= e.target.offsetWidth - 10) {
        this.selectBoxStyle.left = e.target.offsetWidth - 21 + "px";
      } else {
        this.selectBoxStyle.left = e.offsetX - 10 + "px";
      }
    },
    changeAttentionMap(e) {
      this.markImg(e);
      this.emptyAttnData();
      this.getAttentionMap();
      this.setSelectX(this.markX);
      this.setSelectY(this.markY);
    },
    getAttentionMap() {
      this.getSelectLayer.forEach((el) => {
        if (!Object.keys(this.getAttnMap).includes(String(el))) {
          let param = {
            run: this.userSelectRunFile,
            tag: this.getSelectImgTag,
            l: el,
            x: this.markX,
            y: this.markY,
            g: this.getSelectG,
            r: this.getSelectR,
          };
          this.fetchAttentionMap(param);
        }
      });
    },
  },
};
</script>
<style lang="less" scoped>
.attentionmapBody {
  height: 97.5%;
  margin: 1% 1% 0 1%;
  overflow-y: auto;
  background-color: white;
  border-radius: 5px 5px 0 0;
  box-shadow: rgba(0, 0, 0, 0.3) 0 0 10px;
}
#selectList {
  width: 100%;
  height: 9.5%;
  background-color: white;
  display: flex;
  align-items: center;
  border-bottom-style: solid;
  border-width: 1px;
}
.dropdownList {
  margin-left: 50px;
}
.dropDownSelectList {
  margin-left: 50px;
  width: 170px;
}
#imgBox {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
#leftBox {
  width: 40%;
  height: 100%;
  background-color: white;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-content: space-between;
}
#leftBoxTitle {
  display: flex;
  align-items: center;
  height: 10%;
  width: 100%;
}
.titleIcon {
  height: 15px;
  width: 15px;
  background-color: #625eb3;
  border-radius: 4px;
}
.titleText {
  margin-left: 10px;
  font-weight: bold;
}
#leftBoxBottom {
  height: 15%;
  width: 100%;
  display: flex;
}
#leftBoxBottomIcon {
  background-color: #3eb065;
  height: 14px;
  width: 14px;
  margin-left: 70%;
}
#attentionMapBoxTitle {
  display: flex;
  align-items: center;
  height: 10%;
  width: 100%;
}
.layerBoxText {
  line-height: 16px;
  font-size: 16px;
  font-weight: bold;
  margin-left: 2%;
  float: left;
}
.headTextBox {
  height: 20px;
  width: 100%;
  background-color: #625eb3;
  display: flex;
  align-items: center;
}
.headText {
  color: #fff;
  font-size: 14px;
  margin: 0 auto;
}
#originalImgBox {
  height: 55%;
  position: relative;
}
#originalImgBox:hover {
  box-shadow: 0 0 5px #000;
}
.originalImg {
  height: 100%;
}
#selectBox {
  border: 1px dashed #fff;
  background-color: rgba(62, 176, 101, 0.4);
  position: absolute;
  width: 20px;
  height: 20px;
}
#attentionMapBox {
  margin-left: 3%;
  width: 60%;
  height: 100%;
  background-color: white;
  overflow: hidden;
}
#attentionMapBox-size-control {
  overflow: auto;
  width: 100%;
  height: 88%;
}
#skeletonBox {
  width: 60%;
  height: 100%;
}
#rightBox {
  width: 55%;
  height: 100%;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}
.attentionMap {
  margin: 10px;
  width: 12%;
  // padding:0.5% 1%;
  // border: solid 1px #000;
  // margin: 5px 0.5% 0;
}
.layerBox {
  width: 100%;
}
.img_box_content {
  width: calc(98% - 9px);
  margin-left: 7px;
  border-left: 2px solid #aaa;
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  padding: 10px 0 20px 2%;
}
.am_box_title_circle {
  float: left;
  width: 10px;
  height: 10px;
  border: #625eb3 3px solid;
  border-radius: 8px;
  background-color: #fff;
}
</style>
