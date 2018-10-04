'use strict';

/**
 * @ngdoc service
 * @name cpApp.authInterceptor
 * @description
 * # authInterceptor
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('authInterceptor', function ($q, $cookies, $location, notifications) {
    function get_msg(rejection) {
        var msg = 'Unknown Response Error';
        if (rejection.data && rejection.data.message) {
            msg = rejection.data.message;
        }
        else if (rejection.statusText) {
            msg = rejection.statusText;
        }
    }

    return {
      'request': function(config){
        config.withCredentials = true;
        $cookies.put('rm', $cookies.get('rm'));
        return config;
      },
      'response': function(resp){
        return resp;
      },
      'requestError': function(rejection){
        return $q.reject(rejection);
      },
      'responseError': function(rejection){
        notifications.showError(get_msg(rejection));

        if(rejection.status === 401){
          $location.path('/login');
        }

        return $q.reject(rejection);
      }
    };
  });
