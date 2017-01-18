'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpMyAccount
 * @description
 * # cpMyAccount
 */
angular.module('cpApp')
  .directive('cpMyAccount', function (Auth, notifications, errorMapper, config) {
    return {
      templateUrl: 'views/directives/cp-my-account.html',
      restrict: 'E',
      link: function postLink(scope) {
        scope.authUrl = config.apiConfig.authUrl;
        scope.credentials = {};
        Auth.getAccountInfo().then(function(resp){
          scope.account = resp.data;
          scope.account.otp_toggle = scope.account.otp_enabled;
        });
        scope.changePassword = function(){
          Auth.changePassword(scope.credentials).then(
            function(resp){
              notifications.showSuccess(resp.data.message);
            },
            function(err){
              notifications.showError(errorMapper.map(err.data));
            }
          );
        };
        scope.resetAPIKey = function(){
          Auth.resetAPIKey().then(
            function(resp){
              Auth.getAccountInfo().then(function(resp){
                scope.account = resp.data;
              });
              notifications.showSuccess(resp.data.message);
            },
            function(err){
              notifications.showError(err.data);
            }
          );
        };

        scope.toggle2FA = function(){
          Auth.post(scope.account, 'toggle-2fa').then(
            function(resp){
              scope.account.otp_enabled = !scope.account.otp_enabled;
              delete scope.account.totp;
              //scope.account.otp_toggle = !scope.account.otp_toggle;
              notifications.showSuccess(resp.data.message);
            },
            function(err){
              notifications.showError(err.data);
            }
          );
        };
      }
    };
  });
