'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpConfirm
 * @description
 * # cpConfirm
 */
angular.module('cpApp')
  .directive('cpConfirm', function () {
    return {
      priority: -1,
      restrict: 'A',
      link: function postLink(scope, element, attrs) {
        element.bind('click', function (e) {
          var message = attrs.doConfirm;
          if (message && !confirm(message)) {
            e.stopImmediatePropagation();
            e.preventDefault();
          }
        });
      }
    };
  });
