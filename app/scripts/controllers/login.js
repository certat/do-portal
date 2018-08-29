'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:LoginCtrl
 * @description
 * # LoginCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('LoginCtrl', function ($scope, $location, $state, Auth, notifications) {
    $scope.credentials = {email: '', password: ''};
    $scope.login = function () {
      Auth.login($scope.credentials).then(function (response) {
        if(response.headers('cp-totp-required') === 'True'){
          $state.go('two-factor');
        }else{
          $state.go('organization_list');
        }
      }, function(){});
    };
    $scope.verifyTOTP = function(){
      Auth.post($scope.credentials, 'verify-totp').then(function(){
        $state.go('organization_list');
      });
    };

    $scope.lost_password = function () {
      Auth.lost_password({email: $scope.email})
                .then(function(resp){
                    notifications.showSuccess(resp.data.message);
                  }, function(){});
    };
  });
