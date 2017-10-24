'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:OrganizationeditctrlCtrl
 * @description
 * # OrganizationeditctrlCtrl
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

    var loadMemberships = function(){
      return Membership.query().$promise
                .then(function(resp){
                    return resp.organization_memberships;
                  }, function(err){
                    notifications.showError(err.data.message);
                  });
    };

    var loadOrganization = function(org_id) {
      return Organization.query({'id': org_id}).$promise
            .then(function(resp){
                $scope.fuzzed = [];
                angular.forEach(resp.fqdns, function(val){
                    GridData('fqdns').query({'id': val}, function(resp){
                        $scope.fuzzed[val] = resp.typosquats;
                    });
                });
                return resp;
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
        return $q.all([ loadUsers(), loadRoles(), loadMemberships(), loadOrganization($stateParams.id) ])
            .then( function( result ) {
              $scope.users    = _array2hash(result.shift());
              $scope.roles    = _array2hash(result.shift());
              var memberships = result.shift().filter(function(m){return m.organization_id == $stateParams.id});
              memberships.forEach(function(m){ m.country = m.country ? m.country.name : '' });
              $scope.memberships = memberships;

              $scope.org = result.shift();
              if ($scope.org.parent_org_id) {
                loadOrganization($scope.org.parent_org_id)
                  .then(function(resp) {
                    $scope.parent_org = resp;
                  });
              }
            }
        );
    };

    if ($stateParams.edit) {
      $scope.edit = true;
    }

    if ($stateParams.id) {
      loadParallel().catch( function(err) { notifications.showError(err) });
    }
    else {
      $scope.org = {};
      Organization.query_list().$promise.then(function(resp){
        $scope.orgs = resp.organizations;
      }, function(err){
        console.log(err);
        notifications.showError(err.data.message);
      });
    }

    $scope.create_organization = function(){
      Organization.create({}, $scope.org, function(resp){
        $state.go('organizations', {id: resp.organization.id});
        notifications.showSuccess("Organization created.");
      }, function(error){
        notifications.showError(error.data);
      });
    };

    $scope.update_organization = function(){
      Organization.update({'id':$scope.org.id}, $scope.org, function(resp){
        notifications.showSuccess(resp);
      }, function(error){
        notifications.showError(error.data);
      });
    };

    $scope.delete_organization = function(){
      if( window.confirm("Do you really want to delete this organization?") ) {
        Organization.delete({'id':$scope.org.id}, function(resp){
          $state.go('organization_list');
          notifications.showSuccess(resp);
        }, function(error){
          notifications.showError(error.data);
        });
      }
    };
  });
