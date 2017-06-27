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
      var orgs = [];
      make_tree(orgs, resp.organizations)
      $scope.orgs = orgs;
    }, function(err){
      notifications.showError(err.data.message);
    });

    function make_tree(output_orgs, input_orgs, parentid, offset) {
      if (!parentid) {
        input_orgs.forEach(function(o) {
          if (!o.parent_org_id) {
            o.offset = 0;
            output_orgs.push(o);
            make_tree(output_orgs, input_orgs, o.id, 1);
          }
        });
      }
      else {
        input_orgs.forEach(function(o) {
          if (o.parent_org_id === parentid) {
            o.offset = offset;
            output_orgs.push(o);
            make_tree(output_orgs, input_orgs, o.id, offset+1);
          }
        });
      }
    }

  });
