import platform
import time

import common
from log import *
from directive import Directive
from image.com2us import Com2usImage

"""
该脚本仅支持1080*1920分辨率
"""
# has_arena_leader 是否有竞技场领袖技能
monsters = {
    "光人鱼": {
    },
    "光鬼": {
    },
    "水仙人": {
        "arena_leader_weight": 1,
    },
    "水前锋": {
        "arena_leader_weight": 4,
    },
    "水华熊": {
        "arena_leader_weight": 3,
    },
    "水御术师": {
        "arena_leader_weight": 3,
    },
    "风滑板": {
        "arena_leader_weight": 5,
    },
    "风画师": {
        "arena_leader_weight": 2,
    },
    "风马桶": {
    },
}

# 世界竞技场上场魔灵(注意越靠前，被选中的几率越大)
world_arena_monsters = [
    "风滑板",
    "水御术师",
    "光人鱼",
    "风画师",
    "水仙人",
    "水前锋",
    "水华熊",
    "风马桶",
    "光鬼",
]
world_arena_monsters_on = []


class App:
    def __init__(self, buy_power_tag=False, shell_rune_tag=True, email_power_tag=True):
        self.directive = Directive()
        self.image = Com2usImage(directive=self.directive)
        self.run_tag = True
        self.buy_power_tag = buy_power_tag
        self.shell_rune_tag = shell_rune_tag
        self.email_power_tag = email_power_tag

        self.enough_red_heart = True
        self.bloody_palace_is_not_auto_fight = True
        self.enough_email_power = True
        self.no_shelled_rune = True
        self.enough_world_arena_times = True

    def click(self):
        self.directive.click()

    # 不检查体力
    def do_no_check_power(self, func):
        while self.run_tag:
            info_start("脚本正在执行")
            self.directive.re_connect()
            self.directive.get_screenshot()
            func()
            time.sleep(1)
        info("脚本结束")

    # 检查体力
    def do_check_power(self, func):
        while self.run_tag:
            info_start("脚本正在执行")
            self.directive.re_connect()
            self.directive.get_screenshot()
            self.check_power()
            func()
            time.sleep(1)
        info("脚本结束")

    def do_dimension(self, func):
        while self.run_tag:
            info_start("次元脚本正在执行")
            self.directive.re_connect()
            self.directive.get_screenshot()
            func()
            time.sleep(1)
        info("脚本结束")

    def red_heart_buy_power(self):
        while self.run_tag:
            self.directive.get_screenshot()
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
        while self.run_tag:
            self.directive.get_screenshot()
            if is_collect and self.image.find_main_close():
                self.click()
                break
            elif self.image.find_collect():
                self.click()
                is_collect = True
            else:
                self.enough_email_power = False
                break
            time.sleep(2)

    def check_power(self):
        if not self.image.find_energy_shortage():
            return
        info("准备购买体力，优先使用红心")
        if self.buy_power_tag and self.enough_red_heart:
            info("开始使用红心购买体力")
            if self.image.find_store():
                self.click()
                time.sleep(2)
                self.red_heart_buy_power()
                return
        elif self.email_power_tag and self.enough_email_power:
            info("开始领取邮箱体力")
            if self.image.find_gift_box():
                self.click()
                time.sleep(2)
                self.gift_box_power()
                return
        if self.image.find_main_close():
            self.click()
            info(f"等待{common.dungeon_sleep_time}，补充能量")
            time.sleep(common.dungeon_sleep_time)

    def arena(self):
        # TODO 竞技场
        pass

    def special_game(self):
        if self.enough_world_arena_times:
            self.enough_world_arena_times = False

        elif self.image.find_store_confirm():
            self.click()
        elif not self.enough_world_arena_times:
            self.run_tag = False
        elif self.image.find_victory():
            self.click()
        elif self.image.find_failed():
            self.click()
        elif self.image.find_confirm():
            self.click()
        elif self.image.find_game_start():
            self.click()
        elif self.image.find_play():
            self.click()
        else:
            info(f"休眠{common.world_arena_sleep_time}", "节省数据开销")
            time.sleep(common.world_arena_sleep_time)

    def choice_monster(self):
        if len(world_arena_monsters_on) == 5:
            info("已选齐魔灵.......")
            return
        empty_monsters = self.image.find_empty_monsters()
        # 判断当前轮次需要选择几个魔灵
        choice_monster_times = 2
        if len(empty_monsters) == 5 and empty_monsters[0][0] != empty_monsters[1][0] or len(empty_monsters) == 1:
            choice_monster_times = 1
        is_find = False
        for name in world_arena_monsters:
            if choice_monster_times > 0 and name not in world_arena_monsters_on and self.image.find_name(name):
                if self.directive.y < 700:
                    # TODO 变化的 y, 控制到下方可选区域
                    continue
                info(f"找到了:{name}")
                # 选择了进入下一个等待周期
                self.click()
                world_arena_monsters_on.append(name)
                choice_monster_times -= 1
                time.sleep(1)
                is_find = True
        self.directive.get_screenshot()
        time.sleep(1)
        if is_find and self.image.find_monster_confirm():
            self.click()

    def choice_leader(self):
        info(f"当前选择阵容:{world_arena_monsters_on}")
        world_arena_monsters_leader = [{"name": k, "arena_leader_weight": v.get("arena_leader_weight", 0)} for k, v in
                                       monsters.items() if k in world_arena_monsters]
        world_arena_monsters_leader = sorted(world_arena_monsters_leader, key=lambda i: i.get("arena_leader_weight"),
                                             reverse=True)
        world_arena_monsters_leader = [i['name'] for i in world_arena_monsters_leader]
        self.directive.get_screenshot()
        time.sleep(1)
        for name in world_arena_monsters_leader:
            if self.image.find_name(name):
                info(f"选择领袖:{name},{world_arena_monsters_on}")
                self.click()
                break

    def world_arena(self):
        if self.enough_world_arena_times and self.image.find_world_arena_times_less():
            self.enough_world_arena_times = False
        # elif self.image.find_pls_choice_leader():
        #     self.choice_leader()
        #     time.sleep(3)
        # elif self.image.find_pls_choice_monster():
        #     self.choice_monster()
        #     time.sleep(3)
        elif self.image.find_store_confirm():
            self.click()
        elif not self.enough_world_arena_times:
            self.run_tag = False
        elif self.image.find_victory():
            self.click()
        elif self.image.find_failed():
            self.click()
        elif self.image.find_confirm():
            self.click()
        elif self.image.find_rank_fight():
            world_arena_monsters_on.clear()
            self.click()
        elif self.image.find_play_setting() and self.image.find_play():
            self.click()
        else:
            info(f"休眠{common.world_arena_sleep_time}", "节省数据开销")
            time.sleep(common.world_arena_sleep_time)

    def game_start(self):
        if self.enough_world_arena_times and self.image.find_special_game_times_less():
            self.enough_world_arena_times = False
        elif self.image.find_play_setting() and self.image.find_play():
            self.click()
        elif self.image.find_confirm():
            self.click()
        elif self.image.find_store_confirm():
            self.click()
        elif self.image.find_sell_selected_confirm():
            self.click()
        elif self.image.find_game_start():
            self.click()
        elif not self.enough_world_arena_times:
            self.run_tag = False
        elif self.image.find_victory():
            self.click()
        elif self.image.find_failed():
            self.click()
        else:
            info(f"休眠{common.world_arena_sleep_time}", "节省数据开销")
            time.sleep(common.world_arena_sleep_time)

    def shell_rune(self):
        is_sell = False
        while self.run_tag:
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
        elif self.image.find_store_confirm():
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

    def continuous_fight(self):
        """连续战斗,无需处理奖励"""
        if self.image.find_continuous_fight():
            self.click()
            info("开始等待")
        elif self.image.find_yes():
            self.click()
        elif self.image.find_store_confirm():
            self.click()
        elif self.image.find_once_again():
            self.click()
            time.sleep(2)
        elif self.image.find_end_continuous_fight():
            info(f"休眠{common.dungeon_sleep_time}", "节省数据开销")
            time.sleep(common.dungeon_sleep_time)

    def bloody_palace(self):
        if self.image.find_yes():
            self.click()
        elif self.image.find_auto_fight():
            self.bloody_palace_is_not_auto_fight = False
            self.click()
        elif self.image.find_start_fight():
            self.click()
        elif self.bloody_palace_is_not_auto_fight and self.image.find_play():
            self.click()
        elif self.image.find_confirm():
            self.click()
        elif self.image.find_next_floor():
            self.click()
        elif self.image.find_victory():
            self.click()
        else:
            info(f"休眠{common.dungeon_sleep_time}", "节省数据开销")
            time.sleep(common.dungeon_sleep_time)

    def run_script(self):
        info_start("开始检查当前页面")
        self.directive.get_screenshot()
        if self.image.find_dragon_dungeon():
            self.do_check_power(self.dungeon)
        elif self.image.find_bloody_palace():
            self.do_check_power(self.bloody_palace)
        elif self.image.find_giant_dungeon():
            self.do_check_power(self.dungeon)
        elif self.image.find_death_dungeon():
            self.do_check_power(self.dungeon)
        elif self.image.find_game_start():
            self.do_no_check_power(self.game_start)
        elif self.image.find_world_arena():
            self.do_no_check_power(self.world_arena)
        elif self.image.find_continuous_fight():
            # 各种连续战斗都可以识别
            self.do_check_power(self.continuous_fight)
        else:
            warning("无法识别当前页面")

    def run(self):
        info_start("程序开始启动")
        if not self.directive.device_id:
            warning("没有检测到设备")
            return
        self.run_script()


if __name__ == '__main__':
    app = App()
    app.run()
