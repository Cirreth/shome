(function() {

var app = angular.module('shomeUI', ['shomeUiComponents']);

app.controller('MainController', ['$scope', '$http', function($scope, $http){

    $scope.toggle = function() {
        $scope.disabled = !$scope.disabled;
    }

    $scope.init = function() {

        $http.post('/client/execute', {scenario: 'Boiler state'})
        .success(function(data){
            $scope.disabled = data.value == 1 ? false : true;
        })
        .error(function(){

        });

        $http.post('/client/execute', {scenario: 'Today outdoor t'})
        .success(function(data){
            $scope.data = data.result;

            var date = new Date();

            $scope.last = $scope.data.length > 0 ? $scope.data[$scope.data.length-1].value : 'Нет данных';

            $scope.data = $scope.data.map(function(e){
                var dt = e.time.split(':');
                return [Date.UTC(date.getYear(), date.getMonth()+1, date.getDate(), dt[0], dt[1]), e.value];
            });

            $scope.outdoorSeries = [
                {
                    name: 'Улица',
                    data: $scope.data
                }
            ];

    });

    $http.post('/client/execute', {scenario: 'todayTempNursery'})
    .success(function(data){
        $scope.dataNursery = data.result;

        var date = new Date();

        if (!$scope.dataNursery) return;
        $scope.lastNursery = $scope.dataNursery.length > 0 ? $scope.dataNursery[$scope.dataNursery.length-1].value : 'Нет данных';

        $scope.dataNursery = $scope.dataNursery.map(function(e){
            var dt = e.time.split(':');
            return [Date.UTC(date.getYear(), date.getMonth()+1, date.getDate(), dt[0], dt[1]), e.value];
        });

        $scope.nurserySeries = [
            {
                name: 'Детская',
                data: $scope.dataNursery
            }
        ];

    });

    }

}]);

})();