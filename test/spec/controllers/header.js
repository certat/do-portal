'use strict';

describe('Controller: HeaderctrlCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var HeaderctrlCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    HeaderctrlCtrl = $controller('HeaderctrlCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    //expect(HeaderctrlCtrl.awesomeThings.length).toBe(3);
  });
});
