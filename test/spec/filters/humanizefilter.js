'use strict';

describe('Filter: humanizeFilter', function () {

  // load the filter's module
  beforeEach(module('cpApp'));

  // initialize a new instance of the filter before each test
  var humanizeFilter;
  beforeEach(inject(function ($filter) {
    humanizeFilter = $filter('humanizeFilter');
  }));

  it('should return the input prefixed with "humanizeFilter filter:"', function () {
    var text = 'angularjs';
    expect(humanizeFilter(text)).toBe('humanizeFilter filter: ' + text);
  });

});
