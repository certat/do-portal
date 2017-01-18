'use strict';

describe('Controller: VulnerabilitiesCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var VulnerabilitiesCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    VulnerabilitiesCtrl = $controller('VulnerabilitiesCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(VulnerabilitiesCtrl.awesomeThings.length).toBe(3);
  });
});
