(function() {

    angular.module('shomeAdm')
    .controller('SystemController', ['$scope', '$http', 'InfoMessage', function($scope, $http, InfoMessage) {

        $scope.im = InfoMessage;

        $scope.load = function() {
            $http.get('/admin/plugins/all')
                    .success(function(data){
                        $scope.plugins = data;
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

