(function(){

var module = angular.module('shomeUiComponents', []);

module.directive('stringToNumber', function() {
  return {
    require: 'ngModel',
    link: function(scope, element, attrs, ngModel) {
      ngModel.$parsers.push(function(value) {
        return '' + value;
      });
      ngModel.$formatters.push(function(value) {
        return parseFloat(value, 2);
      });
    }
  };
});

module.directive('selectOnClick', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            element.on('click', function () {
                if (!window.getSelection().toString()) {
                    // Required for mobile Safari
                    this.setSelectionRange(0, this.value.length)
                }
            });
        }
    };
});

module.directive('shInterval', ['$http', '$interval', function($http, $interval){
    return {
        restrict: 'E',
        replace: true,
        template: intervalTemplate,
        link: function($scope, element, attrs) {

            updateIfChanged = function() {
                if (!$scope.valueOnUpdateStart) {
                    refresh();
                    return true;
                }
                else if ($scope.valueOnUpdateStart.low != $scope.low || $scope.valueOnUpdateStart.high != $scope.high) {
                    refresh(true);
                    return true;
                }
                return false;
            }

            var refresh = function(sendValues) {
                $scope.updateInProgress = true;
                $scope.valueOnUpdateStart = {
                    low: $scope.low,
                    high: $scope.high
                };
                $http.post('/client/execute', {
                    scenario: $scope.scenario,
                    parameters: sendValues ? {
                        low: parseFloat($scope.low || $scope.high), //align values on first using
                        high: parseFloat($scope.high || $scope.low)
                    } : {}
                }).success(function(data){
                    $scope.updateInProgress = false;
                    if (!updateIfChanged()) {
                        $scope.value = data.value;
                        $scope.low = parseFloat(data.low);
                        $scope.high = parseFloat(data.high);
                        $scope.error = false;
                    }
                }).error(function(error) {
                    $scope.updateInProgress = false;
                    if (!updateIfChanged()) {
                        $scope.error = true;
                    }
                });

            }

            refresh();

            $scope.refresh = function() {
                $scope.low = $scope.low > $scope.high ? $scope.high : $scope.low;
                if (!$scope.updateInProgress) {
                    refresh(true);
                }
            }

            $scope.focus = function($model) {
                $model = $model+1;
            }

            $scope.$watch('low', function(value){
                $scope.high = value > $scope.high ? value : $scope.high;
            });

            $scope.$watch('high', function(value){
                $scope.low = value < $scope.low ? value : $scope.low;
            });

            if ($scope.updateInterval) {
                $interval(function() {
                    if (!$scope.updateInProgress) {
                        refresh();
                    }
                }, $scopeUpdateInterval*1000);
            }

        },
        scope: {
            scenario: '@',
            parameters: '=',
            valueLabel: '@',
            min: '@',
            max: '@'
        }
    }
}]);

var intervalTemplate = ' <div class="uish-btn slider" ng-click="refresh()" ng-cloak> ' +
'        <div class="row"> ' + 
'            <div class="col-md-6 hidden-xs hidden-sm slot-left">{{scenario}}</div>' + 
'            <div class="col-md-6 col-xs-12 slot-right">' +
'                <span><input class="range-label-input" min="{{min}}" max="{{max}}" type="number" step="0.1" string-to-number' +
'                    ng-model="low" ng-model-options="{debounce: 1000}" ng-change="refresh()" select-on-click></span>' +
'                <input type="range" min="{{min}}" max="{{max}}" step="0.1" ng-model="low" ng-mouseup="refresh()" >' +
'                <span><input class="range-label-input" min="{{min}}" max="{{max}}" type="number"  step="0.1" string-to-number' +
'                      ng-model="high" ng-model-options="{debounce: 1000}" ng-change="refresh()" select-on-click></span>' +
'                <input type="range" min="{{min}}" max="{{max}}" step="0.1" ng-model="high" ng-mouseup="refresh()">' +
'                <p><span ng-hide="updateInProgress">{{valueLabel}}: {{value}}</span>' +
'                <span ng-show="updateInProgress">Loading...</span></p>' +
'            </div>' +
'        </div>' + 
'    </div>';

