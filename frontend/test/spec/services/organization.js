'use strict';

describe('Service: Organization', function () {

  // load the service's module
  beforeEach(module('cpApp'));

  // instantiate service
  var Organization;
  beforeEach(inject(function (_Organization_) {
    Organization = _Organization_;
  }));

  it('should do something', function () {
    expect(!!Organization).toBe(true);
  });

});
