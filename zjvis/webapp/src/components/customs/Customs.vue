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

<style lang="less" scoped>
.temp {
  width: 100%;
  height: 100%;
  overflow-y: hidden;
  background-color: white;
}

.display-panel {
  display: flex;
  flex-direction: column;
  height: 97.5%;
  margin: 1% 1% 0 1%;
  overflow-y: auto;
  background-color: white;
  border-radius: 5px 5px 0 0;
  box-shadow: rgba(0, 0, 0, 0.3) 0 0 10px;

  .test1 {
    .test1-title {
      height: 30px;
      background-color: burlywood;
    }

    .test1-content {
      height: 100%;
      overflow-y: auto;
      border: 2px solid #e8eaec;
      border-width: 0 2px 2px 2px;
      border-radius: 0 0 5px 5px;

      .test1-detail-content {
        height: 700px;
        background-color: #fff;
      }
    }
  }

  .scalar {
    display: flex;
    flex-direction: row;
    align-items: center;
    height: auto;
    color: white;
    background-color: white;

    span {
      font-weight: 700;
      line-height: 30px;
    }
  }

  .media {
    display: flex;
    flex-direction: row;
    align-items: center;
    height: auto;
    color: white;
    background-color: white;

    span {
      font-weight: 700;
      line-height: 30px;
    }
  }

  .statistic {
    display: flex;
    flex-direction: row;
    align-items: center;
    height: auto;
    color: white;
    background-color: white;

    span {
      font-weight: 700;
      line-height: 30px;
    }
  }
}

.noneData {
  display: 'none';
}

.line1 {
  width: 88%;
  height: 1px;
  background-color: #f4f6ff;
}

.line2 {
  width: 2.5%;
  height: 5px;
  background-color: #625eb3;
}

.linestyle {
  background-color: #b9c6ff;
}

.scalarcontainer {
  width: 100%;
  height: 100%;
  background-color: white;
}

.scalarscontent {
  padding: 1% 2% 0 2%;
  background-color: white;
}

.content {
  margin-bottom: 0.5%;
}

.statistics-container {
  margin-bottom: 0.5%;
  background-color: #fff;

  .statistics-title {
    display: flex;
    align-items: center;
    height: auto;
    color: white;
    background-color: white;
  }

  .statistics-content {
    position: relative;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
    height: 100%;
    margin-left: 1%;

    .allStatisticContainer {
      width: 31%;
      height: 100%;
      margin: 0.8%;
      background-color: white;

      .statisticContaierContent {
        width: 100%;
        // height: 80%
        .runTag {
          width: 100%;
        }
      }
    }
  }
}

.showClass {
  display: none;
}
</style>
<template>
  <div>
    <div class="temp">
      <div :class="['display-panel']">
        <div id="scalar">
          <div>
            <div class="scalarscontent">
              <el-row :gutter="20">
                <ScalarContainer
                  v-for="(val, name) in scalarData"
                  :key="name"
                  :content="val"
                  :chartname="name"
                />
              </el-row>
            </div>
          </div>
        </div>

        <div id="audio">
          <div :style="hasAudio.hasData ? '' : 'display:none'">
            <div class="scalarscontent">
              <el-row :gutter="20">
                <AudioContainer
                  v-for="item in audioData"
                  ref="AudioContainer"
                  :key="item.index"
                  :content="item.content"
                  :index="item.index"
                />
              </el-row>
            </div>
          </div>
        </div>

        <div id="image">
          <div :style="hasImage.hasData ? '' : 'display:none'">
            <div class="scalarscontent">
              <el-row :gutter="20">
                <ImageContainer
                  v-for="item in imageData"
                  ref="ImageContainer"
                  :key="item.content.run + '/' + Object.keys(item.content.value)[0]"
                  :content="item.content"
                />
              </el-row>
            </div>
          </div>
        </div>

        <div id="text">
          <div :style="hasText.hasData ? '' : 'display:none'">
            <div class="scalarscontent">
              <el-row :gutter="20">
                <TextContainer
                  v-for="item in textData"
                  ref="TextContainer"
                  :key="item.content.run + '/' + Object.keys(item.content.value)[0]"
                  :content="item.content"
                />
              </el-row>
            </div>
          </div>
        </div>

        <div id="histogram">
          <div class="statistics-container">
            <div :class="['statistics-content']">
              <div
                v-for="item in statisticData"
                :id="item.divId"
                :key="item.divId"
                class="allStatisticContainer"
              >
                <statisticContainer
                  ref="histoContainer"
                  :key="item.ttlabel"
                  :data="item.data"
                  :ttlabel="item.ttlabel"
                  :tag="item.tag"
                  :itemp="item.itemp"
                  :componentName="item.componentName"
                  :runColor="item.runColor"
                  :divId="item.divId"
                  :parentComponent="parentComponent"
                  class="statisticContaierContent"
                />
              </div>
            </div>
          </div>
        </div>
        <div v-if="!hasData">
          <p>
            本页面支持将其他页面的数据通过“定制”按钮
            <i class="iconfont icon-ziyuan104" /> 导入到本页面
          </p>
          <p>支持将媒体数据、统计分析和标量数据导入到本页面</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import statisticContainer from '@/components/statistics/drawStatistic/statisticContainer.vue';
