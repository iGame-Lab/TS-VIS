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
import FileSaver from 'file-saver'
const Json2csvParser = require('json2csv').Parser

const covertSVG2Image = (node, name, width, height, type = 'png') => {
  /**
   * @name: 将svg导出成图片
   * @msg: ~
   * @param node svg节点 => document.querySelector('svg')
   * @param name 生成的图片名称
   * @param width 生成的图片宽度
   * @param height 生成的图片高度
   * @param type 生成的图片类型
   * @return: 'img'
   */
  const serializer = new XMLSerializer()
  const source = '<?xml version="1.0" standalone="no"?>\r\n' + serializer.serializeToString(node)
  const image = new Image()
  image.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(source)
  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height
  const context = canvas.getContext('2d')
  context.fillStyle = '#fff'
  context.fillRect(0, 0, 10000, 10000)
  image.onload = function() {
    context.drawImage(image, 0, 0)
    const a = document.createElement('a')
    a.download = `${name}.${type}`
    a.href = canvas.toDataURL(`image/${type}`)
    a.click()
  }
}

const downloadJSON2CSV = (data, filename = 'test.csv') => {
  const parser = new Json2csvParser()
  const csvData = parser.parse(data)
  const blob = new Blob(['\uFEFF' + csvData], { type: 'text/plain;charset=utf-8;' })
  FileSaver.saveAs(blob, filename)
}

export default { covertSVG2Image, downloadJSON2CSV }
