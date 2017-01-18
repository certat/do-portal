'use strict';

describe('Controller: SamplessubmitctrlCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var SamplessubmitctrlCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SamplessubmitctrlCtrl = $controller('SamplessubmitctrlCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    //expect(SamplessubmitctrlCtrl.awesomeThings.length).toBe(3);
  });
});
