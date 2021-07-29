/* * Copyright 2019-2020 Zheng Jie * * Licensed under the Apache License, Version 2.0 (the
"License"); * you may not use this file except in compliance with the License. * You may obtain a
copy of the License at * * http://www.apache.org/licenses/LICENSE-2.0 * * Unless required by
applicable law or agreed to in writing, software * distributed under the License is distributed on
an "AS IS" BASIS, * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. * See
the License for the specific language governing permissions and * limitations under the License. */

<template>
  <div class="sidebar-logo-container">
    <div class="sidebar-logo-link ellipsis">
      <img :src="title" class="sidebar-title" />
    </div>
  </div>
</template>

<script>
import title from '@/assets/images/dl-title.png';

export default {
  name: 'SidebarLogo',
  props: {
    collapse: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      title,
    };
  },
};
</script>

<style lang="scss" scoped>
@import '~@/assets/styles/variables.scss';

.sidebar-logo-container {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
  height: 50px;
  overflow: hidden;

  & .sidebar-logo-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    font-size: 20px;
    font-weight: 600;
    color: 666;

    & .sidebar-logo {
      width: calc(#{$iconBarWidth} - 12px);
      margin-right: 6px;
      margin-left: 6px;
    }

    & .sidebar-title {
      width: 100%;
      // height: 100%;
    }
  }
}
</style>
