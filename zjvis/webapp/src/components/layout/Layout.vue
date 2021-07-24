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

<template>
  <div class="layout-root layout-same-style" style="width: 100%;">
    <el-dialog
      :visible.sync="dialogFormVisible"
      title="图片保存选项"
      class="layout-svg-save-dialog"
    >
      <el-form :model="form">
        <el-form-item :label-width="formLabelWidth" label="图片名称">
          <el-input v-model="form.input" placeholder="请输入名称" clearable />
        </el-form-item>
        <el-form-item :label-width="formLabelWidth" label="图片格式">
          <el-select v-model="form.type" placeholder="请选择保存图片格式">
            <el-option label="png" value="png" />
            <el-option label="eps" value="eps" />
            <el-option label="svg" value="svg" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="downCancel">取 消</el-button>
        <el-button type="primary" @click="downloadSvg">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      :visible.sync="initWaitVisible"
      title="全力加载中,请稍等..."
      class="layout-svg-save-dialog"
    >
      <i class="el-icon-loading" />
    </el-dialog>
    <el-dialog :visible.sync="operationGuide" title="操作指南" class="layout-svg">
      <div id="write" class="">
        <h2>
          <a name="模型结构" class="md-header-anchor" />
          <span>模型结构</span>
        </h2>
        <h3>
          <a name="主体界面" class="md-header-anchor" />
          <span>主体界面</span>
        </h3>
        <p>
          <span>1.通过滚轮实现图的放大与缩小</span>
        </p>
        <p>
          <span>2.通过单击鼠标左键并移动实现图的移动</span>
        </p>
        <p>
          <span
          >3.单击节点会将节点具体信息显示在菜单栏，同时，与该节点相连的其他节点以及边都会标红</span
          >
        </p>
        <p>
          <span>4.双击节点可以实现节点的展开与缩回</span>
        </p>
        <p>
          <span>5.右键节点可以对节点进行边的隐藏、显示以及删除操作</span>
        </p>
        <p>
          <span
          >6.当通过右键删除节点时，节点会被放置在右侧的隐藏栏中。双击隐藏栏内的节点可以实现节点的放回</span
          >
        </p>
        <h3>
          <a name="功能栏" class="md-header-anchor" />
          <span>功能栏</span>
        </h3>
        <h4>
          <a name="计算图" class="md-header-anchor" />
          <span>计算图</span>
        </h4>
        <p>
          <span>1.用户通过条件的输入与选择实现针对节点的</span>
          <strong> <span>批量筛选</span></strong>
        </p>
        <p>
          <span>2.</span>
          <strong> <span>隐藏</span></strong>
          <span>按钮用于实现针对符合批量筛选条件节点的隐藏，但并没有改变图的结构</span>
        </p>
        <p>
          <span>3.</span>
          <strong> <span>布局</span></strong>
          <span
          >按钮用于实现针对符合批量筛选条件以及单独隐藏节点的删除与重新布局，该操作会让剩余节点在当前新条件下重新绘制，会改变图的结构</span
          >
        </p>
        <p>
          <span>4.</span>
          <strong> <span>上一步</span></strong>
          <span>按钮用于返回用户的之前一步操作</span>
        </p>
        <p>
          <span>5.</span>
          <strong> <span>初始化</span></strong>
          <span>按钮用于将图重置为最初未经改变的图像</span>
        </p>
        <h4>
          <a name="结构图" class="md-header-anchor" />
          <span>结构图</span>
        </h4>
        <p>
          <span>1.下拉框用于实现同数据集下结构图的切换</span>
        </p>
        <p>
          <span>2.</span>
          <strong> <span>布局</span></strong>
          <span
          >按钮用于实现针对单独隐藏节点的删除与重新布局，该操作会让剩余节点在当前新条件下重新绘制，会改变图的结构</span
          >
        </p>
        <h4>
          <a name="数据信息栏" class="md-header-anchor" />
          <span>数据信息栏</span>
        </h4>
        <p>
          <span>信息栏用于显示单击特定节点时节点的全部信息，可通过</span>
          <strong> <span>箭头</span></strong>
          <span>按钮实现对信息的折叠与展开</span>
        </p>
        <p>&nbsp;</p>
        <hr >
        <p>&nbsp;</p>
        <h2>
          <a name="标量数据" class="md-header-anchor" />
          <span>标量数据</span>
        </h2>
        <h3>
          <a name="主体界面-n308" class="md-header-anchor" />
          <span>主体界面</span>
        </h3>
        <p>
          <span>标量图表操作：</span>
        </p>
        <ol>
          <li>
            <span>不同分类的图表组可以单击选择关闭或打开视图</span>
          </li>
          <li>
            <span>可以鼠标移动到数据上显示数据信息</span>
          </li>
          <li>
            <span>每一图表右上角有放大缩小按钮</span>
          </li>
          <li>
            <span
            >右上角矩形框可为用户定制所用，选中后再按定制按钮就可以把数据迁移上用户定制上；也可为合并多个图表时所用</span
            >
          </li>
          <li>
            <span>在图表内部拖动鼠标选择一个方形区域可进行图表局部放大，双击图表可还原</span>
          </li>
        </ol>
        <h3>
          <a name="控制栏" class="md-header-anchor" />
          <span>控制栏</span>
        </h3>
        <p>
          <span>Smooth：调整数据显示平滑程度，选择范围为（0 ~ 0.9）</span>
        </p>
        <p>
          <span
          >Y-axis：调整y轴数据显示方式，共两种，一种是linear（原始数据），一种是log-linear（取对数后的数据）</span
          >
        </p>
        <p>
          <span
          >合并按钮：将勾选中的图表进行合并，合并限制：至多可勾选两种tag的图表，至多可勾选6幅图表</span
          >
        </p>
        <p>
          <span>还原按钮：将勾选中的合并图表进行还原</span>
        </p>
        <h3>
          <a name="数据信息栏-n326" class="md-header-anchor" />
          <span>数据信息栏</span>
        </h3>
        <p>
          <span>暂无数据</span>
        </p>
        <p>&nbsp;</p>
        <hr >
        <p>&nbsp;</p>
        <h2>
          <a name="媒体数据" class="md-header-anchor" />
          <span>媒体数据</span>
        </h2>
        <h3>
          <a name="主体界面-n452" class="md-header-anchor" />
          <span>主体界面</span>
        </h3>
        <p>
          <span>可以显示文本，图像，音频</span>
        </p>
        <h4>
          <a name="文本" class="md-header-anchor" />
          <span>文本</span>
        </h4>
        <ol>
          <li>
            <span>显示相应的数据</span>
          </li>
          <li>
            <span>slider 可以对step进行拖拽</span>
          </li>
        </ol>
        <h4>
          <a name="图像" class="md-header-anchor" />
          <span>图像</span>
        </h4>
        <ol>
          <li>
            <span>可以对图像进行点击，显示大图</span>
          </li>
          <li>
            <span>slider 可以对step进行拖拽</span>
          </li>
        </ol>
        <h4>
          <a name="音频" class="md-header-anchor" />
          <span>音频</span>
        </h4>
        <ol>
          <li>
            <span>可以播放音频</span>
          </li>
          <li>
            <span>slider 可以对step进行拖拽</span>
          </li>
        </ol>
        <h3>
          <a name="数据信息栏-n472" class="md-header-anchor" />
          <span>数据信息栏</span>
        </h3>
        <ol>
          <li>
            <p>
              <span>暂时为空</span>
            </p>
            <p>&nbsp;</p>
          </li>
        </ol>
        <hr >
        <p>&nbsp;</p>
        <h2>
          <a name="统计分析" class="md-header-anchor" />
          <span>统计分析</span>
        </h2>
        <h3>
          <a name="主体界面-n551" class="md-header-anchor" />
          <span>主体界面</span>
        </h3>
        <p>
          <span>由直方图和分布图两部分组成</span>
        </p>
        <p>
          <span>直方图操作：</span>
        </p>
        <ol>
          <li>
            <span>直方图可以单击选择关闭或打开视图</span>
          </li>
          <li>
            <span>可以鼠标移动到数据上显示数据信息</span>
          </li>
          <li>
            <span>每一直方图右上角有放大缩小按钮</span>
          </li>
          <li>
            <span>右上角矩形框为用户定制所用，选中后再按定制按钮就可以把数据迁移上用户定制上</span>
          </li>
        </ol>
        <p>
          <span>分布图操作：</span>
        </p>
        <ol>
          <li>
            <span>分布图可以单击选择关闭或打开视图</span>
          </li>
          <li>
            <span>每一直方图右上角有放大缩小按钮</span>
          </li>
          <li>
            <span>右上角矩形框为用户定制所用，选中后再按定制按钮就可以把数据迁移上用户定制上</span>
          </li>
        </ol>
        <h3>
          <a name="控制栏-n571" class="md-header-anchor" />
          <span>控制栏</span>
        </h3>
        <p>
          <span>直方图控制栏：</span>
        </p>
        <p>
          <span>数据显示比率参数：调整数据显示数量</span>
        </p>
        <p>
          <span>统计区间个数参数：调整总体数据的统计区间个数</span>
        </p>
        <p>
          <span>模式下拉框：直方图三维或二维显示</span>
        </p>
        <p>&nbsp;</p>
        <h3>
          <a name="数据信息栏-n577" class="md-header-anchor" />
          <span>数据信息栏</span>
        </h3>
        <p>
          <span>显示直方图选中的原始数据</span>
        </p>
        <p>&nbsp;</p>
        <hr >
        <p>&nbsp;</p>
        <h2>
          <a name="降维分析" class="md-header-anchor" />
          <span>降维分析</span>
        </h2>
        <h3>
          <a name="主体界面-n671" class="md-header-anchor" />
          <span>主体界面</span>
        </h3>
        <p>
          <span>可以显示2维，3维分类结果</span>
        </p>
        <h4>
          <a name="2维操作" class="md-header-anchor" />
          <span>2维操作</span>
        </h4>
        <ol>
          <li>
            <span>可以对点(线条)进行点击，数据信息栏会显示存储的图片/文本</span>
          </li>
          <li>
            <span>鼠标移动上去可以简单显示对应的点和标签</span>
          </li>
          <li>
            <span>拖拽可以对点进行局部放大</span>
          </li>
          <li>
            <span>双击显示窗口可以回到初始的显示界面</span>
          </li>
        </ol>
        <h4>
          <a name="3维操作" class="md-header-anchor" />
          <span>3维操作</span>
        </h4>
        <ol>
          <li>
            <span>可以对点(线条)进行点击，数据信息栏会显示存储的图片/文本</span>
          </li>
          <li>
            <span>鼠标移动上去可以简单显示对应的点和标签</span>
          </li>
          <li>
            <span>鼠标滚轮可以进行缩放</span>
          </li>
        </ol>
        <h3>
          <a name="控制面板" class="md-header-anchor" />
          <span>控制面板</span>
        </h3>
        <ol>
          <li>
            <span>可以选择对应的标签(Tag)</span>
          </li>
          <li>
            <span>可以选择对应的降维方法(PCA TSNE)</span>
          </li>
          <li>
            <span>可以选择维度信息</span>
          </li>
          <li>
            <span>播放按钮可以显示出step动态的动画（这个功能对于应2，3,4-8维）</span>
          </li>
        </ol>
        <h3>
          <a name="数据信息栏-n711" class="md-header-anchor" />
          <span>数据信息栏</span>
        </h3>
        <ol>
          <li>
            <p>
              <span>显示对应的数据（文字和图片）</span>
            </p>
            <p>&nbsp;</p>
          </li>
        </ol>
        <hr >
        <p>&nbsp;</p>
        <h2>
          <a name="超参数" class="md-header-anchor" />
          <span>超参数</span>
        </h2>
        <h3>
          <a name="主体界面-n767" class="md-header-anchor" />
          <span>主体界面</span>
        </h3>
        <p>
          <span>主界面由平行坐标以及表格数据</span>
        </p>
        <p>
          <span>平行坐标操作：</span>
        </p>
        <ol>
          <li>
            <span>选择坐标轴上部分区域高亮显示对应的表格数据也会高亮</span>
          </li>
          <li>
            <span>鼠标移动到线上高亮显示</span>
          </li>
          <li>
            <span>坐标轴移动以改变平行坐标</span>
          </li>
        </ol>
        <p>
          <span>表格操作：</span>
        </p>
        <ol>
          <li>
            <span>鼠标移动到某一行，平行坐标上对应数据会高亮显示</span>
          </li>
        </ol>
        <h3>
          <a name="控制面板-n783" class="md-header-anchor" />
          <span>控制面板</span>
        </h3>
        <p>
          <span>主参数 控制颜色映射对应的数据</span>
        </p>
        <p>
          <span>坐标尺度： 数值型数据可以选择线性坐标轴和对数坐标轴</span>
        </p>
        <h3>
          <a name="统计信息栏" class="md-header-anchor" />
          <span>统计信息栏</span>
        </h3>
        <p>
          <span>显示选中的数据进行统计信息显示。</span>
        </p>
        <p>
          <span>默认选中全部数据</span>
        </p>
        <h3>
          <a name="数据信息栏-n789" class="md-header-anchor" />
          <span>数据信息栏</span>
        </h3>
        <p>
          <span>显示选中数据的原始信息。</span>
        </p>
        <p>&nbsp;</p>
        <hr >
        <p>&nbsp;</p>
        <h2>
          <a name="异常检测" class="md-header-anchor" />
          <span>异常检测</span>
        </h2>
        <h3>
          <a name="主体界面-n811" class="md-header-anchor" />
          <span>主体界面</span>
        </h3>
        <p>
          <span>由直方图、颜色矩阵和盒须图三部分组成</span>
          <span
          >直方图：数据的统计信息，区间不均匀分布，坐标轴上的红色标记对应盒须图异常点的上下边界</span
          >
          <span
          >颜色矩阵：用矩形表示数值点，根据数值大小为矩形赋予一个颜色值，颜色矩阵可以通过滚轮放大缩小查看；</span
          >
          <span />
          <span
          >颜色条上下三角形可拖动，只查看一定范围内的数值分布，数值大小超出上下三角形数值的矩形颜色变灰</span
          >
          <span>盒须图：拖动下方坐标轴上的刷子可查看相应范围内的盒须图，</span>
          <span />
          <span
          >点击某个盒须图，请求异常点数据，在盒须图中用红色圆圈标记出来，并把颜色矩阵中对应的矩形的边界高亮</span
          >
          <span />
          <span>异常值的上下边界也可拖拽，停止拖拽时会重新获取新范围外的异常点数据</span>
          <span />
        </p>
        <h3>
          <a name="控制栏-n813" class="md-header-anchor" />
          <span>控制栏</span>
        </h3>
        <p>
          <span>主要功能：调节盒须图异常值的上下边界</span>
          <span>联动选择：勾选联动后，盒须图异常值的上下边界会同步变化</span>
        </p>
        <h3>
          <a name="数据信息栏-n815" class="md-header-anchor" />
          <span>数据信息栏</span>
        </h3>
        <p>
          <span>鼠标放到颜色矩阵或是盒须图的异常点上，显示该点所在的行、列、数值大小等</span>
        </p>
        <h3>
          <a name="数据信息栏-n817" class="md-header-anchor" />
          <span>数据信息栏</span>
        </h3>
        <p>
          <span>暂无数据</span>
        </p>
        <p>&nbsp;</p>
        <hr >
        <p>&nbsp;</p>
        <h2>
          <a name="用户定制" class="md-header-anchor" />
          <span>用户定制</span>
        </h2>
        <h3>
          <a name="主体界面-n134" class="md-header-anchor" />
          <span>主体界面</span>
        </h3>
        <p>
          <span>可以将媒体数据，标量数据，统计分析数据集中到用户定制集中显示</span>
        </p>
        <ol start="">
          <li>
            <span>通过点击上面信息框的勾选框，再点击用户定制图标，自动跳转到用户定制</span>
          </li>
          <li>
            <span>点击‘X’，会删除对应的显示组件</span>
          </li>
        </ol>
        <h3>
          <a name="控制栏-n141" class="md-header-anchor" />
          <span>控制栏</span>
        </h3>
        <p>
          <span>对应的显示组件有对应的控制栏的话，右边会出现相应的控制栏</span>
        </p>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
      </div>
    </el-dialog>
    <el-dialog
      :visible.sync="dataSyncVisible"
      title="设定数据同步间隔"
      class="layout-svg-save-dialog"
    >
      <div>
        <el-checkbox v-model="syncDataBool">启用同步</el-checkbox>
      </div>
      <div style="margin-top: 10px;">
        <el-input-number
          v-model="timeSync"
          :min="5"
          :disabled="!syncDataBool"
          class="input-number"
          size="mini"
        />秒
      </div>
    </el-dialog>
    <div
      ref="left"
      :style="{ height: leftStyle.height, width: leftStyle.width }"
      class="layout-sidebar layout-same-style"
    >
      <logo :collapse="false" />
      <div :class="['layout-sidebar-category-container']">
        <div class="layout-sidebar-category layout-same-style">
          <div
            v-for="(item, i) in allCategoryInform"
            :key="item.id"
            :class="['layout-sidebar-category-each']"
            :style="{
              height: 100 / allCategoryInform.length + '%',
              lineHeight: 100 / allCategoryInform.length + '%',
            }"
          >
            <div ref="eachTop" :class="['layout-sidebar-category-each-top']" />
            <div
              ref="eachMiddle"
              :class="['layout-sidebar-category-each-middle']"
              :style="
                item.id == selected || (i == initId && initFlag)
                  ? { borderLeft: '4px solid #2e4fde' }
                  : {}
              "
            >
              <router-link
                :to="item.routerName"
                :class="[
                  item.id == selected || (i == initId && initFlag) ? 'category-selected' : '',
                ]"
                tag="li"
                @click.native="change(item)"
              >
                <i :class="['iconfont', item.icon]" :style="{ fontSize: 16 + 'px' }" />
                <span
                  :class="[leftStyle.categoryFlage ? 'span-after' : '']"
                  :style="
                    item.id == selected || (i == initId && initFlag)
                      ? { fontSize: 16 + 'px', color: 'rgb(46, 79, 222)' }
                      : { fontSize: 16 + 'px' }
                  "
                >{{ item.name }}</span
                >
              </router-link>
            </div>
            <div :class="['layout-sidebar-category-each-bottom']" />
          </div>
        </div>
      </div>
      <div :class="['layout-sidebar-setting']">
        <p
          v-for="item in leftSilderIcons"
          v-show="item.shaowFlag"
          ref="item.ref"
          :key="item.id"
          :style="{ position: 'absolute', marginLeft: item.margin }"
          @click="isHide(item)"
        >
          <i :class="['iconfont', item.name]" :style="{ fontSize: item.size }" />
        </p>
      </div>
    </div>
    <div
      :style="{ height: rightStyle.height, width: rightStyle.width }"
      class="layout-header-content layout-same-style"
    >
      <div class="layout-header layout-same-style">
        <div :class="['same-div']" style="width: 400px;">
          <p
            v-for="(item, i) in icons"
            :key="i"
            :class="['same-p']"
            :title="item.chName"
            @click="jsutTest(item.raw)"
          >
            <i :class="['iconfont', item.name]" :style="{ fontSize: item.size }" />
          </p>
          <p :class="['tool-p']" />
          <p :class="['run-select-container']" :style="{ width: '40%' }">
            <el-select
              v-if="update"
              v-model="value1"
              :class="['run-selest']"
              :multiple="multipleFlag === 2 ? false : isMultiple"
              :disabled="multipleFlag === 2 ? true : false"
              :clearable="multipleFlag === 2 ? false : isMultiple"
              size="mini"
              placeholder="RUN"
              collapse-tags
              filterable
              @focus="getOptions()"
            >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </p>
        </div>
        <div :class="['same-div']" style="width: calc(100% - 800px);" />
        <div :class="['same-div', 'search-tag']" style="width: 400px;">
          <p :class="['run-select-container']" :style="{ margin: '0 0 0 0' }">
            <i
              :class="['el-icon-refresh']"
              style="font-size: 19px; color: whitesmoke; cursor: pointer;"
              @click="isClicked"
            />
            <i
              v-for="item in settingHelp"
              :key="item.id"
              :class="['iconfont', item.name, 'icon-setting-help']"
              :style="{ fontSize: item.size, cursor: 'pointer' }"
              @click="getTigger(item)"
            />
          </p>
        </div>
      </div>
      <div
        id="full-screen1"
        class="layout-content layout-same-style"
        style="background-color: white;"
      >
        <div
          :class="['right-slider', rightRetract.retractFlage ? 'right-slider-last' : '']"
          :style="{ right: rightRetract.setBackLeft, width: rightRetract.width }"
        >
          <p
            v-for="item in rightSilderIcons"
            v-show="item.shaowFlag && selectedRaw !== 'graph'"
            :key="item.id"
            @click="rightSilder(item)"
          >
            <i :class="['iconfont', item.name]" :style="{ fontSize: item.size }" />
          </p>
        </div>
        <router-view
          id="full-screen"
          :class="[rawShape, 'layout-same-style']"
          :style="{ width: contentsStyle.leftWidth }"
        />
        <router-view
          v-show="contentsStyle.rightShowFlag"
          name="right"
          class="layout-content-paramenter layout-same-style"
        />
      </div>
    </div>
  </div>
