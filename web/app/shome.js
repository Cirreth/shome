(function() {

var app = angular.module('shomeUI', []);

app.controller('MainController', ['$scope', '$http', function($scope, $http){

    $scope.sliderLow = 23;
    $scope.sliderHigh = 23;

    $scope.disabled = true;

    $scope.toggle = function() {
        $scope.disabled = !$scope.disabled;
    }

    $scope.init = function() {

        $scope.$watch('sliderLow', function(value){
            $scope.sliderHigh = value > $scope.sliderHigh ? value : $scope.sliderHigh;
        });

        $scope.$watch('sliderHigh', function(value){
            $scope.sliderLow = value < $scope.sliderLow ? value : $scope.sliderLow;
        });

        $http.post('/client/execute', {scenario: 'Today outdoor t'})
        .success(function(data){
            $scope.data = data;
        });

    }

}]);

})();