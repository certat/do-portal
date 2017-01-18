'use strict';

describe('Controller: PasswdctrlCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var PasswdctrlCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    PasswdctrlCtrl = $controller('PasswdctrlCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    //expect(PasswdctrlCtrl.awesomeThings.length).toBe(3);
  });
});
