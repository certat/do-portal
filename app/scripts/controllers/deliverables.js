'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:DeliverablesctrlCtrl
 * @description
 * # DeliverablesctrlCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('DeliverablesCtrl', function ($scope, GridData, config) {
    GridData('files').query(function(resp){
      $scope.files = resp.items;
      $scope.webServiceUrl = config.apiConfig.webServiceUrl;
    });
  });
