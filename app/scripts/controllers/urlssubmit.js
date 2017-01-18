'use strict';

/**
 * @ngdoc function
 * @name cpApp.controller:UrlsSubmitCtrl
 * @description
 * # UrlsSubmitCtrl
 * Controller of the cpApp
 */
angular.module('cpApp')
  .controller('URLsSubmitCtrl', function ($scope, GridData, notifications) {
    $scope.urls = '';
    $scope.urls_ = [];
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
      var vxAnalysisAvailable = $scope.sampleActions.dynamic_analysis.vxstream;
      var vxEnvironmentIds = [];
      for(var key in vxAnalysisAvailable){
        if(vxAnalysisAvailable.hasOwnProperty(key)){
          if(vxAnalysisAvailable[key]){
            vxEnvironmentIds.push(parseInt(key, 10));
          }
        }
      }
      $scope.urls_ = $scope.urls.split('\n');
      var dynAnalysis = {
        urls: $scope.urls_,
        dyn_analysis: {vxstream: vxEnvironmentIds}
      };

      GridData('analysis/vxstream-url').save(dynAnalysis, function(resp){
        for(var i in resp.statuses){
          var st = resp.statuses[i];
          if(st.hasOwnProperty('error')){
            notifications.showError(st.error);
          }else if(st.hasOwnProperty('sha256')){
            notifications.showSuccess(
              $scope.urls_[i] + ' has been submitted for dynamic analysis');
          }
        }
      }, function(error){
        notifications.showError(error.data);
      })
    };

    GridData('analysis/vxstream/environments').get().$promise.then(
      function(resp){
        $scope.envs = resp.environments;
      },
      function(err){
        notifications.showError(err.data);
      }
    );
  });
