import cv2
import numpy as np
import os

import common
from log import *

Threshold = 0.60
Offset = 0
error_offset = 20


class Image:

    def __init__(self, directive=None, threshold=Threshold, offset=Offset, is_landscape=True,
                 base_imag=common.summoners_base_img):
        self.threshold = threshold
        self.offset = offset
        self.is_landscape = is_landscape
        self.base_image = os.path.realpath(base_imag)
        if directive is None:
            # self.directive = Directive()

            pass
        else:
            self.directive = directive

    @staticmethod
    def get_error_offset(loc):
        return [i for i in loc if abs(i - np.min(loc) < 5)]

    def find_page_one(self, path, msg=""):
        try:
            path = os.path.realpath(path)
            img_rgb = cv2.imread(self.base_image)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread(path, 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= self.threshold)
            if len(loc[0]) == 0 and len(loc[0]) == 0:
                return False
            self.directive.x = int(np.mean(self.get_error_offset(loc[0]))) + self.offset
            self.directive.y = int(np.mean(self.get_error_offset(loc[1]))) + self.offset
            if self.is_landscape:
                self.directive.x, self.directive.y = self.directive.y, self.directive.x
            if msg:
                debug(msg)
            # debug(loc)
            return True
        except Exception as e:
            warning(e)
            return False

    def find_page(self, path, msg=""):
        try:
            path = os.path.realpath(path)
            # info("path=", path)
            # info("base_image=", self.base_image)
            img_rgb = cv2.imread(self.base_image)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread(path, 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= self.threshold)
            if len(loc[0]) == 0 and len(loc[0]) == 0:
                return False
            self.directive.x = int(np.mean(loc[0])) + self.offset
            self.directive.y = int(np.mean(loc[1])) + self.offset
            if self.is_landscape:
                self.directive.x, self.directive.y = self.directive.y, self.directive.x
            if msg:
                debug(msg)
            # debug(loc)
            return True
        except Exception as e:
            warning(f"{e}", path)
            return False

    def show(self):
        img_rgb = cv2.imread('../summoners.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../img/com2us/store_confirm.png', 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= self.threshold)
        print(loc)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

        cv2.imshow('My Image', img_rgb)
        cv2.waitKey(0)

    def find_loc(self, path, msg="", base_image=""):
        if not base_image:
            base_image = self.base_image
        try:
            path = os.path.realpath(path)
            img_rgb = cv2.imread(base_image)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread(path, 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            return np.where(res >= self.threshold)
        except Exception as e:
            warning(f"{e}", path)
            return False


    @staticmethod
    def mean_coordinates(arr: list):
        i = 0
        while i < len(arr) - 1:
            value_i = arr[i]
            value_i_1 = arr[i + 1]
            if abs(value_i[0] - value_i_1[0]) <= 2 and abs(value_i[1] - value_i_1[1]) <= 2:
                arr[i] = (int(np.mean([value_i[0], value_i_1[0]])), int(np.mean([value_i[1], value_i_1[1]])))
                arr.pop(i + 1)
            else:
                i += 1

    def find_images(self, path, msg="", base_image=""):
        loc = self.find_loc(path, msg, base_image)
        if not loc:
            return False
        coors = list(zip(*loc[::-1]))
        self.mean_coordinates(coors)
        for i in range(len(coors)):
            coors[i] = (coors[i][0] + self.offset, coors[i][1] + self.offset)
        return coors


if __name__ == '__main__':
    i = Image()
    # print(i.find_images('../summoners_2.png', "", '../img/com2us/empty_monster.png'))
    # print(i.find_images('../summoners_2.png', "", '../img/com2us/风画师.png'))
    # print(i.find_images('../summoners_1.png', "", '../img/com2us/光鬼.png'))
    i.show()