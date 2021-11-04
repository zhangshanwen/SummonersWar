## 魔灵召唤/钉钉打卡 自动化脚本
 - 基于```adb``` + ```opencv``` + ```numpy``` 开发
 - 环境: ```python3.6+,windows/macos .....```
 - 安装: ```python3 -m venv venv``` 后面venv 可自行替换
 - 进入虚拟环境 ``soucre venv/bin/active``
 - 依赖 ```pip install -r requirements.txt```
### 魔灵召唤
 - 运行 ```python app.py``` 或者 ```python gui.py``` (可视化)
### 钉钉自动打卡（需配合定时任务(crontab...)）
 - 运行 ```python dd.py```