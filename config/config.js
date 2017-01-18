'use strict';

angular.module('services.config', [])
  .constant('config', {
    version: '@@version',
    apiConfig: {
      webServiceUrl: '@@webServiceUrl',
      authUrl: '@@authUrl'
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
      resource: '/CP',
      connectionStatus: '',
      selfPresence: {
        show: 'online',
        priority: 2,
        status: ''
      }
    }
  });
