'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:OrganizationeditctrlCtrl
 * @description
 * # OrganizationeditctrlCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('OrganizationeditCtrl', function ($scope, $filter, $uibModal, Organization, Auth, GridData, notifications) {
    Organization.query(function(resp){
      $scope.org = resp;
      $scope.fuzzed = [];
      angular.forEach(resp.fqdns, function(val){
        GridData('fqdns').query({'id': val}, function(resp){
          $scope.fuzzed[val] = resp.typosquats;
        });
      });
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
      Organization.update(o, function(resp){
        notifications.showSuccess(resp);
      }, function(error){
        notifications.showError(error.data);
      });
    };
  });
