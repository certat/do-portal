'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:TyposquatsCtrl
 * @description
 * # TyposquatsCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('TyposquatsCtrl', function ($scope, $uibModalInstance, GridData) {
    GridData('fqdns').query(function(resp){
      $scope.fqnds = resp.fqnds;
    });

    $scope.exportCSV = function(){
      var header = ['fqdn', 'dns_a', 'dns_ns', 'dns_mx', 'updated'];
      var rv = [header];
      $scope.exportDate = new Date().getTime();
      angular.forEach($scope.fqdns, function(fqdn){
        var entry = [];
        angular.forEach(fqdn, function(v, k){
          var keyIndex = header.indexOf(k);
          if(keyIndex !== -1){
            entry[keyIndex] = v;
          }
        });
        rv.push(entry);

      });
      return rv;
    };
    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  });
