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

        var beforeDetachConnection = function(conn) {
            var src_jpid = conn.sourceId;
            var tgt_jpid = conn.targetId;
            var src = nodeById(angular.element('#'+src_jpid)[0].attributes.cid.value);
            var tgt_id = angular.element('#'+tgt_jpid)[0].attributes.cid.value;
            service.detachConnections(src, tgt_id);
            return true;
        }

        /* endpoints variables */
        var radius = 4;
        var radiusTop = 6;

        /* StartNode */
        var initStartNode = function(scope, element, attrs, model) {
            /* Bottom endpoint */
            var bottom = instance.addEndpoint(element, {
                endpoint: ["Dot", {radius:radius}],
                anchor:["Bottom"],
                maxConnections:-1,
                beforeDetach: beforeDetachConnection
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
              radius:radiusTop}],
              anchor:["Top"],
              maxConnections:1
          });
          /* Bottom endpoint */
          var bottom = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchor:["Bottom"],
              maxConnections:-1,
                beforeDetach: beforeDetachConnection
          });
          var left = instance.addEndpoint(element, {
            endpoint: ["Dot", {
              radius:radius}],
              anchor:["Left"],
              maxConnections:-1,
              beforeDetach: beforeDetachConnection
          });
          var right = instance.addEndpoint(element, {
            endpoint: ["Dot", {
              radius:radius}],
              anchor:["Right"],
              maxConnections:-1,
              beforeDetach: beforeDetachConnection
          });
          /* Exceptional endpoint */
          var err = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchor:[0.9,1,0,1],
              paintStyle:{ fillStyle:"#e66" },
              maxConnections:-1,
              beforeDetach: beforeDetachConnection
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
              radius:radiusTop}],
              anchors:[0.5, 0, 0, -1],
              maxConnections:1
          });
          /*...*/
          var left = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchors:[0.03, 0.5, -1, -1],
              maxConnections:-1,
              beforeDetach: beforeDetachConnection
          });
          var right = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchors:[0.97, 0.5, 1, -1],
              maxConnections:-1,
              beforeDetach: beforeDetachConnection
          });
          var bottom = instance.addEndpoint(element, {
            endpoint: ["Dot", {
            radius:radius}],
            anchors:[0.5, 1, 0, 1],
            maxConnections:-1,
            beforeDetach: beforeDetachConnection
          });
          /*Exceptional endpoint*/
          var err = instance.addEndpoint(element, {
            endpoint: ["Dot", {
            radius:radius}],
            anchors:[0.75, 0.75, 0, 1],
            paintStyle:{ fillStyle:"#e66" },
            maxConnections:-1,
            beforeDetach: beforeDetachConnection
          });
          //problem with add one connection twice
          service.endpoints.push({id: attrs.cid, top: top, bottom: bottom, left: left, right: right, err: err});
        }

        /* DelayNode */
        var initDelayNode = function(scope, element, attrs, model) {
          /* Top endpoint */
          var top = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radiusTop}],
              anchor:["Top"],
              maxConnections:1
          });
          /* Bottom endpoint */
          var bottom = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchor:["Bottom"],
              maxConnections:-1,
              beforeDetach: beforeDetachConnection
          });
          var left = instance.addEndpoint(element, {
            endpoint: ["Dot", {
              radius:radius}],
              anchor:[1, 0.5, -1, -1],
              maxConnections:-1,
              beforeDetach: beforeDetachConnection
          });
          var right = instance.addEndpoint(element, {
            endpoint: ["Dot", {
              radius:radius}],
              anchor:[1, 0.5, 1, -1],
              maxConnections:-1,
              beforeDetach: beforeDetachConnection
          });
          /* Exceptional endpoint */
          var err = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchor:[0.85,0.85,1,1],
              paintStyle:{ fillStyle:"#e66" },
              maxConnections:-1,
              beforeDetach: beforeDetachConnection
          });

          service.endpoints.push({id: attrs.cid, top: top, left: left, right: right, bottom: bottom, err: err});
        }

        var service =  {
          name: undefined,
          instance: instance,
          nodes: [],
          endpoints: [],
          selected: undefined,
          exceptionalMode: false,
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
          },
          connect: function(scope, element, attrs, model) {
              var selected;
              if (service.selected) {
                  if (!service.selected.type) {
                      delete service.selected;
                      return;
                  }
                  selected = service.selected.id;
              }
              var curid = attrs.cid;
              /* first click. Select element */
              if (!selected) {
                  service.selected = nodeById(curid);
                  service.selected.active = true;
              /* click on already selected - unselect */
              } else if ( selected === curid ) {
                  service.selected.active = false; /* run digest cycle */
                  delete service.selected;
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
                      /*if (nr > sl && nl < sr) {*/
                          start.next.push(node.id);
                      /*} else {
                          start.parallel.push(node.id);
                      }*/
                  } else {
                      var sh = sel.dimension.height;
                      var sw = sel.dimension.width;
                      var st = sel.position.top;
                      var sl = sel.position.left;
                      var sb = st + sh;
                      var sr = sl + sw;

                      var ch = cur.dimension.height;
                      var cw = cur.dimension.width;
                      var ct = cur.position.top;
                      var cl = cur.position.left;
                      var cb = ct + ch;
                      var cr = cl + cw;

                      // connection always will be built from top element to bottom element
                      if (cb > st) {
                          var t;
                          t = ct; ct = st; st = t;
                          t = cl; cl = sl; sl = t;
                          t = cb; cb = sb; sb = t;
                          t = cr; cr = sr; sr = t;
                          t = curid; curid = selected; selected = t;
                          t = cur; cur = sel; sel = t;
                      }
                      if (endpointsById(selected).top.connections.length>0) {
                          return;
                      }
                      if (service.exceptionalMode) {
                          cur.exceptional.push(selected);
                      } else {
                          if (cr < sl || cl > sr) {
                              if (cur.type === 'ConditionalNode') {
                                  if (cr < sl) {
                                      cur.yes.push(selected);
                                  } else {
                                      cur.no.push(selected);
                                  }
                              } else {
                                  cur.parallel.push(selected);
                              }
                          } else {
                              cur.next.push(selected);
                          }
                      }
                  }
                  sel.active = false;
                  cur.active = false;
                  delete service.selected;
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
                yesep = endpointsById(yesnode).top
                service.drawConnection(curep, yesep);
            });
            angular.forEach(node.no, function(nonode) {
                curep = endpointsById(node.id).left;
                noep = endpointsById(nonode).top;
                service.drawConnection(curep, noep);
            });
            angular.forEach(node.exceptional, function(excnode) {
                curep = endpointsById(node.id).err;
                excep = endpointsById(excnode).top;
                service.drawConnection(curep, excep);
            });
          },
          drawAllConnections: function() {
              angular.forEach(service.nodes, function(node) {
                  service.drawElementConnections(node.id);
              });
          },
              hasEndpoints: function(id) {
                  return endpointsById(id) === undefined ? false : true;
              },
              detachConnections: function(src, tgt_id) {
                var findAndDelete = function(array, id) {
                    for (var k=0; k<array.length; k++) {
                        if (array[k] === id) {
                            array.splice(k, 1);
                            return true;
                        }
                    }
                    return false;
                }
                if (src.next) {
                    findAndDelete(src.next, tgt_id);
                }
                if (src.parallel) {
                    findAndDelete(src.parallel, tgt_id);
                }
                if (src.exceptional) {
                    findAndDelete(src.exceptional, tgt_id);
                }
                if (src.yes) {
                    findAndDelete(src.yes, tgt_id);
                }
                if (src.no) {
                    findAndDelete(src.no, tgt_id);
                }
                service.drawElementConnections(src.id);
                $rootScope.$apply();
              },
              deleteNode: function(id) {
                  delete service.selected;
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