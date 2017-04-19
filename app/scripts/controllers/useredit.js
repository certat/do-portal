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
      var user = resp;
      _setup_memberships(user);
      $scope.user = user;
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

    function _setup_memberships(u) {

      /*
      User.memberships().$promise.then(function(resp){
        $scope.memberships = resp.organization_memberships.filter(function(val){return val.user_id === u.id});
      }, function(err){
        notifications.showError(err.data.message);
      });

      User.roles().$promise.then(function(resp){
        $scope.roles = resp.membership_roles;
      }, function(err){
        notifications.showError(err.data.message);
      });
      */

      $scope.memberships = [
          { org: { id: 1, name: "org1" }, role: { id: 1, name: "role1" } },
          { org: { id: 2, name: "org2" }, role: { id: 2, name: "role2" } },
          { org: { id: 3, name: "org3" }, role: { id: 3, name: "role3" } },
      ];
    }

  });
