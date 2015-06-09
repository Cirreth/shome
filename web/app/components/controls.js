(function(){

var module = angular.module('shomeUiComponents', []);

module.directive('interval', ['$http', function($http){
    return {
        restrict: 'E',
        replace: true,
        template: intervalTemplate,
        link: function($scope, element, attrs) {

            var updateIfChanged = function() {
                if ($scope.valueOnUpdateStart.low != $scope.low || $scope.valueOnUpdateStart.high != $scope.high) {
                    refresh(true);
                    return true;
                }
                return false;
            }

            var refresh = function(update) {
                $scope.updateInProgress = true;
                $scope.valueOnUpdateStart = {
                    low: $scope.low,
                    high: $scope.high
                };
                $http.post('/client/execute',
                    {
                        scenario: $scope.scenario,
                        parameters: update ? {
                            low: $scope.low,
                            high: $scope.high
                        } : {}
                    }
                ).success(function(data){
                    $scope.updateInProgress = false;
                    if (!updateIfChanged()) {
                        $scope.value = data.value;
                        $scope.low = data.low;
                        $scope.high = data.high;
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

            $scope.$watch('low', function(value){
                $scope.high = value > $scope.high ? value : $scope.high;
            });

            $scope.$watch('high', function(value){
                $scope.low = value < $scope.low ? value : $scope.low;
            });

        },
        scope: {
            scenario: '@',
            parameters: '=',
            valueLabel: '@'
        }
    }
}]);

var intervalTemplate = ' <div class="uish-btn slider" ng-click="refresh()"> ' +
'        <div class="row"> ' + 
'            <div class="col-md-6 hidden-xs hidden-sm slot-left">{{scenario}}</div>' + 
'            <div class="col-md-6 col-xs-12 slot-right">' +
'                <span>{{low}}</span><input type="range" min="21" max="26" step="0.1" ng-model="low">' +
'                <span>{{high}}</span><input type="range" min="21" max="26" step="0.1" ng-model="high">' +
'                <p><span ng-hide="updateInProgress">{{valueLabel}}: {{value}}</span>' +
'                <span ng-show="updateInProgress">Loading...</span></p>' +
'            </div>' +
'        </div>' + 
'    </div>';


module.directive('toggle', ['$http', function($http){
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
                        console.log(data.value == true, $scope.trueValue)
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

        },
        scope: {
            scenario: '@',
            label: '@',
            trueValue: '@',
            falseValue: '@'
        }
    }
}]);

var toggleTemplate = '<div class="uish-btn toggle" ng-click="toggle()">' +
'            <div class="row">' +
'                <div class="col-md-10 col-xs-6">{{label}}</div>' +
'                <div class="col-md-2 col-xs-6 slot-right">' +
'                    <div class="led-yellow" ng-class="{off: !state}" ng-hide="updateInProgress"></div>' +
'                    <span ng-show="updateInProgress">Loading...</span>' +
'                </div>' +
'            </div>' +
'        </div>';

})();