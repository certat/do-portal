'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UsereditctrlCtrl
 * @description
 * # UsereditctrlCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('UsereditCtrl', function ($scope, $filter, $uibModal, User, Organization, Auth, GridData, notifications, $stateParams, $q) {

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

    var loadOrgs = function(){
      return Organization.query_list().$promise
                .then(function(resp){
                    return resp.organizations;
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

    function _array2hash(arr) {
        var hash = {};
        arr.forEach(function(i) { hash[i.id] = i });
        return hash;
    }
    var loadParallel = function() {
        return $q.all([ loadUser(), loadRoles(), loadOrgs(), loadMemberships() ])
            .then( function( result ) {
              $scope.user        = result.shift();
              $scope.roles       = _array2hash(result.shift())
              $scope.orgs        = _array2hash(result.shift())
              $scope.memberships = result.shift()
                    .filter(function(m){return m.user_id === $scope.user.id});
              $scope.memberships.forEach(function(m){
                  m.org  = {
                      id: m.organization_id,
                      name: $scope.orgs[m.organization_id].display_name
                  };
                  m.role = {
                      id: m.membership_role_id,
                      name: $scope.roles[m.membership_role_id].display_name
                  };
              });
              $scope.memberships = $scope.memberships.sort(function(a,b){
                  if ( a.org.name < b.org.name ) {
                      return -1;
                  } else {
                      return 1;
                  }
              });
            }
        );
    };

    loadParallel()
          .catch( function(err) { notifications.showError(err) });

    $scope.save = function(u){
      User.update({'id':u.id}, u, function(resp){
        notifications.showSuccess(resp);
      }, function(error){
        notifications.showError(error.data);
      });
    };

  });
