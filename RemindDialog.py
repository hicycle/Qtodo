from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt


class Reminder(QWidget):
    done_btn_signal = pyqtSignal()
    snooze_btn_signal = pyqtSignal()

    def __init__(self, task_content):
        super().__init__()
        self.task = task_content
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.initUI()

    def initUI(self):
        doneButton = QPushButton("Done")
        snoozeButton = QPushButton("Snooze")

        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel(self.task))

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(doneButton)
        hbox3.addWidget(snoozeButton)

        vbox = QVBoxLayout()
        # vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)

        self.setGeometry(1000, 600, 300, 100)
        self.setWindowTitle('Reminder')

        doneButton.clicked.connect(self.done)
        snoozeButton.clicked.connect(self.snooze)

    def done(self):
        self.done_btn_signal.emit()
        self.close()

    def snooze(self):
        self.snooze_btn_signal.emit()
        self.close()
