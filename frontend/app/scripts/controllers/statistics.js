'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:StatisticsCtrl
 * @description
 * # StatisticsListCtrl
 * Statistics Controller of the cpApp
 */
angular.module('cpApp')
  .controller('StatisticsCtrl', function ($scope, $stateParams, $sce, config, Statistics) {
      var orgid = $stateParams.orgid;
      var query_params = orgid ? {orgid:orgid} : {};
      Statistics.query(query_params).$promise.then(function(resp){
        var url = config.apiConfig.webServiceUrl + resp.statistics_url;
        $scope.statistics_url = $sce.trustAsResourceUrl(url);
      }, function(){});
});
