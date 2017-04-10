'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:OrganizationListCtrl
 * @description
 * # OrganizationListCtrl
 * List Controller of the cpApp
 */
angular.module('cpApp')
  .controller('OrganizationListCtrl', function ($scope, $filter, $uibModal, Organization, Auth, GridData, notifications) {
    Organization.query_list().$promise.then(function(resp){
      $scope.orgs = resp.organizations;
    }, function(err){
        console.log(err);
      notifications.showError(err.data.message);
    });

  });
