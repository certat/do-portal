'use strict';

describe('Controller: DeliverablesctrlCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var DeliverablesctrlCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    DeliverablesctrlCtrl = $controller('DeliverablesctrlCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(DeliverablesctrlCtrl.awesomeThings.length).toBe(3);
  });
});
