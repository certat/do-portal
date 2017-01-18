'use strict';

describe('Controller: NessusCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var NessusCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    NessusCtrl = $controller('NessusCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(NessusCtrl.awesomeThings.length).toBe(3);
  });
});
