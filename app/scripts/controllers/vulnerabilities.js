'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:VulnerabilitiesCtrl
 * @description
 * # VulnerabilitiesCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('VulnerabilitiesCtrl', function ($scope, GridData) {
    GridData('vulnerabilities').query(function(resp){
      $scope.vulnerabilities = resp.items;
    });
  });
