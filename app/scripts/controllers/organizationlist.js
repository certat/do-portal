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
      var output_orgs = [];
      make_tree(output_orgs, resp.organizations)
      $scope.orgs = output_orgs;
    }, function(err){
      notifications.showError(err.data.message);
    });

    function make_tree(output_orgs, input_orgs) {
      var root_org = find_root(input_orgs);
      root_org.offset = 0;
      output_orgs.push(root_org);
      find_children(output_orgs, input_orgs, root_org.id, 1);
    }

    function find_root(orgs) {
      var root;
      orgs.forEach(function(o) {
        if (!o.parent_org_id) {
          if (typeof root !== 'undefined') {
            notifications.showError('There are multiple root organizations in the database.');
          }
          else {
            root = o;
          }
        }
      });
      if (typeof root === 'undefined') {
        notifications.showError('No root organization found in the database.');
      }
      return root;
    }

    function find_children(output_orgs, input_orgs, parentid, offset) {
      input_orgs.forEach(function(o) {
        if (!o.hasOwnProperty('offset') && o.parent_org_id === parentid) {
          o.offset = offset;
          output_orgs.push(o);
          find_children(output_orgs, input_orgs, o.id, offset+1);
        }
      });
    }
  });
