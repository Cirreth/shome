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


        $('#container').height($('#container').width() > 600 ? 400 : 200);

        $('#container').highcharts({
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Температура на улице'
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                hour: '%H:%M',
                month: ''
            }
        },
        yAxis: {
            title: {
                text: null
            }
        },
        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                }
            }
        },
        tooltip: {
            xDateFormat: '%H:%M'
        },
        series: [{
            name: 'Outdoor',
            data: $scope.data
        }]
    });


        });

    }

}]);

})();