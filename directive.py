import platform
import time
import os

import common
from log import *

import subprocess


class Directive:
    def __init__(self, base_img=common.summoners_base_img, package_name=common.app_package_name):
        info_start("开始检测当前环境")
        system = platform.system().lower()
        info(f"当前运行环境为:{system}")
        if system == common.windows_os:
            self.adb = "./command/adb.exe"
        else:
            self.adb = "./command/adb"
        self.has_device = False
        self.device_id = ""
        self.base_img = base_img
        self.remove_base_image()
        self.package_name = package_name
        # 检测设备
        self.check_device()
        self.x = 0
        self.y = 0
        self.last_modify_time = 0
        self.save_last_modify_time()

    def remove_base_image(self):
        if os.path.exists(self.base_img):
            os.remove(self.base_img)

    def run_directive(self, directive):
        directive = self.adb + " " + directive
        info(f'执行指令 {directive}')
        res = subprocess.getoutput(directive)
        return res

    def connect_device(self, devices):
        while True:
            msg = "".join([f"{index}:{device}" for index, device in enumerate(devices)])
            info("-----------选择设备--------------")
            info(msg)
            info("请选择设备:")
            try:
                num = int(input())
                self.device_id = devices[num]
                break
            except Exception:
                warning("请输入正确值")

        info_start("开始连接设备")
        self.run_directive(f" -s {self.device_id}")

    def check_device(self):
        info_start("开始检查连接设备")
        res = self.run_directive("devices")
        devices = []
        if res:
            if len(res.splitlines()) <= 1:
                return
            for i in res.splitlines()[1:]:
                if i.split()[1] == "device":
                    device = i.split()[0]
                    info(f"检测到设备:{device}")
                    devices.append(device)
            self.has_device = True
            if len(devices) > 1:
                self.connect_device(devices)
            else:
                self.device_id = devices[0]

    def start_app(self):
        info_start("正在启动应用")
        self.run_directive(f"shell am start -W -n {self.package_name}")
        if not self.check_current_active():
            self.start_app()

    def stop_app(self):
        info_start("正在关闭应用")
        self.run_directive(f" shell am force-stop {self.package_name.split('/')[0]}")

    def check_current_active(self):
        res = self.run_directive("shell dumpsys activity | grep mResumedActivity")
        info(res.find(self.package_name.split('/')[0]))
        return res.find(self.package_name.split('/')[0]) > -1

    def do_check_res(self, func, res):
        res = str(res).lower()
        if "failed" in res or "error" in res:
            warning(res)
            time.sleep(1)
            func()

    def click(self):
        res = self.run_directive(f"shell input tap {self.x} {self.y}")
        self.do_check_res(self.click, res)

    def screenshot(self):
        res = self.run_directive(f" shell screencap  /sdcard/{self.base_img}")
        self.do_check_res(self.screenshot, res)

    def pull(self):
        res = self.run_directive(f"pull /sdcard/{self.base_img}")
        self.do_check_res(self.pull, res)

    def get_screenshot(self):
        last_modify_time = 0
        if os.path.exists(self.base_img):
            last_modify_time = os.path.getmtime(self.base_img)
        self.screenshot()
        self.pull()
        if self.last_modify_time >= last_modify_time:
            warning("页面未刷新，重新拉取", self.last_modify_time, last_modify_time)
            self.get_screenshot()
        else:
            self.last_modify_time = last_modify_time

    def save_last_modify_time(self):
        if os.path.exists(self.base_img):
            self.last_modify_time = os.path.getmtime(self.base_img)


if __name__ == '__main__':
    d = Directive()
    ##1475 909
    # d.x, d.y = 484, 1054
    # info(d.click())
    # d.start_app()
    info(d.get_screenshot())
    # info(d.run_directive("  shell pm list packages -3 "))
    # info(d.run_directive(" shell dumpsys activity top | grep ACTIVITY "))
    # info(int(d.last_modify_time))
    # info(d.check_current_active())
