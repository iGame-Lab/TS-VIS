/*
 * @Descripttion: store state management
 * @version: 1.0
 * @Author: xds
 * @Date: 2020-04-26 08:35:48
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2021-12-14 14:51:36
 */
import Vue from "vue";
import Vuex from "vuex";
import layout from "./modules/layout";
import statistic from "./modules/statistic";
import scalar from "./modules/scalar";
import media from "./modules/media";
import graph from "./modules/graph";
import custom from "./modules/custom";
import embedding from "./modules/embedding";
import exception from "./modules/exception";
import hyperparm from "./modules/hyperparm";
import transformer from "./modules/transformer";
import hiddenstate from "./modules/hiddenstate";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    layout: layout,
    statistic: statistic,
    scalar: scalar,
    media: media,
    graph: graph,
    custom: custom,
    embedding: embedding,
    exception: exception,
    hyperparm: hyperparm,
    transformer: transformer,
    hiddenstate: hiddenstate
  }
});

export default store;
