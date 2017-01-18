'use strict';

describe('Directive: cpAvReport', function () {

  // load the directive's module
  beforeEach(module('cpApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<cp-av-report></cp-av-report>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the cpAvReport directive');
  }));
});
