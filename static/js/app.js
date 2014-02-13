'use strict';

angular.module('geonotes', [
  'ngRoute',
  'leaflet-directive',
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
