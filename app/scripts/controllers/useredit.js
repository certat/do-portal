'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UsereditctrlCtrl
 * @description
 * # UsereditctrlCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('UsereditCtrl', function ($scope, $filter, $uibModal, User, Auth, GridData, notifications, $stateParams, $q) {

    var loadUser = function() {
      return User.query({'id': $stateParams.id}).$promise
                .then(function(resp){
                    return resp;
                  }, function(err){
                    notifications.showError(err.data.message);
                  });
    };

    var loadRoles = function(){
      return User.roles().$promise
                .then(function(resp){
                    return resp.membership_roles;
                  }, function(err){
                    notifications.showError(err.data.message);
                  });
    };

    var loadMemberships = function(){
      return User.memberships().$promise
                .then(function(resp){
                    return resp.organization_memberships;
                  }, function(err){
                    notifications.showError(err.data.message);
                  });
    };

    var loadParallel = function() {
        return $q.all([ loadUser(), loadRoles(), loadMemberships() ])
            .then( function( result ) {
              $scope.user = result.shift();
              $scope.roles = result.shift();
              $scope.memberships = result.shift()
                    .filter(function(val){return val.user_id === $scope.user.id});
              console.log($scope.memberships);
//+        $scope.memberships = [
//+            { org: { id: 1, name: "org1" }, role: { id: 1, name: "role1" } },
//+            { org: { id: 2, name: "org2" }, role: { id: 2, name: "role2" } },
//+            { org: { id: 3, name: "org3" }, role: { id: 3, name: "role3" } },
//+        ];
            });
    };

    loadParallel();

    $scope.save = function(u){
      User.update({'id':u.id}, u, function(resp){
        notifications.showSuccess(resp);
      }, function(error){
        notifications.showError(error.data);
      });
    };

  });
