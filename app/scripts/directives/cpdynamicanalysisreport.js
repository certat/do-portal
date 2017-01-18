'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpDynamicAnalysisReport
 * @description
 * # cpDynamicAnalysisReport
 */
angular.module('cpApp')
  .directive('cpDynamicAnalysisReport', function ($q, $filter, $sce, VxStream, notifications, config) {
    return {
      restrict: 'E',
      templateUrl: 'views/directives/cp-dynamic-analysis-report.html',
      link: function(scope, elem, attrs){
        VxStream.envs().$promise.then(function(resp){
          scope.envs = resp.environments;
          var promises = [];
          for(var eid in resp.environments){
            var envId = resp.environments[eid].id;
            promises.push(
              VxStream.get({sha256: attrs.hash, envId: envId}).$promise
            );
          }
          $q.all(promises).then(function(results){
            for(var ridx in results){
              if(results[ridx].response !== false){
                var thisEnv = $filter('filter')(
                  scope.envs, {id: results[ridx].response.environmentId}
                );
                results[ridx].response.environmentName = thisEnv[0].name;
                if(results[ridx].response.analysis_start_time !== undefined){
                  results[ridx].response.html_report = true;
                  results[ridx].response.html_report_url =
                    $sce.trustAsResourceUrl(config.apiConfig.webServiceUrl +
                      '/analysis/vxstream/report/' +
                      attrs.hash + '/' + thisEnv[0].id + '/html');
                }
              }
            }
            scope.summaries = results;
            scope.dld = {
              html: 'HTML',
              json: 'JSON',
              bin: 'Binary',
              pcap: 'PCAP'

            };
            scope.webServiceUrl = config.apiConfig.webServiceUrl;
          });
        }, function(error){
          if(error.data){
            notifications.showError(error.data);
          }
        });
      }
    };
  });
