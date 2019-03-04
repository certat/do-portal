'use strict';

/**
 * @ngdoc filter
 * @name cpApp.filter:eventKeysFilter
 * @function
 * @description
 * # eventKeysFilter
 * Filter in the cpApp.
 */
angular.module('cpApp')
  .filter('eventKeysFilter', function () {
    return function(items){
      var filtered = [];
      angular.forEach(items, function(item){
        angular.forEach(item.experts, function(experts){
          angular.forEach(experts, function(v){
            angular.forEach(v, function(vv, kk){
              if(filtered.indexOf(kk) === -1 && kk.indexOf('$$') !== 0){
                filtered.push(kk);
              }
            });
          });
        });
      });
      return filtered;
    };
  });
