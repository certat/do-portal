'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpSampleDetails
 * @description
 * # cpSampleDetails
 */
angular.module('cpApp')
  .directive('cpSampleDetails', function (GridData, notifications) {
    return {
      restrict: 'E',
      templateUrl: 'views/directives/cp-sample-details.html',
      link: function(scope, elem, attrs){
        GridData('samples').get({id: attrs.hash}).$promise.then(
          function(response){
            scope.sample = response;
          },
          function(error){
            notifications.showError(error.data);
          }
        );
      }
    };
  });
