'use strict';
/**
 * angular-ui-switch
 * Inspired by: https://github.com/xpepermint/angular-ui-switch
 */
angular.module('uiSwitch', ['ui/template/ui-switch.html'])

  .directive('uiSwitch', function () {
    return {
      restrict: 'AE',
      replace: true,
      require: 'ngModel',
      scope: {
        ngModel: '='
      },
      templateUrl: 'ui/template/ui-switch.html',
      link: function(scope, element, attrs, ngModel){
        if(!ngModel) {
          return;
        }

        ngModel.$render = function(){
          if(ngModel.$modelValue){
            element.addClass('checked');
          }else{
            element.removeClass('checked');
          }
          if('disabled' in attrs){
            element.addClass('disabled');
          }
        };

        scope.toggle = function(val){
          if(!('disabled' in attrs)){
            ngModel.$setViewValue(!val);
            if(ngModel.$modelValue){
              element.addClass('checked');
            }else{
              element.removeClass('checked');
            }
          }
        };
      }
    };
  });

angular.module('ui/template/ui-switch.html', []).run(['$templateCache', function($templateCache){
  $templateCache.put('ui/template/ui-switch.html', [
      '<span class="switch" ng-click="toggle(ngModel)">',
      '<small></small>',
      '<input type="checkbox" ng-model="ngModel" style="display:none">',
      '</span>'
    ].join('')

  );
}]);
