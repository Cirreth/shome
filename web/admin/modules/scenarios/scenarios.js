(function() {

    angular.module('shomeAdm')
    .controller('ScenariosController', ['$scope', '$http', 'Notification', 'InfoMessage', function($scope, $http, Notification, InfoMessage) {

        $scope.im = InfoMessage;

        $scope.load = function() {
            $http.get('/admin/scenarios/')
                    .success(function(data){
                        $scope.scenarios = data.scenarios;
                    })
                    .error(function(){
                        Notification.error('Error on scenarios list loading')
                    });
        }

        $scope.load();

        $scope.publish = function(scenario) {
            var initial = scenario.published;
            if (scenario.published) {
                scenario.published = !scenario.published;
            } else {
                scenario.published = true;
            }
            update(scenario, undefined, function() {
                scenario.published = initial;
            });
        }

        $scope.runoninit = function(scenario) {
            var initial = scenario.runoninit;
            if (scenario.runoninit) {
                scenario.runoninit = !scenario.runoninit;
            } else {
                scenario.runoninit = true;
            }
            update(scenario, undefined, function(){
                scenario.runoninit = initial;
            });
        }

        var update = function(scenario, onsuccess, onerror) {
            $scope.im.loader();
            scenario = {
                name: scenario.name,
                description: scenario.description,
                published: scenario.published,
                runoninit: scenario.runoninit
            }
            $http.put('/admin/scenarios/'+scenario.name, scenario)
                    .success(function(data){
                        $scope.im.okMessage(data);
                        if (typeof onsuccess !== "undefined") onsuccess();
                    })
                    .error(function(data, status) {
                        $scope.im.errorMessage(status+': '+data);
                        if (typeof onerror !== "undefined") onerror();
                    });
        }

        $scope.delete = function(tag, accepted) {
            if (!accepted) return;
            $scope.im.loader();
            $http.delete('/admin/scenarios/'+tag)
                .success(function(data) {
                    $scope.im.okMessage(data);
                    $scope.load();
                })
                .error(function(data, status){
                    $scope.im.errorMessage(status+': '+data);
	    	    });
        }


    }]);
}());

