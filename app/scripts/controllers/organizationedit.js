'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:OrganizationeditctrlCtrl
 * @description
 * # OrganizationeditctrlCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('OrganizationeditCtrl', function ($scope, $filter, $uibModal, Organization, User, Membership, Auth, GridData, notifications, $stateParams, $q) {

    var loadUsers = function() {
      if (!$stateParams.id) { return {} };
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
      if (!$stateParams.id) { return [{}] };
      return Membership.query().$promise
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
        return $q.all([ loadUsers(), loadRoles(), loadMemberships() ])
            .then( function( result ) {
              $scope.users       = _array2hash(result.shift());
              $scope.roles       = _array2hash(result.shift());
              $scope.memberships = result.shift().filter(function(m){return m.organization_id == $stateParams.id});
            }
        );
    };
    loadParallel().catch( function(err) { notifications.showError(err) });

    Organization.query({'id': $stateParams.id}).$promise.then(function(resp){
      $scope.org = resp;
      $scope.fuzzed = [];
      angular.forEach(resp.fqdns, function(val){
        GridData('fqdns').query({'id': val}, function(resp){
          $scope.fuzzed[val] = resp.typosquats;
        });
      });
    }, function(err){
      notifications.showError(err.data.message);
    });

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

    $scope.save = function(o){
      Organization.update({'id':o.id}, o, function(resp){
        notifications.showSuccess(resp);
      }, function(error){
        notifications.showError(error.data);
      });
    };
  });
