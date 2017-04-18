'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UserListCtrl
 * @description
 * # UserListCtrl
 * List Controller of the cpApp
 */


/*
var setup_user_membership_watcher = function($scope) {
  $scope.$watch(
      function($scope){
        return $scope.users.map(
          function(u){return {user: u, is_member: u.is_member}}
        )
      },
      function(newV, oldV, scope){console.log(oldV,newV)},
      true
  );
};
*/

      /*
    User.users().$promise.then(function(resp){
      $scope.users = resp.users;
      $scope.users.forEach(function(u){
          if (u.user_id === $scope.org.id) {
              u.is_member=true;
          }
      });
      setup_user_membership_watcher($scope);
    }, function(err){
      notifications.showError(err.data.message);
    });
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
