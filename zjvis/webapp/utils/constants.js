/** Copyright 2020 Tianshu AI Platform. All Rights Reserved.
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
const HOSTNAME = window.location.origin + '/'
const DJANGOHOSTNAME = 'http://localhost:8013/'
// const DJANGOHOSTNAME = process.env.VUE_APP_VISUAL_IMG_API
// const DJANGOHOSTNAME = 'http://192.168.157.100:8001'
// const DJANGOHOSTNAME = '' // 生成服务器静态页面接口
const IMGURl = DJANGOHOSTNAME
// const IMGURl = process.env.VUE_APP_VISUAL_API
const CATEGORY = [
  ['GRAPH', 'Graphs', 'GraphsPanel', '模型结构', 'icon-moxingjiegou_1'],
  ['SCALAR', 'Scalars', 'ScalarsPanel', '标量数据', 'icon-biaoliangshuju1'],
  ['MEDIA', 'Medias', 'MediasPanel', '媒体数据', 'icon-meitishuju_1'],
  ['STATISTIC', 'Statistics', 'StatisticsPanel', '统计分析', 'icon-tongjifenxi_1'],
  ['EMBEDDING', 'Embeddings', 'EmbeddingsPanel', '降维分析', 'icon-jiangweifenxi_1'],
  ['FEATURE', 'Features', 'FeaturesPanel', '特征分析', 'icon-feature'],
  ['ROC', 'ROCs', 'ROCsPanel', '评测曲线', 'icon-roc'],
  ['HYPERPARM', 'Hyperparms', 'HyperparmsPanel', '超参分析', 'icon-chaocanfenxi_1'],
  ['EXCEPTION', 'Exception', 'ExceptionPanel', '异常检测', 'icon-yichang3'],
  ['CUSTOM', 'Customs', 'CustomsPanel', '用户定制', 'icon-yonghudingzhi_1']
]
const CATEGORYORDER = ['graph', 'scalar', 'media', 'statistic', 'embedding', 'feature', 'roc', 'hyperparm', 'exception', 'custom']
const RUNFILESHOWFlAG = { 'graph': 0, 'scalar': 1, 'media': 1, 'statistic': 1, 'embedding': 0, 'feature': 0, 'roc': 1, 'hyperparm': 0, 'exception': 1, 'custom': 2 }

export default { HOSTNAME, DJANGOHOSTNAME, CATEGORY, CATEGORYORDER, RUNFILESHOWFlAG, IMGURl }
