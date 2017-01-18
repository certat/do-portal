'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpOnEnter
 * @description
 * # cpOnEnter
 */
angular.module('cpApp')
  .directive('cpOnEnter', function () {
    return function (scope, element, attrs) {
      element.bind('keydown keypress', function (event) {
        if(event.which === 13) {
          scope.$apply(function (){
            scope.$eval(attrs.cpOnEnter);
          });
          event.preventDefault();
        }
      });
    };
  });
