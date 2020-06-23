'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:HeaderCtrl
 * @description
 * # HeaderCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('HeaderCtrl', function ($scope, Auth) {
    $scope.logout = function () {
      Auth.logout();
    };
  });
