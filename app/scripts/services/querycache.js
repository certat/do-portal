'use strict';

/**
 * @ngdoc service
 * @name cpApp.QueryCache
 * @description
 * # QueryCache
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('QueryCache', function ($cacheFactory) {
    // Public API here
    return $cacheFactory('QueryCache');
  });
