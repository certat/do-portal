'use strict';

/**
 * @ngdoc service
 * @name cpApp.Auth
 * @description
 * # Auth
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('Auth', function ($http, $cookies, $log, Session, config, $location) {
    // Service logic
    // ...

    var cacheSession = function(response) {
      // this is never used, we pass the cookie with all requests
      // using the authInterceptor
      Session.set('auth', $cookies.get('rm'));
      return response;
    };
    var uncacheSession = function (response) {
      Session.unset('auth');
      $cookies.remove('username');
      return response;
    };

    // Public API here
    return {
      login: function (credentials) {
        return $http.post(config.apiConfig.authUrl + '/login', credentials)
          .then(cacheSession);
      },
      logout: function () {
        return $http.get(config.apiConfig.authUrl + '/logout')
          .then(uncacheSession, function(err){
            return err;
          });
      },
      isLoggedIn: function () {
        return Session.get('auth');
      },
      post: function(data, endpoint){
        return $http.post(config.apiConfig.authUrl + '/' + endpoint, data);
      },
      get: function(endpoint){
        return $http.get(config.apiConfig.authUrl + '/' + endpoint);
      },
      activate_account: function(token, password) {
          return $http.post(
              config.apiConfig.authUrl + '/activate-account',
              {'token':token, 'password':password}
          ).then(function(){ $location.url('/login'); });
      },
      registerCPAccount: function(userInfo){
        console.log('Deprecated! Use Auth.' + this.post.name + '("register")');
        return this.post(userInfo, 'register');
      },
      unregisterCPAccount: function(userInfo){
        console.log('Deprecated! Use Auth.' + this.post.name + '('+userInfo+', "unregister")');
        return this.post(userInfo, 'unregister');
      },
      getAccountInfo: function(){
        console.log('Deprecated! Use Auth.' + this.get.name + '("account")');
        return this.get('account');
      },
      changePassword: function(credentials){
        console.log('Deprecated! Use Auth.' + this.post.name + '('+credentials+', "change-password")');
        return this.post(credentials, 'change-password');
      },
      resetAPIKey: function(){
        console.log('Deprecated! Use Auth.' + this.get.name + '("reset-api-key")');
        return this.get('reset-api-key');
      },

      lost_password: function(email) {
        return $http.post(config.apiConfig.authUrl+'/lost_password', email);
      }
    };
  });
