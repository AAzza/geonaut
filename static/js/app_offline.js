'use strict';

angular.module('geonotes', [
  'ngRoute',
  'ui.bootstrap',
  'geonoteControllers'
]).config(function ($routeProvider) {
  $routeProvider
  .when('/', {
     templateUrl: 'static/partials/main_offline.html',
     controller: 'CreateNoteController'
  })
  .otherwise({
    redirectTo: '/'
  });
});
