'use strict';

describe('Service: FileReader', function () {

  // load the service's module
  beforeEach(module('cpApp'));

  // instantiate service
  var FileReader;
  beforeEach(inject(function (_FileReader_) {
    FileReader = _FileReader_;
  }));

  it('should do something', function () {
    expect(!!FileReader).toBe(true);
  });

});
