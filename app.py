import platform
import time

import common
from log import *
from directive import Directive
from image.com2us import Com2usImage


class App:
    def __init__(self, buy_power_tag=True, shell_rune_tag=True, email_power_tag=True):
        self.directive = Directive()
        self.image = Com2usImage(directive=self.directive)
        self.run_tag = True
        self.buy_power_tag = buy_power_tag
        self.shell_rune_tag = shell_rune_tag
        self.email_power_tag = email_power_tag

        self.enough_red_heart = True
        self.enough_email_power = True
        self.no_shelled_rune = True
        self.enough_world_arena_times = True

    def click(self):
        self.directive.click()

    def do_arena(self, func):
        while self.run_tag:
            info_start("脚本正在执行")
            self.directive.get_screenshot()
            func()
            time.sleep(1)
        info("脚本结束")

    def do_script(self, func):
        while self.run_tag:
            info_start("脚本正在执行")
            self.directive.get_screenshot()
            self.check_power()
            func()
            time.sleep(1)
        info("脚本结束")

    def do_dimension(self, func):
        while self.run_tag:
            info_start("次元脚本正在执行")
            self.directive.get_screenshot()
            func()
            time.sleep(1)
        info("脚本结束")

    def red_heart_buy_power(self):
        while True:
            self.directive.get_screenshot()
            if self.image.find_store():
                self.click()
                continue
            if not self.enough_red_heart and self.image.find_store_close():
                self.click()
                break
            elif self.image.find_red_heart_shortage():
                if self.image.find_store_confirm():
                    self.click()
                    self.enough_red_heart = False
            elif self.image.find_five_hundred_red_heart():
                self.click()
            elif self.image.find_store_yes():
                self.click()
            elif self.image.find_store_confirm():
                self.click()
            time.sleep(2)

    def gift_box_power(self):
        is_collect = False
        while True:
            self.directive.get_screenshot()
            if self.image.find_gift_box():
                self.click()
                continue
            if is_collect and self.image.find_main_close():
                self.click()
                break
            elif self.image.find_collect():
                is_collect = True
                self.click()
            else:
                self.enough_email_power = False
                is_collect = True
            time.sleep(2)

    def check_power(self):
        if not self.image.find_energy_shortage():
            return
        info("准备购买体力，优先使用红心")
        if self.buy_power_tag and self.enough_red_heart:
            info("开始使用红心购买体力")
            if self.image.find_store():
                self.click()
                self.red_heart_buy_power()
                return
        elif self.email_power_tag and self.enough_email_power:
            info("开始领取邮箱体力")
            if self.image.find_gift_box():
                self.click()
                self.gift_box_power()
                return
        if self.image.find_main_close():
            self.click()
            info(f"等待{common.dungeon_sleep_time}，补充能量")
            time.sleep(common.dungeon_sleep_time)

    def arena(self):
        # TODO 竞技场
        pass

    def world_arena(self):
        if self.enough_world_arena_times and self.image.find_world_arena_times_less():
            self.enough_world_arena_times = False
        elif self.image.find_store_confirm():
            self.click()
        elif not self.enough_world_arena_times:
            self.run_tag = False
        elif self.image.find_rank_fight():
            self.click()
        elif self.image.find_victory():
            self.click()
        elif self.image.find_failed():
            self.click()
        elif self.image.find_play():
            self.click()
        elif self.image.find_confirm():
            self.click()
        else:
            info(f"休眠{common.world_arena_sleep_time}", "节省数据开销")
            time.sleep(common.world_arena_sleep_time)

    def shell_rune(self):
        is_sell = False
        while True:
            if is_sell and self.image.find_cancel():
                self.click()
                break
            elif self.image.find_yes():
                self.click()
            elif self.image.find_no_sell():
                if self.image.find_store_confirm():
                    self.click()
                    is_sell = True
            elif self.image.find_sell_selected():
                self.click()
            elif self.image.find_sell_selected_confirm():
                self.click()

            self.directive.get_screenshot()

    def dungeon(self):
        if self.image.find_continuous_fight():
            self.click()
            info("开始等待")
        elif self.image.find_yes():
            self.click()
        elif self.image.find_once_again():
            if self.no_shelled_rune and self.shell_rune_tag:
                self.shell_rune()
                self.no_shelled_rune = False
                return
            self.click()
            time.sleep(2)
            self.no_shelled_rune = True
        elif self.image.find_end_continuous_fight():
            info(f"休眠{common.dungeon_sleep_time}", "节省数据开销")
            time.sleep(common.dungeon_sleep_time)

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
            self.do_script(self.dungeon)
        elif self.image.find_bloody_palace():
            self.do_script(self.bloody_palace)
        elif self.image.find_giant_dungeon():
            self.do_script(self.dungeon)
        elif self.image.find_death_dungeon():
            self.do_script(self.dungeon)
        elif self.image.find_world_arena():
            self.do_arena(self.world_arena)
        else:
            warning("无法识别当前页面")

    def run(self):
        info_start("程序开始启动")
        if not self.directive.device_id:
            warning("没有检测到设备")
            return
        self.run_script()


if __name__ == '__main_ _':
    app = App()
    app.run()
    # app.directive.get_screenshot()
    # app.check_power()
    # app.directive.get_screenshot()
    # app.shell_rune()
    # app.world_arena()
    # app.do_script(app.dungeon)
    # app.red_heart_buy_power()
    # app.directive.get_screenshot()
    # app.shell_rune()
