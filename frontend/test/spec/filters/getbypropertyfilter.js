'use strict';

describe('Filter: getByPropertyFilter', function () {

  // load the filter's module
  beforeEach(module('cpApp'));

  // initialize a new instance of the filter before each test
  var getByPropertyFilter;
  beforeEach(inject(function ($filter) {
    getByPropertyFilter = $filter('getByPropertyFilter');
  }));

  it('should return the input prefixed with "getByPropertyFilter filter:"', function () {
    var text = 'angularjs';
    expect(getByPropertyFilter(text)).toBe('getByPropertyFilter filter: ' + text);
  });

});
