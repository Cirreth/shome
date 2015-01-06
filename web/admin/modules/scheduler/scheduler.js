(function() {

    angular.module('shomeAdm')
    .controller('SchedulerController', ['$scope', '$http', 'InfoMessage', function($scope, $http, InfoMessage) {

    $scope.im = InfoMessage;

    $scope.mode = undefined;

    $scope.load = function() {
        $http.get('/admin/scheduler/alltasks')
        .success(function(data){
            $scope.tasks = data;
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
        $http.put('/admin/scheduler/task/'+task.title,
            {
                isrunned: !task.isrunned
            })
            .success(function() {
                $scope.im.okMessage(task.title+' '+(task.isrunned ? 'enabled' : 'disabled'));
            })
            .error(function(data, status){
                $scope.im.errorMessage(status+': '+data);
            }
        );
    }

    /*
        {
            title: task.title,
            description: task.description,
            process: task.process,
            type: task.type,
            scheme: task.scheme,
            isrunned: !task.isrunned
        }
    */

	$scope.saveTask = function() {
	    if ($scope.mode == 'new') {
	    	$http.post('/admin/scheduler/task/'+$scope.editing.title, $scope.editing)
	    	.success(function() {
                $scope.im.okMessage($scope.editing.title+' saved');
                endEditing();
	    	    $scope.load();
	    	})
	    	.error(function(data, status){
                $scope.im.errorMessage(status+': '+data);
	    	});
	    } else if ($scope.mode == 'delete') {
            $http.delete('/admin/scheduler/task/'+$scope.editing.title)
	    	.success(function(data) {
	    	    $scope.im.okMessage(data);
                for (var i=0; i<$scope.tasks.length; i++) {
                    if ($scope.tasks[i].title == $scope.editing.title) {
                        delete $scope.tasks[i];
                        break;
                    }
                }
                endEditing();
                $scope.load();
	    	})
	    	.error(function(data, status){
                $scope.im.errorMessage(status+': '+data);
	    	});
	    } else {
            $http.put('/admin/scheduler/task/'+$scope.editing.title, $scope.editing)
	    	.success(function() {
	    	    $scope.im.okMessage($scope.editing.title+' updated');
                endEditing();
                $scope.load();
	    	})
	    	.error(function(data, status){
                $scope.im.errorMessage(status+': '+data);
	    	});
        }
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
            scheme: null,
            isrunned: false
		}
	}

  }]);

}());