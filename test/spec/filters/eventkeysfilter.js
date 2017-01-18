'use strict';

describe('Filter: eventKeysFilter', function () {

  // load the filter's module
  beforeEach(module('cpApp'));

  // initialize a new instance of the filter before each test
  var eventKeysFilter;
  beforeEach(inject(function ($filter) {
    eventKeysFilter = $filter('eventKeysFilter');
  }));

  it('should return the input prefixed with "eventKeysFilter filter:"', function () {
    var text = 'angularjs';
    expect(eventKeysFilter(text)).toBe('eventKeysFilter filter: ' + text);
  });

});
