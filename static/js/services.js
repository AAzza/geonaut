'use strict';

var services = angular.module('StorageServices', []);

services.factory('NotesStorage', function($http, PopupRenderer, Markers) {
  var addNote = function(note) {
    var fd = new FormData();
    fd.append('lat', note.lat);
    fd.append('lng', note.lng);
    fd.append('date', note.date);
    fd.append('text_content', note.text_content);
    fd.append('media_content', note.media_content);

    $http.post('/geonotes', fd, {
      transformRequest: angular.identity,
      headers: {'Content-Type': undefined}
    })
    .success(function(data) {
      var marker = {
        'lat': parseFloat(note.lat),
        'lng': parseFloat(note.lng),
        'message': PopupRenderer.render(note),
        'draggable': false
      };
      Markers.createMarker(note.id, marker);
    });
  };

  var bootstrap = function() {
    var stored = angular.fromJson(localStorage.getItem('geonauts_cache'));
    if(stored) {
      angular.forEach(stored, addNote);
      localStorage.clear();
    }

    $http.get('/geonotes')
    .success(function(data) {
      angular.forEach(
        data,
        function(note) {
          var marker = {
            'lat': parseFloat(note.lat),
            'lng': parseFloat(note.lng),
            'message': PopupRenderer.render(note),
            'draggable': false
          };
          Markers.createMarker(note.id, marker);
      });
      Markers.zoomToMarkers(null);
    });
  };

  return {
    'bootstrap': bootstrap,
    'addNote': addNote
  };
});


services.factory("POI", function($http) {
  var getPOIreq = function(lat, lng) {
    return "http://nominatim.openstreetmap.org/reverse?format=json&lat="
    + lat + "&lon=" + lng;
  };

  var getPOIbyCoords = function(lat, lon, callback) {
    $http.get(getPOIreq(lat, lon))
    .success(callback);
  };

  return {
    'getPOIbyCoords': getPOIbyCoords
  };
});


services.factory('Markers', function(leafletData) {
  var markers = {};

  var createMarker = function(id_, marker) {
    markers[id_] = marker;
  };

  var zoomToMarkers = function(current_loc) {
    var current_loc = current_loc || {};
    var minLat = current_loc.lat || 1000;
    var maxLat = current_loc.lat || -1000;
    var minLng = current_loc.lng || 1000;
    var maxLng = current_loc.lng || -1000;

    for (var key in markers) {
      var marker = markers[key];
      minLat = Math.min(minLat, marker.lat);
      maxLat = Math.max(maxLat, marker.lat);
      minLng = Math.min(minLng, marker.lng);
      maxLng = Math.max(maxLng, marker.lng);
    }

    var height = maxLat - minLat;
    var width = maxLng - minLng;
    leafletData.getMap().then(function(m) {
      m.fitBounds([
        [minLat - 0.05*height, minLng - 0.05*width],
        [maxLat + 0.05*height, maxLng + 0.05*width]
      ]);
    });
  };

  return {
    'markers': markers,
    'createMarker': createMarker,
    'zoomToMarkers': zoomToMarkers
  }
});

services.factory('PopupRenderer', function($interpolate, $templateCache) {
  var render = function(note) {
    var template = $templateCache.get('/static/partials/marker.html')[1];

    var values = {};
    values.text = note.text_content;
    values.image = note.media_content || '/static/images/no-image.svg';
    values.createDate = note.date;
    return $interpolate(template)(values);
  };

  return {
    'render': render
  };
});
// Local Variables:
// js-indent-level: 2
// End:
