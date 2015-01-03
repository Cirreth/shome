(function() {

    var app = angular.module('shomeAdm');

    app.directive('startNode', ['Constructor', function(Constructor) {
        return {
            restrict: 'E',
            require: '?ngModel',
            link: function(scope, element, attrs, model) {
                Constructor.initNode(scope, element, attrs, model, 'Start');
                scope.connect = function() {Constructor.connect(scope, element, attrs, model)};
            }
        }
    }]);

    app.directive('requestNode', ['Constructor', function(Constructor) {
        return {
            restrict: 'E',
            require: '?ngModel',
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
            require: '?ngModel',
            link: function(scope, element, attrs, model) {
                if (attrs.hasOwnProperty('mock')) return false;
                Constructor.initNode(scope, element, attrs, model, 'C');
                scope.connect = function() {Constructor.connect(scope, element, attrs, model)};
            }
        }
    }]);

    /*
    --- Expected Constructor service methods ---

        before we are beginning, notice:
            1. link to model is stored in Constructor service


    */

    app.controller('ConstructorController', ['$scope', '$http', '$interval', 'Constructor',
                                                    function($scope, $http, $interval, Constructor) {

        /* convert server process representation to client process representation */
        function convertToViewFormat(data) {
            var start = {
                id: 'Start',
                type: 'StartNode',
                next: [].concat(data)
            };
            return treeToList(start);
        }

        function treeToList(root) {
            var list = [];
            list.push(root);
            var nextNames = [];
            var parallelNames = [];
            var exceptionalNames = [];
            if (root.next) {
                for (var i=0; i<root.next.length; i++) {
                    var nl = treeToList(root.next[i]);
                    list = list.concat(nl);
                    nextNames.push(root.next[i].id);
                }
            }
            if (root.parallel) {
                for (var i=0; i<root.parallel.length; i++) {
                    list = list.concat(treeToList(root.parallel[i]));
                    parallelNames.push(root.parallel[i].id);
                }
            }
            if (root.exceptional) {
                for (var i=0; i<root.exceptional.length; i++) {
                    //var exceptional = root.exceptional[i];
                    //exceptionalNames.push(root.exceptional[i].id);
                }
            }
            root.next = nextNames;
            root.parallel = parallelNames;
            root.exceptional = exceptionalNames;
            return list;
        }

        $scope.init = function() {
            //$http.get('./data-examples/process1.json')
            $http.get('/admin/scenarios/t_nursery')
            .success(function(data){
                Constructor.init();
                Constructor.name = "test";
                Constructor.nodes = convertToViewFormat(data);
                console.log('nodes', Constructor.nodes);
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