'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:StatisticsCtrl
 * @description
 * # StatisticsListCtrl
 * Statistics Controller of the cpApp
 */
angular.module('cpApp')
  .controller('StatisticsCtrl', function ($scope, $sce, config) {
      $scope.statistics_url = $sce.trustAsResourceUrl(config.apiConfig.webServiceUrl + '/statistics');
});
