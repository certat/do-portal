'use strict';

describe('Controller: InvestigationctrlCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var InvestigationctrlCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    InvestigationctrlCtrl = $controller('InvestigationctrlCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    //expect(InvestigationctrlCtrl.awesomeThings.length).toBe(3);
  });
});
