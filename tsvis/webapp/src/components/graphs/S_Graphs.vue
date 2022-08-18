/** Copyright 2021 Tianshu AI Platform. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =============================================================
 */

<template>
  <div style="position: relative">
    <div id="test" class="Graph">
      <svg id="svg-canvas">
        <g id="draw" />
      </svg>
      <iframe
        id="size-watch"
        style="width: 100%; height: 0; border: 0"
      ></iframe>
    </div>
  </div>
</template>
<script>
import * as d3 from "d3";
import dagreD3 from "dagre-d3/dist/dagre-d3";
import { createNamespacedHelpers } from "vuex";
const {
  mapGetters: mapGraphGetters,
  mapActions: mapGraphActions,
  mapMutations: mapGraphMutations,
} = createNamespacedHelpers("graph");
const { mapState: mapLayoutStates } = createNamespacedHelpers("layout");
export default {
  name: "S_Graph",
  data() {
    return {
      graphData: "",
    };
  },
  computed: {
    ...mapGraphGetters([
      "getStructureGraphData",
      "getTagName",
      "getRunName",
      "getCurTag",
      "getFmType",
      "getSelectFmType",
      "getTaskType",
    ]),
    ...mapLayoutStates(["userSelectRunFile"]),
  },
  watch: {
    getStructureGraphData(val) {
      if (val !== "") {
        this.graphData = val;
        this.drawGraph();
      }
    },
    userSelectRunFile(val) {
      let k = 0;
      for (let i = 0; i < this.getRunName.length; i += 1) {
        if (val === this.getRunName[i]) {
          k = i;
          break;
        }
      }
      this.setCurTag(this.getTagName[k][0]);
      const param = { run: val, tag: this.getCurTag };
      this.getFullData(param);
    },
    getSelectFmType(val) {
      this.signAvailableNode(val);
    },
  },

  mounted() {
    this.clearFeatureMap("all");
    this.graphData = this.getStructureGraphData;
    if (this.graphData === "") {
      const param = { run: this.userSelectRunFile, tag: this.getCurTag };
      this.getFullData(param);
    } else {
      this.drawGraph();
    }
    //当sGraph画布大小变化时，调整图居中
    //size-watch用于检测画布大小变化，graphSizeWatch用于给元素el绑定resize事件
    let el = document.querySelector("#size-watch");
    this.graphSizeWatch(el);
  },
  methods: {
    ...mapGraphActions(["getFullData", "fetchFeatures"]),
    ...mapGraphMutations(["setCurTag", "clearFeatureMap"]),
    drawGraph() {
      const self = this;
      const {
        userSelectRunFile,
        idTransformerFrontend,
        edgeLabelAnimation,
        getFMType,
        fetchFeatures,
        clearFeatureMap,
        getTaskType,
      } = this;
      const data = this.graphData;
      if (data === undefined) {
        return;
      }
      //根据label返回节点颜色，结构图使用
      function GetStyleByLabel(label) {
        let sd = new Array("", "");
        let sp = [
          "Identity",
          "RNN",
          "RNNBase",
          "LSTM",
          "GRU",
          "RNNCellBase",
          "RNNCell",
          "LSTMCell",
          "GRUCell",
          "BertLayer",
          "BertEmbeddings",
          "Flatten",
          "Unflatten",
        ];
        let activation = [
          "Threshold",
          "ReLU",
          "Hardtanh",
          "ReLU6",
          "Sigmoid",
          "Tanh",
          "Softmax",
          "Softmax2d",
          "LogSoftmax",
          "ELU",
          "SELU",
          "CELU",
          "GELU",
          "Hardshrink",
          "LeakyReLU",
          "LogSigmoid",
          "Softplus",
          "Softshrink",
          "MultiheadAttention",
          "PReLU",
          "Softsign",
          "Softmin",
          "Tanhshrink",
          "RReLU",
          "GLU",
          "Hardsigmoid",
          "Hardswish",
          "SiLU",
          "Mish",
          "listconstruct",
          "cat",
          "constant",
          "flatten",
          "add",
          "size",
          "numtotensor",
          "int",
          "view",
          "unsqueeze",
          "rsub",
          "mul",
          "expand",
          "select",
        ];
        let conv = [
          "Conv1d",
          "Conv2d",
          "Conv3d",
          "ConvTranspose1d",
          "ConvTranspose2d",
          "ConvTranspose3d",
          "LazyConv1d",
          "LazyConv2d",
          "LazyConv3d",
          "LazyConvTranspose1d",
          "LazyConvTranspose2d",
          "LazyConvTranspose3d",
          "Linear",
          "Bilinear",
          "LazyLinear",
          "AvgPool1d",
          "AvgPool2d",
          "AvgPool3d",
          "MaxPool1d",
          "MaxPool2d",
          "MaxPool3d",
          "MaxUnpool1d",
          "MaxUnpool2d",
          "MaxUnpool3d",
          "FractionalMaxPool2d",
          "FractionalMaxPool3d",
          "LPPool1d",
          "LPPool2d",
          "AdaptiveMaxPool1d",
          "AdaptiveMaxPool2d",
          "AdaptiveMaxPool3d",
          "AdaptiveAvgPool1d",
          "AdaptiveAvgPool2d",
          "AdaptiveAvgPool3d",
        ];
        let other = [
          "L1Loss",
          "NLLLoss",
          "KLDivLoss",
          "MSELoss",
          "BCELoss",
          "BCEWithLogitsLoss",
          "NLLLoss2d",
          "CosineEmbeddingLoss",
          "CTCLoss",
          "HingeEmbeddingLoss",
          "MarginRankingLoss",
          "MultiLabelMarginLoss",
          "MultiLabelSoftMarginLoss",
          "MultiMarginLoss",
          "SmoothL1Loss",
          "HuberLoss",
          "SoftMarginLoss",
          "CrossEntropyLoss",
          "TripletMarginLoss",
          "TripletMarginWithDistanceLoss",
          "PoissonNLLLoss",
          "GaussianNLLLoss",
          "BatchNorm1d",
          "BatchNorm2d",
          "BatchNorm3d",
          "SyncBatchNorm",
          "LazyBatchNorm1d",
          "LazyBatchNorm2d",
          "LazyBatchNorm3d",
          "InstanceNorm1d",
          "InstanceNorm2d",
          "InstanceNorm3d",
          "LazyInstanceNorm1d",
          "LazyInstanceNorm2d",
          "LazyInstanceNorm3d",
          "LocalResponseNorm",
          "CrossMapLRN2d",
          "LayerNorm",
          "GroupNorm",
          "Dropout",
          "Dropout2d",
          "Dropout3d",
          "AlphaDropout",
          "FeatureAlphaDropout",
          "ReflectionPad1d",
          "ReflectionPad2d",
          "ReflectionPad3d",
          "ReplicationPad1d",
          "ReplicationPad2d",
          "ReplicationPad3d",
          "ZeroPad2d",
          "ConstantPad1d",
          "ConstantPad2d",
          "ConstantPad3d",
        ];
        let i_o = ["Input", "output"];
        //该部分需要修改
        if (i_o.includes(label)) {
          sd[0] = "#b0cfeb";
          sd[1] = 120;
        } else if (activation.includes(label)) {
          sd[0] = "#6584ff";
          sd[1] = 70;
        } else if (other.includes(label)) {
          sd[0] = "#dbd65f";
          sd[1] = 120;
        } else if (sp.includes(label)) {
          sd[0] = "#ade292";
          sd[1] = 150;
        } else if (conv.includes(label)) {
          sd[0] = "#3e39a3";
          sd[1] = 120;
        } else {
          sd[0] = "#eeeeee";
          sd[1] = 120;
        }
        if (label.length > 13) {
          sd[1] = 20 * label.length;
        } else if (label.length < 5) {
          sd[1] = 70;
        }
        return sd;
      }
      // 画图
      // eslint-disable-next-line
      const draw = function (data, init) {
        d3.select("#svg-canvas").select("g").selectAll("g").remove();
        const g = new dagreD3.graphlib.Graph({ compound: true })
          .setGraph({})
          .setDefaultEdgeLabel(() => {
            return {};
          });
        data.forEach((v) => {
          v.id = v.uid;
          if (v.label) {
            let index;
            if (v.label.indexOf("[") > 0) {
              index = v.label.indexOf("[");
              v.label = v.label.substring(0, index);
            } else if (v.label.indexOf("_") > 0) {
              index = v.label.indexOf("_");
              v.label = v.label.substring(0, index);
            } else {
              v.label = v.label;
            }
          }
          g.setNode(v.uid, v);
          v.targets.forEach((u) => {
            // if (find(u.id)) {
            const edgeLabel = `${v.uid}__${u.id}`;
            g.setEdge(v.uid, u.id, {
              id: edgeLabel,
              label: u.info,
              curve: d3.curveBasis,
            });
          });
        });
        // 设置节点样式
        g.nodes().forEach((v) => {
          const node = g.node(v);
          if (node !== undefined) {
            if (node.type == "VirtualNode") {
              node.rx = node.ry = 20;
              node.width = 5;
              node.height = 5;
              node.style = "fill:#625eb3;stroke-width:0.5;stroke:black";
              node.labelStyle = "fill:#fff;font-weight:500";
              node.label = "v";
            } else {
              let style_data = GetStyleByLabel(node.label);
              node.rx = node.ry = 10;
              node.width = style_data[1];
              node.height = 20;
              node.style = `fill:${style_data[0]};stroke-width:0.5;stroke:black`;
              node.labelStyle = "fill:#fff;font-weight:500";
              if (node.label === "input" || node.label === "output") {
                node.labelStyle = "fill:#000;font-weight:500";
              }
            }
          }
        });

        const render = new dagreD3.render();
        const svg = d3.select("#svg-canvas");
        render(d3.select("#svg-canvas g"), g);
        d3.selectAll(".edgeLabel").style("visibility", "hidden");
        d3.select("#svg-canvas").attr("width", "100%").attr("height", "100%");
        // 初次绘制中将图居中,并设置zoom的初始位置
        if (init) {
          init = false;
          const canvas = d3.select("#svg-canvas")._groups[0][0];
          const canvasHeight = canvas.scrollHeight;
          const canvasWidth = canvas.scrollWidth;
          const graph = d3.select("#svg-canvas g")._groups[0][0];
          const graphHeight = graph.getBBox().height;
          const graphWidth = graph.getBBox().width;
          const index = Math.min(
            canvasHeight / graphHeight,
            canvasWidth / graphWidth,
            1
          );
          const scale = `scale(${index})`;
          d3.select("#svg-canvas g").attr(
            "transform",
            ` translate(${(canvasWidth - graphWidth * index) / 2},${
              (canvasHeight - graphHeight * index) / 2
            }) ${scale}`
          );
          const transform = d3
            .zoomTransform(0)
            .translate(
              (canvasWidth - graphWidth * index) / 2,
              (canvasHeight - graphHeight * index) / 2
            )
            .scale(index);
          d3.zoom().transform(svg, transform);
        }

        edgeLabelAnimation();
        //滚动放大，拖拽移动
        const zoom = d3.zoom().on("zoom", () => {
          d3.select("#svg-canvas g").attr("transform", d3.event.transform);
        });
        svg.call(zoom).on("dblclick.zoom", null);

        //连接线样式
        d3.selectAll(".path")
          .style("fill-opacity", 1)
          .style("stroke", "black")
          .style("stroke-opacity", 1)
          .attr("marker-start", "url(#dot)");

        // 功能：为每个节点添加动画
        svg.selectAll(".node")._groups[0].forEach((nodeKey) => {
          let nodeName = nodeKey.id;
          nodeName = nodeName.split("/");
          nodeName = nodeName[nodeName.length - 1];
          nodeName = nodeName.slice(0, nodeName.length);
          const nodeId = idTransformerFrontend(nodeKey.id);
          const nodeThis = d3.select(nodeKey);

          nodeThis.on("mouseenter", () => {
            //鼠标悬浮在节点上时，节点的样式改变
            let cl = d3
              .select(`#${nodeId}`)
              .select(".label-container")
              .style("fill");
            d3.select(`#${nodeId}`)
              .select(".label-container")
              .style("fill", "#fff");

            d3.select(`#${nodeId}`)
              .select("g")
              .select("g")
              .select("text")
              .style("fill", cl)
              .style("font-weight", "520");
            d3.select(`#${nodeId}`)
              .select(".sign-available")
              .select(".sign-available-circle")
              .style("fill", cl);
            d3.select(`#${nodeId}`)
              .select(".sign-available")
              .selectAll(".sign-available-content")
              .style("fill", "#fff");
          });
          nodeThis.on("mouseleave", () => {
            // d3.select(`#${nodeId}`).attr("flag", 0);
            // d3.select("#messageBox").remove();
            let cl = d3
              .select(`#${nodeId}`)
              .select("g")
              .select("g")
              .select("text")
              .style("fill");
            d3.select(`#${nodeId}`)
              .select(".label-container")
              .style("fill", cl);

            d3.select(`#${nodeId}`)
              .select("g")
              .select("g")
              .select("text")
              .style("fill", "#fff")
              .style("font-weight", "500");
            d3.select(`#${nodeId}`)
              .select(".sign-available")
              .select(".sign-available-circle")
              .style("fill", "#fff");
            d3.select(`#${nodeId}`)
              .select(".sign-available")
              .selectAll(".sign-available-content")
              .style("fill", cl);
          });
          //单击事件
          nodeThis.on("click", () => {
            //结构图的点击事件 需要修改添加点击之后传递点击的节点的数据至后端

            let fmType = getFMType();

            if (fmType !== undefined) {
              let tag = d3
                .select(idTransformerFrontend(`#${nodeKey.id}`))
                .attr("clicked");
              if (tag === "1") {
                let fmType = getFMType();
                d3.select(idTransformerFrontend(`#${nodeKey.id}`)).attr(
                  "clicked",
                  "0"
                );
                //去除阴影和特征图预览窗口
                d3.select(idTransformerFrontend(`#${nodeKey.id}`))
                  .select("#shadow")
                  .remove();
                clearFeatureMap(nodeKey.id + "-" + fmType);
                let translate_str = d3
                  .select(idTransformerFrontend(`#${nodeKey.id}`))
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
                d3.select(idTransformerFrontend(`#${nodeKey.id}`)).attr(
                  "transform",
                  "translate(" + translate_x + "," + translate_y + ")"
                );
              } else {
                d3.select(idTransformerFrontend(`#${nodeKey.id}`)).attr(
                  "clicked",
                  "1"
                );
                let translate_str = d3
                  .select(idTransformerFrontend(`#${nodeKey.id}`))
                  .attr("transform");
                let translate_x =
                  parseFloat(
                    translate_str.substring(
                      translate_str.indexOf("(") + 1,
                      translate_str.indexOf(",")
                    )
                  ) - 10;
                let translate_y =
                  parseFloat(
                    translate_str.substring(
                      translate_str.indexOf(",") + 1,
                      translate_str.indexOf(")")
                    )
                  ) - 10;
                let shadow_width = parseFloat(
                  d3
                    .select(idTransformerFrontend(`#${nodeKey.id}`))
                    .select(".label-container")
                    .attr("width")
                );
                let shadow_height = parseFloat(
                  d3
                    .select(idTransformerFrontend(`#${nodeKey.id}`))
                    .select(".label-container")
                    .attr("height")
                );
                d3.select(idTransformerFrontend(`#${nodeKey.id}`)).attr(
                  "transform",
                  "translate(" + translate_x + "," + translate_y + ")"
                );
                //添加阴影
                d3.select(idTransformerFrontend(`#${nodeKey.id}`))
                  .insert("rect", ".label-container")
                  .style("fill", "#000")
                  .attr("id", "shadow")
                  .attr("rx", "10")
                  .attr("ry", "10")
                  .attr("width", shadow_width.toString())
                  .attr("height", shadow_height.toString())
                  .attr("x", (10 - shadow_width / 2).toString())
                  .attr("y", (10 - shadow_height / 2).toString())
                  .attr("opacity", "0.5");
                //特征图预览窗口添加数据
                let param_tag = nodeKey.id + "-" + fmType;
                if (fmType !== "") {
                  let para = {
                    run: userSelectRunFile,
                    tag: param_tag,
                    range: 0,
                    task: getTaskType[userSelectRunFile],
                  };
                  fetchFeatures(para);
                }
              }
            }
          });
        });
      };
      const init = true;
      draw(data, init);
      self.signAvailableNode(this.getFmType[this.userSelectRunFile][0]);
    },
    signAvailableNode(type) {
      if (type !== undefined) {
        d3.selectAll(".sign-available").remove();
        this.getFmType[this.userSelectRunFile][type].forEach((nodeId) => {
          let node = d3.select(this.idTransformerFrontend(`#${nodeId}`));
          let rect_width = node.select("rect").attr("width");
          let rect_color = node.select("rect").style("fill");
          let circle = node
            .append("g")
            .attr("class", "sign-available")
            .attr("transform", `translate(${(3 * rect_width) / 8},0)`);
          circle
            .append("circle")
            .attr("class", "sign-available-circle")
            .attr("fill", "#fff")
            .attr("r", "8");
          circle
            .append("circle")
            .attr("class", "sign-available-content")
            .attr("fill", rect_color)
            .attr("r", "1.5")
            .attr("cy", "-4.5");
          circle
            .append("rect")
            .attr("class", "sign-available-content")
            .attr("fill", rect_color)
            .attr("width", "2")
            .attr("height", "8")
            .attr("x", "-1")
            .attr("y", "-2")
            .attr("rx", "1")
            .attr("ry", "1");
        });
      }
    },
    graphSizeWatch(el) {
      el.contentWindow.addEventListener(
        "resize",
        function () {
          let target = this;
          if (target.resizeFlag) {
            clearTimeout(target.resizeFlag);
          }
          target.resizeFlag = setTimeout(function () {
            const canvas = d3.select("#svg-canvas")._groups[0][0];
            const canvasHeight = canvas.scrollHeight;
            const canvasWidth = canvas.scrollWidth;
            const graph = d3.select("#svg-canvas g")._groups[0][0];
            const graphHeight = graph.getBBox().height;
            const graphWidth = graph.getBBox().width;
            const index = Math.min(
              canvasHeight / graphHeight,
              canvasWidth / graphWidth,
              1
            );
            d3.select("#svg-canvas g").attr(
              "transform",
              ` translate(${(canvasWidth - graphWidth * index) / 2},${
                (canvasHeight - graphHeight * index) / 2
              })`
            );
            const transform = d3
              .zoomTransform(0)
              .translate(
                (canvasWidth - graphWidth * index) / 2,
                (canvasHeight - graphHeight * index) / 2
              );
            d3.zoom().transform(d3.select("#svg-canvas"), transform);
            target.resizeFlag = null;
          }, 20);
        },
        false
      );
    },
    getFMType() {
      return this.getSelectFmType;
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
    edgeLabelAnimation() {
      const edgeGroup = Array.from(d3.selectAll(".edgePath")._groups[0]);
      edgeGroup.forEach((edge, index) => {
        const oraclePath = d3.select(edge).select("path");
        var newPath = d3.select(edge).append("path");
        newPath
          .attr("d", oraclePath.attr("d"))
          .style("opacity", 0)
          .style("stroke", "white")
          .style("stroke-width", "20px")
          .attr("marker-end", "url(http://localhost:8080/#arrowhead146)")
          .attr("marker-start", "url(#dot)")
          .style("fill", "none");
      });
    },
  },
};
</script>
<style lang="less" scoped>
/deep/ .Graph {
  height: 97.5%;
  width: 98%;
  margin: 1% 1% 0 1%;
  background-color: white;
  border-radius: 5px 5px 0 0;
  box-shadow: rgba(0, 0, 0, 0.3) 0 0 10px;
}
.node rect {
  opacity: 0.85;
  fill: #fff;
  stroke: #646464;
  stroke-width: 2.5px;
}
text {
  font-size: 16px;
  fill: #000;
}

.edgeLabel text {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe WPC", "Segoe UI",
    "Ubuntu", "Droid Sans", sans-serif, "PingFang SC";
  font-size: 1px;
}

.edgePath path {
  stroke: #333;
  stroke-width: 1.5px;
}

line {
  stroke: red;
  stroke-width: 2px;
}
.icon {
  font-size: 80px;
  color: #004986;
  opacity: 0.4;
}
#fmBox {
  width: 790px;
  height: calc(99% - 132px);
  position: absolute;
  top: 132px;
  right: -282.3px;
  border-radius: 3px;
  box-shadow: 0 0 10px #ccc;
}
</style>