</template>
<script>
import * as d3 from 'd3'
import { createNamespacedHelpers } from 'vuex'
import download from '@/utils/download'
import constants from '@/utils/constants'

// import { param2Obj } from '@/utils'
import Logo from '@/components/layout/Logo'
const {
  mapMutations: mapLayoutMutations,
  mapActions: mapLayoutActions,
  mapGetters: mapLayoutGetters,
  mapState: mapLayoutState
} = createNamespacedHelpers('layout')
const { mapMutations: mapCustomMutations } = createNamespacedHelpers('custom')

export default {
  components: {
    Logo
  },
  data() {
    return {
      timer: null,
      downloadList: [],
      downloadState: ['graph', 'scalar', 'statistic'],
      init: 1,
      screenWidth: '0px',
      titleSrc:
      'data:image/png;base64,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',
      selected: -1,
      selectedRaw: '',
      value: '',
      setintervalFlag: null,
      initFlag: true,
      initId: 0,
      inputValue: '',
      isMultiple: '',
      update: true,
      logoImgStyleFlage: false,
      dialogFormVisible: false,
      initWaitVisible: true,
      formLabelWidth: '120px',
      autoFontSize: 16,
      actegoryClickStyle: {
        divTop: '',
        divAim: '',
        divBottom: ''
      },
      form: {
        name: '',
        type: 'png',
        input: '下载'
      },
      rightRetract: {
        setBackLeft: '0',
        width: '290px',
        retractFlage: false
      },
      todoName: '',
      logoSourse: 'static/img/left_logo.png',
      logoFlag: true,
      rawShape: 'layout-content-panel',
      leftStyle: {
        width: '180px',
        height: '100%',
        categoryFlage: false
      },
      rightStyle: {
        width: 'calc(100% - 180px)',
        height: '100%'
      },
      contentsStyle: {
        leftWidth: 'calc(100% - 290px)',
        rightShowFlag: true
      },
      options: '',
      value1: [],
      icons: [
        {
          value: 0,
          chName: '定制',
          raw: 'custom',
          name: 'icon-ziyuan104',
          size: '16px'
        },
        {
          value: 1,
          chName: '下载',
          raw: 'download',
          name: 'icon-xiazai3',
          size: '16px'
        },
        {
          value: 2,
          chName: '全屏',
          raw: 'fullScreen',
          name: 'icon-ziyuan111',
          size: '16px'
        }
      ],
      sync: false,
      leftSilderIcons: [
        {
          value: 0,
          name: 'icon-zuohua',
          ref: 'left',
          shaowFlag: true,
          size: '25px',
          margin: '90px'
        },
        {
          value: 1,
          name: 'icon-zhegeyidinghang',
          ref: 'right',
          shaowFlag: false,
          size: '25px',
          margin: '10px'
        }
      ],
      rightSilderIcons: [
        {
          value: 2,
          name: 'icon-zhegeyidinghang',
          ref: 'right',
          shaowFlag: true,
          size: '25px'
        },
        {
          value: 3,
          name: 'icon-zuohua',
          ref: 'left',
          shaowFlag: false,
          size: '25px'
        }
      ],
      settingHelp: [
        {
          id: 0,
          name: 'icon-ziyuan107',
          ref: 'setting',
          size: '19px'
        },
        {
          id: 1,
          name: 'icon-ziyuan105',
          ref: 'help',
          size: '19px'
        }
      ],
      syncDataBool: false, // 用来设定timeSync显示是否正常 和 作为开关是否进行同步
      dataSyncVisible: false, // 用来是否显示整个设定数据同步界面
      timeSync: '5',
      operationGuide: false
    }
  },
  computed: {
    ...mapLayoutGetters([
      'allCategoryInform',
      'initShowPanelInfo',
      'initRunFile',
      'waitingPage',
      'initWaitingMessage',
      'getErrorMessage',
      'setDownloadSvgClass',
      'getStateStore'
    ]),
    ...mapLayoutState([
      'userSelectRunFile',
      'multipleFlag',
      'svgDownloadList',
      'initSidebarId',
      'categoryIndex',
      'stateStore'
    ])
  },
  watch: {
    getErrorMessage(val) {
      this.$message({
        message: val.split('_')[0],
        type: 'error'
      })
    },
    selectedRaw(val) {
      if (val === 'media') {
        this.rightSilder(this.rightSilderIcons[0])
      } else if (val === 'graph') {
        this.rightSilder(this.rightSilderIcons[1])
      } else if (this.screenWidth < 1000) {
        this.rightSilder(this.rightSilderIcons[0])
      } else if (this.screenWidth >= 1000) {
        this.rightSilder(this.rightSilderIcons[1])
      }
    },
    screenWidth(val) {
      if (val < 1000) {
        this.isHide(this.leftSilderIcons[0])
        if (this.selectedRaw !== 'graph') {
          this.rightSilder(this.rightSilderIcons[0])
        }
      }
    },
    $route() {
      const path = this.$route.path.split('/')
      const name = path[path.length - 1]
      const id = this.categoryIndex.indexOf(constants.CATEGORYORDER.indexOf(name))
      const item = this.allCategoryInform[id]
      this.initFlag = false
      this.selected = item.id
      this.init = 1
      this.selectedRaw = item.rawName
      this.setRunCategory(item.rawName)
      this.todoName = item.rawName
      // 同步更新
      if (this.syncDataBool) {
        // 开启同步
        this.clearSync()
        this.timingFeatchCategory([this.timeSync * 1000, this.$route.path])
      } else {
        // 关闭同步
        this.clearSync()
      }
    },
    initShowPanelInfo() {
      if (this.$route.path === '/index') {
        this.$router.push({ path: this.initShowPanelInfo.routerName })
      }
      this.initId = this.initSidebarId
    },
    userSelectRunFile() {
      this.$forceUpdate()
      this.value1 = this.userSelectRunFile
    },
    value1() {
      this.getStateStore[this.selectedRaw] = this.value1
      this.setUserSelectRunFile(this.value1)
    },
    inputValue() {},
    multipleFlag() {
      this.isMultiple = this.multipleFlag
    },
    isMultiple() {
      this.update = false
      setTimeout(() => {
        this.update = true
      })
    },
    initWaitingMessage() {
      this.initWaitVisible = false
      if (this.initWaitingMessage === 'error') {
        this.$alert('对不起您没有权限', '警告', {
          confirmButtonText: '确定',
          type: 'error'
        })
      } else {
        this.initFeatchCategory(this.$route.path)
        this.fontSize()
      }
    },
    syncDataBool() {
      // if (this.syncDataBool) {
      //   // 开启同步
      //   this.timingFeatchCategory([this.timeSync * 1000, this.$route.path])
      // } else {
      //   // 关闭同步
      //   this.clearSync()
      // }
    },
    allCategoryInform() {
      if (!this.leftSilderIcons[0].shaowFlag) {
        this.isHide(this.leftSilderIcons[0])
      }
    },
    dataSyncVisible(val) {
      var self = this
      if (!val && this.syncDataBool) {
        if (self.timer) {
          clearTimeout(self.timer)
        }
        self.timer = setInterval(function() {
          self.setTimer()
        }, 1000 * self.timeSync)
      } else if (!val && !this.syncDataBool) {
        if (self.timer) {
          clearTimeout(self.timer)
        }
        self.timer = null
      }
    }
  },
  created() {
    // const params = param2Obj(window.location.href)
    // if (typeof (params.id) === 'undefined' || typeof (params.trainJobName) === 'undefined') {
    //   // 查看sessionStorage里面是否有这两个数据
    //   if (typeof (Storage) !== 'undefined') {
    //     if (sessionStorage.id && sessionStorage.trainJobName) {
    //       params.id = sessionStorage.id
    //       params.trainJobName = sessionStorage.trainJobName
    //     } else {
    //       this.setErrorMessage('没有参数 id 和 trainJobName!!!' + '_' + new Date().getTime())
    //     }
    //   } else {
    //     this.setErrorMessage('对不起，你的浏览器不支持 web storage!!!' + '_' + new Date().getTime())
    //     // document.getElementById("result").innerHTML = "Sorry, your browser does not support web storage...";
    //   }
    // } else {
    //   // 存储一份到sessionStorage里面
    //   sessionStorage.id = params.id
    //   sessionStorage.trainJobName = params.trainJobName
    // }
    // TODO 临时解决方案，最终使用上面的方案
    const params = {
      trainJobName: 'test'
    }
    this.setParams(params)
    this.initWaitingPage({})
  },
  mounted() {
    const h =
      window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
    const hReal = h * 0.905 * 0.075 * 0.5
    this.actegoryClickStyle.divTop = `0 0 ${hReal / 2}px 0`
    this.actegoryClickStyle.divAim = `${hReal}px 0 0 ${hReal}px`
    this.actegoryClickStyle.divBottom = `0 ${hReal / 2}px 0 0`
    const that = this
    window.onresize = () => {
      return (() => {
        window.screenWidth = document.body.clientWidth
        that.screenWidth = window.screenWidth
      })()
    }
    that.screenWidth = document.body.clientWidth
    const secondIndex = 2
    this.selectedRaw = this.$route.path.split('/')[secondIndex]
  },
  methods: {
    ...mapLayoutActions([
      'initFeatchCategory',
      'timingFeatchCategory',
      'timingFeatchCategoryOnce',
      'initWaitingPage'
    ]),
    ...mapLayoutMutations([
      'setCategory',
      'setUserSelectRunFile',
      'setRunCategory',
      'setTimer',
      'clearSync',
      'setParams',
      'setErrorMessage'
    ]),
    ...mapCustomMutations(['setData']),
    isClicked() {
      d3.select('.el-icon-refresh').attr('class', 'el-icon-refresh anim')
      setTimeout(() => {
        d3.select('.anim').attr('class', 'el-icon-refresh')
      }, 5000)
      // 手动的数据同步
      this.timingFeatchCategoryOnce(this.$route.path)
    },
    change(item) {
      this.initFlag = false
      this.selected = item.id
      this.todoName = item.rawName
    },
    getOptions() {
      this.options = this.initRunFile
    },
    isHide(item) {
      if (item.ref === 'left') {
        item.shaowFlag = false
        this.leftSilderIcons[1].shaowFlag = true
        this.leftStyle.width = '62px'
        this.rightStyle.width = 'calc(100% - 62px)'
        this.logoFlag = false
        this.allCategoryInform.forEach((val) => {
          val.name = ''
        })
        this.leftStyle.categoryFlage = true
        this.logoImgStyleFlage = true
      } else if (item.ref === 'right') {
        item.shaowFlag = false
        this.leftSilderIcons[0].shaowFlag = true
        this.leftStyle.width = '180px'
        this.rightStyle.width = 'calc(100% - 180px)'
        this.logoFlag = true
        this.allCategoryInform.forEach((val) => {
          val.icon = val.iconCopy
          val.name = val.nameCopy
        })
        this.leftStyle.categoryFlage = false
        this.logoImgStyleFlage = false
      }
    },
    rightSilder(item) {
      if (item.ref === 'right') {
        item.shaowFlag = false
        this.rightSilderIcons[1].shaowFlag = true
        this.contentsStyle.leftWidth = 'calc(100% - 26px)'
        this.contentsStyle.rightShowFlag = false
        this.rightRetract.setBackLeft = '0.5'
        this.rightRetract.width = '26px'
        this.rightRetract.retractFlage = true
      } else if (item.ref === 'left') {
        item.shaowFlag = false
        this.rightSilderIcons[0].shaowFlag = true
        this.contentsStyle.leftWidth = 'calc(100% - 290px)'
        this.contentsStyle.rightShowFlag = true
        this.rightRetract.setBackLeft = '0'
        this.rightRetract.width = '290px'
        this.rightRetract.retractFlage = false
      }
    },
    jsutTest(val) {
      if (val === 'download') {
        if (this.downloadState.indexOf(this.selectedRaw) >= 0) {
          if (this.svgDownloadList[this.selectedRaw].length === 0) {
            this.setErrorMessage(
              `${'请先在当前页面勾选需要下载的图片' + '_'}${new Date().getTime()}`
            )
          } else {
            this.dialogFormVisible = true
          }
        } else {
          this.setErrorMessage(`${'当前页面不支持下载' + '_'}${new Date().getTime()}`)
          this.dialogFormVisible = false
        }
      } else if (val === 'fullScreen') {
        const isFull =
          document.fullscreenElement ||
          document.mozFullScreenElement ||
          document.webkitFullscreenElement ||
          document.msFullscreenElement
        if (isFull) {
          if (document.cancelFullScreen) {
            document.cancelFullScreen()
          } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen()
          } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen()
          } else if (document.msExitFullscreen) {
            document.msExitFullscreen()
          }
        } else {
          let element
          if (this.selectedRaw === 'graph') {
            element = document.getElementById('full-screen1')
          } else {
            element = document.getElementById('full-screen')
          }
          if (element.requestFullscreen) {
            element.requestFullscreen()
          } else if (element.msRequestFullscreen) {
            element.msRequestFullscreen()
          } else if (element.mozRequestFullScreen) {
            element.mozRequestFullScreen()
          } else if (element.webkitRequestFullScreen) {
            element.webkitRequestFullScreen()
          }
        }
      } else if (val === 'custom') {
        const { className } = document
          .getElementsByClassName('category-selected')[0]
          .getElementsByTagName('i')[0]
        const iconName = className.split(' ')[1]
        let index = 0
        for (; index < this.allCategoryInform.length; index += 1) {
          if (this.allCategoryInform[index].icon === iconName) {
            index = this.allCategoryInform[index].rawName
            break
          }
        }
        this.setData(index)
        if (this.$route.path !== '/index/custom') {
          this.$router.push({ path: '/index/custom' })
        }
      }
    },
    downloadSvg() {
      this.dialogFormVisible = false
      this.svgDownloadList[this.selectedRaw].forEach((val) => {
        const testDOM = document.querySelector(val)
        download.covertSVG2Image(
          testDOM,
          this.form.input,
          testDOM.width.baseVal.value,
          testDOM.height.baseVal.value,
          this.form.type
        )
      })
      this.form.input = '下载'
      this.form.type = 'png'
    },
    downCancel() {
      this.dialogFormVisible = false
      this.form.input = '下载'
      this.form.type = 'png'
    },
    testDownloadJson2csv() {
      const testObject = [
        {
          name: 'xds',
          age: '26',
          gender: 'male'
        },
        {
          name: 'zhngsnan',
          age: '22',
          gender: 'male'
        }
      ]
      download.downloadJSON2CSV(testObject)
    },
    getTigger(val) {
      // const time = new Date()
      // const currentTime = time.toLocaleString()
      // if (val.ref === 'setting') {
      //   this.setTimer(currentTime)
      // }
      if (val.ref === 'setting') {
        // 将同步窗口显示
        this.dataSyncVisible = true
      }
      if (val.ref === 'help') {
        this.operationGuide = true
      }
    },
    fontSize() {
      const deviceWidth = document.documentElement.offsetWidth
      this.autoFontSize = parseInt(deviceWidth / 109, 10)
    }
  }
}
</script>

