from core.entities.Task import Task


class Scheduler:

    def __init__(self, action_processor):
        self._action_processor = action_processor
        Task._action_processor = action_processor
        self._tasks = {task.name: task for task in Task.get_all()}

    def start_task(self, name):
        if name in self._tasks:
            return self._tasks[name].start()
        else:
            raise Exception('There is no task with name '+name)

    def stop_task(self, name):
        if name in self._tasks:
            return self._tasks[name].stop()
        else:
            raise Exception('There is no task with name '+name)

    def get_task(self, name):
        if name in self._tasks:
            return self._tasks[name].dict_repr()
        else:
            raise Exception('There is no task with name '+name)

    def list_all(self):
        return [task.dict_repr() for task in self._tasks.values()]