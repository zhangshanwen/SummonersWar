import platform
import time

import common
from log import *

import subprocess


class Directive:
    def __init__(self):
        info_start("开始检测当前环境")
        system = platform.system().lower()
        info(f"当前运行环境为:{system}")
        if system == common.windows_os:
            self.adb = "./command/adb.bat"
        else:
            self.adb = "./command/adb"
        self.has_device = False
        self.device_id = ""
        # 检测设备
        self.check_device()

    def run_directive(self, directive):
        info(f'执行指令{directive}')
        res = subprocess.getoutput(self.adb + " " + directive)
        time.sleep(1)
        return res

    def click(self, x, y):
        return self.run_directive(f"shell input tap {x} {y}")

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
        info("正在启动应用")
        self.run_directive(f"shell am start -W -n {common.app_package_name}")

    def check_current_active(self):
        res = self.run_directive("shell dumpsys activity | grep mResumedActivity")
        info(res)
        return res.find(common.app_package_name) > -1

    def screenshot(self):
        self.run_directive(" shell screencap  /sdcard/summoners.png")
        time.sleep(0.5)

    def pull(self):
        self.run_directive("pull /sdcard/summoners.png")

    def get_screenshot(self):
        self.screenshot()
        time.sleep(0.5)
        self.pull()


if __name__ == '__main__':
    d = Directive()
    ##1475 909
    # info(d.click(1545, 979))
    # d.start_app()
    info(d.screenshot())
    info(d.pull())
    # info(d.run_directive(d.adb + "  shell pm list packages -3 "))
    # info(d.run_directive(d.adb + " shell dumpsys activity activities | grep mFocusedActivity "))
