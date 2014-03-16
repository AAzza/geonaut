'use strict';

var directives = angular.module("geonoteDirectives", []);
directives.directive("fileUploader", ["$parse", function ($parse) {
  return function (scope, $elem, attrs) {
    var fn = $parse(attrs.fileUploader);
    $elem.on("change", function (e) {
      fn(scope, { $files: e.target.files });
    });
  };
}]);
