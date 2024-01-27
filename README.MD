## 项目名称

黔职通打卡系统

## 项目描述

本项目旨在帮助黔职通用户实现自动打卡，并提供打卡状态推送功能。

## 项目架构

本项目由以下几个部分组成：

- main.py：登录黔职通，获取用户信息，并保存至数据库。
- database.py：数据库配置。
- punchClock.py：上下班打卡和打卡状态推送。

## 安装

ImportError: libGL.so.1: cannot open shared object file: No such file or directory
apt install libgl1-mesa-glx

```
pip install -r requirements.txt
```
> Linux 使用虚拟环境
> python3 -m venv /opt/qzt/qzt_venv
> source qzt_venv/bin/activate
> pip install -r requirements.txt

## 使用

1. 在 main.py 中设置数据库地址。
2. 运行 main.py 登录黔职通并获取用户信息。
```
python3 main.py {phonenumber} {password}
```
3. 运行 punchClock.py 实现上下班打卡和打卡状态推送。
```
python3 punchClock.py {userId}
```

## 定时任务

crontab 表达式，定时执行打卡任务
```
32 9 * * 1-6 cd /opt/qzt && source qzt_venv/bin/activate && python punchClock.py 391997
28 17 * * 1-6 cd /opt/qzt && source qzt_venv/bin/activate && python punchClock.py 391997

51 9 * * 1-6 cd /opt/qzt && source qzt_venv/bin/activate && python punchClock.py 391998
36 17 * * 1-6 cd /opt/qzt && source qzt_venv/bin/activate && python punchClock.py 391998
```

## 注意

- 本项目仅供学习交流使用，请勿用于非法用途。
- 本项目不保证打卡成功，请自行承担使用风险。

## 贡献

欢迎对本项目进行贡献。请在提交代码前仔细阅读贡献指南。
