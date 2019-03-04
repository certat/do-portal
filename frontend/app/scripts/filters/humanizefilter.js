'use strict';

/**
 * @ngdoc filter
 * @name cpApp.filter:humanizeFilter
 * @function
 * @description
 * # humanizeFilter
 * Filter in the cpApp.
 */
angular.module('cpApp')
  .filter('humanizeFilter', function () {
    return function(input, char){
      char = char || '_';
      input = input.replace(new RegExp(char, 'g'), ' ');
      return (input).replace(/^([a-z])|\s+([a-z])/g, function ($1){
        return $1.toUpperCase();
      });
    };
  });
