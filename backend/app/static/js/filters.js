'use strict';

angular.module('Portal.filters', [])
    .filter('propsFilter', function () {
      return function (items, props) {
        var out = [];

        if (angular.isArray(items)) {
          items.forEach(function (item) {
            var itemMatches = false;

            var keys = Object.keys(props);
            for (var i = 0; i < keys.length; i++) {
              var prop = keys[i];
              var text = props[prop].toLowerCase();
              if (item[prop].toString().toLowerCase().indexOf(text) !== -1) {
                itemMatches = true;
                break;
              }
            }
            if (itemMatches) {
              out.push(item);
            }
          });
        } else {
          // Let the output be the input untouched
          out = items;
        }
        return out;
      }
    })
    .filter('eventKeys', function () {
      return function (items) {
        var filtered = [];
        angular.forEach(items, function (item) {
          angular.forEach(item.experts, function (experts) {
            angular.forEach(experts, function (v, k) {
              angular.forEach(v, function (vv, kk) {
                if (filtered.indexOf(kk) === -1 && kk.indexOf('$$') !== 0) {
                  filtered.push(kk);
                }
              });
            });
          });
        });
        return filtered;
      }
    })
    .filter('pathsEnd', function () {
      return function (path) {
        return path.split('/').reverse()[0]
      }
    })
    .filter('isEmpty', function () {
      var prop;
      return function (obj) {
        for (prop in obj) {
          if (obj.hasOwnProperty(prop)) {
            return false;
          }
        }
        return true;
      };
    })
    .filter('getByProperty', function () {
      return function (propertyName, propertyValue, collection) {
        var i = 0, len = collection.length;
        for (; i < len; i++) {
          if (collection[i][propertyName] === propertyValue) {
            return collection[i];
          }
        }
        return null;
      }
    })
    .filter('humanize', function () {
      return function (input, char) {
        char = char || '_';
        input = input.replace(new RegExp(char, "g"), ' ');
        return (input).replace(/^([a-z])|\s+([a-z])/g, function ($1) {
          return $1.toUpperCase();
        });
      };
      //return function (input, char) {
      //    char = char || '-';
      //    return input.replace(/ /g, char);
      //}
    });