<style lang="less" scoped>
@deep: ~'/deep/';

.layout-same-style {
  padding: 0;
  margin: 0;
}

.layout-root {
  display: flex;
  flex-direction: row;
  height: 100%;
  overflow: hidden;
  text-align: center;

  ::-webkit-scrollbar {
    width: 5px;
    height: 1px;
    background-color: white;
  }

  ::-webkit-scrollbar-track {
    border-radius: 0;
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.1);
  }

  ::-webkit-scrollbar-thumb {
    background-color: #ccc;
    border-radius: 10px;
  }
}

.layout-header .search-tag input::-webkit-input-placeholder {
  font-size: 12px;
  color: #c0c4ce;
}

.layout-header .search-tag input::-moz-placeholder {
  font-size: 12px;
  color: #c0c4ce;
}

.run-selest {
  width: 100%;
  height: 70%;
  color: #757575;
  border: 1px solid #2f2f2f;
  border-width: 0 0 1px 0;
  border-radius: 3px;

  /deep/ .el-select__tags {
    top: 40%;
    flex-wrap: nowrap;
    overflow: hidden;
  }

  /deep/ .el-input {
    height: 100%;

    /deep/ input {
      height: 100%;
      background-color: transparent;
      border-width: 0;
    }
  }

  /deep/ .el-input__inner {
    font-size: 14px;
    color: #909399;
  }

  /deep/ .el-tag {
    padding-bottom: 4%;
  }

  /deep/ .el-input__suffix {
    top: 10%;
  }

  /deep/ .is-reverse {
    margin: -20% 0 0 0;
  }
}

