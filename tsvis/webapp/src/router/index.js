/*
 * @Description: router
 * @version: 1.0
 * @Author: xds
 * @Date: 2020-05-08 10:52:00
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2021-12-14 15:42:40
 */
import Vue from "vue";
import Router from "vue-router";
import { Scalars, ScalarsPanel } from "@/components/scalars";
import { Medias, MediasPanel } from "@/components/medias";
const layout = () => import("@/components/layout/Layout.vue");
const graph = () => import("@/components/graphs/Graphs.vue");
const graphpanel = () => import("@/components/graphs/GraphsPanel.vue");
import { Hyperparms, HyperparmsPanel } from "@/components/hyperparms";
import { Customs, CustomsPanel } from "@/components/customs";
import { Statistics, StatisticsPanel } from "@/components/statistics";
import { Embeddings, EmbeddingsPanel } from "@/components/embeddings";
import { Exception, ExceptionPanel } from "@/components/exception";
import { Transformer, TransformerPanel } from "@/components/transformer";
import { HiddenState, HiddenStatePanel } from "@/components/hiddenstate";
Vue.use(Router);

export default new Router({
  routes: [
    { path: "/", redirect: "/index" },
    {
      path: "/index",
      name: "Layout",
      component: layout,
      children: [
        {
          path: "graph",
          components: {
            default: graph,
            right: graphpanel
          }
        },
        {
          path: "scalar",
          components: {
            default: Scalars,
            right: ScalarsPanel
          }
        },
        {
          path: "media",
          components: {
            default: Medias,
            right: MediasPanel
          }
        },
        {
          path: "statistic",
          components: {
            default: Statistics,
            right: StatisticsPanel
          }
        },
        {
          path: "embedding",
          components: {
            default: Embeddings,
            right: EmbeddingsPanel
          }
        },
        {
          path: "hyperparm",
          components: {
            default: Hyperparms,
            right: HyperparmsPanel
          }
        },
        {
          path: "exception",
          components: {
            default: Exception,
            right: ExceptionPanel
          }
        },
        {
          path: "transformer",
          components: {
            default: Transformer,
            right: TransformerPanel
          }
        },
        {
          path: "hiddenstate",
          components: {
            default: HiddenState,
            right: HiddenStatePanel
          }
        },
        {
          path: "custom",
          components: {
            default: Customs,
            right: CustomsPanel
          }
        }
      ]
    }
  ]
});
