'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:SamplesctrlCtrl
 * @description
 * # SamplesctrlCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('SamplesCtrl', function ($scope, GridData, notifications) {
    $scope.pageChanged = function(){
      //$log.log('Page changed to: ' + $scope.currentPage);
      $scope.loadPage($scope.currentPage);
    };
    $scope.deleteFile = function(fobj){
      GridData('files').delete({id: fobj.id}, function(){
        $scope.loadPage($scope.currentPage);
      }, function(error){
        notifications.showError(error.data);
      });
    };
    $scope.loadPage = function(no){
      if(no === undefined){
        no = 1;
      }
      GridData('samples').query({page: no}, function(resp){
        $scope.files = resp.items;
        $scope.totalItems = resp.count;
        $scope.currentPage = resp.page;
      }, function(err){
        notifications.showError(err);
      });
    };
    $scope.loadPage();
  });
