'use strict';

/**
 * @ngdoc service
 * @name cpApp.BOSH
 * @description
 * # BOSH
 * Factory in the cpApp.
 */
angular.module('cpApp')
  .factory('BOSH', function ($rootScope, $cookies, config) {
    // Service logic
    // ...

    var props = config.boshConfig;

    // Public API here
    return {
      getJid: function (obj) {
        var sess = $cookies.get('bosh_session');
        var jid = props.connection ? (props.connection.jid ||
        props.connection._proto.jid) : sess.jid;
        if (obj.bare) {
          return jid.split('/')[0];
        } else {
          return jid;
        }
      },
      hasPreviousSession: function () {
        return !!$cookies.get('bosh_session');
      },
      setSession: function () {
        var session = {};
        session.url = props.connection.service;
        session.jid = props.connection.jid || props.connection._proto.jid;
        session.sid = props.connection.sid || props.connection._proto.sid;
        session.rid = props.connection.rid || props.connection._proto.rid;
        $cookies.putObject('bosh_session', session);
      },
      deleteSession: function () {
        $cookies.remove('bosh_session');
      },
      storeSessionData: function () {
        if (props.connection) {
          this.setSession();
        } else {
          this.deleteSession();
        }
      },
      attach: function (sess) {
        props.connection = new Strophe.Connection(sess.service, {'keepalive': true});
        props.connection.attach(sess.jid, sess.sid, sess.rid, this.checkStatus, 60);
      },
      connect: function (obj) {
        props.connection = new Strophe.Connection(obj.url);
        props.connection.connect(obj.jid + props.resource, obj.passwd, this.checkStatus, 60);
      },
      disconnect: function () {
        if(props !== undefined && props.connection != null){ // jshint ignore:line
          props.connection.flush();
          props.connection.options.sync = true;
          props.connection.disconnect();
        }else{
          console.log('props empty...');
        }

      },
      checkConnection: function () {
        return props.connection != null ? props.connection.connected : false; // jshint ignore:line
      },

      checkStatus: function (status) {
        switch (status) {
          case Strophe.Status.CONNECTING:
            props.connectionStatus = 'Connecting';
            break;
          case Strophe.Status.CONNECTED:
            props.connectionStatus = 'Connected';
            $rootScope.$broadcast('bosh-connected');
            break;
          case Strophe.Status.CONNFAIL:
            props.connectionStatus = 'Failed to connect';
            break;
          case Strophe.Status.AUTHENTICATING:
            props.connectionStatus = 'Authenticating';
            break;
          case Strophe.Status.AUTHFAIL:
            props.connectionStatus = 'Failed to authenticate';
            break;
          case Strophe.Status.DISCONNECTING:
            props.connectionStatus = 'Disconnecting';
            break;
          case Strophe.Status.DISCONNECTED:
            props.connectionStatus = 'Disconnected';
            break;
          case Strophe.Status.ATTACHED:
            props.connectionStatus = 'Connected';
            $rootScope.$broadcast('bosh-attached');
            break;
          case Strophe.Status.ERROR:
            props.connectionStatus = 'Error';
            break;
          default:
            break;
        }
        return true;
      }
    };
  });
