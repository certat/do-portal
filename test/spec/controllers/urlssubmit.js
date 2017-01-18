'use strict';

describe('Controller: UrlsSubmitCtrl', function () {

  // load the controller's module
  beforeEach(module('cpApp'));

  var UrlsSubmitCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    UrlsSubmitCtrl = $controller('UrlsSubmitCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(UrlsSubmitCtrl.awesomeThings.length).toBe(3);
  });
});
