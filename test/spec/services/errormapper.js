'use strict';

describe('Service: errorMapper', function () {

  // load the service's module
  beforeEach(module('cpApp'));

  // instantiate service
  var errorMapper;
  beforeEach(inject(function (_errorMapper_) {
    errorMapper = _errorMapper_;
  }));

  it('should do something', function () {
    expect(!!errorMapper).toBe(true);
  });

});
