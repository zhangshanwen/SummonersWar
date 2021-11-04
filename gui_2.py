import os
import sys
from threading import Thread

from PyQt5.Qt import QUrl, QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QCheckBox
from PyQt5.QtCore import Qt, QTimer, QRect

import common
from app import App
from log import *
from directive import Directive
from code import get_id


class Gui(QWidget):

    def __init__(self):
        super().__init__()

        self.mp4_path = ""
        # self.check_path()

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
        self.add_index = 0
        self.pull_index = 0

        self.directive = Directive()
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(vw)
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        # self.start_record()
        for i in range(7):
            self.playlist.addMedia(
                QMediaContent(QUrl.fromLocalFile(os.path.realpath(f"mp4/com2us/d40359fa7d65473eb172e6bc95bbbaa3/summoners_{i}.mp4")))
            )
        # self.playlist.addMedia(
        #         QMediaContent(QUrl.fromLocalFile(os.path.realpath(f"mp4/com2us/summoners_{i}.mp4")))
        #     )
        self.player.play()
        # timer = QTimer(self)
        # timer.timeout.connect(self.start_record)
        # timer.start()
        # self.start_thread()
        self.last_modify_time = 0
        self.show()

    def run_start_record(self):
        while True:
            # if not self.starting:
            #     continue
            self.directive.screen_record()
            self.directive.pull_record()
            file_name = self.new_file_name(self.pull_index)
            os.renames(self.base_mp4_name, file_name)
            self.pull_index += 1

    def start_thread(self):
        t = Thread(target=self.run_start_record)
        t.start()

    def check_path(self):
        self.mp4_path = os.path.join(common.summoners_mp4_path, get_id())
        if os.path.exists(self.mp4_path):
            return
        os.makedirs(self.mp4_path)

    @property
    def base_mp4_name(self):
        return common.summoners_base_mp4_name + ".mp4"

    @staticmethod
    def get_mp4_name(*args):
        name = "".join(args)
        return name + ".mp4"

    def new_file_name(self, index):
        new_name = self.get_mp4_name(common.summoners_base_mp4_name, f"_{index}")
        new_path = os.path.join(self.mp4_path, new_name)
        return new_path

    def start_record(self):
        file_name = self.new_file_name(self.add_index)
        if not os.path.exists(file_name):
            return
        self.playlist.addMedia(
            QMediaContent(QUrl.fromLocalFile(os.path.realpath(file_name)))
        )
        if self.player.state() != 1:
            self.playlist.setCurrentIndex(self.add_index)
            self.player.play()
        self.add_index += 1

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
