const StrategyMap = {
  Max: function(tag, number, data) {
    return context("max", tag, number, data);
  },
  Min: function(tag, number, data) {
    return context("min", tag, number, data);
  },
  Quar: function(tag, number, data) {
    return context("quar", tag, number, data);
  },
  Vari: function(tag, number, data) {
    return context("vari", tag, number, data);
  }
};

const context = function(metric, tag, number, data) {
  return filterMap[tag] && filterMap[tag](metric, number, data);
};

const filterMap = {
  "<": function(metric, number, data) {
    return data.filter(item => item[metric] < number);
  },
  "<=": function(metric, number, data) {
    return data.filter(item => item[metric] <= number);
  },
  ">=": function(metric, number, data) {
    return data.filter(item => item[metric] >= number);
  },
  ">": function(metric, number, data) {
    return data.filter(item => item[metric] > number);
  }
};

export default StrategyMap;
