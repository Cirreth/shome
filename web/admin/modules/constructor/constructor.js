(function() {

    var app = angular.module('shomeAdm');

    app.directive('startNode', ['$rootScope', 'Notification', 'Constructor',  function($rootScope, Notification, Constructor) {
        return {
            restrict: 'E',
            require: '?ngModel',
            link: function(scope, element, attrs, model) {
                Constructor.initNode(scope, element, attrs, model, 'StartNode');
                scope.connect = function() {
                    Constructor.connect(scope, element, attrs, model);
                    $rootScope.selected = Constructor.selected;
                };
            }
        }
    }]);

    app.directive('delayNode', ['$rootScope', 'Constructor', function($rootScope, Constructor) {
        return {
            restrict: 'E',
            require: '?ngModel',
            link: function(scope, element, attrs, model) {
                if (attrs.hasOwnProperty('mock')) return false;
                Constructor.initNode(scope, element, attrs, model, 'DelayNode');
                scope.connect = function() {
                    Constructor.connect(scope, element, attrs, model);
                    $rootScope.selected = Constructor.selected;
                };
            }
        }
    }]);

    app.directive('requestNode', ['$rootScope', 'Constructor', function($rootScope, Constructor) {
        return {
            restrict: 'E',
            require: '?ngModel',
            link: function(scope, element, attrs, model) {
                if (attrs.hasOwnProperty('mock')) return false;
                Constructor.initNode(scope, element, attrs, model, 'RequestNode');
                scope.connect = function() {
                    Constructor.connect(scope, element, attrs, model);
                    $rootScope.selected = Constructor.selected;
                };
            }
        }
    }]);

    app.directive('conditionalNode', ['$rootScope', 'Constructor', function($rootScope, Constructor) {
        return {
            restrict: 'E',
            require: '?ngModel',
            link: function(scope, element, attrs, model) {
                if (attrs.hasOwnProperty('mock')) return false;
                Constructor.initNode(scope, element, attrs, model, 'ConditionalNode');
                scope.connect = function() {
                    Constructor.connect(scope, element, attrs, model);
                    $rootScope.selected = Constructor.selected;
                };
            }
        }
    }]);

    app.directive('schedulerNode', ['$rootScope', 'Constructor', function($rootScope, Constructor) {
        return {
            restrict: 'E',
            require: '?ngModel',
            link: function(scope, element, attrs, model) {
                if (attrs.hasOwnProperty('mock')) return false;
                Constructor.initNode(scope, element, attrs, model, 'RequestNode');
                scope.connect = function() {
                    Constructor.connect(scope, element, attrs, model);
                    $rootScope.selected = Constructor.selected;
                };
            }
        }
    }]);

    app.directive('executeNode', ['$rootScope', 'Constructor', function($rootScope, Constructor) {
        return {
            restrict: 'E',
            require: '?ngModel',
            link: function(scope, element, attrs, model) {
                if (attrs.hasOwnProperty('mock')) return false;
                Constructor.initNode(scope, element, attrs, model, 'RequestNode');
                scope.connect = function() {
                    Constructor.connect(scope, element, attrs, model);
                    $rootScope.selected = Constructor.selected;
                };
            }
        }
    }]);

    /*
    --- Expected Constructor service methods ---

        before we are beginning, notice:
            1. link to model is stored in Constructor service


    */

    app.controller('ConstructorController',
                            ['$scope', '$rootScope', '$http', '$interval', '$routeParams', 'Notification', 'Constructor',
                             function($scope, $rootScope, $http, $interval, $routeParams, Notification, Constructor) {

        window.onresize = function(event) {
            Constructor.repaint();
        };

        $scope.exceptionalMode = Constructor.exceptionalMode;

        $scope.$watchCollection('selected', function(value) {
            if ($scope.selected && !$scope.selected.type) {
                delete $scope.selected;
            }
        });

        var startNode = {
                id: 'Start',
                type: 'StartNode',
                next: [],
                parallel: []
        };

        /* convert server process representation to client process representation */
        function unpackScenario(data) {
            startNode.next = startNode.next.concat(data);
            return treeToList(startNode);
        }

        function treeToList(root) {
            var list = [];
            list.push(root);
            var nextNames = [];
            var parallelNames = [];
            var exceptionalNames = [];
            var yesNames = [];
            var noNames = [];
            var prepare = function(direction, resultSet) {
                for (var i=0; i<direction.length; i++) {
                    var nl = treeToList(direction[i]);
                    list = list.concat(nl);
                    resultSet.push(direction[i].id);
                }
            }
            if (root.next) prepare(root.next, nextNames);
            if (root.yes) prepare(root.yes, yesNames);
            if (root.no) prepare(root.no, noNames);
            if (root.parallel) prepare(root.parallel, parallelNames);
            if (root.exceptional) prepare(root.exceptional, exceptionalNames);
            root.next = nextNames;
            root.parallel = parallelNames;
            root.exceptional = exceptionalNames;
            if (root.type === 'ConditionalNode') {
                root.yes = yesNames;
                root.no = noNames;
            }
            return list;
        }

        function listToTree(data, nodeId) {
            var node = findNodeWithId(data, nodeId);
            if (!node) return;
            var next = [];
            var parallel = [];
            var exceptional = [];
            var prepare = function(direction, resultSet) {
                for (var i=0; i<direction.length; i++) {
                    resultSet.push(listToTree(data, direction[i]));
                }
            }
            /* excess fields */
            delete node.active;
            /**/
            if (node.next) prepare(node.next, next);
            if (node.parallel) prepare(node.parallel, parallel);
            if (node.exceptional) prepare(node.exceptional, exceptional);
            node.next = next;
            node.parallel = parallel;
            node.exceptional = exceptional;
            if (node.type === 'ConditionalNode') {
                var yes = [];
                var no = [];
                if (node.yes) prepare(node.yes, yes);
                if (node.no) prepare(node.no, no);
                node.yes = yes;
                node.no = no;
            }
            return node;
        }

        function findNodeWithId(array, id) {
            for (var i=0; i<array.length; i++) {
                if (array[i].id === id) {
                    return array[i];
                }
            }
        }

        $scope.packScenario = function() {
            var nodes = angular.copy($scope.nodes);
            var start = findNodeWithId(nodes, 'Start');
            var list = [];
            for (var i=0; i<start.next.length; i++) {
                list.push(listToTree(nodes, start.next[i]));
            }
            if (list.length === 0 ) {
                delete $scope.scenario;
            } else if (list.length === 1) {
                $scope.scenario = list[0];
            } else {
                $scope.scenario = list;
            }
        }

        function initConstructor(scenario) {
            Constructor.init();
            Constructor.name = scenario;
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
        }

        $scope.init = function() {
            $scope.name = $routeParams.scenario;
            if ($scope.name) {
                $http.get('/admin/scenarios/'+$scope.name)
                .success(function(data){
                    Constructor.nodes = unpackScenario(data);
                    $scope.nodes = Constructor.nodes;
                    initConstructor($scope.name);
                });
            } else {
                $scope.name = "New scenario name";
                $scope.new = true;
                Constructor.nodes = [startNode];
                $scope.nodes = Constructor.nodes;
                initConstructor($scope.name);
            }
            $http.get('/admin/plugins')
                .success(function(data){
                    var plugins = [];
                    angular.forEach(data.plugins, function(v, k) {
                        if (v.state == 'active') plugins.push(k);
                    });
                    $scope.plugins = plugins;
                });
            $http.get('/admin/scenarios/')
                .success(function(data){
                    $scope.scenarios = [];
                    angular.forEach(data, function(v) {
                        $scope.scenarios.push(v.name);
                    });
                });
        }

        $scope.toggleExceptional = function() {
            Constructor.exceptionalMode = !Constructor.exceptionalMode;
            $scope.exceptionalMode = Constructor.exceptionalMode;
        }

        var checkScenario = function() {
            var start = $scope.nodes.filter(function(a) {return a.id == 'Start'})[0];
            if (!start.next || start.next.length == 0) {
                Notification.error('There are no nodes connected to start');
                return false;
            }
            return true;
        }

        $scope.checkScenario = function() {
            if (!checkScenario()) return;
            Notification('...')
            $http.post('/admin/constructor/check', {expression: angular.toJson($scope.nodes)})
            .success(function(data) {
                Notification.success('Result: '+angular.toJson(data));
            })
            .error(function(data, status){
                Notification.error({message: 'Error: '+data, delay: 30000});
            });
        }

        $scope.saveScenario = function() {
            if (!checkScenario()) return;
            if ($scope.new) {
                $http.post('/admin/scenarios/'+$scope.name, {expression: angular.toJson($scope.scenario)})
                .success(function(data) {
                    delete $scope.new;
                    Notification.success('Result: '+data);
                })
                .error(function(data, status){
                    Notification.error('Error: '+data);
                });
            } else {
                $http.put('/admin/scenarios/'+$scope.name, {expression: angular.toJson($scope.scenario)})
                .success(function(data) {
                    Notification.success('Result: '+data);
                })
                .error(function(data, status){
                    Notification.error('Error: '+data);
                });
            }
        }

        $scope.deleteSelected = function() {
            var id = $scope.selected.id;
            var nodes = $scope.nodes;
            var findAndDelete = function(array, id) {
                for (var k=0; k<array.length; k++) {
                    if (array[k] === id) {
                        array.splice(k, 1);
                        return true;
                    }
                }
                return false;
            }
            Constructor.deleteNode(id);
            $rootScope.selected = Constructor.selected;
            for (var i=0; i<nodes.length; i++) {
                  if (nodes[i].id == id) {
                      nodes.splice(i, 1);
                      break;
                  }
              }
            for (var i=0; i<nodes.length; i++) {
                if (nodes[i].next) {
                    if (findAndDelete(nodes[i].next, id)) return;
                }
                if (nodes[i].parallel) {
                    if (findAndDelete(nodes[i].parallel, id)) return;
                }
                if (nodes[i].exceptional) {
                    if (findAndDelete(nodes[i].exceptional, id)) return;
                }
                if (nodes[i].yes) {
                    if (findAndDelete(nodes[i].yes, id)) return;
                }
                if (nodes[i].no) {
                    if (findAndDelete(nodes[i].no, id)) return;
                }
            }
        }

        $scope.newRequestNode = function() {
            Constructor.nodes.push({
                id: 'rn'+parseInt(Math.random()*500),
                type: "RequestNode",
                plugin: "mock",
                reference: "change me",
                position: {
                    left: 100,
                    top: 100
                },
                next: [],
                parallel: [],
                exceptional: []
            });
        };

        $scope.newSchedulerNode = function() {
            Constructor.nodes.push({
                id: 'rn'+parseInt(Math.random()*500),
                type: "SchedulerNode",
                task: "...",
                action: "...",
                position: {
                    left: 100,
                    top: 100
                },
                next: [],
                parallel: [],
                exceptional: []
            });
        };

        $scope.newExecuteNode = function() {
            Constructor.nodes.push({
                id: 'rn'+parseInt(Math.random()*500),
                type: "ExecuteNode",
                name: "",
                position: {
                    left: 100,
                    top: 100
                },
                next: [],
                parallel: [],
                exceptional: [],
                values: "",
                merge: 'false'
            });
        };

        $scope.newDelayNode = function() {
            Constructor.nodes.push({
                id: 'rn'+parseInt(Math.random()*500),
                type: "DelayNode",
                delay:0,
                position: {
                    left: 100,
                    top: 100
                },
                next: [],
                parallel: [],
                exceptional: []
            });
        };

        $scope.newConditionalNode = function() {
            Constructor.nodes.push({
                id: 'cn'+parseInt(Math.random()*500),
                type: "ConditionalNode",
                condition: "not defined",
                position: {
                    left: 100,
                    top: 100
                },
                yes:[],
                no:[],
                next: [],
                parallel: [],
                exceptional: []
            });
        };

        $scope.$on('$locationChangeStart',function(evt, absNewUrl, absOldUrl) {
            if (absOldUrl.indexOf('#/constructor')>-1) Constructor.destroy();
        });


    }]);

}());