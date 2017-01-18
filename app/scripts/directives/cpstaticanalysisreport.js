'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpStatisAnalysisReport
 * @description
 * # cpStatisAnalysisReport
 */
angular.module('cpApp')
  .directive('cpStaticAnalysisReport', function (GridData, notifications) {
    return {
      restrict: 'E',
      templateUrl: 'views/directives/cp-static-analysis-report.html',
      link: function(scope, elem, attrs){
        GridData('analysis/static').get({id: attrs.hash}).$promise.then(
          function(response){
            scope.static_report = response;
            scope.hexdump_lines = response.report_parsed.hex.match(/^.*((\r\n|\n|\r)|$)/gm);
            var bytes = [];
            for(var i=0; i<= 15; i++){
              bytes.push('0'+i.toString(16).toUpperCase());
              scope.bytes = bytes;
            }
          },
          function(error){
            notifications.showError(error.data);
          }
        );
      }
    };
  });
