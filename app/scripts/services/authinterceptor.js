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
    // Service logic
    // ...

    // Public API here
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
        if (rejection.data && rejection.data.message) {
            notifications.showError(rejection.data.message);
        }
        else if (rejection.statusText) {
            notifications.showError(rejection.statusText);
        }
        else {
            //console.log(rejection);
            notifications.showError('Unknown Response Error');
        }

        if(rejection.status === 401){
          $location.path('/login');
        }

        return $q.reject(rejection);
      }
    };
  });
