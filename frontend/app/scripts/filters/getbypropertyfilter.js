'use strict';

/**
 * @ngdoc filter
 * @name cpApp.filter:getByPropertyFilter
 * @function
 * @description
 * # getByPropertyFilter
 * Filter in the cpApp.
 */
angular.module('cpApp')
  .filter('getByPropertyFilter', function () {
    return function (propertyName, propertyValue, collection) {
      var i = 0, len = collection.length;
      for (; i < len; i++) {
        if (collection[i][propertyName] === propertyValue) {
          return collection[i];
        }
      }
      return null;
    };
  });
