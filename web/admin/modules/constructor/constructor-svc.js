(function() {
    angular.module('shomeAdm')
    .service('Constructor', ['$rootScope', '$http', function($rootScope, $http) {

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
        var radius = 4;
        var initRequestNode = function(scope, element, attrs, model) {
          /* Top endpoint */
          var top = instance.addEndpoint(element, {
              endpoint: ["Dot", {
              radius:radius}],
              anchor:[0.5, 0, 0, -1],
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
              anchors:[0.97, 0.5, 1, 0],
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
                fh = parseInt(element.css("height").slice(0,-2));
                fw = parseInt(element.css("width").slice(0,-2));
                sh = parseInt(angular.element('[cid="'+selected+'"]').css("height").slice(0,-2));
                sw = parseInt(angular.element('[cid="'+selected+'"]').css("width").slice(0,-2));
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
                if (fr < sl || fl > sr) {
                  nodeById(curid).parallel.push(selected);
                } else {
                  nodeById(curid).next.push(selected);
                }
                instance.detachEveryConnection();
                service.drawAllConnections();
                service.selected = null;
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
            console.log('id: '+id, node);
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
}());