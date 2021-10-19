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
        self.enough_red_heart = True
        self.shell_rune_tag = True

    def click(self):
        self.directive.click()

    def do_script(self, func):
        while self.run_tag:
            info_start("脚本正在执行")
            self.directive.get_screenshot()
            self.check_power()
            func()
            time.sleep(1)

    def red_heart_buy_power(self):
        while True:
            self.directive.get_screenshot()
            if self.image.find_store():
                self.click()
            else:
                break

    def check_power(self):
        if self.buy_power_tag and self.image.find_energy_shortage():
            info("准备购买体力，优先使用红心")
            if self.enough_red_heart:
                info("开始使用红心购买体力")
                self.red_heart_buy_power()
            else:
                info("红心不足，使用邮箱体力")

    def arena(self):
        # TODO 竞技场
        pass

    def shell_rune(self):
        if self.image.find_shell_selected():
            self.click()
            time.sleep(1)

    def dragon(self):
        if self.image.find_continuous_fight():
            self.click()
        elif self.image.find_once_again():
            # TODO 出售符文,自动购买体力
            if self.shell_rune_tag:
                self.shell_rune()
            self.click()

    def bloody_palace(self):
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
        self.directive.get_screenshot()
        if self.image.find_dragon_dungeon():
            self.do_script(self.dragon)
        elif self.image.find_bloody_palace():
            self.do_script(self.bloody_palace)
        elif self.image.find_giant_dungeon():
            pass
        elif self.image.find_death_dungeon():
            pass

        else:
            warning("无法识别当前页面")

    def run(self):
        info_start("程序开始启动")
        self.run_script()


if __name__ == '__main__':
    app = App()
    app.run()