.layout-header {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 28px;
  background-color: #625eb3;

  .same-div {
    display: flex;
    flex-direction: row;
    width: 33.3%;
    height: 100%;

    .same-p {
      display: flex;
      align-items: center;
      width: 30px;
      height: 100%;
      padding: 0;
      margin: 0;
      cursor: pointer;

      i {
        margin: auto;
        color: white;
      }
    }

    .run-select-container {
      display: flex;
      align-items: center;
      padding: 0;
      margin: 0 0 0 3.5%;

      .icon-setting-help {
        margin: 0 0 0 10px;
        color: white;
      }
    }

    .tool-p {
      height: 70%;
      margin: 1% 0 0 1%;
      border: 1px dashed #bfbfbf;
      border-width: 0 0 0 1px;
    }
  }

  .search-tag {
    flex-direction: row-reverse;

    input:-moz-placeholder {
      font-size: 12px;
      color: #c0c4ce;
    }

    input:-ms-input-placeholder {
      font-size: 12px;
      color: #c0c4ce;
    }
  }
}

.right-slider {
  position: absolute;
  bottom: 0;
  z-index: 10;
  height: 47px;
  clear: none;

  p {
    position: relative;
    font-weight: 700;
    color: #625eb3;
    cursor: pointer;
  }
}

