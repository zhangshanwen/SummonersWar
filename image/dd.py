from .image import Image


class DDImage(Image):
    def find_check_point(self):
        return self.find_page("img/dd/check_point.png", "考勤打卡")

    def find_work_start(self):
        return self.find_page("img/dd/work_start.png", "上班打卡")

    def find_work_end(self):
        return self.find_page("img/dd/work_end.png", "下班打卡")

    def find_work_space(self):
        return self.find_page("img/dd/work_space.png", "工作台")

    def find_check_point_success(self):
        return self.find_page("img/dd/check_point_success.png", "打卡成功")
