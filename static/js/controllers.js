'use strict';

var controllers = angular.module("geonoteControllers", ["StorageServices"])


controllers.controller("CreateNoteController", ["$scope", "$injector", "NotesStorage",
    function ($scope, $injector, NotesStorage) {
  $scope.isModal = $injector.has("$modalInstance");
  $scope.noteContent = {};
  $scope.hasCoords = false;

  $scope.ok = function (form) {
    if(form.$invalid) {
      return;
    }
    $scope.noteContent.date = new Date().toISOString();

    NotesStorage.addNote($scope.noteContent);
    if($scope.isModal) {
      $injector.get("$modalInstance").close($scope.noteContent);
    } else {
      $scope.noteContent = {};
      form.$setPristine();
    }
  };

  $scope.cancel = function () {
    if($scope.isModal) {
      $injector.get("$modalInstance").dismiss('cancel');
    }
  };

  window.navigator.geolocation.watchPosition(function(pos) {
    $scope.$apply(function() {
      $scope.noteContent.lat = pos.coords.latitude;
      $scope.noteContent.lng = pos.coords.longitude;
      $scope.hasCoords = true;
    });
  });
}]);


controllers.controller("MapViewController", ["$scope", "NotesStorage",
    function ($scope, NotesStorage) {
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
}]);
