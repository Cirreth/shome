(function() {

    var app = angular.module('shomeAdm');

    app.directive('requestNode', ['Constructor', function(Constructor) {
        return {
        restrict: 'E',
        require: 'ngModel',
        link: function(scope, element, attrs, model) {
            if (attrs.hasOwnProperty('mock')) return false;
            Constructor.initNode(scope, element, attrs, model, 'R');
            scope.connect = function() {Constructor.connect(scope, element, attrs, model)};
        }
        }
    }]);

    app.directive('conditionalNode', ['Constructor', function(Constructor) {
        return {
            restrict: 'E',
            require: 'ngModel',
            link: function(scope, element, attrs, model) {
                if (attrs.hasOwnProperty('mock')) return false;
                Constructor.initNode(scope, element, attrs, model, 'C');
                scope.connect = function() {Constructor.connect(scope, element, attrs, model)};
            }
        }
    }]);

    app.controller('ConstructorController', ['$scope', '$http', '$interval', 'Constructor',
                                                    function($scope, $http, $interval, Constructor) {

        $scope.init = function() {
            $http.get('./data-examples/process1.json')
            .success(function(data){
                Constructor.name = "test";
                Constructor.nodes = data;
                $scope.nodes = Constructor.nodes;
                /* endpoints polling for init connections*/
                var epp = setInterval(function() {
                    var state = true;
                    for (i=0; i<Constructor.nodes.length; i++) {
                        if (!Constructor.hasEndpoints(Constructor.nodes[i].id)) {
                            state = false;
                            break;
                        }
                    }
                    /* all endpoints created */
                    if (state) {
                        clearInterval(epp);
                        Constructor.drawAllConnections();
                    }
                }, 200);
                /* end */
            });
        }

        $scope.newRequestNode = function() {
            Constructor.nodes.push({
                "id": 'rn'+parseInt(Math.random()*500),
                "type": "RequestNode",
                "plugin": "...",
                "reference": "...",
                "position": {
                    "left": 680,
                    "top": 25
                },
                "next": [],
                "parallel": [],
                "exceptional": []
            });
        };

        $scope.newConditionalNode = function() {
            Constructor.nodes.push({
                "id": 'cn'+parseInt(Math.random()*500),
                "type": "ConditionalNode",
                "condition": "not defined",
                "position": {
                    "left": 653,
                    "top": 123
                },
                "next": [],
                "parallel": [],
                "exceptional": []
            });
        };

        $scope.$on('$locationChangeStart',function(evt, absNewUrl, absOldUrl) {
            if (absOldUrl.indexOf('#/constructor')>-1) Constructor.destroy();
        });


    }]);

}());