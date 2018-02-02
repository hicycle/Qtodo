import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, QObject

from apscheduler.schedulers.background import BackgroundScheduler

from db import DbOperation
from TaskDialog import TaskDialog
from task import TASK
from RemindDialog import Reminder

sched = BackgroundScheduler()


class Worker(QObject):
    sig_pop = pyqtSignal(TASK)
    finished = pyqtSignal()

    def __init__(self, task):
        super().__init__()
        self.task = task

    def work(self):
        self.sig_pop.emit(self.task)
        self.finished.emit()



class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.tasks = []

        _tasks = DbOperation.queryTask()
        for _task in _tasks:
            self.tasks.append(TASK(_task[0], _task[1], _task[2]))

        self.initUI()

    def initUI(self):
        self.vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        btn_add = QPushButton("ADD")
        hbox1.addWidget(btn_add)
        hbox1.addStretch(1)
        btn_add.clicked.connect(self.addTaskDialog)

        self.vbox.addLayout(hbox1)
        for task in self.tasks:
            self.addTaskUI(task)
        self.setLayout(self.vbox)
        self.setGeometry(1000, 300, 300, 150)
        self.setWindowTitle('Todo')
        # self.show()

        sched.start()
        self.show()
        # sched.print_jobs()

    # Construct UI for task
    def constructTaskUI(self, hbox, task):
        task.checkbox_done = QCheckBox()
        task.label_task_content = QLabel(task.task_content)
        task.label_datetime = QLabel(time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(task.task_date)))
        btn_edit = QPushButton('EDIT')
        btn_edit.setFixedWidth(40)
        btn_del = QPushButton('DEL')
        btn_del.setFixedWidth(40)
        for widget in (task.checkbox_done, task.label_task_content, task.label_datetime, btn_edit, btn_del):
            hbox.addWidget(widget)
        btn_edit.clicked.connect(lambda: self.editTask(task))
        btn_del.clicked.connect(lambda: self.delTask(task))
        task.checkbox_done.stateChanged.connect(lambda: self.doneTask(task))

    # Add Task UI to main window, initial the reminder dialog and schedule job for task
    def addTaskUI(self, task):
        task.hbox = QHBoxLayout()
        self.constructTaskUI(task.hbox, task)
        self.vbox.addLayout(task.hbox)
        task.edit_window = TaskDialog(task)
        task.edit_window.ok_btn_signal.connect(self.editTaskUI)
        task.reminder = Reminder(task.task_content)
        task.reminder.done_btn_signal.connect(lambda: self.doneTask(task))
        task.reminder.snooze_btn_signal.connect(lambda: self.snooze(task))
        task.worker = Worker(task)
        task.thread = QThread()
        task.worker.finished.connect(task.thread.quit)
        task.worker.moveToThread(task.thread)
        task.worker.sig_pop.connect(self.remind)
        self.add_job(task)

    # Pop up dialog to add Task
    def addTaskDialog(self):
        self.taskDialog = TaskDialog()
        self.taskDialog.ok_btn_signal.connect(self.addTask)
        self.taskDialog.show()

    def editTask(self, task):
        task.edit_window.show()

    def delTask(self, task):
        self.removeTaskUI(task)
        dbOp = DbOperation(task)
        dbOp.delTask()
        self.remove_job(task)

    def doneTask(self, task):
        self.removeTaskUI(task)
        dbOp = DbOperation(task)
        dbOp.doneTask()

    def addTask(self, task):
        self.tasks.append(task)
        self.addTaskUI(task)
        # self.taskDialog.destroy() # cause the bug: if add new task, main process won't end after close the main window

    def removeTaskUI(self, task):
        for i in reversed(range(task.hbox.count())):
            task.hbox.itemAt(i).widget().setParent(None)

    # Update UI for task after edit task done.
    def editTaskUI(self, task):
        self.remove_job(task)
        self.add_job(task)
        task.label_task_content.setText(task.task_content)
        task.label_datetime.setText(time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(task.task_date)))

    def add_job(self, task):
        if time.time() < task.task_date:
            task.job = sched.add_job(self.startThread,
                                     'date',
                                     run_date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(task.task_date)),
                                     args=[task])
            sched.print_jobs()

    def remind(self, task):
        task.reminder.show()
        task.thread.quit()

    def snooze(self, task):
        task.task_date += 1800
        self.add_job(task)
        self.editTaskUI(task)
        dbOp = DbOperation(task)
        dbOp.updateTask()
        # print("new date for %d: %s" % (task.taskid, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(task.task_date))))

    def remove_job(self, task):
        if task.job is not None:
            task.job.remove()

    def closeEvent(self, e):
        sched.shutdown()
        # for task in self.tasks:
        #     print('Quit Thread:', task.taskid)
        #     task.thread.quit()
        #     task.thread.wait()

    def startThread(self, task):
        task.thread.started.connect(task.worker.work)
        task.thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = MyApp()
    sys.exit(app.exec_())
