'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpMyAccount
 * @description
 * # cpMyAccount
 */
angular.module('cpApp')
  .directive('cpMyAccount', function (Auth, notify, errorMapper, config) {
    return {
      templateUrl: 'views/directives/cp-my-account.html',
      restrict: 'E',
      link: function postLink(scope) {
        scope.authUrl = config.apiConfig.authUrl;
        scope.credentials = {};

        Auth.get('account').then(function(resp){
          scope.account = resp.data;
          scope.account.otp_toggle = scope.account.otp_enabled;
        });
        scope.changePassword = function(){
          Auth.changePassword(scope.credentials).then(
            function(resp){
              notify({classes: 'notify-success', message: resp.data.message});
            },
            function(){}
          );
        };
      }
    };
  });
