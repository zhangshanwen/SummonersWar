import sys

from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QCheckBox
from PyQt5.QtCore import QCoreApplication, Qt


class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.buy_power_tag = False
        self.shell_rune_tag = False

        self.starting = False

        self.cb_power = QCheckBox('自动购买体力', self)
        self.cb_power.move(20, 20)
        self.cb_power.toggle()
        self.cb_power.stateChanged.connect(self.change_buy_power)

        self.btn_start = QPushButton('开始', self)
        self.btn_start.clicked.connect(self.start_click)
        self.btn_start.move(170, 340)

        self.show()

    def start_click(self):
        if self.starting:
            self.btn_start.setText("停止")
        else:
            self.btn_start.setText("开始")
        self.starting = not self.starting

    def change_buy_power(self, state):
        if state == Qt.Checked:
            self.buy_power_tag = True
        else:
            self.buy_power_tag = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Gui()
    w.resize(400, 400)
    sys.exit(app.exec_())
