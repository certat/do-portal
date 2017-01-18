'use strict';

/**
 * @ngdoc filter
 * @name cpApp.filter:isEmptyFilter
 * @function
 * @description
 * # isEmptyFilter
 * Filter in the cpApp.
 */
angular.module('cpApp')
  .filter('isEmptyFilter', function () {
    var prop;
    return function (obj) {
      for (prop in obj) {
        if (obj.hasOwnProperty(prop)) {
          return false;
        }
      }
      return true;
    };
  });
