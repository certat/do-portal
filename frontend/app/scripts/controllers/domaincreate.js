'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:DomaincreateCtrl
 * @description
 * # DomaincreateCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('DomaincreateCtrl', function ($scope, $filter, $uibModal, Domain, Organization, Auth, GridData, notify, $stateParams, $state, $q) {
    function _array2hash(arr) {
        var hash = {};
        arr.forEach(function(i) { hash[i.id] = i; });
        return hash;
    }

    var loadOrganization = function(org_id) {
      if (!org_id) { return {}; }
      return Organization.query({'id': org_id}).$promise
            .then(function(resp){
                return resp;
            }, function(){});
    };

    var loadParallel = function() {
        return $q.all([loadOrganization($stateParams.org_id)])
            .then(function(result) {
              var organization = result.shift();
              if (organization.id == undefined) {
                $state.go('organization_list', {});
                notify({classes: 'notify-error', message: 'Organization not found.'});
              }
              else {
                $scope.organization = organization;
                $scope.domain = {'organization_id': $scope.organization.id};
              }
            }
        );
    };

    loadParallel();

    $scope.create_domain = function(){
      Domain.create({}, $scope.domain, function(resp){
        $state.go('organizations', {'id': $scope.organization.id});
        notify({classes: 'notify-success', message: resp.message});
      }, function(){});
    };
  });
