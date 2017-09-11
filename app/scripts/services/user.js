'use strict';

/**
 * @ngdoc service
 * @name cpApp.User
 * @description
 * # User
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('User', function ($resource, config) {
    // Service logic
    // ...

    // Public API here
    return $resource(config.apiConfig.webServiceUrl+'/users/:id', {}, {
      query_list: {
        url: config.apiConfig.webServiceUrl+'/users',
        method: 'GET',
        isArray: false
      },
      query: {
        method: 'GET',
        isArray: false
      },
      create: {
        url: config.apiConfig.webServiceUrl+'/users',
        method: 'POST',
        isArray: false,
        withCredentials: true
      },
      update: {
        method: 'PUT',
        withCredentials: true
      },
      delete: {
        method: 'DELETE',
        withCredentials: true
      },
      memberships: {
          url: config.apiConfig.webServiceUrl+'/users/:id/memberships',
        method: 'GET',
        isArray: false,
        withCredentials: true
      },
    });
  });
