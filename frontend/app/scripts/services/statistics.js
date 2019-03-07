'use strict';

angular.module('cpApp')
  .factory('Statistics', function ($resource, config) {

    return $resource(config.apiConfig.webServiceUrl+'/statistics', {}, {
      query: {
        method: 'GET',
        isArray: false
      },
    });
  });
