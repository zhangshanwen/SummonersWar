from .image import Image


class Com2usImage(Image):
    def find_ad(self):
        return self.find_page('img/com2us/ad_total_not_tip.png', "启动app 弹出广告")

    def find_ad_close(self):
        return self.find_page('img/com2us/ad_close.png', "启动app 关闭广告且不提示")

    def find_main_close(self):
        return self.find_page('img/com2us/main_close.png', "天空岛 广告关闭")

    def find_fight(self):
        return self.find_page('img/com2us/fight.png', "天空岛 战斗--->>>app启动完成")

    def find_dragon_dungeon(self):
        return self.find_page('img/com2us/dragon_dungeon.png', "龙之地下城")

    def find_giant_dungeon(self):
        return self.find_page("img/com2us/giant_dungeon.png", "巨人地下城")

    def find_death_dungeon(self):
        return self.find_page("img/com2us/death_dungeon.png", "死亡地下城")

    def find_bloody_palace(self):
        return self.find_page('img/com2us/bloody_palace.png', "试炼之塔")

    def find_start_fight(self):
        return self.find_page('img/com2us/start_fight.png', "开始战斗")

    def find_play(self):
        return self.find_page('img/com2us/play.png', "自动战斗")

    def find_continuous_fight(self):
        return self.find_page("img/com2us/continuous_fight.png", "连续战斗")

    def find_end_continuous_fight(self):
        return self.find_page("img/com2us/end_continuous_fight.png", "结束连续战斗")

    def find_once_again(self):
        return self.find_page("img/com2us/once_again.png", "再来一次")

    def find_victory(self):
        return self.find_page("img/com2us/victory.png", "胜利")

    def find_defeated(self):
        return self.find_page("img/com2us/defeated.png", "失败")

    def find_confirm(self):
        return self.find_page("img/com2us/confirm.png", "确认")

    def find_next_floor(self):
        return self.find_page("img/com2us/next_floor.png", "下一层")

    def find_energy_shortage_need_recharge(self):
        return self.find_page("img/com2us/energy_shortage_need_recharge.png", "能量不足,需要充值")

    def find_energy_shortage(self):
        return self.find_page("img/com2us/energy_shortage.png", "能量不足")

    def find_store(self):
        return self.find_page("img/com2us/store.png", "商店")

    def find_gift_box(self):
        return self.find_page("img/com2us/gift_box.png", "礼物箱")

    def find_sell_selected(self):
        return self.find_page("img/com2us/sell_selected.png", "出售所选")

    def find_sell_selected_confirm(self):
        return self.find_page("img/com2us/sell_selected_confirm.png", "出售所选,确认")

    def find_no_sell(self):
        return self.find_page("img/com2us/no_sell.png", "没有出售")

    def find_purple(self):
        return self.find_page("img/com2us/purple.png", "紫色")

    def find_yes(self):
        return self.find_page("img/com2us/yes.png", "是")

    def find_store_yes(self):
        return self.find_page("img/com2us/store_yes.png", "是")

    def find_store_confirm(self):
        return self.find_page("img/com2us/store_confirm.png", "确认")

    def find_store_close(self):
        return self.find_page("img/com2us/store_close.png", "关闭")

    def find_five_hundred_red_heart(self):
        return self.find_page("img/com2us/five_hundred_red_heart.png", "500红心")

    def find_red_heart_shortage(self):
        return self.find_page("img/com2us/red_heart_shortage.png", "红心不足")