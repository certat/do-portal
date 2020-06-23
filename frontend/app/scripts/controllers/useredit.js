'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UsereditCtrl
 * @description
 * # UsereditCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('UsereditCtrl', function ($scope, $filter, $uibModal, User, Organization, Country, Membership, Auth, GridData, notify, $stateParams, $state, $q, FileReader) {

    var loadUser = function() {
      if (!$stateParams.id) { return {}; } // new contact
      return User.query({'id': $stateParams.id}).$promise
                .then(function(resp){
                    if (resp.birthdate) { resp.birthdate = new Date(resp.birthdate); }
                    return resp;
                  }, function(){});
    };

    var loadRoles = function(){
      return Membership.roles().$promise
                .then(function(resp){
                    return resp.membership_roles;
                  }, function(){});
    };

    var loadOrgs = function(){
      return Organization.query_list().$promise
                .then(function(resp){
                    return resp.organizations.sort(function(a,b){return a.abbreviation > b.abbreviation;});
                  }, function(){});
    };

    var loadMemberships = function(){
      if (!$stateParams.id) { return [{}]; }
      return User.memberships({'id': $stateParams.id}).$promise
                .then(function(resp){
                    return resp.memberships;
                  }, function(){});
    };

    var loadCountries = function(){
      return Country.query_list().$promise
                .then(function(resp){
                    return resp.countries;
                  }, function(){});
    };

    function _array2hash(arr) {
        var hash = {};
        arr.forEach(function(i) { hash[i.id] = i; });
        return hash;
    }
    var loadParallel = function() {
        return $q.all([ loadUser(), loadRoles(), loadOrgs(), loadCountries(), loadMemberships() ])
            .then( function( result ) {
              $scope.user          = result.shift();
              $scope.roles         = _array2hash(result.shift());
              $scope.organizations = result.shift();
              $scope.countries     = result.shift();
              $scope.memberships   = result.shift();
            }
        );
    };

    function _handle_upload_field(obj, key) {
      if (obj['delete_'+key]) { obj[key] = ''; } // delete checkbox is checked
      delete obj['delete_'+key]; // dont send checkbox value to server
      angular.element("input[type='file'][data-key='"+key+"']").val(null); // reset input field
    }

    // e.g.: if a phone number is deleted the value is set to the empty string
    // but the server expects { phone: null }
    function emptyToNull(obj) {
        Object.keys(obj).forEach(function(key) {
            if( obj[key] === '' ) { obj[key] = null; }
        });
    }

    $scope.field_is_required = function(field_name, m) {
        var role_id = m.membership_role_id;
        if (!m.membership_role_id) { return false; }
        var role_name = $scope.roles[m.membership_role_id].display_name;

        if( field_name === 'email' && role_name === 'Single Point of Contact (SPoC)') {
            return true;
        }
        return false;
    };

    $scope.get_org_by_id = function(oid) {
        return $scope.organizations.find(function(o) { return o.id === oid; });
    };
    $scope.save_membership = function(m, form) {
      if (!validateForm(form)) { return; }
      _handle_upload_field(m,'coc');
      _handle_upload_field(m,'smime');

      if(m.id) {
        emptyToNull(m);
        Membership.update({'id':m.id}, m, function(resp) {
          notify({classes:'notify-success', message: resp.message});
        }, function(){});
      }
      else {
        Membership.create({}, m, function(resp) {
          m.id = resp.organization_membership.id;
          notify({classes:'notify-success', message: resp.message});
        }, function(){});
      }
    };

    $scope.create_user = function(form){
      if (!validateForm(form)) { return; }
      _handle_upload_field($scope.user,'picture');
      if ($scope.user.password === '') { delete $scope.user.password; }
      var data = { user: $scope.user, organization_membership: $scope.memberships[0] };
      User.create({}, data, function(resp){
        $state.go('user_edit', {id: resp.user.id});
        notify({classes:'notify-success', message: resp.message});
      }, function(){});
    };

    $scope.update_user = function(form){
      if (!validateForm(form)) { return; }
      var u = $scope.user;
      _handle_upload_field(u,'picture');
      User.update({'id':u.id}, u, function(resp){
        notify({classes:'notify-success', message: resp.message});
      }, function(){});
    };

    $scope.delete_user = function(){
      if( window.confirm('Do you really want to delete this user?') ) {
        User.delete({'id':$scope.user.id}, function(resp){
          $state.go('user_list');
          notify({classes:'notify-success', message: resp.message});
        }, function(){});
      }
    };

    $scope.delete_membership = function(m_id, index){
      if( window.confirm('Do you really want to delete this membership?') ) {

        if (!m_id) {
          // membership not saved to backend yet
          $scope.memberships.splice(index, 1);
        }
        else {
          // only delete if at least one membership exists on the server
          var count = 0;
          $scope.memberships.forEach(function(m) {
            if (m.id) { count++; }
          });
          if (count < 2) {
            notify({classes:'notify-error', message: 'Cannot delete membership. A user needs at least 1 membership!'});
            return;
          }

          Membership.delete({'id':m_id},
              function(resp){
                notify({classes:'notify-success', message: resp.message});
                $scope.memberships.splice(index, 1);
              }, function(){});

        }
      }
    };

    $scope.add_membership = function(){ $scope.memberships.push({ user_id: $scope.user.id }); };

    loadParallel();

    // adds an inputfile to the membership.
    // example: <input type="file" cp-file-select data-key="smime">
    // result: { ..., m.smime: "data:text/plain;base64,iVB... }
    $scope.getFile = function (file, inputscope, element) {
      FileReader.readAsDataUrl(file, $scope)
        .then(function (result) {
          var key = element.data('key');
          var obj;
          if (key === 'picture') {
            obj = inputscope.user;
            if ( file.size > 1024*1024 ) {
              notify({classes:'notify-error', message: 'picture size exceeded 1MB'});
              return;
            }
          }
          else {
            obj = inputscope.m;
          }
          obj[key] = result;
          obj[key+'_filename'] = file.name;
        });
    };

    $scope.deleteFile = function(obj, key) {
      if (window.confirm('Do you really want to delete this file?')) {
        obj[key]             = '';
        obj[key+'_filename'] = '';
      }
    };

    function startDownload(href, filename) {
        var dl = document.createElement('a');
        dl.setAttribute('href', href);
        dl.setAttribute('download', filename);
        dl.setAttribute('visibility', 'hidden');
        dl.setAttribute('display', 'none');
        // Append to page, wont work in FF otherwise
        document.body.appendChild(dl);
        dl.click();
    }
    $scope.downloadFile = function(m, key, ev) {
        ev.stopPropagation();
        if(!m[key]) {
            User.membership({'id':$scope.user.id, mid:m.id}, function(resp) {
                m[key] = resp[key];
                startDownload(m[key], m[key+'_filename']);
            }, function(){});
        }
        else {
            startDownload(m[key], m[key+'_filename']);
        }
    };
    $scope.birthdate = {
      options: {
        startingDay: 1,
        showWeeks: false,
      },
      popup: { opened: false },
      open: function() { $scope.birthdate.popup.opened = true; }
    };
    function validateForm(form) {
        if (form.$valid) {
            return true;
        }
        else {
            angular.forEach(form.$error, function (field) {
                angular.forEach(field, function(errorField){
                    errorField.$setTouched();
                    var name = errorField.$$attr.name;
                    notify({classes:'notify-error', message: 'field "'+name+'" is invalid!'});
                })
            });
            return false;
        }
    }

  });
