'use strict';

describe('Controller: FileuploadctrlCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var FileuploadctrlCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    FileuploadctrlCtrl = $controller('FileuploadctrlCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    //expect(FileuploadctrlCtrl.awesomeThings.length).toBe(3);
  });
});
