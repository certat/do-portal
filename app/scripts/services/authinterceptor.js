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
        if(rejection.status === 401){
          if(rejection.data.validator === 'signature'){
            //$cookies.remove('rm');
          }
          $location.path('/login');
          notifications.showError('Please log in to continue');
          return $q.reject(rejection);
        }
        return $q.reject(rejection);
      }
    };
  });
