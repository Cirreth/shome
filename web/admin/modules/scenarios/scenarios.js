(function() {

    angular.module('shomeAdm')
    .controller('ScenariosController', ['$scope', '$http', function($scope, $http) {

        $http.get('/admin/scenarios/')
                .success(function(data){
                    $scope.scenarios = data;
                    console.log(data);
                });

    }]);
}());

