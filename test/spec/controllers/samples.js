'use strict';

describe('Controller: SamplesctrlCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var SamplesctrlCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SamplesctrlCtrl = $controller('SamplesctrlCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    //expect(SamplesctrlCtrl.awesomeThings.length).toBe(3);
  });
});
