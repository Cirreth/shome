(function(){

var module = angular.module('shomeUiComponents', []);

module.directive('interval', ['$http', function($http){
    return {
        restrict: 'E',
        replace: true,
        template: template,
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

var template = ' <div class="uish-btn slider" ng-click="refresh()"> ' +
'        <div class="row"> ' + 
'            <div class="col-md-6 hidden-xs hidden-sm slot-left">{{scenario}}</div>' + 
'            <div class="col-md-6 col-xs-12 slot-right">' +
'                <input type="range" min="21" max="26" step="0.1" ng-model="low">' +
'                 <input type="range" min="21" max="26" step="0.1" ng-model="high">' +
'                <span ng-hide="updateInProgress">{{valueLabel}}: {{value}}</span>' +
'                <span ng-show="updateInProgress">Loading...</span>' +
'            </div>' +
'        </div>' + 
'    </div>';

})();