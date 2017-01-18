'use strict';

describe('Controller: OrganizationeditctrlCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var OrganizationeditctrlCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    OrganizationeditctrlCtrl = $controller('OrganizationeditctrlCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    //expect(OrganizationeditctrlCtrl.awesomeThings.length).toBe(3);
  });
});
