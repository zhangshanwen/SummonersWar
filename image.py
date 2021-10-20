import cv2
import numpy as np

from directive import Directive
import common
from log import *

Threshold = 0.9
Offset = 0


class Image:

    def __init__(self, directive=None, threshold=Threshold, offset=Offset):
        self.threshold = threshold
        self.offset = offset
        if directive is None:
            self.directive = Directive()
        else:
            self.directive = directive

    def find_page(self, path, msg=""):
        img_rgb = cv2.imread(common.summoners_base_img)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(path, 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= self.threshold)
        if len(loc[0]) == 0 and len(loc[0]) == 0:
            return False
        self.directive.x = int(np.mean(loc[1])) + self.offset
        self.directive.y = int(np.mean(loc[0])) + self.offset
        if msg:
            info(msg)
        return True

    def find_ad(self):
        return self.find_page('img/ad_total_not_tip.png', "启动app 弹出广告")

    def find_ad_close(self):
        return self.find_page('img/ad_close.png', "启动app 关闭广告且不提示")

    def find_main_close(self):
        return self.find_page('img/main_close.png', "天空岛 广告关闭")

    def find_fight(self):
        return self.find_page('img/fight.png', "天空岛 战斗--->>>app启动完成")

    def find_dragon_dungeon(self):
        return self.find_page('img/dragon_dungeon.png', "龙之地下城")

    def find_giant_dungeon(self):
        return self.find_page("img/giant_dungeon.png", "巨人地下城")

    def find_death_dungeon(self):
        return self.find_page("img/death_dungeon.png", "死亡地下城")

    def find_bloody_palace(self):
        return self.find_page('img/bloody_palace.png', "试炼之塔")

    def find_start_fight(self):
        return self.find_page('img/start_fight.png', "开始战斗")

    def find_play(self):
        return self.find_page('img/play.png', "自动战斗")

    def find_continuous_fight(self):
        return self.find_page("img/continuous_fight.png", "连续战斗")

    def find_once_again(self):
        return self.find_page("img/once_again.png", "再来一次")

    def find_victory(self):
        return self.find_page("img/victory.png", "胜利")

    def find_defeated(self):
        return self.find_page("img/defeated.png", "失败")

    def find_confirm(self):
        return self.find_page("img/confirm.png", "确认")

    def find_next_floor(self):
        return self.find_page("img/next_floor.png", "下一层")

    def find_energy_shortage_need_recharge(self):
        return self.find_page("img/energy_shortage_need_recharge.png", "能量不足,需要充值")

    def find_energy_shortage(self):
        return self.find_page("img/energy_shortage.png", "能量不足")

    def find_store(self):
        return self.find_page("img/store.png", "商店")

    def find_gift_box(self):
        return self.find_page("img/gift_box.png", "礼物箱")

    def find_shell_selected(self):
        return self.find_page("img/shell_selected.png", "出售所选")

    def find_purple(self):
        return self.find_page("img/purple.png", "紫色")

    def find_yes(self):
        return self.find_page("img/yes.png", "是")

    def find_store_yes(self):
        return self.find_page("img/store_yes.png", "是")

    def find_store_confirm(self):
        return self.find_page("img/store_confirm.png", "确认")

    def find_store_close(self):
        return self.find_page("img/store_close.png", "关闭")

    def find_five_hundred_red_heart(self):
        return self.find_page("img/five_hundred_red_heart.png", "500红心")

    def find_red_heart_shortage(self):
        return self.find_page("img/red_heart_shortage.png", "红心不足")

    def show(self):
        img_rgb = cv2.imread('./summoners.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('img/five_hundred_red_heart.png', 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= self.threshold)
        print(loc)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

        cv2.imshow('My Image', img_rgb)
        cv2.waitKey(0)


if __name__ == '__main__':
    i = Image()
    # i.show()
    i.find_continuous_fight()
    # # print(i.directive.x, i.directive.y)
    # # i.show()
