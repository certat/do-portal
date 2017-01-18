'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:FileuploadctrlCtrl
 * @description
 * # FileuploadctrlCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('FileUploadCtrl', function ($scope, $timeout, config, Upload) {
    $scope.uploadPath = '/upload';
    $scope.uploadFiles = function (files) {
      $scope.files = files;
      if (files && files.length) {
        $scope.uploadProgress = 0;
        Upload.upload({
          url: config.apiConfig.webServiceUrl + $scope.uploadPath,
          data: {
            files: files
          }
        }).then(function (response) {
          $timeout(function () {
            $scope.result = response.data;
            $scope.$emit('files-uploaded', response.data.files);
          });
        }, function (response) {
          if (response.status > 0) {
            $scope.msg = response.status + ': ' + response.statusText;
            $scope.$emit('upload-error', $scope.msg);
          }
        }, function (evt) {
          $scope.uploadProgress =
            Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
        });
      }
    };
    $scope.discardFiles = function(){
      $scope.$broadcast('clear-files');
    };
    $scope.$on('clear-files', function(){
      delete $scope.files;
      delete $scope.uploadProgress;
      $scope.$emit('files-cleared');
    });
  });
