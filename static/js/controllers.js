'use strict';

var controllers = angular.module("geonoteControllers", ["StorageServices"])

controllers.controller("CreateNoteModalController",
    function ($scope, NotesStorage, $modalInstance, latlng, POI) {
  $scope.isModal = true;
  $scope.noteContent = {};
  $scope.hasCoords = true;
  $scope.hasPOI = false;
  $scope.noteContent.lat = latlng.lat;
  $scope.noteContent.lng = latlng.lng;

  POI.getPOIbyCoords(
    latlng.lat, latlng.lng,
    function(data) {
      $scope.hasPOI = true;
      $scope.noteContent.display_name = data.display_name;
    });

  $scope.ok = function (form) {
    if(form.$invalid) {
      return;
    }
    $scope.noteContent.date = new Date().toISOString();

    NotesStorage.addNote($scope.noteContent);
    $modalInstance.close($scope.noteContent);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };

  $scope.setFile = function($files) {
    $scope.noteContent.media_content = $files[0];
  };
});


controllers.controller("CreateNoteController", function ($scope, NotesStorage) {
  $scope.isModal = false;
  $scope.noteContent = {};
  $scope.hasCoords = false;

  $scope.ok = function (form) {
    if(form.$invalid) {
      return;
    }
    $scope.noteContent.date = new Date().toISOString();

    NotesStorage.addNote($scope.noteContent);
    $scope.noteContent = {};
    form.$setPristine();
  };

  window.navigator.geolocation.watchPosition(function(pos) {
    $scope.$apply(function() {
      $scope.noteContent.lat = pos.coords.latitude;
      $scope.noteContent.lng = pos.coords.longitude;
      $scope.hasCoords = true;
    });
  });
});


controllers.controller("MapViewController", function ($scope, $modal, Markers) {
  angular.extend($scope, {
    events: {
      map: {
        enable: ['click', 'popupopen'],
        logic: 'emit'
      }
    },
    defaults: {
      doubleClickZoom: false,
      scrollWheelZoom: true,
    }
  });

  window.navigator.geolocation.watchPosition(function(pos) {
    $scope.$apply(function() {
      setTimeout(function() {
        Markers.zoomToMarkers({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        Markers.createMarker(null, {
          lat: pos.coords.latitude, lng: pos.coords.longitude,
          message: "You are here",
          icon: {
            iconUrl: 'static/images/current_icon.png',
            iconSize: [48, 48],
            iconAnchor: [23, 42],
          },
          focus: true
        });
      }, 750);
    });
  });

  $scope.markers = Markers.markers;

  $scope.$on('leafletDirectiveMap.click', function(event, args) {
    var latlng = args.leafletEvent.latlng;
    var modalInstance = $modal.open({
      templateUrl: 'static/partials/note_form.html',
      controller: "CreateNoteModalController",
      resolve: {
        latlng: function () {
          return latlng;
        },
      }
    });
  });
});

// Local Variables:
// js-indent-level: 2
// End:
