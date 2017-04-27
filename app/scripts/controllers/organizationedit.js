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

    var loadOrganization = function() {
      return Organization.query({'id': $stateParams.id}).$promise
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
        return $q.all([ loadUsers(), loadRoles(), loadMemberships(), loadOrganization() ])
            .then( function( result ) {
              $scope.users       = _array2hash(result.shift());
              $scope.roles       = _array2hash(result.shift());
              $scope.memberships = result.shift().filter(function(m){return m.organization_id == $stateParams.id});
              $scope.org = result.shift();
            }
        );
    };

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

    $scope.toggleFuzzyList = function(list, parent){
      var modalInstance = $uibModal.open({
        templateUrl: 'views/modal-list-typosquats.html',
        controller: 'TyposquatsmodalCtrl',
        size: 'lg',
        resolve: {
          fqdns: function(){
            return list;
          },
          parent: function(){
            return parent;
          }
        }
      });
      modalInstance.result.then(function (resp) {
        console.log(resp);
        //success
      }, function () {
        // modal dismissed, do cleanup
      });
    };

    $scope.appendItem = function(type, org){
      if(org.hasOwnProperty(type)){
        org[type].unshift('');
      }else{
        org[type] = [''];
      }
    };
    $scope.removeItem = function(type, org, val){
      org[type] = $filter('filter')(
        org[type],
        function(v){
          return v !== val;
        }
      );
    };

    $scope.cpAccess = function(org, contactEmail){
      var newAccount = {
        organization_id: org.id,
        name: org.abbreviation + ' (' + contactEmail + ')',
        email: contactEmail
      };
      Auth.registerCPAccount(newAccount).then(function(resp){
        notifications.showSuccess(resp.data);
        Organization.query(function(resp){
          $scope.org = resp;
        });
      }, function(error){
        notifications.showError(error.data);
      });
    };
    $scope.cpRevokeAccess = function(org, contactEmail){
      var unregAccount = {
        organization_id: org.id,
        name: org.abbreviation + ' (' + contactEmail + ')',
        email: contactEmail
      };
      Auth.unregisterCPAccount(unregAccount).then(function(resp){
        notifications.showSuccess(resp.data);
        Organization.query(function(resp){
          $scope.org = resp;
        });
      }, function(error){
        notifications.showError(error.data);
      });
    };

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
