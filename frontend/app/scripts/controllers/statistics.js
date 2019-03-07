'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:StatisticsCtrl
 * @description
 * # StatisticsListCtrl
 * Statistics Controller of the cpApp
 */
angular.module('cpApp')
  .controller('StatisticsCtrl', function ($scope, Statistics) {
      Statistics.query().$promise
                .then(function(resp){
                    console.log(resp);
                    $scope.statistics_content = resp;
                  }, function(){});
});
