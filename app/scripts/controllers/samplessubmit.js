'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:SamplessubmitCtrl
 * @description
 * # SamplessubmitCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('SamplesSubmitCtrl', function ($scope, $location, GridData, notifications) {
    $scope.files = [];
    $scope.submitEnvs = [];
    $scope.sampleActions = {
      av_scan: true,
      static_analysis: true,
      dynamic_analysis: {
        vxstream: {
          1: true,
          2: false,
          3: false,
          4: false
        }
      }
    };
    $scope.save = function(){
      GridData('analysis/static').save({files: $scope.files});
      GridData('analysis/av').save({files: $scope.files}, function(resp){
        notifications.showSuccess(resp);
        $scope.files = [];
        $scope.$broadcast('clear-files');
        $location.path('/samples');
        //$log.debug('start scan... redirect to results page');
      }, function(error){
        notifications.showError(error.data);
      });

      var vxAnalysisAvailable = $scope.sampleActions.dynamic_analysis.vxstream;
      var vxEnvironmentIds = [];
      for(var key in vxAnalysisAvailable){
        if(vxAnalysisAvailable.hasOwnProperty(key)){
          if(vxAnalysisAvailable[key]){
            vxEnvironmentIds.push(parseInt(key, 10));
          }
        }
      }
      var dynAnalysis = {
        files: $scope.files,
        dyn_analysis: {vxstream: vxEnvironmentIds}
      };

      GridData('analysis/vxstream').save(dynAnalysis, function(resp){
        for(var i in resp.statuses){
          var st = resp.statuses[i];
          if(st.hasOwnProperty('error')){
            notifications.showError(st.error);
          }else if(st.hasOwnProperty('sha256')){
            notifications.showSuccess(
              st.sha256 + ' has been submitted for dynamic analysis');
          }
        }
      }, function(error){
        notifications.showError(error.data);
      });
      GridData('analysis/fireeye').save({}, function(resp){
        console.log(resp);
      }, function(err){
        notifications.showError(err.data);
      });
    };

    $scope.$on('files-uploaded', function(event, files){
      $scope.files = $scope.files.concat(files);
      $scope.canSave = true;
    });
    $scope.$on('upload-error', function(event, error){
      $scope.msg = error;
    });
    $scope.engines = GridData('analysis/av').get({id: 'engines'});
    GridData('analysis/vxstream/environments').get(function(resp){
      $scope.envs = resp.environments;
    }, function(err){
      if(err.data){
        notifications.showError(err.data);
      }
    });
    GridData('analysis/fireeye/environments').get(function(resp){
      $scope.feenvs = resp.environments;
    }, function(err){
      notifications.showError(err.data);
    });
  });
