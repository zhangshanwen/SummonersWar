import time

from directive import Directive
from image.dd import DDImage
import common
from log import *


class App:
    def __init__(self):
        self.directive = Directive(base_img=common.dd_base_img, package_name=common.dd_app_package_name)
        self.image = DDImage(directive=self.directive, base_imag=common.dd_base_img, offset=30)
        self.no_click_work_space = True
        self.not_check_point = True

    def start_app(self):
        self.directive.start_app()

    def click(self):
        self.directive.click()

    def get_screenshot(self):
        self.directive.get_screenshot()

    def run(self):

        while True:
            self.get_screenshot()
            if self.not_check_point and not self.directive.check_current_active():
                self.start_app()
            elif self.no_click_work_space and self.image.find_work_space():
                self.click()
                self.no_click_work_space = False
            elif self.image.find_check_point():
                self.click()
            elif self.image.find_work_start():
                self.click()
                self.not_check_point = False
            elif self.image.find_work_end():
                self.click()
                self.not_check_point = False
            elif self.image.find_check_point_success():
                self.directive.stop_app()
                break
            else:
                self.no_click_work_space = True


if __name__ == '__main__':
    a = App()
    a.run()
