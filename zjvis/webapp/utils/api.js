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
export default {
  manage: {
    initCategory: '/api/getCategory',
    waitingPage: '/api/init'
  },
  category: {
    scalar: '/api/scalar',
    histogram: '/api/histogram',
    graph: '/api/graph',
    distribution: '/api/distribution',
    embedding: '/api/getEmbedding',
    text: '/api/text',
    audio: '/api/audio',
    audio_raw: '/api/audio_raw',
    image: '/api/image',
    image_raw: '/api/image_raw',
    roc: '/api/getRoc',
    hyperparm: '/api/hyperparm',
    custom: '/api/getCustom',
    projector: '/api/projector',
    projector_data: '/api/projector_data',
    projector_sample: '/api/projector_sample',
    exception: '/api/exception',
    exception_data: '/api/exception_data',
    exception_hist: '/api/exception_hist',
    exception_box: '/api/exception_box'
  }
}
