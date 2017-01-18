'use strict';

var config_module = angular.module('Portal.configuration', []);

var configs = {
  generalConfig: {},
  apiConfig: {
    urlPrefix: '/api/1.0'
  },
  boshConfig: {
    jid: null,
    nickname: null,
    connection: null,
    roster: {},
    participants: {},
    messagePool: {},
    rooms: {},
    services: {},
    unread: 0,
    subscriptions: [],
    activeChat: null,
    resource: '/DO',
    connectionStatus: '',
    selfPresence: {
      show: 'online',
      priority: 2,
      status: ''
    }
  }
};
angular.forEach(configs, function (k, v) {
  config_module.constant(v, k);
});