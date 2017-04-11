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
    return $resource(config.apiConfig.webServiceUrl+'/organizations/:id', {}, {
      query_list: {
        url: config.apiConfig.webServiceUrl+'/organizations',
        method: 'GET',
        isArray: false
      },
      query: {
        method: 'GET',
        isArray: false
      },
      update: {
        method: 'PUT',
        withCredentials: true
      }
    });
  });
