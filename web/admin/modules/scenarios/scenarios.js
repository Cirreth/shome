(function() {

    angular.module('shomeAdm')
    .controller('ScenariosController', ['$scope', '$http', 'InfoMessage', function($scope, $http, InfoMessage) {

        $scope.im = InfoMessage;

        $scope.load = function() {
            $http.get('/admin/scenarios/')
                    .success(function(data){
                        $scope.scenarios = data;
                        console.log(data);
                    });
        }

        $scope.load();

        $scope.delete = function(tag, accepted) {
            if (!accepted) return;
            $http.delete('/admin/scenarios/'+tag)
                .success(function(data) {
                    $scope.im.okMessage(data);
                    $scope.load();
                })
                .error(function(data, status){
                    $scope.im.errorMessage(status+': '+data);
	    	    });
        }

    }]);
}());

