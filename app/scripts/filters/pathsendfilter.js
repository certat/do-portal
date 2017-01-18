'use strict';

/**
 * @ngdoc filter
 * @name cpApp.filter:pathsEndFilter
 * @function
 * @description
 * # pathsEndFilter
 * Filter in the cpApp.
 */
angular.module('cpApp')
  .filter('pathsEndFilter', function () {
    return function(path){
      return path.split('/').reverse()[0];
    };
  });
