'use strict';

describe('Service: QueryCache', function () {

  // load the service's module
  beforeEach(module('cpApp'));

  // instantiate service
  var QueryCache;
  beforeEach(inject(function (_QueryCache_) {
    QueryCache = _QueryCache_;
  }));

  it('should do something', function () {
    expect(!!QueryCache).toBe(true);
  });

});
