'use strict';

var controllers = angular.module("geonoteControllers", ["StorageServices"])

controllers.controller("CreateNoteController", ["$scope", "$injector", "NotesStorage", function ($scope, $injector, NotesStorage) {
    $scope.is_modal = $injector.has("$modalInstance");
    angular.extend($scope, {
        events: {
            map: {
                enable: ['locationfound', 'locationerror']
            }
        },
        center: {
            autoDiscover: true,
        }
    });

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

    $scope.$on('leafletDirectiveMap.locationfound', function(event, args) {
        $scope.note_content.lat = args.latlng.lat;
        $scope.note_content.lng = args.latlng.lng;
    });

    $scope.$on('leafletDirectiveMap.locationerror', function(event, args) {
        console.log("error");
        console.log(event);
    });
}]);
