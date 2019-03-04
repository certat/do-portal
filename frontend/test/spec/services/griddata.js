'use strict';

describe('Service: GridData', function () {

  // load the service's module
  beforeEach(module('cpApp'));

  // instantiate service
  var GridData;
  beforeEach(inject(function (_GridData_) {
    GridData = _GridData_;
  }));

  it('should do something', function () {
    expect(!!GridData).toBe(true);
  });

});
