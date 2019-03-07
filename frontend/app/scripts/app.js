'use strict';

/**
 * @ngdoc overview
 * @name cpApp
 * @description
 * # cpApp
 *
 * Main module of the application.
 */
angular
  .module('cpApp', ['ngAnimate', 'ngCookies', 'ngMessages', 'ngResource', 'ngSanitize',
    'ngTouch', 'ngCsv', 'ngFileUpload', 'ui.bootstrap', 'ui.select', 'uiSwitch', 'ui.router',
    'angular-loading-bar', 'services.config', 'cgNotify',
    'ui.grid', 'ui.grid.exporter', 'ui.grid.resizeColumns', 'ui.grid.autoResize'
  ])
  .config(function ($stateProvider) {
    $stateProvider
      .state('home', {
        url: '/home',
        views: {
          content: {
            template: '',
            controller: 'HomeCtrl'
          }
        }
      })
      .state('login', {
        url: '/login',
        views: {
          content: {
            templateUrl: 'views/login.html',
            controller: 'LoginCtrl'
          }
        }
      })
      .state('activate-account', {
          url: '/activate-account?token&email',
        views: {
          content: {
            templateUrl: 'views/activate-account.html',
            controller: 'LoginCtrl'
          }
        }
      })
      .state('two-factor', {
        url: '/two-factor',
        views:{
          content:{
            templateUrl: 'views/two-factor.html',
            controller: 'LoginCtrl'
          }
        }
      })
      .state('lost_password', {
        url: '/lost_password',
        views: {
          content: {
            templateUrl: 'views/lost-password.html',
            controller: 'LoginCtrl'
          }
        }
      })
      .state('statistics', {
        url: '/statistics',
        views: {
          header: {
            templateUrl: 'views/header.html',
            controller: 'HeaderCtrl'
          },
          content: {
            templateUrl: 'views/statistics.html',
            controller: 'StatisticsCtrl'
          }
        }
      })
      .state('organization_list', {
        url: '/organization_list',
        views: {
          header: {
            templateUrl: 'views/header.html',
            controller: 'HeaderCtrl'
          },
          content: {
            templateUrl: 'views/organization-list.html',
            controller: 'OrganizationListCtrl'
          }
        }
      })
      .state('organization_create', {
        url: '/organizations?edit=1',
        views: {
          header: {
            templateUrl: 'views/header.html',
            controller: 'HeaderCtrl'
          },
          content: {
            templateUrl: 'views/organization-edit.html',
            controller: 'OrganizationeditCtrl'
          }
        }
      })
      .state('organizations', {
        url: '/organizations/:id',
        views: {
          header: {
            templateUrl: 'views/header.html',
            controller: 'HeaderCtrl'
          },
          content: {
            templateUrl: 'views/organization-edit.html',
            controller: 'OrganizationeditCtrl'
          }
        }
      })
      .state('user_list', {
        url: '/user_list',
        views: {
          header: {
            templateUrl: 'views/header.html',
            controller: 'HeaderCtrl'
          },
          content: {
            templateUrl: 'views/user-list.html',
            controller: 'UserListCtrl'
          }
        }
      })
      .state('user_create', {
        url: '/users',
        views: {
          header: {
            templateUrl: 'views/header.html',
            controller: 'HeaderCtrl'
          },
          content: {
            templateUrl: 'views/user-edit.html',
            controller: 'UsereditCtrl'
          }
        }
      })
      .state('user_edit', {
        url: '/users/:id',
        views: {
          header: {
            templateUrl: 'views/header.html',
            controller: 'HeaderCtrl'
          },
          content: {
            templateUrl: 'views/user-edit.html',
            controller: 'UsereditCtrl'
          }
        }
      })
      .state('account', {
        url: '/account',
        views: {
          header: {
            templateUrl: 'views/header.html',
            controller: 'HeaderCtrl'
          },
          content: {
            template: '<cp-my-account></cp-my-account>'
          }
        }
      })
      .state('viewReport', {
        url: '/report/:sha256',
        views: {
          header: {
            templateUrl: 'views/header.html',
            controller: 'HeaderCtrl'
          },
          content: {
            templateUrl: 'views/report.html',
            controller: function($scope, $stateParams){
              $scope.sha256 = $stateParams.sha256;
            }
          }
        }
      })
      .state('viewAllReports', {
        url: '/multiav/all/:sha256',
        views: {
          header: {
            templateUrl: 'views/header.html',
            controller: 'HeaderCtrl'
          },
          content: {
            templateUrl: 'views/multiav-all-reports.html',
            controller: 'MultiAVAllReportsController'
          }
        }
      });
  })
  .config(['$urlRouterProvider', function($urlRouterProvider) {
    $urlRouterProvider.otherwise('/home');
  }])
  .config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
    //cfpLoadingBarProvider.includeSpinner = true;
    cfpLoadingBarProvider.latencyThreshold = 250; //ms
  }])
  .config(['$httpProvider', function($httpProvider){
    $httpProvider.interceptors.push('authInterceptor');
    $httpProvider.defaults.withCredentials = true;
  }])
  .run(function($rootScope, notify, $cookies){
    var username = $cookies.get('username');
    if (username) {
      $rootScope.username = username;
    }
    else {
      $rootScope.username = '';
    }
    $rootScope.alerts = [];
    $rootScope.closeAlert = function(index){
      $rootScope.alerts.splice(index, 1);
    };
    notify.config({
        position: 'right',
    });
  });
