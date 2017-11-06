'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UserListCtrl
 * @description
 * # UserListCtrl
 * List Controller of the cpApp
 */

function _array2hash(arr) {
    if(!arr) {return {};}
    var hash = {};
    arr.forEach(function(i) { hash[i.id] = i; });
    return hash;
}

angular.module('cpApp')
  // helps with watching the value in the view scope
  .directive('watchModel', function() {
    return {
      require: 'ngModel',
      link: function(scope, element, attrs, ngModel) {
        scope.$watch(function (){
          return ngModel.$modelValue;
        }, function (v) {
          function filter_memberships(id) {

            // obj2arr
            var users_arr = [];
            for (var key in scope.users) {
              if (scope.users.hasOwnProperty(key)) {
                users_arr.push(scope.users[key]);
              }
            }
            var memberships = [];
            if (id) {
              users_arr.forEach(function(u) {
                u.memberships.forEach(function(m) {
                  if (m.membership_role_id === id) {
                    memberships.push(
                      [u.name,
                       scope.organizations[m.organization_id].full_name,
                       m.email,
                       m.phone,
                       m.mobile
                      ]
                    );
                  }
                });
              });
            }
            else {
              var roles = _array2hash(scope.roles);
              users_arr.forEach(function(u) {
                u.memberships.forEach(function(m) {
                  memberships.push(
                    [u.name,
                     scope.organizations[m.organization_id].full_name,
                     roles[m.membership_role_id].display_name,
                     m.email,
                     m.phone,
                     m.mobile,
                     m.street,
                     m.zip,
                     m.city
                    ]
                  );
                });
              });
            };
            return memberships;
          }

          scope.filtered_memberships_headers = scope.get_filtered_membership_headers();
          scope.filtered_memberships = filter_memberships(v);
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

    var loadParallel = function() {
        return $q.all([ loadUsers(), loadMemberships(), loadRoles(), loadOrganizations() ])
            .then( function( result ) {
              $scope.users         = _array2hash(result.shift());
              $scope.memberships   = result.shift();
              $scope.roles         = result.shift();
              $scope.organizations = _array2hash(result.shift());

              // populates the dropdown list in user_export
              $scope.export_types = angular.copy($scope.roles);
              $scope.export_types.push({ display_name: 'all', id: '0' });

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

    $scope.get_filtered_membership_headers = function(){
      if($scope.membership_role_id) {
        return [ 'name', 'organization', 'email', 'phone', 'mobile' ];
      }
      else {
        return [ 'name', 'organization', 'role', 'email', 'phone', 'mobile', 'street', 'zip', 'city' ];
      }
    };
    $scope.addHeader = function(txt) {
      return $scope.get_filtered_membership_headers().join(',')+'\n'+txt;
    };

    $scope.arr2text = function(arr) {
      if (!arr) return '';
      var res = '';
      arr.forEach(function(i) {
        res = res + i.join() + '\n';
      });
      return res;
    };

  });
