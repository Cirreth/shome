(function() {

    angular.module('shomeAdm')
    .controller('ScenariosController', ['$scope', '$http', function($scope, $http) {

        $http.get('./data-examples/scenarios.json')
                .success(function(data){
                    $scope.scenarios = data;
                });

    }]);
}());

