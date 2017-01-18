'use strict';

/**
 * @ngdoc service
 * @name cpApp.GridData
 * @description
 * # GridData
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('GridData', function ($resource, config) {
    // Service logic
    // ...

    // Public API here
    return function(endpoint){
      return $resource(config.apiConfig.webServiceUrl+'/'+endpoint+'/:id', {}, {
        query: {
          method: 'GET',
          isArray: false,
          params: {id: '@id'}
        },
        update: {
          url: config.apiConfig.webServiceUrl+'/'+endpoint+'/:id',
          method: 'PUT',
          params: {id: '@id'}
        }
      });
    };
  });