module.directive('shToggle', ['$http', '$interval', function($http, $interval){
    return {
        restrict: 'E',
        replace: true,
        template: toggleTemplate,
        link: function($scope, element, attrs) {

            $scope.toggle = function() {
                $scope.state = !$scope.state;
                refresh(true);
            }

            var updateIfChanged = function() {
                if ($scope.state != $scope.valueOnUpdateStart) {
                    refresh(true);
                    return true;
                }
                return false;
            }

            var refresh = function(update) {
                $scope.updateInProgress = true;
                $scope.valueOnUpdateStart = $scope.state;
                var value = undefined;
                if ($scope.state) {
                    value = $scope.trueValue ? $scope.trueValue : true;
                } else {
                    value = $scope.falseValue ? $scope.falseValue : false;
                }
                $http.post('/client/execute',
                    {
                        scenario: $scope.scenario,
                        parameters: update ? {
                            state: value
                        } : {}
                    }
                ).success(function(data){
                    $scope.updateInProgress = false;
                    if (!updateIfChanged()) {
                        if ($scope.trueValue && data.value == $scope.trueValue || data.value == true) {
                            $scope.state = true;
                        } else {
                            $scope.state = false;
                        }
                        $scope.error = false;
                    }
                }).error(function(error) {
                    $scope.updateInProgress = false;
                    if (!updateIfChanged()) {
                        $scope.error = true;
                    }
                });

            }

            refresh();

            $scope.refresh = function() {
                if (!$scope.updateInProgress) {
                    refresh(true);
                }
            }

            if ($scope.updateInterval) {
                $interval(function() {
                    if (!$scope.updateInProgress) {
                        refresh();
                    }
                }, $scope.updateInterval*1000);
            }

        },
        scope: {
            scenario: '@',
            label: '@',
            trueValue: '@',
            falseValue: '@',
            updateInterval: '@'
        }
    }
}]);

var toggleTemplate = '<div class="uish-btn toggle" ng-click="toggle()" ng-cloak>' +
'            <div class="row">' +
'                <div class="col-md-10 col-xs-6">{{label}}</div>' +
'                <div class="col-md-2 col-xs-6 slot-right">' +
'                    <div class="led-yellow" ng-class="{off: !state}" ng-hide="updateInProgress"></div>' +
'                    <span ng-show="updateInProgress">Loading...</span>' +
'                </div>' +
'            </div>' +
'        </div>';

module.directive('shChart', ['$http', '$interval', function($http, $interval) {
    return {
        restrict: 'E',
        replace: true,
        template: chartTemplate,
        scope: {
            label: '@',
            scenario: '@',
            updateInterval: '@'
        },
        link: function($scope, element, attrs) {

            element.height(element.width() > 600 ? 400 : 200);

            var rebuildCharts = function() {

                element.highcharts({
                    chart: {
                        type: 'spline'
                    },
                    title: {
                        text: $scope.label
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
                    series: $scope.series
                });

            }

            var refresh = function() {

                $http.post('/client/execute', {scenario: $scope.scenario})
                .success(function(data){

                    if (!data) {
                        $scope.error = true;
                         console.log('Graph element '+$scope.scenario+' was hidden', 'no data', data);
                        return;
                    }

                    $scope.data = data.result;

                    var date = new Date();

                    $scope.last = $scope.data.length > 0 ? $scope.data[$scope.data.length-1].value : 'Нет данных';

                    $scope.data = $scope.data.map(function(e){
                        var dt = e.time.split(':');
                        return [Date.UTC(date.getYear(), date.getMonth()+1, date.getDate(), dt[0], dt[1]), e.value];
                    });

                    $scope.series = [
                        {
                            name: 'Улица',
                            data: $scope.data
                        }
                    ];

                    if ($scope.series && $scope.series.length > 0) {
                        rebuildCharts();
                    }

                    $scope.error = false;

                }).error(function(error) {
                    $scope.error = true;
                    console.log('Graph element '+$scope.scenario+' was hidden', error);
                });

            }

            $scope.refresh = function() {
               refresh();
            }

            refresh();

            if ($scope.updateInterval) { //seconds to milliseconds
                $interval(function() {
                    $scope.refresh();
                }, $scope.updateInterval*1000);
            }

        }
    }
}]);

var chartTemplate = '<div class="uish-btn" ng-cloak ng-hide="error">' +
'    <div style="min-width: 250px; margin: 0 auto"></div>' +
'</div>'

module.directive('shValue', ['$http', '$interval', function($http, $interval) {
    return {
        restrict: 'E',
        replace: true,
        template: valueTemplate,
        scope: {
            label: '@',
            scenario: '@',
            units: '@',
            updateInterval: '@'
        },
        link: function($scope, element, attrs) {

            $scope.loading = false;

            $scope.refresh = function() {
                $scope.loading = true;
                $scope.value = 'Loading...';
                $http.post('/client/execute', {scenario: $scope.scenario})
                .success(function(value) {
                    $scope.value = value.value;
                    $scope.loading = false;
                })
                .error(function(error) {
                    $scope.loading = false;
                });
            }

            $scope.refresh();

            if ($scope.updateInterval) {
                $interval(function() {
                    $scope.refresh();
                }, $scope.updateInterval*1000);
            }

        }
    }
}]);

var valueTemplate = '<div class="uish-btn" ng-click="refresh()" ng-cloak>' +
'   <span><b ng-bind="label" style="padding-right: 7px;"></b><span ng-bind="value"></span><span ng-bind="units"></span></span>' +
'</div>'

})();