# coding=utf-8


class TASK:

    def __init__(self, taskid, task, date):
        self.taskid = taskid
        self.task_content = task
        self.task_date = date
        self.row = None
        self.label_task_content = None
        self.label_datetime = None
        self.checkbox_done = None
        self.job = None
        self.reminder = None
