'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UserListCtrl
 * @description
 * # UserListCtrl
 * List Controller of the cpApp
 */

angular.module('cpApp')
  // helps with watching the value in the view scope
  .directive('watchModel', function() {
    return {
      require: 'ngModel',
      link: function(scope, element, attrs, ngModel) {
        scope.$watch(function (){
          return ngModel.$modelValue;
        }, function (v) {
          if (!ngModel.$modelValue) {return}
          scope.filtered_memberships = [];

          // obj2arr
          var users_arr = [];
          for (var key in scope.users) {
            if (scope.users.hasOwnProperty(key)) {
              users_arr.push(scope.users[key]);
            }
          }

          users_arr.forEach(function(u) {
            u.memberships.forEach(function(m) {
              if (m.membership_role_id === scope.membership_role_id) {
                scope.filtered_memberships.push(
                  [u.name,
                   scope.organizations[m.organization_id].full_name,
                   m.email,
                   m.phone
                  ]
                );
              }
            });
          });
        })
      }
    };
  })
  .controller('UserListCtrl', function ($scope, $filter, $uibModal, User, Membership, Organization, Auth, GridData, notifications, $q) {

    var loadUsers = function() {
      return User.query_list().$promise
                .then(function(resp){
                    return resp.users;
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

    var loadRoles = function(){
      return Membership.roles().$promise
                .then(function(resp){
                    return resp.membership_roles;
                  }, function(err){
                    notifications.showError(err.data.message);
                  });
    };

    var loadOrganizations = function(){
      return Organization.query_list().$promise
                .then(function(resp){
                    return resp.organizations;
                  }, function(err){
                    notifications.showError(err.data.message);
                  });
    };

    function _array2hash(arr) {
        var hash = {};
        arr.forEach(function(i) { hash[i.id] = i; });
        return hash;
    }
    var loadParallel = function() {
        return $q.all([ loadUsers(), loadMemberships(), loadRoles(), loadOrganizations() ])
            .then( function( result ) {
              $scope.users         = _array2hash(result.shift());
              $scope.memberships   = result.shift();
              $scope.roles         = result.shift();
              $scope.organizations = _array2hash(result.shift());

              $scope.memberships.forEach(function(m) {
                var u = $scope.users[m.user_id];
                if (!u.hasOwnProperty('memberships')) {
                  u.memberships = [];
                }
                u.memberships.push(m);

                if (!u.hasOwnProperty('organizations')) {
                  u.organizations = [];
                }
                u.organizations.push($scope.organizations[m.organization_id].full_name);
              });

              Object.keys($scope.users).forEach(function(id){
                $scope.users[id].organizations = $scope.users[id].organizations.join(', ');
              });
            }
        );
    };

    loadParallel();

    $scope.arr2text = function(arr) {
      if (!arr) return '';
      var res = '';
      arr.forEach(function(i) {
        res = res + i.join() + '\n';
      });
      return res;
    };

  });