.right-slider-last {
  box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.1);

  p {
    position: relative;
    font-weight: 700;
    color: #625eb3;
    cursor: pointer;
  }
}

.layout-sidebar {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background-color: #f3f7ff;

  .layout-logo {
    display: -webkit-box;
    align-items: center;
    width: 100%;
    height: 50px;
    text-align: center;
    background-color: #f3f7ff;

    img {
      width: 52px;
      height: 27.24px;
      margin-right: 6px;
      margin-left: 6px;
    }

    .img-after {
      width: 52px;
      height: 27.24px;
    }

    span {
      margin: 0 0 0 7%;
      font-family: PingFangSC-Semibold, sans-serif;
      color: white;
    }
  }

  .layout-sidebar-category-container {
    height: calc(100% - 97px);

    .toolDiv {
      height: 3%;
      background-color: #f3f7ff;
    }

    .layout-sidebar-category {
      display: flex;
      flex-direction: column;
      justify-content: space-around;
      width: 100%;
      margin: 0% 0 0 0;
      background-color: #f3f7ff;

      .layout-sidebar-category-each {
        display: flex;
        flex-direction: column;
        background-color: #fff;

        .layout-sidebar-category-each-top {
          flex-grow: 1;
          height: 0%;
          background-color: #f3f7ff;
          border-radius: 0;
        }

        .layout-sidebar-category-each-bottom {
          flex-grow: 1;
          height: 0%;
          background-color: #f3f7ff;
        }

        .layout-sidebar-category-each-middle {
          flex-grow: 1;
          width: 100%;
          height: 56px;
          background-color: #f3f7ff;

          li {
            display: flex;
            align-items: center;
            justify-content: space-around;
            width: 100%;
            height: 100%;
            padding: 0;
            margin: 0 0 0 0%;
            color: rgb(102, 102, 102);
            list-style: none;
            cursor: pointer;
            background-color: #f3f7ff;
            border-radius: 0 0 0 0;

            span {
              float: right;
              margin: 0 20% 0 0;
              font-family: PingFangSC-Regular, sans-serif;
            }

            .span-after {
              margin: 0;
            }

            i {
              float: left;
              margin: 0 0 0 10px;
              font-weight: 500;
            }
          }
        }
      }
    }
  }

  .layout-sidebar-setting {
    width: 100%;
    height: 47px;

    p {
      position: relative;
      font-weight: 700;
      color: #625eb3;
      cursor: pointer;
    }
  }
}

