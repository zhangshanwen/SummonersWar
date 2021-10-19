import platform
import time

import common
from log import *
from directive import Directive
from image import Image


class App:
    def __init__(self):
        self.directive = Directive()
        self.image = Image(directive=self.directive)
        self.run_tag = True
        self.buy_power_tag = True

    def click(self):
        self.directive.click()

    def do_script(self, func):
        while self.run_tag:
            info_start("脚本正在执行")
            func()
            time.sleep(1)

    def buy_power(self):
        pass

    def dragon(self):
        if self.image.find_continuous_fight():
            self.click()
        elif self.image.find_once_again():
            # TODO 出售符文,自动购买体力
            self.click()

    def bloody_palace(self):
        self.directive.get_screenshot()
        if self.image.find_start_fight():
            self.click()
        elif self.image.find_play():
            self.click()
        elif self.image.find_confirm():
            self.click()
        elif self.image.find_next_floor():
            self.click()
        elif self.image.find_victory():
            self.click()

    def run_script(self):
        info_start("开始检查当前页面")
        if self.image.find_dragon():
            self.do_script(self.dragon)
        elif self.image.find_bloody_palace():
            self.do_script(self.bloody_palace)

        else:
            warning("无法识别当前页面")

    def run(self):
        info_start("程序开始启动")
        self.run_script()


if __name__ == '__main__':
    app = App()
    app.do_script(app.bloody_palace)
