'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:HeaderctrlCtrl
 * @description
 * # HeaderctrlCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('HeaderCtrl', function ($scope, $location, Auth, BOSH) {
    $scope.isLoggedIn = Auth.isLoggedIn();
    $scope.logout = function () {
      BOSH.disconnect();
      Auth.logout().success(function () {
        $location.path('/login');
      });
    };
  });
