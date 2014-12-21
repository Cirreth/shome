(function(){

  var app = angular.module('shomeAdm',['ngAnimate','ngRoute']);

  app.filter('capitalize',function(){
    return function(input) {
        return input.charAt(0).toUpperCase()+input.slice(1);
    };
  });

  app.config(['$routeProvider',
    function($routeProvider) {
      $routeProvider.
        when('/main', {
          templateUrl: 'modules/main.html',
          controller: 'OverviewController',
        }).
        when('/constructor', {
          templateUrl: 'modules/constructor.html',
          controller: 'ConstructorController'
        }).
        when('/scheduler', {
          templateUrl: 'modules/scheduler.html',
          controller: 'SchedulerController'
        }).
        when('/scenarios', {
          templateUrl: 'modules/scenarios.html',
          controller: 'ScenariosController'
        }).
        otherwise({
          redirectTo: '/main'
        });
  }]);

  app.directive('setFocus', function($timeout) {
    return {
      scope: { trigger: '@setFocus' },
      link: function(scope, element) {
        scope.$watch('trigger', function(value) {
          if(value === "true") { 
            $timeout(function() {
              element[0].focus(); 
            });
          }
        });
      }
    };
  });

  app.controller('MenuController', ['$scope', '$http', function($scope, $http) {


  }]);


  app.controller('OverviewController', ['$scope', '$http', function($scope, $http) {


  }]);
  
  
  app.service('Constructor', ['$rootScope', '$http', function($rootScope, $http) {
  
    var instance = jsPlumb.getInstance({Container: "workspace"});
    
    
    var nodeById =  function(id){
      for (i=0; i<service.nodes.length; i++) {
        if (service.nodes[i].id === id) return service.nodes[i];
      }
    }
      
    var endpointsById = function(id) {
      for (i=0; i<service.endpoints.length; i++) {
        if (service.endpoints[i].id === id) return service.endpoints[i];
      }
    };
    
    /* RequestNode */
    var initRequestNode = function(scope, element, attrs, model) {
      /* Top endpoint */
      var top = instance.addEndpoint(element, {
	      endpoint: ["Dot", {
	      radius:5}],
	      anchor:["Top"],
	      maxConnections:1
      });
      /* Bottom endpoint */
      var bottom = instance.addEndpoint(element, {
	      endpoint: ["Dot", {
	      radius:5}],
	      anchor:["Bottom"],
	      maxConnections:-1
      });
      var left = instance.addEndpoint(element, {
        endpoint: ["Dot", {
	      radius:5}],
	      anchor:["Left"],
	      maxConnections:-1
      });
      var right = instance.addEndpoint(element, {
        endpoint: ["Dot", {
	      radius:5}],
	      anchor:["Right"],
	      maxConnections:-1
      });
      /* Exceptional endpoint */
      var err = instance.addEndpoint(element, {
	      endpoint: ["Dot", {
	      radius:5}],
	      anchor:[0.9,1,1,1],
	      paintStyle:{ fillStyle:"#e66" },
	      maxConnections:-1
      });

      service.endpoints.push({id: attrs.cid, top: top, left: left, right: right, bottom: bottom, err: err});
    }

    /*
	    ConditionalNode
    */
    var initConditionalNode = function(scope, element, attrs, model) {
      /*Top endpoint*/
      var top = instance.addEndpoint(element, {
	      endpoint: ["Dot", {
	      radius:5}],
	      anchors:[0.5, 0, 0, -1],
	      maxConnections:1
      });
      /*...*/
      var left = instance.addEndpoint(element, {
	      endpoint: ["Dot", {
	      radius:5}],
	      anchors:[0.03, 0.5, -1, 1],
	      maxConnections:-1
      });
      var right = instance.addEndpoint(element, {
	      endpoint: ["Dot", {
	      radius:5}],
	      anchors:[0.97, 0.5, 1, 1],
	      maxConnections:-1
      });
      var bottom = instance.addEndpoint(element, {
        endpoint: ["Dot", {
        radius:5}],
        anchors:[0.5, 1, 0, 1],
        maxConnections:-1
      });
      /*Exceptional endpoint*/
      var err = instance.addEndpoint(element, {
        endpoint: ["Dot", {
        radius:5}],
        anchors:[0.75, 0.75, 0, 1],
        paintStyle:{ fillStyle:"#e66" },
        maxConnections:-1
      });
      //problem with add one connection twice
      service.endpoints.push({id: attrs.cid, top: top, bottom: bottom, left: left, right: right, err: err});
    }
    
    var service =  {
      name: null,
      instance: instance,
      nodes: [],
      endpoints: [],
      selected: null,
      /* initialize process */
      initNode: function(scope, element, attrs, model, type) {
        if (type==='R') {
          initRequestNode(scope, element, attrs, model);
        } else if (type==='C') {
          initConditionalNode(scope, element, attrs, model);
        } else {
          return new Error('Unknown node type');
        }
        service.bindNodeEvents(scope, element, attrs, model);
      },
      bindNodeEvents: function(scope, element, attrs, model) {
        instance.draggable(element,
        {
          containment: 'parent',
          //view -> model binding
          drag: function() {
          },
          stop: function() {
            scope.node.position.left = parseInt(element.css("left").slice(0,-2));
            scope.node.position.top = parseInt(element.css("top").slice(0,-2)); 
            if (element[0].tagName==='CONDITIONAL-NODE') element.click();
            scope.$apply();
          }
        });
        
        //model -> view binding
        scope.$watchCollection('node.position', function(value) {
          element.css("left", model.$viewValue.position.left);
          element.css("top", model.$viewValue.position.top);
          service.repaint();
        });
        
        scope.$watchCollection('node.next',function () {
          var id = attrs.cid;
          var cur = nodeById(id);
          var src = endpointsById(id).bottom;
        });
      },
      connect: function(scope, element, attrs, model) {
          var selected = service.selected;
          var curid = attrs.cid; //current element id
          if (!selected) {
            service.selected = curid;
   	        nodeById(service.selected).active = true;
          } else if (selected==curid) {
            nodeById(service.selected).active = false;
            service.selected = null;
          } else {
            //Constructor.selected
            nodeById(selected).active = false;
            nodeById(curid).active = false;
            request_node_height = 65;
            request_node_width = 180;
            fh = element.css("height");
            fw = element.css("width");
            sh = angular.element('[cid="'+selected+'"]').css("height");
            sw = angular.element('[cid="'+selected+'"]').css("width");
            console.log('fw:'+fw, 'fh:'+fh, 'sh:'+sh, 'sw:'+sw); 
            //
            //selected first
            ft = nodeById(curid).position.top;
            fl = nodeById(curid).position.left;
            fb = ft + fh;
            fr = fl + fw;
            //selected second
            st = nodeById(selected).position.top;
            sl = nodeById(selected).position.left;
            sb = st + sh;
            sr = sl + sw;
            //swap elements if the first element above than the second.
            if (fb > st) {
              var t;
              t = ft; ft = st; st = t;
              t = fl; fl = sl; sl = t;
              t = fb; fb = sb; sb = t;
              t = fr; fr = sr; sr = t;
              t = curid; curid = selected; selected = t;
            }
            /*
            if (fr < sl || fl > sr) {
              service.nodeById(curid).parallel.push(selected);
              //#
                start = service.endpointsById(curid);
                end = service.endpointsById(selected);
                //service.drawConnection(start.left,end.top);
              //#
            } else {
            */
            nodeById(curid).next.push(selected);
            instance.detachEveryConnection();
            service.drawAllConnections();
            //}
            service.selected = null;
          }
      },
      drawConnection: function(e1, e2) {
        instance.connect({
          source: e1,
          target: e2,
          connector: [ "Bezier", { curviness:40 } ],
          paintStyle:{ lineWidth:3, strokeStyle:'#456' }
        });
      },
      drawElementConnections: function(id) {
        node = nodeById(id);
        console.log('id: '+id, node);
        angular.forEach(node.next, function(nextnode) {
          curep = endpointsById(node.id).bottom;
          nextep = endpointsById(nextnode).top;
          service.drawConnection(curep, nextep);
        });
      },
      drawAllConnections: function() {
        angular.forEach(service.nodes, function(node) {
          angular.forEach(node.next, function(nextnode) {
            curep = endpointsById(node.id).bottom;
            nextep = endpointsById(nextnode).top;
            service.drawConnection(curep, nextep);
          });
        });
      },
      hasEndpoints: function(id) {
        return endpointsById(id) === undefined ? false : true;
      },
      /* post process definition to server */
      saveProcess: function() {
        console.log('not implemented');
      },
      repaint: function() {
        instance.repaintEverything();
      },
      destroy: function() {
        instance.reset();
      }
    }
    
    return service;
}]);
  
  app.controller('ConstructorController', ['$scope', '$http', '$interval', 'Constructor', function($scope, $http, $interval, Constructor) {
	  
	  $scope.init = function() {
	    console.log('init');
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
        "expectional": []
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
        "expectional": []
      });
	  };

    $scope.$on('$locationChangeStart',function(evt, absNewUrl, absOldUrl) {
      if (absOldUrl.indexOf('#/constructor')>-1) {
        Constructor.destroy();
      }
    });

  }]);

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

  /* end */

  app.controller('ScenariosController', ['$scope', '$http', function($scope, $http) {

    $http.get('./data-examples/scenarios.json')
            .success(function(data){
                $scope.scenarios = data;
            });
  }]);

  app.controller('SchedulerController', ['$scope', '$http', function($scope, $http) {
    //$scope.editing = false;
    $scope.mode = undefined;
    $http.get('http://localhost:8082/admin/scheduler/tasks')
    .success(function(data){
        $scope.tasks = data;
    });

    $scope.startScheduling = function(){
      $scope.schemeconfig = true;
    }

    $scope.stopScheduling = function(){
      $scope.schemeconfig = false;
    }

    $scope.edit = function(task) {
        $scope.oldtask = {};
        angular.copy(task, $scope.oldtask);
        $scope.mode = 'edit';
        $scope.editing = task;
    }

    $scope.newTask = function() {
        $scope.editing = getNewTask();
        $scope.mode='new';
    }

	$scope.saveTask = function() {
	    if ($scope.mode == 'new') {
	    	$scope.tasks.push($scope.editing);
        }
        $scope.mode = undefined;
        $scope.editing = undefined;
	}

	$scope.cancel = function(task) {
        if ($scope.mode == 'edit') {
            for (var i=0; i<$scope.tasks.length; i++) {
                if ($scope.tasks[i].title == task.title) {
                    $scope.tasks[i] = $scope.oldtask;
                }
            }
            $scope.oldtask = undefined;
        }
        $scope.editing = undefined;
        $scope.mode = undefined;
	}
	
	function getNewTask() {
        return {
            title: "",
            description: "",
            process: "",
            type: "",
            schema: null,
            isrunned: false
		}
	}

  }]);

   

})();



