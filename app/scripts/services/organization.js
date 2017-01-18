'use strict';

/**
 * @ngdoc service
 * @name cpApp.Organization
 * @description
 * # Organization
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('Organization', function ($resource, config) {
    // Service logic
    // ...

    // Public API here
    return $resource(config.apiConfig.webServiceUrl+'/organizations', {}, {
      query: {
        method: 'GET',
        isArray: false
      },
      update: {
        url: config.apiConfig.webServiceUrl+'/organizations',
        method: 'PUT',
        withCredentials: true
      }
    });
  });
