'use strict';

/**
 * @ngdoc service
 * @name cpApp.User
 * @description
 * # User
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('Membership', function ($resource, config) {
    // Service logic
    // ...

    // Public API here
    return $resource(config.apiConfig.webServiceUrl+'/organization_memberships/:id', {}, {
      query: {
        url: config.apiConfig.webServiceUrl+'/organization_memberships',
        method: 'GET',
        isArray: false
      },
      update: {
        method: 'PUT',
        withCredentials: true
      },
      create: {
        url: config.apiConfig.webServiceUrl+'/organization_memberships',
        method: 'POST',
        isArray: false,
        withCredentials: true
      },
      delete: {
        method: 'DELETE',
        withCredentials: true
      },
      roles: {
        url: config.apiConfig.webServiceUrl+'/membership_roles',
        method: 'GET',
        isArray: false
      }
    });
  });
