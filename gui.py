import sys
import time

from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QCheckBox
from PyQt5.QtCore import QCoreApplication, Qt
from app import App
from threading import Thread


class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.buy_power_tag = True
        self.sell_rune_tag = True
        self.email_power_tag = True

        self.app = None

        self.starting = False

        self.cb_power = QCheckBox('自动红心购买体力', self)
        self.cb_power.move(20, 20)
        self.cb_power.toggle()
        self.cb_power.stateChanged.connect(self.change_buy_power)

        self.cb_power = QCheckBox('自动领取邮箱体力', self)
        self.cb_power.move(20, 60)
        self.cb_power.toggle()
        self.cb_power.stateChanged.connect(self.change_email_power)

        self.cb_power = QCheckBox('自动出售符文', self)
        self.cb_power.move(20, 100)
        self.cb_power.toggle()
        self.cb_power.stateChanged.connect(self.change_shell_rune)

        self.btn_start = QPushButton('开始', self)
        self.btn_start.clicked.connect(self.start_click)
        self.btn_start.move(170, 340)

        self.show()

    def run_app_thread(self):
        if not self.app:
            self.app = App(self.buy_power_tag, self.sell_rune_tag, self.email_power_tag)
        self.app.run_tag = True
        self.app.run()
        self.starting = False
        self.btn_start.setText("开始")

    def start(self):
        t = Thread(target=self.run_app_thread)
        t.start()

    def stop(self):
        self.app.run_tag = False

    def start_click(self):
        if self.starting:
            self.btn_start.setText("开始")
            self.stop()
        else:
            self.btn_start.setText("停止")
            self.start()
        self.starting = not self.starting

    def change_buy_power(self, state):
        if state == Qt.Checked:
            self.buy_power_tag = True
        else:
            self.buy_power_tag = False

    def change_email_power(self, state):
        if state == Qt.Checked:
            self.email_power_tag = True
        else:
            self.email_power_tag = False

    def change_shell_rune(self, state):
        if state == Qt.Checked:
            self.sell_rune_tag = True
        else:
            self.sell_rune_tag = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Gui()
    w.resize(400, 400)
    sys.exit(app.exec_())
