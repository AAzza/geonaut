'use strict';

angular.module('geonoteServices', [])
    .service('Notes', function() {
        this.markers = [];

        this.addNote = function(latlng, content, date) {
            this.markers.push({
                lat: latlng.lat,
                lng: latlng.lng,
                message: '<div ng-include="\'partials/marker.html\'"></div>',
                // focus: true,
                draggable: false,
                content: content,
                date: date
            });
        };
    })
