import platform
import time

import common
from log import *
from directive import Directive
from image import Image


class App:
    def __init__(self):
        self.directive = Directive()
        self.image = Image()

    def check_page(self, func):
        self.directive.get_screenshot()
        x, y = func()
        if x == y == 0:
            return
        return True

    def do_directive(self, func):
        self.directive.get_screenshot()
        x, y = func()
        if x == y == 0:
            return
        self.directive.click(x, y)

    def check_home_page(self):
        return self.check_page(self.image.find_fight)

    def check_dragon_page(self):
        return self.check_page(self.image.find_dragon)

    def close_main_ad(self):
        self.do_directive(self.image.find_main_close)

    def close_ad(self):
        self.do_directive(self.image.find_ad_close)

    def continuous_fight(self):
        return self.do_directive(self.image.find_continuous_fight)

    def check_continuous_fight(self):
        return self.check_page(self.image.find_continuous_fight)

    def once_again(self):
        return self.do_directive(self.image.find_once_again)

    def check_once_again(self):
        return self.check_page(self.image.find_once_again)

    def dragon_script(self):
        while True:
            time.sleep(1)
            info_start("正在执行")
            if self.check_continuous_fight():
                info_start("开始战斗")
                self.check_continuous_fight()
            if self.check_once_again():
                info("准备再来一次")
                # TODO 如何出售符文
                self.once_again()

    def run_script(self):
        info_start("开始检查当前页面")
        if self.check_dragon_page():
            info("当前页面为:龙之地下城")
            self.dragon_script()

    def run(self):
        info_start("程序开始启动")
        self.run_script()
        # 检查当前应用是否为魔灵召唤
        # if self.directive.check_current_active():
        #     info("当前app为魔灵召唤")
        #     self.run_script()
        #
        # else:
        #     warning("当前app不是魔灵召唤")
        #     self.directive.start_app()
        #     while True:
        #         self.close_ad()
        #         if self.check_home_page():
        #             break


if __name__ == '__main__':
    app = App()
    app.run()
