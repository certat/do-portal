'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpFileSelect
 * @description
 * # cpFileSelect
 */
angular.module('cpApp')
  .directive('cpFileSelect', function () {
    return {
      link: function postLink(scope, element) {
        element.bind('change', function(e){
          scope.getFile(e.target.files[0], scope, element);
        });
      }
    };
  });