.layout-header-content {
  display: flex;
  flex-direction: column;
}

.layout-content {
  position: relative;
  width: 100%;
  height: 96.5%;

  .layout-content-panel {
    z-index: 0;
    float: left;
    height: 100%;
    background-color: white;
  }

  .layout-content-panel-full-screen {
    position: absolute;
    width: 100%;
    height: 100%;
  }

  .layout-content-paramenter {
    z-index: 0;
    float: right;
    width: 290px;
    height: 94%;
    margin-right: 0;
    overflow-y: auto;
  }
}

.layout-input {
  float: right;
  width: 10%;
  height: 5%;
  margin-top: 0.8%;
}

.category-selected {
  background-color: #d8dfff !important;
}

.tag-search {
  width: 100%;
  height: 70%;
  background: none;
  border: 1px solid #2f2f2f;
  border-width: 0 0 1px 0;
  border-radius: 3px;
  outline: none;

  ::-webkit-input-placeholder {
    color: black;
  }
}

.layout-svg-save-dialog {
  /deep/ .el-dialog {
    width: 360px;
    padding-right: 20px;
    border-radius: 10px;
  }

  /deep/ .el-form-item__label {
    text-align: center;
  }

  /deep/ .el-dialog__body {
    padding: 12px 22px;
  }

  /deep/ .el-dialog__footer {
    padding: 5px 20px 10px;
  }

  /deep/ .el-input-number {
    line-height: 26px;
  }
}
/* stylelint-disable */
.layout-svg {
  * {
    text-align: left;
  }
  .in-text-selection,
  ::selection {
    color: var(--select-text-font-color);
    text-shadow: none;
    background: var(--select-text-bg-color);
  }
  #write {
    position: relative;
    width: inherit;
    height: auto;
    padding-top: 40px;
    margin: 0 auto;
    overflow-x: visible;
    word-break: normal;
    word-wrap: break-word;
    white-space: normal;
  }
  #write.first-line-indent p {
    text-indent: 2em;
  }
  #write.first-line-indent li p,
  #write.first-line-indent p * {
    text-indent: 0;
  }
  #write.first-line-indent li {
    margin-left: 2em;
  }
  .for-image #write {
    padding-right: 8px;
    padding-left: 8px;
  }
  body.typora-export {
    padding-right: 30px;
    padding-left: 30px;
  }
  .typora-export .footnote-line,
  .typora-export li,
  .typora-export p {
    white-space: pre-wrap;
  }

  @media screen and (max-width: 500px) {
    body.typora-export {
      padding-right: 0;
      padding-left: 0;
    }
    #write {
      padding-right: 20px;
      padding-left: 20px;
    }
    .CodeMirror-sizer {
      margin-left: 0 !important;
    }
    .CodeMirror-gutters {
      display: none !important;
    }
  }
  #write li > figure:last-child {
    margin-bottom: 0.5rem;
  }
  #write ol,
  #write ul {
    position: relative;
  }
  img {
    max-width: 100%;
    vertical-align: middle;
    image-orientation: from-image;
  }
  button,
  input,
  select,
  textarea {
    font-family: inherit;
    font-size: inherit;
    font-style: inherit;
    font-weight: inherit;
    font-stretch: inherit;
    line-height: inherit;
    color: inherit;
    font-variant-caps: inherit;
  }
  input[type='checkbox'],
  input[type='radio'] {
    padding: 0;
    line-height: normal;
  }
  *,
  ::after,
  ::before {
    box-sizing: border-box;
  }
  #write h1,
  #write h2,
  #write h3,
  #write h4,
  #write h5,
  #write h6,
  #write p,
  #write pre {
    width: inherit;
  }
  #write h1,
  #write h2,
  #write h3,
  #write h4,
  #write h5,
  #write h6,
  #write p {
    position: relative;
  }
  p {
    line-height: inherit;
  }
  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    break-after: avoid-page;
    break-inside: avoid;
    orphans: 4;
  }
  p {
    orphans: 4;
  }
  h1 {
    font-size: 2rem;
  }
  h2 {
    font-size: 1.8rem;
  }
  h3 {
    font-size: 1.6rem;
  }
  h4 {
    font-size: 1.4rem;
  }
  h5 {
    font-size: 1.2rem;
  }
  h6 {
    font-size: 1rem;
  }
  .md-math-block,
  .md-rawblock,
  h1,
  h2,
  h3,
  h4,
  h5,
  h6,
  p {
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
  .hidden {
    display: none;
  }
  .md-blockmeta {
    font-style: italic;
    font-weight: 700;
    color: rgb(204, 204, 204);
  }
  a {
    cursor: pointer;
  }
  sup.md-footnote {
    padding: 2px 4px;
    color: rgb(85, 85, 85);
    cursor: pointer;
    background-color: rgba(238, 238, 238, 0.7);
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    border-bottom-left-radius: 4px;
  }
  sup.md-footnote a,
  sup.md-footnote a:hover {
    color: inherit;
    text-decoration: inherit;
    text-transform: inherit;
  }
  #write input[type='checkbox'] {
    width: inherit;
    height: inherit;
    cursor: pointer;
  }
  figure {
    max-width: calc(100% + 16px);
    padding: 0;
    margin: 1.2em 0;
    overflow-x: auto;
  }
  figure > table {
    margin: 0;
  }
  tr {
    break-inside: avoid;
    break-after: auto;
  }
  thead {
    display: table-header-group;
  }
  table {
    width: 100%;
    overflow: auto;
    text-align: left;
    border-spacing: 0;
    border-collapse: collapse;
    break-inside: auto;
  }
  table.md-table td {
    min-width: 32px;
  }
  .CodeMirror-gutters {
    background-color: inherit;
    border-right-width: 0;
  }
  .CodeMirror-linenumber {
  }
  .CodeMirror {
    text-align: left;
  }
  .CodeMirror-placeholder {
    opacity: 0.3;
  }
  .CodeMirror pre {
    padding: 0 4px;
  }
  .CodeMirror-lines {
    padding: 0;
  }
  div.hr:focus {
    cursor: none;
  }
  #write pre {
    white-space: pre-wrap;
  }
  #write.fences-no-line-wrapping pre {
    white-space: pre;
  }
  #write pre.ty-contain-cm {
    white-space: normal;
  }
  .CodeMirror-gutters {
    margin-right: 4px;
  }
  .md-fences {
    position: relative !important;
    display: block;
    overflow: visible;
    font-size: 0.9rem;
    text-align: left;
    white-space: pre;
    background-color: inherit;
    background-image: inherit;
    background-repeat: inherit inherit;
    background-attachment: inherit;
    background-position: inherit inherit;
    background-clip: inherit;
    background-origin: inherit;
    background-size: inherit;
    break-inside: avoid;
  }
  .md-diagram-panel {
    width: 100%;
    padding-top: 0;
    padding-bottom: 8px;
    margin-top: 10px;
    overflow-x: auto;
    text-align: center;
  }
  #write .md-fences.mock-cm {
    white-space: pre-wrap;
  }
  .md-fences.md-fences-with-lineno {
    padding-left: 0;
  }
  #write.fences-no-line-wrapping .md-fences.mock-cm {
    overflow-x: auto;
    white-space: pre;
  }
  .md-fences.mock-cm.md-fences-with-lineno {
    padding-left: 8px;
  }
  .CodeMirror-line,
  twitterwidget {
    break-inside: avoid;
  }
  .footnotes {
    margin-top: 1em;
    margin-bottom: 1em;
    font-size: 0.9rem;
    opacity: 0.8;
  }
  .footnotes + .footnotes {
    margin-top: 0;
  }
  .md-reset {
    position: static;
    box-sizing: content-box;
    float: none;
    width: auto;
    height: auto;
    padding: 0;
    margin: 0;
    font-weight: 400;
    line-height: normal;
    text-align: left;
    text-decoration: none;
    text-shadow: none;
    white-space: nowrap;
    vertical-align: top;
    cursor: inherit;
    background-repeat: initial initial;
    background-position: 0 0;
    border: 0;
    outline: 0;
    direction: ltr;
  }
  li div {
    padding-top: 0;
  }
  blockquote {
    margin: 1rem 0;
  }
  li .mathjax-block,
  li p {
    margin: 0.5rem 0;
  }
  li {
    position: relative;
    margin: 0;
  }
  blockquote > :last-child {
    margin-bottom: 0;
  }
  blockquote > :first-child,
  li > :first-child {
    margin-top: 0;
  }
  .footnotes-area {
    padding-bottom: 0.143rem;
    margin-top: 0.714rem;
    color: rgb(136, 136, 136);
    white-space: normal;
  }
  #write .footnote-line {
    white-space: pre-wrap;
  }

  @media print {
    body,
    html {
      height: 99%;
      border: 1px solid transparent;
      break-after: avoid;
      break-before: avoid;
      font-variant-ligatures: no-common-ligatures;
    }
    #write {
      padding-top: 0;
      margin-top: 0;
      border-color: transparent !important;
    }
    .typora-export * {
      -webkit-print-color-adjust: exact;
    }
    html.blink-to-pdf {
      font-size: 13px;
    }
    .typora-export #write {
      padding-right: 32px;
      padding-bottom: 0;
      padding-left: 32px;
      break-after: avoid;
    }
    .typora-export #write::after {
      height: 0;
    }
    .is-mac table {
      break-inside: avoid;
    }
  }
  .footnote-line {
    margin-top: 0.714em;
    font-size: 0.7em;
  }
  a img,
  img a {
    cursor: pointer;
  }
  pre.md-meta-block {
    display: block;
    min-height: 0.8rem;
    overflow-x: hidden;
    font-size: 0.8rem;
    white-space: pre-wrap;
    background-color: rgb(204, 204, 204);
    background-repeat: initial initial;
    background-position: initial initial;
  }
  p > .md-image:only-child:not(.md-img-error) img,
  p > img:only-child {
    display: block;
    margin: auto;
  }
  #write.first-line-indent p > .md-image:only-child:not(.md-img-error) img {
    position: relative;
    left: -2em;
  }
  p > .md-image:only-child {
    display: inline-block;
    width: 100%;
  }
  #write .MathJax_Display {
    margin: 0.8em 0 0;
  }
  .md-math-block {
    width: 100%;
  }
  .md-math-block:not(:empty)::after {
    display: none;
  }
  [contenteditable='true']:active,
  [contenteditable='true']:focus,
  [contenteditable='false']:active,
  [contenteditable='false']:focus {
    outline: 0;
    box-shadow: none;
  }
  .md-task-list-item {
    position: relative;
    list-style-type: none;
  }
  .task-list-item.md-task-list-item {
    padding-left: 0;
  }
  .md-task-list-item > input {
    position: absolute;
    top: 0;
    left: 0;
    margin-top: calc(1em - 10px);
    margin-left: -1.2em;
    border: none;
  }
  .math {
    font-size: 1rem;
  }
  .md-toc {
    position: relative;
    min-height: 3.58rem;
    font-size: 0.9rem;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
  }
  .md-toc-content {
    position: relative;
    margin-left: 0;
  }
  .md-toc-content::after,
  .md-toc::after {
    display: none;
  }
  .md-toc-item {
    display: block;
    color: rgb(65, 131, 196);
  }
  .md-toc-item a {
    text-decoration: none;
  }
  .md-toc-inner:hover {
    text-decoration: underline;
  }
  .md-toc-inner {
    display: inline-block;
    cursor: pointer;
  }
  .md-toc-h1 .md-toc-inner {
    margin-left: 0;
    font-weight: 700;
  }
  .md-toc-h2 .md-toc-inner {
    margin-left: 2em;
  }
  .md-toc-h3 .md-toc-inner {
    margin-left: 4em;
  }
  .md-toc-h4 .md-toc-inner {
    margin-left: 6em;
  }
  .md-toc-h5 .md-toc-inner {
    margin-left: 8em;
  }
  .md-toc-h6 .md-toc-inner {
    margin-left: 10em;
  }

  @media screen and (max-width: 48em) {
    .md-toc-h3 .md-toc-inner {
      margin-left: 3.5em;
    }
    .md-toc-h4 .md-toc-inner {
      margin-left: 5em;
    }
    .md-toc-h5 .md-toc-inner {
      margin-left: 6.5em;
    }
    .md-toc-h6 .md-toc-inner {
      margin-left: 8em;
    }
  }
  a.md-toc-inner {
    font-size: inherit;
    font-style: inherit;
    font-weight: inherit;
    line-height: inherit;
  }
  .footnote-line a:not(.reversefootnote) {
    color: inherit;
  }
  .md-attr {
    display: none;
  }
  .md-fn-count::after {
    content: '.';
  }
  code,
  pre,
  samp,
  tt {
    font-family: var(--monospace);
  }
  kbd {
    padding: 0.1em 0.6em;
    margin: 0 0.1em;
    font-size: 0.8em;
    color: rgb(36, 39, 41);
    white-space: nowrap;
    vertical-align: middle;
    background-color: rgb(255, 255, 255);
    background-repeat: initial initial;
    background-position: initial initial;
    border: 1px solid rgb(173, 179, 185);
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
    border-bottom-left-radius: 3px;
    box-shadow: rgba(12, 13, 14, 0.2) 0 1px 0, rgb(255, 255, 255) 0 0 0 2px inset;
  }
  .md-comment {
    font-family: var(--monospace);
    color: rgb(162, 127, 3);
    opacity: 0.8;
  }
  code {
    text-align: left;
  }
  a.md-print-anchor {
    position: absolute !important;
    right: 0 !important;
    display: inline-block !important;
    width: 1px !important;
    text-shadow: initial !important;
    white-space: pre !important;
    background-repeat: initial initial !important;
    background-position: 0 0 !important;
    border: none !important;
    outline: 0 !important;
  }
  .md-inline-math .MathJax_SVG .noError {
    display: none !important;
  }
  .html-for-mac .inline-math-svg .MathJax_SVG {
    vertical-align: 0.2px;
  }
  .md-math-block .MathJax_SVG_Display {
    position: relative;
    display: block !important;
    width: auto;
    min-width: 100%;
    max-width: none;
    min-height: 0;
    max-height: none;
    margin: 0;
    overflow-y: hidden;
    text-align: center;
    text-indent: 0;
  }
  .MathJax_SVG_Display,
  .md-inline-math .MathJax_SVG_Display {
    display: inline-block !important;
    width: auto;
    margin: inherit;
  }
  .MathJax_SVG .MJX-monospace {
    font-family: var(--monospace);
  }
  .MathJax_SVG .MJX-sans-serif {
    font-family: sans-serif;
  }
  .MathJax_SVG {
    display: inline;
    float: none;
    min-width: 0;
    max-width: none;
    min-height: 0;
    max-height: none;
    padding: 0;
    margin: 0;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    text-align: left;
    text-indent: 0;
    text-transform: none;
    letter-spacing: normal;
    word-wrap: normal;
    white-space: nowrap;
    zoom: 90%;
    border: 0;
    word-spacing: normal;
    direction: ltr;
  }
  .MathJax_SVG * {
    transition: none;
  }
  .MathJax_SVG_Display svg {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    vertical-align: middle !important;
  }
  .os-windows.monocolor-emoji .md-emoji {
    font-family: 'Segoe UI Symbol', sans-serif;
  }
  .md-diagram-panel > svg {
    max-width: 100%;
  }
  [lang='flow'] svg,
  [lang='mermaid'] svg {
    max-width: 100%;
    height: auto;
  }
  [lang='mermaid'] .node text {
    font-size: 1rem;
  }
  table tr th {
    border-bottom-width: 0;
  }
  video {
    display: block;
    max-width: 100%;
    margin: 0 auto;
  }
  iframe {
    width: 100%;
    max-width: 100%;
    border: none;
  }
  .highlight td,
  .highlight tr {
    border: 0;
  }
  svg[id^='mermaidChart'] {
    line-height: 1em;
  }
  mark {
    color: rgb(0, 0, 0);
    background-color: rgb(255, 255, 0);
    background-repeat: initial initial;
    background-position: initial initial;
  }
  .md-html-inline .md-plain,
  .md-html-inline strong,
  mark .md-inline-math,
  mark strong {
    color: inherit;
  }
  mark .md-meta {
    color: rgb(0, 0, 0);
    opacity: 0.3 !important;
  }

  :root {
    --side-bar-bg-color: #fafafa;
    --control-text-color: #777;
  }

  @include-when-export url(https://fonts.loli.net/css?family=Open+Sans:400italic,700italic,700,400&subset=latin,latin-ext);

  /* open-sans-regular - latin-ext_latin */

  /* open-sans-italic - latin-ext_latin */

  /* open-sans-700 - latin-ext_latin */

  /* open-sans-700italic - latin-ext_latin */
  html {
    font-size: 16px;
  }

  body {
    font-family: 'Open Sans', 'Clear Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: rgb(51, 51, 51);
  }

  #write {
    max-width: 860px;
    padding: 30px;
    padding-bottom: 100px;
    margin: 0 auto;
  }

  @media only screen and (min-width: 1400px) {
    #write {
      max-width: 1024px;
    }
  }

  @media only screen and (min-width: 1800px) {
    #write {
      max-width: 1200px;
    }
  }

  #write > ul:first-child,
  #write > ol:first-child {
    margin-top: 30px;
  }

  a {
    color: #4183c4;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    position: relative;
    margin-top: 1rem;
    margin-bottom: 1rem;
    font-weight: bold;
    line-height: 1.4;
    cursor: text;
  }

  h1:hover a.anchor,
  h2:hover a.anchor,
  h3:hover a.anchor,
  h4:hover a.anchor,
  h5:hover a.anchor,
  h6:hover a.anchor {
    text-decoration: none;
  }

  h1 tt,
  h1 code {
    font-size: inherit;
  }

  h2 tt,
  h2 code {
    font-size: inherit;
  }

  h3 tt,
  h3 code {
    font-size: inherit;
  }

  h4 tt,
  h4 code {
    font-size: inherit;
  }

  h5 tt,
  h5 code {
    font-size: inherit;
  }

  h6 tt,
  h6 code {
    font-size: inherit;
  }

  h1 {
    padding-bottom: 0.3em;
    font-size: 2.25em;
    line-height: 1.2;
    border-bottom: 1px solid #eee;
  }

  h2 {
    padding-bottom: 0.3em;
    font-size: 1.75em;
    line-height: 1.225;
    border-bottom: 1px solid #eee;
  }

  h3 {
    font-size: 1.5em;
    line-height: 1.43;
  }

  h4 {
    font-size: 1.25em;
  }

  h5 {
    font-size: 1em;
  }

  h6 {
    font-size: 1em;
    color: #777;
  }

  p,
  blockquote,
  ul,
  ol,
  dl,
  table {
    margin: 0.8em 0;
  }

  li > ol,
  li > ul {
    margin: 0 0;
  }

  hr {
    box-sizing: content-box;
    height: 2px;
    padding: 0;
    margin: 16px 0;
    overflow: hidden;
    background-color: #e7e7e7;
    border: 0 none;
  }

  li p.first {
    display: inline-block;
  }

  ul,
  ol {
    padding-left: 30px;
  }

  ul:first-child,
  ol:first-child {
    margin-top: 0;
  }

  ul:last-child,
  ol:last-child {
    margin-bottom: 0;
  }

  blockquote {
    padding: 0 15px;
    color: #777;
    border-left: 4px solid #dfe2e5;
  }

  blockquote blockquote {
    padding-right: 0;
  }

  table {
    padding: 0;
    word-break: initial;
  }

  table tr {
    padding: 0;
    margin: 0;
    border-top: 1px solid #dfe2e5;
  }

  table tr:nth-child(2n),
  thead {
    background-color: #f8f8f8;
  }

  table tr th {
    padding: 6px 13px;
    margin: 0;
    font-weight: bold;
    border: 1px solid #dfe2e5;
    border-bottom: 0;
  }

  table tr td {
    padding: 6px 13px;
    margin: 0;
    border: 1px solid #dfe2e5;
  }

  table tr th:first-child,
  table tr td:first-child {
    margin-top: 0;
  }

  table tr th:last-child,
  table tr td:last-child {
    margin-bottom: 0;
  }

  .CodeMirror-lines {
    padding-left: 4px;
  }

  .code-tooltip {
    border-top: 1px solid #eef2f2;
    box-shadow: 0 1px 1px 0 rgba(0, 28, 36, 0.3);
  }

  .md-fences,
  code,
  tt {
    padding: 0;
    padding: 2px 4px 0 4px;
    font-size: 0.9em;
    background-color: #f8f8f8;
    border: 1px solid #e7eaed;
    border-radius: 3px;
  }

  code {
    padding: 0 2px 0 2px;
    background-color: #f3f4f4;
  }

  .md-fences {
    padding-top: 8px;
    padding-bottom: 6px;
    margin-top: 15px;
    margin-bottom: 15px;
  }

  .md-task-list-item > input {
    margin-left: -1.3em;
  }

  @media print {
    html {
      font-size: 13px;
    }

    table,
    pre {
      page-break-inside: avoid;
    }

    pre {
      word-wrap: break-word;
    }
  }

  .md-fences {
    background-color: #f8f8f8;
  }

  #write pre.md-meta-block {
    padding: 1rem;
    margin-top: 0 !important;
    font-size: 85%;
    line-height: 1.45;
    color: #777;
    background-color: #f7f7f7;
    border: 0;
    border-radius: 3px;
  }

  .mathjax-block > .code-tooltip {
    bottom: 0.375rem;
  }

  .md-mathjax-midline {
    background: #fafafa;
  }

  #write > h3.md-focus::before {
    top: 0.375rem;
    left: -1.5625rem;
  }

  #write > h4.md-focus::before {
    top: 0.285714286rem;
    left: -1.5625rem;
  }

  #write > h5.md-focus::before {
    top: 0.285714286rem;
    left: -1.5625rem;
  }

  #write > h6.md-focus::before {
    top: 0.285714286rem;
    left: -1.5625rem;
  }

  .md-image > .md-meta {
    padding: 2px 0 0 4px;
    font-size: 0.9em;
    color: inherit;

    /* border: 1px solid #ddd; */
    border-radius: 3px;
  }

  .md-tag {
    color: #a7a7a7;
    opacity: 1;
  }

  .md-toc {
    padding-bottom: 20px;
    margin-top: 20px;
  }

  .sidebar-tabs {
    border-bottom: none;
  }

  #typora-quick-open {
    background-color: #f8f8f8;
    border: 1px solid #ddd;
  }

  #typora-quick-open-item {
    background-color: #fafafa;
    border-color: #fefefe #e5e5e5 #e5e5e5 #eee;
    border-style: solid;
    border-width: 1px;
  }

  /** focus mode */
  .on-focus-mode blockquote {
    border-left-color: rgba(85, 85, 85, 0.12);
  }

  header,
  .context-menu,
  .megamenu-content,
  footer {
    font-family: 'Segoe UI', 'Arial', sans-serif;
  }

  .file-node-content:hover .file-node-icon,
  .file-node-content:hover .file-node-open-state {
    visibility: visible;
  }

  .mac-seamless-mode #typora-sidebar {
    background-color: #fafafa;
    background-color: var(--side-bar-bg-color);
  }

  .md-lang {
    color: #b4654d;
  }

  .html-for-mac .context-menu {
    --item-hover-bg-color: #e6f0fe;
  }

  #md-notification .btn {
    border: 0;
  }

  .dropdown-menu .divider {
    border-color: #e5e5e5;
  }

  .ty-preferences .window-content {
    background-color: #fafafa;
  }

  .ty-preferences .nav-group-item.active {
    color: white;
    background: #999;
  }

  .typora-export li,
  .typora-export p,
  .typora-export,
  .footnote-line {
    white-space: normal;
  }

  /deep/ .el-dialog {
    width: 40%;
    border-radius: 10px;
  }

  /deep/ .el-form-item__label {
    text-align: center;
  }

  /deep/ .el-dialog__body {
    padding: 12px 22px;
  }

  /deep/ .el-dialog__footer {
    padding: 5px 20px 10px;
  }

  /deep/ .el-input-number {
    line-height: 26px;
  }
}
/* stylelint-enable*/
@{deep}.anim {
  animation: myfirst 5s;
}

@keyframes myfirst {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(-360deg);
  }
}
</style>
