'use strict';

/**
 * @ngdoc service
 * @name cpApp.Session
 * @description
 * # Session
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('Session', function () {
    // Service logic
    // ...

    // Public API here
    return {
      get: function (key) {
        return sessionStorage.getItem(key);
      },
      set: function (key, val) {
        return sessionStorage.setItem(key, val);
      },
      unset: function (key) {
        return sessionStorage.removeItem(key);
      }
    };
  });
