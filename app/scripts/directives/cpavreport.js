'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpAvReport
 * @description
 * # cpAvReport
 */
angular.module('cpApp')
  .directive('cpAvReport', function (GridData, notifications) {
    return {
      restrict: 'E',
      templateUrl: 'views/directives/cp-av-report.html',
      link: function(scope, elem, attrs){
        GridData('analysis/av').get({id: attrs.hash}).$promise.then(
          function(response){
            scope.av_results = response;
          },
          function(error){
            notifications.showError(error.data);
          }
        );
      }
    };
  });
