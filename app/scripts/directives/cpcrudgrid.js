'use strict';

/**
 * @ngdoc directive
 * @name cpApp.directive:cpCrudGrid
 * @description
 * # cpCrudGrid
 */
angular.module('cpApp')
  .directive('cpCrudGrid', function ($filter, GridData, notifications) {
    return {
      restrict: 'A',
      replace: false,
      scope: {
        excludeKeys: '=?'
      },
      templateUrl: 'views/directives/directive-crud-grid-template.html',
      link: function(scope, elem, attrs){
        scope.objects = [];
        scope.properties = [];
        scope.excludeKeys = scope.excludeKeys || ['id'];
        scope.toggleEditMode = function(o){
          o.active = !o.active;
        };
        scope.toggleAdd = function(){
          var o = { active: true, name: ''};
          if(!scope.properties || !scope.properties.length){
            scope.properties = ['name'];
          }
          //scope.properties.forEach(function(field){
          //    o[field] = '';
          //});
          scope.objects.unshift(o);
          //console.log(scope.objects);
        };
        var errorCallback = function(e){
          notifications.showError(e.data);
        };
        scope.updateItem = function(o){
          GridData(attrs.endpoint).update({id: o.id}, o, function(){
            o.active = false;
          }, errorCallback);
        };
        scope.deleteItem = function(o){
          GridData(attrs.endpoint).delete({id: o.id}, function(){
            scope.objects = $filter('filter')(
              scope.objects,
              function(v){
                return v.id !== o.id;
              }
            );
          }, errorCallback);
        };
        var data = GridData(attrs.endpoint).query(function(){
          scope.objects = data[attrs.endpoint];
          var properties = [];
          var obj = scope.objects[0];
          for(var key in obj) {
            if(obj.hasOwnProperty(key) && typeof obj[key] !== 'function' && scope.excludeKeys.indexOf(key) === -1) {
              properties.push(key);
            }
          }
          scope.properties = properties;
        });
      }
    };
  });
