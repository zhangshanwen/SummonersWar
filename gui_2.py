import os.path
import sys
from PyQt5.Qt import QUrl, QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

import sys
import time

from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QCheckBox, QLabel
from PyQt5.QtCore import QCoreApplication, Qt, QTimer, QRect
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from threading import Thread
import common
from app import App
from threading import Thread
from log import *
from directive import Directive


class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.buy_power_tag = True
        self.sell_rune_tag = True
        self.email_power_tag = True

        self.app = None

        self.img = common.summoners_base_img

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
        self.btn_start.setGeometry(0, 0, 100, 100)
        self.btn_start.clicked.connect(self.start_click)
        self.btn_start.move(320, 20)
        vw = QVideoWidget(self)  # 定义视频显示的widget
        vw.setGeometry(QRect(100, 200, 600, 270))
        self.directive = Directive()
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(vw)

        self.last_modify_time = 0
        self.start_thread()
        self.update_image()
        timer = QTimer(self)
        timer.timeout.connect(self.update_image)
        timer.start(500)
        self.show()

    def start_thread(self):
        t = Thread(target=self.start_record)
        t.start()

    def start_record(self):
        while True:
            self.directive.screen_record()
            self.directive.pull_record()

    def update_image(self):
        if not os.path.exists("demo.mp4"):
            return
        try:
            if self.last_modify_time >= os.path.getmtime(common.summoners_base_mp4):
                return
            self.last_modify_time = os.path.getmtime(common.summoners_base_mp4)
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.realpath(common.summoners_base_mp4))))
            self.player.play()
        except Exception as e:
            warning(e)

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
    w.resize(800, 500)
    sys.exit(app.exec_())
