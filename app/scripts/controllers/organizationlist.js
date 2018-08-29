'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:OrganizationListCtrl
 * @description
 * # OrganizationListCtrl
 * List Controller of the cpApp
 */
angular.module('cpApp')
  .controller('OrganizationListCtrl', function ($scope, $filter, $uibModal, Organization) {

    Organization.query_list().$promise.then(function(resp){
      var tree = arr2tree(resp.organizations, 'id','parent_org_id');
      var orgs = [];
      tree2offset(tree, orgs, 0);
      $scope.orgs = orgs;
    }, function(){});

    // creates a tree from a flat set of hierarchically related data
    function arr2tree(treeData, key, parentKey) {
      var keys = [];
      treeData.map(function(x){
        x.Children = [];
        keys.push(x[key]);
      });
      var roots = treeData.filter(function(x){return keys.indexOf(x[parentKey])===-1;});
      var nodes = [];
      roots.map(function(x){nodes.push(x);});
      while(nodes.length > 0) {
        var node = nodes.pop();
        var children = treeData.filter(function(x){return x[parentKey] === node[key];});
        children.map(function(x){
          node.Children.push(x);
          nodes.push(x);
        });
      }
      return roots;
    }

    // flatten the tree but remember the parent/child structure via an offset property
    function tree2offset(tree, orgs, offset) {
      tree.forEach(function(x) {
        x.offset = offset;
        orgs.push(x);
        tree2offset(x.Children, orgs, offset+1);
        delete x.Children;
      });
    }

  });
