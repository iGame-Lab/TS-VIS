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
