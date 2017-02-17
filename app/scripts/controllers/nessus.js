'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:NessusCtrl
 * @description
 * # NessusCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('NessusCtrl', function(GridData, $scope, notifications) {
    GridData('analysis/nessus/environments').get().$promise.then(
      function(resp) {
        $scope.envs = resp.environments;
      },
      function(err) {
        notifications.showError(err.data);
      }
    );
  });

