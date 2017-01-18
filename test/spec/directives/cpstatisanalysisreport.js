'use strict';

describe('Directive: cpStatisAnalysisReport', function () {

  // load the directive's module
  beforeEach(module('cpApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<cp-statis-analysis-report></cp-statis-analysis-report>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the cpStatisAnalysisReport directive');
  }));
});
