'use strict';

angular.module('services.config', [])
  .constant('config', {
    version: '@@version',
    apiConfig: {
      webServiceUrl: '@@webServiceUrl',
      authUrl: '@@authUrl'
    },
    enableStatistics: false,
  });
