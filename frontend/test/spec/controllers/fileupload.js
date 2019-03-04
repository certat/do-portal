'use strict';

describe('Controller: FileuploadCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var FileUploadCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    FileUploadCtrl = $controller('FileUploadCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    //expect(FileuploadCtrl.awesomeThings.length).toBe(3);
  });
});
