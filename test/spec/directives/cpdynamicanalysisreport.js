'use strict';

describe('Directive: cpDynamicAnalysisReport', function () {

  // load the directive's module
  beforeEach(module('cpApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<cp-dynamic-analysis-report></cp-dynamic-analysis-report>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the cpDynamicAnalysisReport directive');
  }));
});
