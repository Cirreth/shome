(function() {

var app = angular.module('shomeUI', ['shomeUiComponents']);

app.controller('MainController', ['$scope', '$http', function($scope, $http){

    $scope.toggle = function() {
        $scope.disabled = !$scope.disabled;
    }

    $scope.init = function() {

    }

}]);

})();