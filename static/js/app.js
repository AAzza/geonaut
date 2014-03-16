'use strict';

angular.module('geonotes', [
  'ngRoute',
  'ui.bootstrap',
  'leaflet-directive',
  'geonoteControllers',
  'geonoteDirectives'
]).config(function ($routeProvider) {
  $routeProvider
  .when('/', {
     templateUrl: 'static/partials/main.html',
     controller: 'MapViewController'
  })
  .otherwise({
    redirectTo: '/'
  });
});
