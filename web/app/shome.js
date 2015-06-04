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

        $http.post('/client/execute', {scenario: 'getHallTemp'})
        .success(function(data){
            $scope.hallTemp = data.value;
        })
        .error(function(){

        });

        $scope.$watch('sliderLow', function(value){
            $scope.sliderHigh = value > $scope.sliderHigh ? value : $scope.sliderHigh;
        });

        $scope.$watch('sliderHigh', function(value){
            $scope.sliderLow = value < $scope.sliderLow ? value : $scope.sliderLow;
        });

        $http.post('/client/execute', {scenario: 'Today outdoor t'})
        .success(function(data){
            $scope.data = data.result;

            var date = new Date();

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