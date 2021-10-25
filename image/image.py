import cv2
import numpy as np
import os

from directive import Directive
import common
from log import *

Threshold = 0.9
Offset = 0


class Image:

    def __init__(self, directive=None, threshold=Threshold, offset=Offset, is_landscape=True,
                 base_imag=common.summoners_base_img):
        self.threshold = threshold
        self.offset = offset
        self.is_landscape = is_landscape
        self.base_image = os.path.realpath(base_imag)
        if directive is None:
            self.directive = Directive()
        else:
            self.directive = directive

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
            warning(e)
            return False

    def show(self):
        img_rgb = cv2.imread('../dd.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('img/dd/check_point.png', 0)
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
    i.show()
