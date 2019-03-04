'use strict';

describe('Controller: PasswdCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var PasswdCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    PasswdCtrl = $controller('LoginCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    //expect(PasswdCtrl.awesomeThings.length).toBe(3);
  });
});
