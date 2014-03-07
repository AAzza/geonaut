'use strict';

var controllers = angular.module("geonoteControllers", ["StorageServices"])

controllers.controller("CreateNoteModalController", ["$scope", "NotesStorage", "$modalInstance", "latlng",
    function ($scope, NotesStorage, $modalInstance, latlng) {
  $scope.isModal = true;
  $scope.noteContent = {};
  $scope.hasCoords = true;
  $scope.noteContent.lat = latlng.lat;
  $scope.noteContent.lng = latlng.lng;

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
}]);

controllers.controller("CreateNoteController", ["$scope", "NotesStorage",
    function ($scope, NotesStorage) {
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
}]);


controllers.controller("MapViewController", ["$scope", "NotesStorage", "$modal",
    function ($scope, NotesStorage, $modal) {
  angular.extend($scope, {
    events: {
      map: {
        enable: ['click', 'popupopen'],
        logic: 'emit'
      }
    },
    center: {
      autoDiscover: true
    }
  });

  $scope.markers = NotesStorage.markers;

  $scope.$on('leafletDirectiveMap.click', function(event, args) {
    var latlng = args.leafletEvent.latlng;
    var modalInstance = $modal.open({
      templateUrl: 'partials/note_form.html',
      controller: "CreateNoteModalController",
      resolve: {
        latlng: function () {
          return latlng;
        },
      }
    });
  });
}]);
