'use strict';

angular.module('cpApp')
  .factory('Country', function ($resource, config) {
    return $resource(config.apiConfig.webServiceUrl+'/countries/:id', {}, {
      query_list: {
        url: config.apiConfig.webServiceUrl+'/countries',
        method: 'GET',
        isArray: false
      },
      query: {
        method: 'GET',
        isArray: false
      },
    });
  });
