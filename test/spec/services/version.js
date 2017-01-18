'use strict';

describe('Service: version', function () {

  // load the service's module
  beforeEach(module('cpApp'));

  // instantiate service
  var version;
  beforeEach(inject(function (_version_) {
    version = _version_;
  }));

  it('should do something', function () {
    expect(!!version).toBe(true);
  });

});
