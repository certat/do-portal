'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UserListCtrl
 * @description
 * # UserListCtrl
 * List Controller of the cpApp
 */

angular.module('cpApp')
  .controller('UserListCtrl', function ($scope, $filter, $uibModal, User, Auth, GridData, notifications) {
    User.query_list().$promise.then(function(resp){
      $scope.users = resp.users;
    }, function(err){
        console.log(err);
      notifications.showError(err.data.message);
    });

  });
