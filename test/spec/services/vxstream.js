'use strict';

describe('Service: VxStream', function () {

  // load the service's module
  beforeEach(module('cpApp'));

  // instantiate service
  var VxStream;
  beforeEach(inject(function (_VxStream_) {
    VxStream = _VxStream_;
  }));

  it('should do something', function () {
    expect(!!VxStream).toBe(true);
  });

});
