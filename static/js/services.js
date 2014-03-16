'use strict';

angular.module('StorageServices', []).factory('NotesStorage', function($http) {
  var markers = {};

  var createMarker = function(note) {
    var marker = {
      'lat': parseFloat(note.lat),
      'lng': parseFloat(note.lng),
      'message': note.text_content,
      'focus': true,
      'draggable': false
    };
    var id_ = note.id;
    markers[id_] = marker;
  };

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
      createMarker(data);
    })
    .error(function(data) {
      console.log('Error');
    });
  };

  var stored = angular.fromJson(localStorage.getItem('geonauts_cache'));
  if(stored) {
    angular.forEach(stored, addNote);
    localStorage.clear();
  }

  $http.get('/geonotes')
  .success(function(data) {
    angular.forEach(data, createMarker);
  });

  return {
    'markers': markers,
    'addNote': addNote
  };
});
