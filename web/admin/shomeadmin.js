(function(){

  var app = angular.module('shomeAdm',['ngAnimate','ngRoute', 'ui-notification']);

  app.config(['$routeProvider',
    function($routeProvider, $locationProvider) {
      $routeProvider.
        when('/main', {
          templateUrl: 'modules/main.html',
          controller: 'OverviewController',
        }).
        when('/constructor/', {
          templateUrl: 'modules/constructor/constructor.html',
          controller: 'ConstructorController'
        }).
        when('/constructor/:scenario', {
          templateUrl: 'modules/constructor/constructor.html',
          controller: 'ConstructorController'
        }).
        when('/scheduler', {
          templateUrl: 'modules/scheduler/scheduler.html',
          controller: 'SchedulerController'
        }).
        when('/scenarios', {
          templateUrl: 'modules/scenarios/scenarios.html',
          controller: 'ScenariosController'
        }).
        when('/system', {
          templateUrl: 'modules/system/system.html',
          controller: 'SystemController'
        }).
        otherwise({
          redirectTo: '/main'
        });
  }]);

  app.filter('capitalize', function(){
    return function(input) {
        return input.charAt(0).toUpperCase()+input.slice(1);
    }
  });

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

  app.service('InfoMessage', ['$rootScope', '$timeout', function($rootScope, $timeout) {

    var type = undefined //message type: ok, info, error
    var timeout;

    var setMessage = function(type, data) {
        if (angular.isDefined(timeout)) $timeout.cancel(timeout);
        service.type = type;
        service.message = data;
        $rootScope.$broadcast('changeMessage');
        timeout = $timeout(function() {
            service.message = undefined;
            service.type = undefined;
            $rootScope.$broadcast('changeMessage');
        }, 4500); //change it in pair with animation
    }

    var service = {
        type: undefined,
        message: '',
        okMessage: function(data) {
            setMessage('ok', data);
        },
        infoMessage: function(data) {
            setMessage('info', data);
        },
        errorMessage: function(data) {
            setMessage('error', data);
        },
        loader: function(data) {
            setMessage('loader', 'processing');
        },
        clear: function() {
            service.message = undefined;
            type = undefined;
            $rootScope.$broadcast('changeMessage');
        }
    }

    return service;

  }]);


  app.controller('InfoMessageController', ['$scope', 'InfoMessage', function($scope, InfoMessage) {

    $scope.$on('changeMessage', function() {
        $scope.message = InfoMessage.message;
        $scope.type = InfoMessage.type;
    });

  }]);


  app.controller('MenuController', ['$scope', '$http', function($scope, $http) {

  }]);

  app.controller('OverviewController', ['$scope', '$http', function($scope, $http) {


  }]);

  /* end */

})();



