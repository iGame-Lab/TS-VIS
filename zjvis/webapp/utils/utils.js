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
/**
 * @param {string} url
 * @returns {Object}
 */
export function param2Obj(url) {
  const search = url.split('?')[1]
  if (!search) {
    return {}
  }
  return JSON.parse(
    '{"' +
        decodeURIComponent(search)
          .replace(/"/g, '\\"')
          .replace(/&/g, '","')
          .replace(/=/g, '":"')
          .replace(/\+/g, ' ') +
        '"}'
  )
}

/**
 * @param {string} unixTimestamp
 * @returns {string} normalTime
 */
export function unixTimestamp2Normal(unixTimestamp) {
  var unixTimestampLocal = new Date(unixTimestamp * 1000)
  var commonTime = unixTimestampLocal.toLocaleString('en-GB', { hour12: false })
  var tim = commonTime.split('\/')
  var year = tim[2].split(',')[0]
  var month = tim[1]
  var day = tim[0]
  var tt = tim[2].split(',')[1]
  return year + '/' + month + '/' + day + tt
}
