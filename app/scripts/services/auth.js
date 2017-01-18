'use strict';

/**
 * @ngdoc service
 * @name cpApp.Auth
 * @description
 * # Auth
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('Auth', function ($http, $cookies, $log, Session, config, notifications) {
    // Service logic
    // ...

    var cacheSession = function(data, status, headers) {
      // this is never used, we pass the cookie with all requests
      // using the authInterceptor
      Session.set('auth', $cookies.get('rm'));
    };
    var uncacheSession = function () {
      Session.unset('auth');
    };

    var loginError = function (response) {
      notifications.showError(response);
    };

    // Public API here
    return {
      login: function (credentials) {
        var login = $http.post(config.apiConfig.authUrl + '/login', credentials);
        login.error(loginError);
        login.success(cacheSession);
        return login;
      },
      logout: function () {
        var logout = $http.get(config.apiConfig.authUrl + '/logout');
        logout.success(uncacheSession);
        return logout;
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
      }
    };
  });
