'use strict';

describe('Service: DOAPI', function () {

  // load the service's module
  beforeEach(module('cpApp'));

  // instantiate service
  var DOAPI;
  beforeEach(inject(function (_DOAPI_) {
    DOAPI = _DOAPI_;
  }));

  it('should do something', function () {
    expect(!!DOAPI).toBe(true);
  });

});
