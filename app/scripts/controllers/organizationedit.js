'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:OrganizationeditCtrl
 * @description
 * # OrganizationeditCtrl
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
  .controller('OrganizationeditCtrl', function ($scope, $filter, $uibModal, Organization, User, Membership, Auth, GridData, notify, $stateParams, $q, $state, uiGridConstants) {

    var loadUsers = function() {
      return User.query_list().$promise
                .then(function(resp){
                    return resp.users;
                  }, function(){});
    };

    var loadRoles = function(){
      return Membership.roles().$promise
                .then(function(resp){
                    return resp.membership_roles;
                  }, function(){});
    };

    var loadMemberships = function(){
      return Membership.query().$promise
                .then(function(resp){
                    return resp.organization_memberships;
                  }, function(){});
    };

    var loadOrganization = function(org_id) {
      return Organization.query({'id': org_id}).$promise
            .then(function(resp){
                return resp;
            }, function(){});
    };

    function _array2hash(arr) {
        var hash = {};
        arr.forEach(function(i) { hash[i.id] = i; });
        return hash;
    }
    function get_role_options(roles) {
        var roleOptions = [];
        for(var role_name in roles) {
          roleOptions.push({value: role_name, label: role_name});
        }
        return roleOptions.sort(function(a,b){
	  var nameA = a.label.toUpperCase();
	  var nameB = b.label.toUpperCase();
	  if (nameA < nameB) { return -1; }
	  if (nameA > nameB) { return 1; }
	  return 0;
        });
    }
    var loadParallel = function() {
        return $q.all([ loadUsers(), loadRoles(), loadMemberships(), loadOrganization($stateParams.id) ])
            .then( function( result ) {
              $scope.users    = _array2hash(result.shift());
              $scope.roles    = _array2hash(result.shift());
              var memberships = result.shift().filter(function(m){return m.organization_id === parseInt($stateParams.id);});
              var gridData = [];
              var roles = {};
              memberships.forEach(function(m){
                  var role_name = $scope.roles[m.membership_role_id].display_name;
                  roles[role_name] = 1;
                  gridData.push({
                      user_id: m.user_id,
                      user: $scope.users[m.user_id].name,
                      role: role_name,
                      email: m.email,
                      phone: m.phone,
                      city: m.city,
                      country: m.country ? m.country.name : '',
                      street: m.street,
                      zip: m.zip,
                      comment: m.comment,
                  });
              });

              $scope.org = result.shift();
              $scope.gridOptions.data = gridData;
              $scope.roleColumnDef.filter.selectOptions = get_role_options(roles);
            }
        );
    };

    if ($stateParams.edit) {
      $scope.edit = true;
    }

    if ($stateParams.id) {
      loadParallel();

      $scope.roleColumnDef = {
             name: 'role',
             filter: {
                     type: uiGridConstants.filter.SELECT,
                     condition: uiGridConstants.filter.EXACT,
                     selectOptions: []
             }
      };
      $scope.gridOptions = {
          enableFiltering: true,
          columnDefs: [
            { field: 'user_id', visible: false },
            { field: 'user',
              cellTemplate: '<div class="ui-grid-cell-contents"><a ui-sref="user_edit({id:row.entity.user_id})">{{row.entity.user}}</a></div>',
            },
            $scope.roleColumnDef,
            { field: 'email' },
            { field: 'phone' },
            { field: 'city' },
            { field: 'country' },
            { field: 'street' },
            { field: 'zip' },
            { field: 'comment' },
          ],
      };
    }
    else {
      $scope.org = {};
      Organization.query_list().$promise.then(function(resp){
        $scope.orgs = resp.organizations;
      }, function(){});
    }

    $scope.create_organization = function(){
      Organization.create({}, $scope.org, function(resp){
        $state.go('organizations', {id: resp.organization.id});
        notify({classes: 'notify-success', message: resp.message});
      }, function(){});
    };

    $scope.update_organization = function(){
      Organization.update({'id':$scope.org.id}, $scope.org, function(resp){
        notify({classes: 'notify-success', message: resp});
      }, function(){});
    };

    $scope.delete_organization = function(){
      if( window.confirm('Do you really want to delete this organization?') ) {
        Organization.delete({'id':$scope.org.id}, function(resp){
          $state.go('organization_list');
          notify({classes: 'notify-success', message: resp});
        }, function(){});
      }
    };
  });
