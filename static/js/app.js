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
     templateUrl: '/static/partials/main.html',
     controller: 'MapViewController'
  })
  .otherwise({
    redirectTo: '/'
  });
}).run(function ($templateCache, $http) {
  $http.get('/static/partials/marker.html', { cache: $templateCache });
}).run(function (NotesStorage) {
  NotesStorage.bootstrap();
}).run(function ($window) {
  var onUpdateReady = function() {
    var answer = $window.confirm("New version of page is available. Do you want to reload now?");
    if(answer) {
      $window.location.reload();
    }
  };

  $window.applicationCache.addEventListener('updateready', onUpdateReady);
  if($window.applicationCache.status === $window.applicationCache.UPDATEREADY) {
    onUpdateReady();
  }
});
