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

    def create_task(self, name, scenario, task_type, scheme, enabled, description=None):
        self._tasks[name] = Task(name=name, scenario=scenario, task_type=task_type, scheme=scheme,
                                 enabled=enabled, description=description)
        self._tasks[name].save()

    def change_task(self, name, description=None, scenario=None, task_type=None, scheme=None, enabled=None):
        task = self._tasks[name]
        task_type = task_type if task_type else task.task_type
        if Task.check_scheme(task_type, scheme):
            task.description = description if description else task.description
            task.scenario = scenario if scenario else task.scenario
            task.task_type = task_type
            task.set_scheme(scheme)
            if enabled is not None:
                if enabled:
                    if not task.enabled:
                        task.start(save=False)
                else:
                    if task.enabled:
                        task.stop(save=False)
            task.enabled = enabled
            task.save()
        else:
            raise Exception('Task type '+task_type+" can't by used with scheme "+str(scheme)+" (task: "+task.name)

    def delete_task(self, name):
        task = self._tasks[name]
        task.delete()
        del self._tasks[name]

    def list_all(self):
        return [task.dict_repr() for task in self._tasks.values()]