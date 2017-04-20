'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UsereditctrlCtrl
 * @description
 * # UsereditctrlCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .directive('convertToNumber', function() {
    return {
      require: 'ngModel',
      link: function(scope, element, attrs, ngModel) {
          ngModel.$parsers.push(function(val) {
            return parseInt(val, 10);
          });
          ngModel.$formatters.push(function(val) {
            return '' + val;
          });
        }
    };
  })
  .controller('UsereditCtrl', function ($scope, $filter, $uibModal, User, Organization, Membership, Auth, GridData, notifications, $stateParams, $state, $q) {

    var loadUser = function() {
      return User.query({'id': $stateParams.id}).$promise
                .then(function(resp){
                    return resp;
                  }, function(err){
                    notifications.showError(err.data.message);
                  });
    };

    var loadRoles = function(){
      return Membership.roles().$promise
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
      return Membership.query().$promise
                .then(function(resp){
                    return resp.organization_memberships;
                  }, function(err){
                    notifications.showError(err.data.message);
                  });
    };

    function _prepare_memberships(memberships) {
      memberships = memberships.filter(function(m){return m.user_id === $scope.user.id});
      memberships.forEach(function(m){
          m.org  = {
            id: m.organization_id,
            name: $scope.organizations[m.organization_id].display_name
          };
          m.role = {
              id: m.membership_role_id,
              name: $scope.roles[m.membership_role_id].display_name
          };
      });
      memberships = memberships.sort(function(a,b){
          if ( a.org.name < b.org.name ) {
              return -1;
          } else {
              return 1;
          }
      });
      return memberships;
    }
    function _array2hash(arr) {
        var hash = {};
        arr.forEach(function(i) { hash[i.id] = i });
        return hash;
    }
    var loadParallel = function() {
        return $q.all([ loadUser(), loadRoles(), loadOrgs(), loadMemberships() ])
            .then( function( result ) {
              $scope.user          = result.shift();
              $scope.roles         = _array2hash(result.shift())
              $scope.organizations = _array2hash(result.shift())
              $scope.memberships   = _prepare_memberships(result.shift());
              if ($scope.memberships.length <= 0) {
                $scope.memberships = [{}];
              }
            }
        );
    };

    var create_user = function(){
      var u = $scope.user;
      u.role_id = $scope.memberships[0].membership_role_id;
      u.organization_id = $scope.memberships[0].organization_id;
      User.create({}, u, function(resp){
        var user_id = resp.user.id;
        var m = angular.merge({}, resp.membership, $scope.memberships[0]);
        Membership.update({'id':m.id}, m, function(resp) {
          $state.go('user_edit',{id: user_id});
          notifications.showSuccess(resp);
        }, function(error){
          notifications.showError(error.data);
        });

      }, function(error){
        notifications.showError(error.data);
      });
    };

    var update_user = function(){
      var u = $scope.user;
      User.update({'id':u.id}, u, function(resp){
        notifications.showSuccess(resp);
      }, function(error){
        notifications.showError(error.data);
      });
      $scope.memberships.forEach(function(m) {
        Membership.update({'id':m.id}, m, function(resp) {
          $state.go('user_edit',{id: u.id});
          notifications.showSuccess(resp);
        }, function(error){
          notifications.showError(error.data);
        });
      });
    };

    $scope.delete_membership = function(m_id, index){
      Membership.delete({'id':m_id}).$promise
            .then(function(resp){
                notifications.showSuccess(resp);
                $scope.memberships.splice(index, 1);
            }, function(error){
                notifications.showError(error.data);
            });
        };

    loadParallel().catch( function(err) { notifications.showError(err) });
    if ($stateParams.id) {
      $scope.save = update_user;
    }
    else {
      $scope.save = create_user;
    }

  });
