'use strict';

describe('Directive: cpSampleDetails', function () {

  // load the directive's module
  beforeEach(module('cpApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<cp-sample-details></cp-sample-details>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the cpSampleDetails directive');
  }));
});
