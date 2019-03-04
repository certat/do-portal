'use strict';

/**
 * @ngdoc service
 * @name cpApp.errorMapper
 * @description
 * # errorMapper
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('errorMapper', function ($filter) {
    // Service logic
    var fieldNames = {
      abbreviation: 'Abbreviation',
      full_name: 'Address',
      cidr: 'CIDR',
      subject: 'Subject',
      list_id: 'Mailing list'
    };
    var validatorMessages = {
      // json schema validators
      '$ref': true,
      'additionalItems': true,
      'additionalProperties': true,
      'allOf': true,
      'anyOf': true,
      'dependencies': true,
      'enum': true,
      'format': {
        default: 'is invalid',
        cidr: 'is invalid'
      },
      'items': true,
      'maxItems': true,
      'maxLength': true,
      'maxProperties': true,
      'maximum': true,
      'minItems': true,
      'minLength': true,
      'minProperties': true,
      'minimum': true,
      'multipleOf': true,
      'not': true,
      'oneOf': true,
      'pattern': true,
      'patternProperties': true,
      'properties': true,
      required: {
        default: 'is required',
        terms: 'must be accepted'
      },
      'type': true,
      'uniqueItems': true

    };

    // Public API here
    return {
      map: function(response){
        if(!response.hasOwnProperty('validator')){
          return response.message;
        }
        var field = response.message.split("'")[1];
        if(response.validator === 'format'){
          field = response.message.split("'")[3];
        }
        if(!fieldNames.hasOwnProperty(field)){
          fieldNames[field] = $filter('humanizeFilter')(field);
        }
        //console.log(inflector(field, 'humanize'));
        var v = response.validator;
        if(validatorMessages[v][field] !== undefined){

          return fieldNames[field] + ' ' + validatorMessages[v][field];
        }
        return fieldNames[field] + ' ' + validatorMessages[v]['default'];
      }
    };
  });
