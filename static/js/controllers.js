'use strict';

var controllers = angular.module("geonoteControllers", ["StorageServices"])

// controllers.controller("GeoNoteController",
//     ["$scope", "$modal", "Notes", "$compile", function($scope, $modal, Notes, $compile) {
//         angular.extend($scope, {
//             oslo: {
//                 lat: 59.95,
//                 lng: 10.7,
//                 zoom: 15
//             },
//             events: {
//                 map: {
//                     enable: ['click', 'popupopen'],
//                     logic: 'emit'
//                 }
//             },
//             markers: Notes.markers
//         });
//
//         var open_form_modal = function (latlng) {
//             var modalInstance = $modal.open({
//                 templateUrl: 'static/partials/note_form.html',
//                 controller: "ModalInstanceCtrl",
//                 resolve: {
//                     latlng: function() { return latlng; }
//                 }
//             });
//             modalInstance.result.then(function (noteContent) {
//                 Notes.addNote(latlng, noteContent, new Date());
//             });
//         };
//         $scope.$on('leafletDirectiveMap.click', function(event, args) {
//             var latlng = args.leafletEvent.latlng;
//             open_form_modal(latlng);
//         });
//         $scope.$on('leafletDirectiveMarker.popupopen', function(event, leafletEvent){
//             var newScope = $scope.$new();
//             console.log(leafletEvent);
//             newScope.note = Notes.markers[leafletEvent.markerName];
//             $compile(leafletEvent.leafletEvent.popup._contentNode)(newScope);
//         });
// }]);

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

    $scope.ok = function () {
        $scope.note_content.date = new Date().toISOString();

        NotesStorage.addNote($scope.note_content);
        if($scope.is_modal) {
            $injector.get("$modalInstance").close($scope.note_content);
        }
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
