/* global angular */
/**
 * https://gist.github.com/mlynch/dd407b93ed288d499778
 *
 * the HTML5 autofocus property can be finicky when it comes to dynamically
 * loaded templates and such with AngularJS. Use this simple directive to tame
 * this beast once and for all.
 *
 * Usage:
 * <input type="text" autofocus>
 */
(function () {
  'use strict';

  angular.module('utils.autofocus', [])

  .directive('autofocus', ['$timeout',
    function ($timeout) {
      return {
        restrict: 'A',
        link: function ($scope, $element) {
          $timeout(function () {
            $element[0].focus();
          });
        }
      };
    }
  ]);
})();
