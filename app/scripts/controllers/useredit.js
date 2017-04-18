'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UsereditctrlCtrl
 * @description
 * # UsereditctrlCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('UsereditCtrl', function ($scope, $filter, $uibModal, User, Auth, GridData, notifications, $stateParams) {
    User.query({'id': $stateParams.id}).$promise.then(function(resp){
      $scope.user = resp;
    }, function(err){
      notifications.showError(err.data.message);
    });

    $scope.save = function(u){
      User.update({'id':u.id}, u, function(resp){
        notifications.showSuccess(resp);
      }, function(error){
        notifications.showError(error.data);
      });
    };
  });
