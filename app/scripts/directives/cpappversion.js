'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpAppVersion
 * @description
 * # cpAppVersion
 */
angular.module('cpApp')
  .directive('cpAppVersion', function (config) {
    return function(scope, elem){
      elem.text(config.version);
    };
  });
