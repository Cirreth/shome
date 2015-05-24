(function() {

    var app = angular.module('shomeAdm');

    app.filter('schemeRepr', function() {
        return function(value) {
            if (!value) return 'Undefined?';
            if (value.interval) return value.interval + ' s.';
        }
    });

    app.controller('SchedulerController', ['$scope', '$http', 'Notification', function($scope, $http, Notification) {

    $scope.mode = undefined;

    $scope.load = function() {
        $http.get('/admin/scheduler/tasks')
        .success(function(data){
            $scope.tasks = data.tasks;
        });
    }

    $scope.load();

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

    function endEditing() {
        $scope.mode = undefined;
        $scope.editing = undefined;
    }

    $scope.delete = function() {
        $scope.mode = 'delete';
    }

    $scope.updateTaskStatus = function(task) {
        $http.put('/admin/scheduler/task/'+task.name,
            {
                enabled: task.enabled
            })
            .success(function() {
                Notification.success(task.name+' '+(task.enabled ? 'enabled' : 'disabled'));
            })
            .error(function(data, status){
                Notification.error(status+': '+data);
            }
        );
    }

	$scope.saveTask = function() {
	    if ($scope.mode == 'new') {
	    	$http.post('/admin/scheduler/task/'+$scope.editing.name, $scope.editing)
	    	.success(function() {
                Notification.success($scope.editing.name+' saved');
                endEditing();
	    	    $scope.load();
	    	})
	    	.error(function(data, status){
                Notification.error(status+': '+data);
	    	});
	    } else if ($scope.mode == 'delete') {
            $http.delete('/admin/scheduler/task/'+$scope.editing.name)
	    	.success(function(data) {
	    	    Notification.success('Deleted successfully');
                for (var i=0; i<$scope.tasks.length; i++) {
                    if ($scope.tasks[i].title == $scope.editing.name) {
                        delete $scope.tasks[i];
                        break;
                    }
                }
                endEditing();
                $scope.load();
	    	})
	    	.error(function(data, status){
                Notification.error(status+': '+data);
	    	});
	    } else {
            $http.put('/admin/scheduler/task/'+$scope.editing.name, $scope.editing)
	    	.success(function() {
	    	    Notification.success($scope.editing.name+' updated');
                endEditing();
                $scope.load();
	    	})
	    	.error(function(data, status){
                Notification.error(status+': '+data);
	    	});
        }
	}

	$scope.cancel = function(task) {
        if ($scope.mode == 'edit') {
            for (var i=0; i<$scope.tasks.length; i++) {
                if ($scope.tasks[i].title == task.name) {
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
            scheme: null,
            enabled: false
		}
	}

  }]);

}());