from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QTime, pyqtSignal
import time
from task import TASK
from db import DbOperation


class TaskDialog(QWidget):

    ok_btn_signal = pyqtSignal(TASK)

    def __init__(self, task=None):
        super().__init__()
        self.task = task

        self.initUI()

    def initUI(self):
        self.input_task_content = QLineEdit()
        self.input_date = QDateEdit(QDate.currentDate())
        self.input_time = QTimeEdit(QTime.currentTime())

        if self.task is not None:
            self.input_task_content.setText(self.task.task_content)
            self.input_date.setDate(QDate.fromString(time.strftime(
                "%Y-%m-%d", time.localtime(self.task.task_date)), 'yyyy-MM-dd'))
            self.input_time.setTime(QTime.fromString(time.strftime(
                "%H:%M:%S", time.localtime(self.task.task_date)), 'hh:mm:ss'))
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Task:"))
        hbox1.addWidget(self.input_task_content)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Date:"))
        hbox2.addWidget(self.input_date)
        hbox2.addWidget(self.input_time)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(okButton)
        hbox3.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Task')

        okButton.clicked.connect(self.ok)
        cancelButton.clicked.connect(self.close)

    def ok(self):
        _date = self.input_date.date().toPyDate()
        _time = self.input_time.time().toPyTime()
        _task_content = self.input_task_content.text()
        _task_date = time.mktime(
            (_date.year, _date.month, _date.day, _time.hour, _time.minute, _time.second, 0, 0, 0))
        if self.task is None:
            DbOperation.addTask(_task_content, _task_date)
            _task = DbOperation.queryNewTask()
            self.task = TASK(_task[0], _task[1], _task[2])
        else:
            self.task.task_content = _task_content
            self.task.task_date = _task_date
            dbOp = DbOperation(self.task)
            dbOp.updateTask()
        self.ok_btn_signal.emit(self.task)
        self.close()

    def cancel(self):
        self.close()

    def closeEvent(self, e):
        pass


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = TaskDialog()
#     ex.show()
#     sys.exit(app.exec_())
