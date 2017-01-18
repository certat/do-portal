'use strict';

describe('Service: BOSH', function () {

  // load the service's module
  beforeEach(module('cpApp'));

  // instantiate service
  var BOSH;
  beforeEach(inject(function (_BOSH_) {
    BOSH = _BOSH_;
  }));

  it('should do something', function () {
    expect(!!BOSH).toBe(true);
  });

});
