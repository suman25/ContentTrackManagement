
class Task(object):
    def __init__(self, task_name, task_minutes):
        self.task_name = task_name
        if task_minutes.isdigit():
            self.task_minutes = int(task_minutes)
        if task_minutes == 'lightning':
            self.task_minutes = 5
        self.is_scheduled = 0
        