'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:OrganizationeditCtrl
 * @description
 * # OrganizationeditCtrl
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
  .directive('positiveInteger', function() {
    return {
      require: 'ngModel',
      link: function(scope, element, attrs, ctrl) {
        ctrl.$validators.integer = function(modelValue, viewValue) {
          var val = parseInt(viewValue, 10);
	  return (val > 0);
        };
      }
    };
  })
  .controller('OrganizationeditCtrl', function ($scope, $filter, $uibModal, Organization, User, Membership, Auth, GridData, notifications, $stateParams, $q, $state) {

    var loadUsers = function() {
      return User.query_list().$promise
                .then(function(resp){
                    return resp.users;
                  }, function(){});
    };

    var loadRoles = function(){
      return Membership.roles().$promise
                .then(function(resp){
                    return resp.membership_roles;
                  }, function(){});
    };

    var loadMemberships = function(){
      return Membership.query().$promise
                .then(function(resp){
                    return resp.organization_memberships;
                  }, function(){});
    };

    var loadOrganization = function(org_id) {
      return Organization.query({'id': org_id}).$promise
            .then(function(resp){
                return resp;
            }, function(){});
    };

    function _array2hash(arr) {
        var hash = {};
        arr.forEach(function(i) { hash[i.id] = i; });
        return hash;
    }
    var loadParallel = function() {
        return $q.all([ loadUsers(), loadRoles(), loadMemberships(), loadOrganization($stateParams.id) ])
            .then( function( result ) {
              $scope.users    = _array2hash(result.shift());
              $scope.roles    = _array2hash(result.shift());
              var memberships = result.shift().filter(function(m){return m.organization_id === parseInt($stateParams.id);});
              memberships.forEach(function(m){ m.country = m.country ? m.country.name : ''; });
              $scope.memberships = memberships;

              $scope.org = result.shift();
            }
        );
    };

    if ($stateParams.edit) {
      $scope.edit = true;
    }

    if ($stateParams.id) {
      loadParallel();
    }
    else {
      $scope.org = {};
      Organization.query_list().$promise.then(function(resp){
        $scope.orgs = resp.organizations;
      }, function(){});
    }

    $scope.create_organization = function(){
      Organization.create({}, $scope.org, function(resp){
        $state.go('organizations', {id: resp.organization.id});
        notifications.showSuccess('Organization created.');
      }, function(){});
    };

    $scope.update_organization = function(){
      Organization.update({'id':$scope.org.id}, $scope.org, function(resp){
        notifications.showSuccess(resp);
      }, function(){});
    };

    $scope.delete_organization = function(){
      if( window.confirm('Do you really want to delete this organization?') ) {
        Organization.delete({'id':$scope.org.id}, function(resp){
          $state.go('organization_list');
          notifications.showSuccess(resp);
        }, function(){});
      }
    };
  });
