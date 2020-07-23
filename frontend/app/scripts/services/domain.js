'use strict';

/**
 * @ngdoc service
 * @name cpApp.Domain
 * @description
 * # Domain
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('Domain', function($resource, config) {
    return $resource(config.apiConfig.webServiceUrl+'/domains/:id', {}, {
      query: {
        method: 'GET',
        isArray: false
      },
      create: {
        url: config.apiConfig.webServiceUrl+'/domains',
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
      }
    });
  });