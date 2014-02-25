'use strict';

var controllers = angular.module("geonoteControllers", ["StorageServices"])

controllers.controller("CreateNoteController", ["$scope", "$injector", "NotesStorage", function ($scope, $injector, NotesStorage) {
    $scope.is_modal = $injector.has("$modalInstance");

    $scope.note_content = {};

    $scope.ok = function (form) {
        $scope.note_content.date = new Date().toISOString();

        NotesStorage.addNote($scope.note_content);
        if($scope.is_modal) {
            $injector.get("$modalInstance").close($scope.note_content);
        }
        form.$setPristine();
    };

    $scope.cancel = function () {
        if($scope.is_modal) {
            $injector.get("$modalInstance").dismiss('cancel');
        }
    };

    window.navigator.geolocation.watchPosition(function(pos) {
        $scope.$apply(function(){
            $scope.note_content.lat = pos.coords.latitude;
            $scope.note_content.lng = pos.coords.longitude;
        });
    });
}]);
