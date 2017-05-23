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
      var orgs = resp.organizations;
      set_offset(orgs);
      $scope.orgs = orgs;
    }, function(err){
        console.log(err);
      notifications.showError(err.data.message);
    });

    function set_offset(orgs, parentid, offset) {
      if (!parentid) {
        orgs.forEach(function(o) {
          if (!o.parent_org_id) {
            o.offset = 0;
            set_offset(orgs, o.id, 1);
          }
        });
      }
      else {
        orgs.forEach(function(o) {
          if (o.parent_org_id === parentid) {
            o.offset = offset;
            set_offset(orgs, o.id, offset+1);
          }
        });
      }
    }

  });
