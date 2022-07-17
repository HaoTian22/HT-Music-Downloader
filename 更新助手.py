import requests
import json
import time
import sys


def update():
    # ----------------自定义区域---------------
    # 版本
    Version = "0.2"
    # 设置本地代理(可以加速下载)
    # port = input("输入本地代理的端口")
    # proxy = {'http': 'http://127.0.0.1:'+port}
    proxy = None
    # -----------------代码区域----------------
    last_update = requests.get(
        "https://api.github.com/repos/HaoTian22/kugou-spider/releases/latest", proxies=proxy)
    last_update = json.loads(last_update.text)
    if Version != last_update["tag_name"]:
        print("最新版本："+last_update["tag_name"])
        print("更新内容："+last_update["body"])
        mode = input("确定更新请输入y，按其他键返回")
        if mode == "y":
            result = requests.get("https://github.com/HaoTian22/kugou-spider/releases/download/{}/kugou-spider.exe".format(
                last_update["tag_name"]), proxies=proxy).content
            with open("酷狗音乐下载.exe", "wb") as f:
                f.write(result)
            print("更新完成，将在5秒自动关闭程序")
            time.sleep(5)
            quit()
    else:
        print("已是最新版本")
    return None
