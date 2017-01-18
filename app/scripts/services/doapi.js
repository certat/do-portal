'use strict';

/**
 * @ngdoc service
 * @name cpApp.DOAPI
 * @description
 * # DOAPI
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('DOAPI', function ($log) {
    return {
      getAugmentKey: function(string){
        var JsSHA = jsSHA; // jshint ignore:line
        var shaObj = new JsSHA('SHA-1', 'B64');
        shaObj.update(btoa(string));
        return shaObj.getHash('HEX');

      },
      getId: function(length){
        var len = (angular.isNumber(length)) ? length: 8;
        var text = '';
        var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

        for( var i=0; i < len; i++ ) {
          text += possible.charAt(Math.floor(Math.random() * possible.length));
        }

        return text;
      },
      getRandomInt: function(min, max){
        return Math.floor(Math.random() * (max - min)) + min;
      },
      logRawInput: function (data) {
        $log.debug('RECV: ' + data);
      },
      logRawOutput: function (data) {
        $log.debug('SENT: ' + data);
      }
    };
  });
