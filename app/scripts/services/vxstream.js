'use strict';

/**
 * @ngdoc service
 * @name cpApp.VxStream
 * @description
 * # VxStream
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('VxStream', function ($resource, config) {
    // Service logic
    // ...

    // Public API here
    return $resource(config.apiConfig.webServiceUrl + '/analysis/vxstream/:sha256/:envId', {}, {
      query: {
        method: 'GET',
        isArray: false,
        params: {sha256: '@sha256', envId: '@envId'}
      },
      envs: {
        url: config.apiConfig.webServiceUrl + '/analysis/vxstream/environments',
        method: 'GET',
        cache: true

      },
      report: {
        url: config.apiConfig.webServiceUrl + '/analysis/vxstream/report/:sha256/:envId/:type',
        method: 'GET',
        params: {sha256: '@sha256', envId: '@envId', type: '@type'},
        cache: true

      }
    });
  });
