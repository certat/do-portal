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
      query_list: {
        method: 'GET',
        isArray: false
      },
      query: {
        url: config.apiConfig.webServiceUrl+'/organizations/1',
        method: 'GET',
        isArray: false
      },
      update: {
        url: config.apiConfig.webServiceUrl+'/organizations/1',
        method: 'PUT',
        withCredentials: true
      }
    });
  });