import ImageContainer from '@/components/medias/image/imagecontainer/ImageContainer.vue';
import TextContainer from '@/components/medias/text/textContainer/TextContainer.vue';
import AudioContainer from '@/components/medias/audio/audioContainer/AudioContainer.vue';
import ScalarContainer from '@/components/scalars/scalarcontainer/ScalarCustom.vue';


import { createNamespacedHelpers } from 'vuex';
const { mapActions: mapCustomActions, mapMutations: mapCustomMutations, mapGetters: mapCustomGetters } = createNamespacedHelpers(
  'custom'
);
const { mapGetters: mapLayoutGetters } = createNamespacedHelpers('layout')

export default {
  components: {
    statisticContainer,
    ImageContainer,
    TextContainer,
    AudioContainer,
    ScalarContainer,
  },
  data() {
    return {
      showFlag: false,
      parentComponent: false,
      data: [[], [], [], [], [], []],
      textChecked: [],
      hasScalar: {
        hasData: 0,
        showFlag: 0,
      },
      hasAudio: {
        hasData: 0,
        showFlag: 0,
      },
      hasImage: {
        hasData: 0,
        showFlag: 0,
      },
      hasText: {
        hasData: 0,
        showFlag: 0,
      },
      scalarData: {},
      audioData: [],
      imageData: [],
      textData: [],
      statisticData: [],
      hasData: false,
    };
  },
  computed: {

    ...mapLayoutGetters(['getTimer']),
    ...mapCustomGetters([
      'getAudioData',
      'getTextData',
      'getTextChecked',
      'getImageData',
      'getStatisticData',
      'getScalarData',
    ])
    
  },
  beforeRouteLeave(to, from, next) {
    this.setRouter(7);
    next();
  },
  watch: {
    getTimer: function() {
      console.log('getTimer')
      for(let i=0; i<this.audioData.length; i++) {
        this.getAudioDataInterval([i, this.audioData[i]])
      }
      for(let i=0; i<this.imageData.length; i++) {
        this.getImageDataInterval([i, this.imageData[i]])
      }
      for(let i=0; i<this.textData.length; i++) {
        this.getTextDataInterval([i, this.textData[i]])
      }
    },
    getAudioData() {
      this.audioData = this.getAudioData;
      if (this.audioData.length === 0) {
        this.hasAudio.hasData = 0;
        this.hasAudio.showFlag = 0;
      }
      if (this.audioData.length || this.textData.length || this.imageData.length || this.statisticData.length || Object.keys(this.scalarData).length) {
        this.hasData = true
      } else {
        this.hasData = false
      }
    },
    getTextData() {
      this.textData = this.getTextData;
      if (this.textData.length === 0) {
        this.hasText.hasData = 0;
        this.hasText.showFlag = 0;
      }
      if (
        this.audioData.length ||
        this.textData.length ||
        this.imageData.length ||
        this.statisticData.length ||
        Object.keys(this.scalarData).length
      ) {
        this.hasData = true;
      } else {
        this.hasData = false;
      }
    },
    getImageData() {
      if (this.imageData.length === 0) {
        this.hasImage.hasData = 0;
        this.hasImage.showFlag = 0;
      }
      this.imageData = this.getImageData;
      if (
        this.audioData.length ||
        this.textData.length ||
        this.imageData.length ||
        this.statisticData.length ||
        Object.keys(this.scalarData).length
      ) {
        this.hasData = true;
      } else {
        this.hasData = false;
      }
    },
    getScalarData(val) {
      this.scalarData = val;
      if (
        this.audioData.length ||
        this.textData.length ||
        this.imageData.length ||
        this.statisticData.length ||
        Object.keys(this.scalarData).length
      ) {
        this.hasData = true;
      } else {
        this.hasData = false;
      }
    },
    getStatisticData(val) {
      this.statisticData = val;
      if (
        this.audioData.length ||
        this.textData.length ||
        this.imageData.length ||
        this.statisticData.length ||
        Object.keys(this.scalarData).length
      ) {
        this.hasData = true;
      } else {
        this.hasData = false;
      }
    },
  },
  created() {
    this.audioData = this.getAudioData;
    this.textData = this.getTextData;
    this.imageData = this.getImageData;
    this.scalarData = this.getScalarData;
    this.statisticData = this.getStatisticData;
    if (
      this.audioData.length ||
      this.textData.length ||
      this.imageData.length ||
      this.statisticData.length ||
      Object.keys(this.scalarData).length
    ) {
      this.hasData = true;
    } else {
      this.hasData = false;
    }
  },
  mounted() {
    if (this.audioData.length) {
      this.hasAudio.hasData = 1;
    }
    if (this.imageData.length) {
      this.hasImage.hasData = 1;
    }
    if (this.textData.length) {
      this.hasText.hasData = 1;
    }
  },
  methods: {
    ...mapCustomMutations(['setTextData', 'setRouter']),
    ...mapCustomActions(['getAudioDataInterval', 'getImageDataInterval', 'getTextDataInterval']),
    showContent(title) {
      this[title].showFlag = (this[title].showFlag + 1) % 2;
    }
  },
};
</script>
