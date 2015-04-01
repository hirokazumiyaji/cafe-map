(function () {
  'use strict';

  var Client = (function() {
    function Client() {
      this.xhr = null;
      this.requestType = "";
      this.url = "";
      this.query = "";
      this.headers = {};
      this.data = null;
      this.successCallback = function(status, data) {};
      this.erroCallback = function(status, data) {};
    }

    Client.prototype.get = function(url, query, headers) {
      var key, q, value;
      if (query == null) {
        query = {};
      }
      if (headers == null) {
        headers = {};
      }
      this.xhr = new XMLHttpRequest();
      this.headers = headers;
      this.requestType = "GET";
      this.query = ((function() {
        var results;
        results = [];
        for (key in query) {
          value = query[key];
          results.push(key + "=" + encodeURIComponent(value));
        }
        return results;
      })()).join("&");
      this.url = this.query ? url + "?" + this.query : url;
      return this;
    };

    Client.prototype.post = function(url, data, query, headers) {
      var key, q, value;
      if (query == null) {
        query = {};
      }
      if (headers == null) {
        headers = {};
      }
      this.headers = headers;
      this.requestType = "GET";
      q = ((function() {
        var results;
        results = [];
        for (key in query) {
          value = query[key];
          results.push(key + "=" + encodeURIComponent(value));
        }
        return results;
      })()).join("&");
      this.url = q ? url + "?" + q : url;
      this.data = JSON.stringfity(data);
      return this;
    };

    Client.prototype.success = function(callback) {
      this.successCallback = callback;
      return this;
    };

    Client.prototype.error = function(callback) {
      this.errorCallback = callback;
      return this;
    };

    Client.prototype.execute = function() {
      var kind, value;
      var xhr = new XMLHttpRequest();
      xhr.open(this.requestType, this.url);
      for (kind in this.headers) {
        value = headers[kind];
        xhr.setRequestHeader(key, value);
      }
      var successCallback = this.successCallback;
      var errorCallback = this.errorCallback;
      xhr.onreadystatechange = function() {
        switch (xhr.readyState) {
          case 4:
            if ((200 <= xhr.status && xhr.status < 300) || xhr.status === 304) {
              successCallback(xhr.status, JSON.parse(xhr.responseText));
            } else {
              errorCallback(xhr.status, JSON.parse(xhr.responseText));
            }
            break;
        }
      };
      return xhr.send(this.data);
    };

    return Client;

  })();

  var Map = (function() {
    function Map() {
      this.reg = /.*駅/g;
      this.map = new google.maps.Map(document.getElementById('map-canvas'), {
        zoom: 5,
        center: new google.maps.LatLng(35, 135),
        mapTypeId: google.maps.MapTypeId.ROADMAP
      });
    }

    Map.prototype.search = function(station, genre) {
      var s;
      s = station.match(this.reg) ? station : station + '駅';
      var client = new Client();
      var map = this.map;
      client
        .get("/search", {station: s, genre: genre})
        .success(function (status, data) {
          var i, len, ref, results, store;
          map.setCenter(new google.maps.LatLng(data.station.lat, data.station.lng));
          map.setZoom(20);
          ref = data.stores;
          results = [];
          for (i = 0, len = ref.length; i < len; i++) {
            store = ref[i];
            results.push(new google.maps.Marker({
              position: new google.maps.LatLng(store.lat, store.lng),
              map: map,
              title: store.name
            }));
          }
          return results;
        })
        .execute();
    };
    return Map;
  })();

  function search() {
    var station = document.getElementById('station').value;
    var genre = document.getElementById('genre').value;
    Map.search(station, genre);
  }

  document.body.onload = function () {
    Map = new Map();
  };

  var button = document.getElementById('button-search');
  button.addEventListener('click', search, false);
})();
