'use strict';

describe('Filter: isEmptyFilter', function () {

  // load the filter's module
  beforeEach(module('cpApp'));

  // initialize a new instance of the filter before each test
  var isEmptyFilter;
  beforeEach(inject(function ($filter) {
    isEmptyFilter = $filter('isEmptyFilter');
  }));

  it('should return the input prefixed with "isEmptyFilter filter:"', function () {
    var text = 'angularjs';
    expect(isEmptyFilter(text)).toBe('isEmptyFilter filter: ' + text);
  });

});
