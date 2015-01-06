(function() {
    angular.module('shomeAdm')
    .service('Constructor', ['$rootScope', '$http', function($rootScope, $http) {

        var instance = null;

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

        /* endpoints variables */
        var radius = 4;

        /* StartNode */
        var initStartNode = function(scope, element, attrs, model) {
            /* Bottom endpoint */
            var bottom = instance.addEndpoint(element, {
                endpoint: ["Dot", {radius:radius}],
                anchor:["Bottom"],
                maxConnections:-1
            });
            /* not supported yet
                var left = instance.addEndpoint(element, {
                    endpoint: ["Dot", {radius:radius}],
                    anchor:["Left"],
                    maxConnections:-1
                });
                var right = instance.addEndpoint(element, {
                    endpoint: ["Dot", {radius:radius}],
                    anchor:["Right"],
                    maxConnections:-1
                });
                var err = instance.addEndpoint(element, {
                    endpoint: ["Dot", {
                    radius:radius}],
                    anchor:[0.8,1,1,1],
                    paintStyle:{ fillStyle:"#e66" },
                    maxConnections:-1
                });
            */
            service.start = {};
            service.start.position = {};
            service.start.position.left = parseInt(angular.element("start-node").css("left").slice(0,-2));
            service.start.position.right = service.start.position.left
                                              + parseInt(angular.element("start-node").css("width").slice(0,-2));
            service.endpoints.push({id: attrs.cid, bottom: bottom}); /* left: left, right: right, err: err */
        }

        /* RequestNode */
        var initRequestNode = function(scope, element, attrs, model) {
          /* Top endpoint */
          var top = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchor:["Top"],
              maxConnections:1
          });
          /* Bottom endpoint */
          var bottom = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchor:["Bottom"],
              maxConnections:-1
          });
          var left = instance.addEndpoint(element, {
            endpoint: ["Dot", {
              radius:radius}],
              anchor:["Left"],
              maxConnections:-1
          });
          var right = instance.addEndpoint(element, {
            endpoint: ["Dot", {
              radius:radius}],
              anchor:["Right"],
              maxConnections:-1
          });
          /* Exceptional endpoint */
          var err = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
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
              radius:radius}],
              anchors:[0.5, 0, 0, -1],
              maxConnections:1
          });
          /*...*/
          var left = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchors:[0.03, 0.5, -1, 0],
              maxConnections:-1
          });
          var right = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchors:[0.97, 0.5, 0, -1],
              maxConnections:-1
          });
          var bottom = instance.addEndpoint(element, {
            endpoint: ["Dot", {
            radius:radius}],
            anchors:[0.5, 1, 0, 1],
            maxConnections:-1
          });
          /*Exceptional endpoint*/
          var err = instance.addEndpoint(element, {
            endpoint: ["Dot", {
            radius:radius}],
            anchors:[0.75, 0.75, 0, 1],
            paintStyle:{ fillStyle:"#e66" },
            maxConnections:-1
          });
          //problem with add one connection twice
          service.endpoints.push({id: attrs.cid, top: top, bottom: bottom, left: left, right: right, err: err});
        }

        /* DelayNode */
        var initDelayNode = function(scope, element, attrs, model) {
          /* Top endpoint */
          var top = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchor:["Top"],
              maxConnections:1
          });
          /* Bottom endpoint */
          var bottom = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchor:["Bottom"],
              maxConnections:-1
          });
          var left = instance.addEndpoint(element, {
            endpoint: ["Dot", {
              radius:radius}],
              anchor:["Left"],
              maxConnections:-1
          });
          var right = instance.addEndpoint(element, {
            endpoint: ["Dot", {
              radius:radius}],
              anchor:["Right"],
              maxConnections:-1
          });
          /* Exceptional endpoint */
          var err = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchor:[0.85,0.85,1,1],
              paintStyle:{ fillStyle:"#e66" },
              maxConnections:-1
          });

          service.endpoints.push({id: attrs.cid, top: top, left: left, right: right, bottom: bottom, err: err});
        }

        var service =  {
          name: null,
          instance: instance,
          nodes: [],
          endpoints: [],
          selected: null,
          /* initialize process */
          initNode: function(scope, element, attrs, model, type) {
            if (type==='RequestNode') {
                initRequestNode(scope, element, attrs, model);
            } else if (type==='StartNode') {
                initStartNode(scope, element, attrs, model);
            } else if (type==='ConditionalNode') {
                initConditionalNode(scope, element, attrs, model);
            } else if (type==='SchedulerNode') {
                initRequestNode(scope, element, attrs, model);
            } else if (type==='ExecuteNode') {
                initRequestNode(scope, element, attrs, model);
            } else if (type==='DelayNode') {
                initDelayNode(scope, element, attrs, model);
            } else {
                return new Error('Unknown node type');
            }
            if (type!=='Start') {
                service.bindNodeEvents(scope, element, attrs, model);
            }
          },
          bindNodeEvents: function(scope, element, attrs, model) {
            scope.node.dimension = {};
            scope.node.dimension.width = parseInt(element.css("width").slice(0,-2));
            scope.node.dimension.height = parseInt(element.css("height").slice(0,-2));
            instance.draggable(element,
            {
              containment: 'parent',
              drag: function() {
              },
              stop: function() {
                scope.node.position.left = parseInt(element.css("left").slice(0,-2));
                scope.node.position.top = parseInt(element.css("top").slice(0,-2));
                if (element[0].tagName==='CONDITIONAL-NODE' || element[0].tagName==='DELAY-NODE') element.click();
                scope.$apply();
              }
            });

            scope.$watchCollection('node.position', function(value) {
              if (model.$viewValue.position) {
                  element.css("left", model.$viewValue.position.left);
                  element.css("top", model.$viewValue.position.top);
                  service.repaint();
              }
            });

            /*
            scope.$watchCollection('node.next',function () {
              var id = attrs.cid;
              var cur = nodeById(id);
              var src = endpointsById(id).bottom;
            });
            */
          },
          connect: function(scope, element, attrs, model) {
              var selected = service.selected ? service.selected.id : null;
              var curid = attrs.cid;
              /* first clicked - select it */
              if (!selected) {
                  service.selected = nodeById(curid);
                  service.selected.active = true;
              /* click on already selected - unselect */
              } else if ( selected === curid ) {
                service.selected.active = false; /* run digest cycle */
                service.selected = null;
              /* two different nodes */
              } else {
                var sel = service.selected;
                var cur = nodeById(curid);
                /* start node processing */
                if (sel.type === 'StartNode' || cur.type === 'StartNode') {
                    if (sel.type === 'StartNode') {
                        var start = sel;
                        var node = cur;
                    } else {
                        var start = cur;
                        var node = sel;
                    }
                    var sl = service.start.position.left;
                    var sr = service.start.position.right;
                    var nl = node.position.left;
                    var nr = node.position.left+node.dimension.width;
                    if (nr > sl && nl < sr) {
                        start.next.push(node.id);
                    } else {
                        start.parallel.push(node.id);
                    }
                } else {
                    var fh = cur.dimension.height;
                    var fw = cur.dimension.width;
                    var sh = sel.dimension.height;
                    var sw = sel.dimension.width;
                    //selected first
                    var ft = cur.position.top;
                    var fl = cur.position.left;
                    var fb = ft + fh;
                    var fr = fl + fw;
                    //selected second
                    var st = sel.position.top;
                    var sl = sel.position.left;
                    var sb = st + sh;
                    var sr = sl + sw;
                    //swap elements if the first element above than the second.
                    if (fb > st) {
                        var t;
                        t = ft; ft = st; st = t;
                        t = fl; fl = sl; sl = t;
                        t = fb; fb = sb; sb = t;
                        t = fr; fr = sr; sr = t;
                        t = curid; curid = selected; selected = t;
                    }
                    if (fr < sl || fl > sr) {
                        cur.parallel.push(selected);
                    } else {
                        cur.next.push(selected);
                    }
                }
                sel.active = false;
                cur.active = false;
                service.selected = null;
                instance.detachEveryConnection();
                service.drawAllConnections();
              }
          },
          drawConnection: function(e1, e2) {
            instance.connect({
              source: e1,
              target: e2,
              connector: [ "Bezier", { curviness:60 } ],
              paintStyle:{ lineWidth:3, strokeStyle:'#456' }
            });
          },
          drawElementConnections: function(id) {
            node = nodeById(id);
            angular.forEach(node.next, function(nextnode) {
              curep = endpointsById(node.id).bottom;
              nextep = endpointsById(nextnode).top;
              service.drawConnection(curep, nextep);
            });
            angular.forEach(node.parallel, function(prlnode) {
                curep = endpointsById(node.id).right;
                prlep = endpointsById(prlnode).top;
                service.drawConnection(curep, prlep);
            });
            angular.forEach(node.yes, function(yesnode) {
                curep = endpointsById(node.id).right;
                yesep = endpointsById(yesnode).top;
                service.drawConnection(yesep, curep);
            });
            angular.forEach(node.no, function(nonode) {
                curep = endpointsById(node.id).left;
                noep = endpointsById(nonode).top;
                service.drawConnection(curep, noep);
            });
          },
          drawAllConnections: function() {
              angular.forEach(service.nodes, function(node) {
                  angular.forEach(node.next, function(nextnode) {
                       curep = endpointsById(node.id).bottom;
                       nextep = endpointsById(nextnode).top;
                       service.drawConnection(curep, nextep);
                  });
                  angular.forEach(node.parallel, function(prlnode) {
                      curep = endpointsById(node.id).right;
                      prlep = endpointsById(prlnode).top;
                      service.drawConnection(curep, prlep);
                  });
                  angular.forEach(node.yes, function(yesnode) {
                      curep = endpointsById(node.id).right;
                      yesep = endpointsById(yesnode).top;
                      service.drawConnection(yesep, curep);
                  });
                  angular.forEach(node.no, function(nonode) {
                      curep = endpointsById(node.id).left;
                      noep = endpointsById(nonode).top;
                      service.drawConnection(curep, noep);
                  });
                });
              },
              hasEndpoints: function(id) {
                  return endpointsById(id) === undefined ? false : true;
              },
              deleteNode: function(id) {
                  if (service.selected.id == id) {
                      service.selected = null;
                  }
                  var eps = service.endpoints;
                  for (var i=0; i<eps.length; i++) {
                      if (eps[i].id === id) {
                           angular.forEach(eps[i], function(ep) {
                               instance.deleteEndpoint(ep);
                           });
                           eps.splice(i, 1);
                           service.repaint();
                           return;
                      }
                  }
              },
              repaint: function() {
                  instance.repaintEverything();
              },
              init: function() {
                  instance = jsPlumb.getInstance({Container: "workspace"});
              },
              destroy: function() {
                  service.endpoints = [];
                  instance.reset();
              }
          }

        return service;
    }]);

}());