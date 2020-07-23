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
      create: {
        url: config.apiConfig.webServiceUrl+'/organizations',
        method: 'POST',
        isArray: false,
        withCredentials: true
      },
      query: {
        method: 'GET',
        isArray: false
      },
      update: {
        method: 'PUT',
        withCredentials: true
      },
      delete: {
        method: 'DELETE',
        withCredentials: true
      },
      ripe_details: {
        url: config.apiConfig.webServiceUrl+'/ripe/settings/:org_id/:ripe_handle',
        method: 'GET',
        isArray: false
      },
      update_ripe_detail: {
        url: config.apiConfig.webServiceUrl+'/ripe/settings/:org_id/:ripe_handle',
        method: 'PUT',
      },
      domains: {
        url: config.apiConfig.webServiceUrl+'/organizations/:org_id/domains',
        method: 'GET',
        isArray: false,
        withCredentials: true
      }
    });
  });
