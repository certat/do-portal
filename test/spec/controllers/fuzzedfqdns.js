'use strict';

describe('Controller: FuzzedfqdnsCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var FuzzedfqdnsCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    FuzzedfqdnsCtrl = $controller('FuzzedfqdnsCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(FuzzedfqdnsCtrl.awesomeThings.length).toBe(3);
  });
});
