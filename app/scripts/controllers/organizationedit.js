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

    var loadRipeDetails = function() {
      $scope.ripe_details = {
          asns:  [],
          cidrs: [],
      };
      $scope.org.ripe_handles.forEach(function(ripe_handle) {
          Organization.ripe_details({'org_id': $scope.org.id ,'ripe_handle': ripe_handle}).$promise
            .then(function(resp){
                resp.asns.forEach(function(asn) {
                  asn.ripe_org_hdl = ripe_handle;
                  $scope.ripe_details.asns.push(asn);
                });
                resp.cidrs.forEach(function(cidr) {
                  cidr.ripe_org_hdl = ripe_handle;
                  $scope.ripe_details.cidrs.push(cidr);
                });
                if (resp.abusecs) {
                  resp.abusecs.forEach(function(abusec) {
                      $scope.gridOptions.data.push({
                        user_id: '',
                        user: '',
                        role: 'Abuse-C Automatic',
                        email: abusec,
                        phone: '',
                        city: '',
                        country: '',
                        street: '',
                        zip: '',
                        comment: 'RIPE handle: ' + ripe_handle,
                      });
                  });
                }
            }, function(){});
      });
    };

    function _array2hash(arr) {
        var hash = {};
        arr.forEach(function(i) { hash[i.id] = i; });
        return hash;
    }
    function get_role_options(roles) {
        var roleOptions = [];
        roleOptions.push({value: 'Abuse-C Automatic', label: 'Abuse-C Automatic'});
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
              loadRipeDetails();
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
              cellTemplate: '<div class="ui-grid-cell-contents"><a ng-if="row.entity.user_id" ui-sref="user_edit({id:row.entity.user_id})">{{row.entity.user}}</a><span ng-if="!row.entity.user_id">{{row.entity.user}}</span></div>',
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

    $scope.update_organization = function(success_cb, error_cb){
      return Organization.update({'id':$scope.org.id}, $scope.org, function(resp){
        notify({classes: 'notify-success', message: resp.message});
        if (typeof success_cb === 'function') { success_cb(); }
      }, function(){
        if (typeof error_cb === 'function') { error_cb(); }
      });
    };

    $scope.delete_organization = function(){
      if( window.confirm('Do you really want to delete this organization?') ) {
        Organization.delete({'id':$scope.org.id}, function(resp){
          $state.go('organization_list');
          notify({classes: 'notify-success', message: resp.message});
        }, function(){});
      }
    };
    $scope.add_ripe_handle = function(){
        if ($scope.org.hasOwnProperty('ripe_handles')) {
          if ($scope.org.ripe_handles.includes($scope.new_ripe_handle)) {
              notify({classes: 'notify-error', message: 'this RIPE handle already exists.'});
              return;
          }
          $scope.org.ripe_handles.push($scope.new_ripe_handle);
        }
        else {
            $scope.org.ripe_handles = [$scope.new_ripe_handle];
        }
        $scope.update_organization(
          function(){
            notify({
              classes: 'notify-success',
              message: 'added new RIPE handle: ' + $scope.new_ripe_handle
            });
            $scope.new_ripe_handle = '';
            loadParallel();
          },
          function() {
            $scope.org.ripe_handles.splice(-1,1);
          }
        );
    };
    $scope.delete_ripe_handle = function(ripe_handle, index){
        if( window.confirm('Do you really want to delete this RIPE handle? (' + ripe_handle + ')') ) {
          $scope.org.ripe_handles.splice(index, 1);
          $scope.update_organization(
            function(){
              notify({
                classes: 'notify-success',
                message: 'deleted RIPE handle: ' + ripe_handle
              });
              loadParallel();
            },
            function() {
              $scope.org.ripe_handles.splice(index, 0, ripe_handle);
            }
          );
        }
    };
    $scope.edit_ripe_detail = function(item) {
        if (typeof item.notification_setting.delivery_protocol === 'undefined') {
            item.notification_setting.delivery_protocol = 'Mail';
        }
        if (typeof item.notification_setting.delivery_format === 'undefined') {
            item.notification_setting.delivery_format = 'CSV';
        }
        if (typeof item.notification_setting.notification_interval === 'undefined') {
            item.notification_setting.notification_interval = 604800;
        }
        item.dirty = true;
    };
    $scope.update_ripe_detail = function(item) {
      var obj = angular.copy(item);
      delete obj.dirty;
      delete obj.ripe_org_hdl;
      return Organization.update_ripe_detail(
        {'org_id':$scope.org.id, 'ripe_handle': item.ripe_org_hdl}, obj,
        function(resp){
          delete item.dirty;
          notify({classes: 'notify-success', message: resp.message});
        },
        function(){
        }
      );
    };
  });
