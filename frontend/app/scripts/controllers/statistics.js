'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:StatisticsCtrl
 * @description
 * # StatisticsListCtrl
 * Statistics Controller of the cpApp
 */
angular.module('cpApp')
  .controller('StatisticsCtrl', function ($scope, $stateParams, $sce, config) {
      var url = config.apiConfig.webServiceUrl + '/statistics';
      if ($stateParams.orgid) {
          url = url + '?orgid=' + $stateParams.orgid;
      }
      $scope.statistics_url = $sce.trustAsResourceUrl(url);
});
