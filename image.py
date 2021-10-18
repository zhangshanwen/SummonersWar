import cv2
import numpy as np

Threshold = 0.8
Offset = 70


class Image:

    def __init__(self, threshold=Threshold, offset=Offset):
        self.threshold = threshold
        self.offset = offset

    def find_page(self, path):
        img_rgb = cv2.imread('./summoners.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(path, 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= self.threshold)
        if len(loc[0]) == 0 and len(loc[0]) == 0:
            return 0, 0
        return int(np.mean(loc[1])) + self.offset, int(np.mean(loc[0])) + self.offset

    def find_ad(self):
        return self.find_page('img/ad_total_not_tip.png')

    def find_ad_close(self):
        return self.find_page('img/ad_close.png')

    def find_main_close(self):
        return self.find_page('img/main_close.png')

    def find_fight(self):
        return self.find_page('img/fight.png')

    def find_dragon(self):
        return self.find_page('img/dragon.png')

    def find_continuous_fight(self):
        return self.find_page("img/continuous_fight.png")

    def find_once_again(self):
        return self.find_page("img/once_again.png")

    def show(self):
        img_rgb = cv2.imread('./summoners.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('img/main_close.png', 0)
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
    loc = i.find_fight()
    print(loc)
    # i.show()
