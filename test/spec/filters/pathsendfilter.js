'use strict';

describe('Filter: pathsEndFilter', function () {

  // load the filter's module
  beforeEach(module('cpApp'));

  // initialize a new instance of the filter before each test
  var pathsEndFilter;
  beforeEach(inject(function ($filter) {
    pathsEndFilter = $filter('pathsEndFilter');
  }));

  it('should return the input prefixed with "pathsEndFilter filter:"', function () {
    var text = 'angularjs';
    expect(pathsEndFilter(text)).toBe('pathsEndFilter filter: ' + text);
  });

});
