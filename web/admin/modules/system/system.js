(function() {

    angular.module('shomeAdm')
    .controller('SystemController', ['$scope', '$http', 'InfoMessage', function($scope, $http, InfoMessage) {

        $scope.im = InfoMessage;

        $scope.load = function() {
            $http.get('/admin/plugins')
                    .success(function(data){
                        $scope.plugins = data.plugins;
                        angular.forEach($scope.plugins, function(p) {
                            if (p.params) {
                                p.params = angular.fromJson(p.params);
                            }
                        });
                    });
        }

        $scope.load();

    }]);
}());

