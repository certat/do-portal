String.prototype.format = function () {
  var formatted = this;
  for (var prop in arguments[0]) {
    var regexp = new RegExp('\\{' + prop + '\\}', 'gi');
    formatted = formatted.replace(regexp, arguments[0][prop]);
  }
  return formatted;
};
if (typeof String.prototype.trim !== 'function') {
  String.prototype.trim = function () {
    return this.replace(/^\s+|\s+$/g, '');
  }
}
