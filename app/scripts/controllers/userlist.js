'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UserListCtrl
 * @description
 * # UserListCtrl
 * List Controller of the cpApp
 */

angular.module('cpApp')
  .controller('UserListCtrl', function ($scope, $filter, $uibModal, User, Membership, Organization, Auth, GridData, notifications) {

    function _update_users() {
      User.query_list().$promise.then(function(resp){
        $scope.users = resp.users;
      }, function(err){
          console.log(err);
        notifications.showError(err.data.message);
      });
    }
    _update_users();

    $scope.show_form = false;

    Membership.roles().$promise
                .then(function(resp){
                    $scope.roles = resp.membership_roles;
                  }, function(err){
                    notifications.showError(err.data.message);
                  });

    Organization.query_list().$promise
                .then(function(resp){
                    $scope.organizations = resp.organizations;
                  }, function(err){
                    notifications.showError(err.data.message);
                  });

    $scope.create_user = function(u){
      User.create({}, u, function(resp){

        var m = angular.merge({}, resp.membership, $scope.membership);

        Membership.update({'id':m.id}, m, function(resp) {
          $scope.show_form  = false;
          $scope.user       = {};
          $scope.membership = {};
          _update_users();
          notifications.showSuccess(resp);
        }, function(error){
          notifications.showError(error.data);
        });

      }, function(error){
        notifications.showError(error.data);
      });
    };

  });
