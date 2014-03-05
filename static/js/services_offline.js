'use strict';

angular.module('StorageServices', []).service('NotesStorage', function() {
  var stored = angular.fromJson(localStorage.getItem('geonauts_cache'));
  if(stored) {
    this.notes = stored;
  } else {
    this.notes = [];
  }

  this.addNote = function(note) {
    this.notes.push(note);
    localStorage.setItem('geonauts_cache', angular.toJson(this.notes));
  };
});
