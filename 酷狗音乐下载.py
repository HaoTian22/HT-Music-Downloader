from threading import Thread
import time
from 下载组件 import *
from 更新助手 import *
import os
import easygui
import threading

try:  # 检测音乐文件夹，没有则新建
    os.mkdir('音乐')
except:
    print('检测到音乐文件夹已存在')
try:
    os.mkdir('数据')
except:
    print('检测到数据文件夹已存在')

with open("数据/log.txt", 'w'):
    pass
with open('数据/cookies.txt', 'a'):
    pass
with open('数据/歌单列表.txt', 'a'):
    pass
with open('数据/歌单哈希值列表.txt', 'a'):
    pass
with open('数据/options.ini', 'a'):
    pass
with open('数据/options.ini', 'r+') as f:
    options = f.read().replace('\n', '')
    if options == '':
        settings = {"debug": False}
        f.write('"debug": False')
    else:
        settings = eval("{" + options + "}")


# 导入类
song_download = kugou_download()


def download_list(hash, lyrics_mode):
    print(song_download.download_main(hash, lyrics_mode))


def download():
    # 选择模式
    mode_list = ['输入酷狗码', '关键词搜索下载', '根据哈希值下载',
                '哈希值批量下载', '更新cookies','检查更新']
    mode = easygui.choicebox(msg='请选择下载模式', title='选择模式', choices=mode_list)
    if mode == '输入酷狗码':
        code = easygui.integerbox('请输入酷狗码', '输入酷狗码', upperbound=None)
        if code == None:
            return
        code_return = kugou_code(code)
        # print(type(code_return))
        if str(type(code_return)) == "<class 'list'>":
            # 写入数据
            with open("数据/歌单列表.txt", "w", encoding="utf-8") as f:
                with open("数据/歌单哈希值列表.txt", "w") as d:
                    num = 1
                    song_list = []
                    song_choice_list = []
                    for i in code_return:
                        song_name = i['filename']
                        song_hash = i['hash']
                        f.write(song_name + '\n')
                        d.write(song_hash + '\n')
                        song_list.append(str(num)+' '+song_name)
                        num += 1

                    song_choice_name = easygui.multchoicebox(
                        msg='选择你要下载的歌曲(可多选，按Cancel退出下载操作)', title='选择歌曲', choices=song_list)
                    if song_choice_name == None:
                        pass
                    else:
                        for i in song_choice_name:
                            song_choice_list.append(int(i.split(' ')[0])-1)
                        lyrics_mode = easygui.boolbox(
                            msg='是否需要一键下载全部歌词？', choices=['是', '否'])
                        for i in song_choice_list:
                            t = threading.Thread(target=download_list, args=(
                                code_return[i]['hash'], lyrics_mode),)
                            # print(song_download.download_main(code_return[i]['hash'], lyrics_mode))
                            t.start()
                            time.sleep(0.1)
        else:
            lyrics_mode = easygui.boolbox('是否下载歌词？', choices=['是', '否'])
            easygui.msgbox(msg=song_download.download_main(
                code_return, lyrics_mode), ok_button='继续')

    elif mode == '关键词搜索下载':
        song_name = easygui.enterbox(msg='请输入歌曲名称')
        song_name_json = song_download.download_name(song_name)
        i = 1
        song_list = []
        for song in song_name_json['data']['lists']:
            file_name = str(i) + ' ' + song['FileName'].replace(
                '<em>', '').replace('</em>', '').replace('<\\/em>', '')
            song_list.append(file_name)
            i += 1
        num = int(easygui.choicebox(msg='请在以上结果中选择你要下载的歌曲',
                                    choices=song_list).split(" ")[0])
        lyrics_mode = easygui.boolbox('是否下载歌词？', choices=['是', '否'])
        print('标准版本:'+song_name_json['data']['lists'][num - 1]['FileHash'])
        print('高清版本(大概率没用):'+song_name_json['data']
            ['lists'][num - 1]['HQFileHash'])
        easygui.msgbox(
            msg=song_download.download_main(
                song_name_json['data']['lists'][num - 1]['FileHash'], lyrics_mode),
            ok_button='继续')

    elif mode == '根据哈希值下载':
        song_hash = easygui.enterbox(msg='输入哈希值', title='哈希值')
        lyrics_mode = easygui.boolbox('是否下载歌词？', choices=['是', '否'])
        easygui.msgbox(msg=song_download.download_main(
            song_hash, lyrics_mode), ok_button='继续')

    elif mode == '哈希值批量下载':
        song_hash = easygui.textbox(
            '请填写哈希值，换行分割\n如果此处为空，则读取并导入文件“数据/歌单哈希值列表.txt”', '输入哈希值')
        if song_hash == None:
            with open('数据/歌单哈希值列表.txt', 'r') as f:
                song_hash_list = f.read().split()  # 读取文件并换行分割
        else:
            song_hash_list = song_hash.split()  # 换行分割
        lyrics_mode = easygui.boolbox(msg='是否需要一键下载全部歌词？', choices=['是', '否'])
        for i in song_hash_list:
            t = threading.Thread(target=download_list, args=(i, lyrics_mode),)
            t.start()
            time.sleep(0.1)

    elif mode == '更新cookies':
        with open('数据/cookies.txt', 'r') as f:
            cookies_old = f.read()
        cookies = easygui.textbox(
            '输入cookies,可在浏览器酷狗音乐页面按f12寻找\n下面的是原来的cookies,请删除后更改', '更新cookies', cookies_old)
        if cookies:
            with open('数据/cookies.txt', 'w') as f:
                f.write(cookies)
    elif mode == '检查更新':
        update()


# 调用函数
if settings["debug"] == False:
    try:
        while(1):
            download()
            else_mode = easygui.choicebox(msg='本次操作已完成，是否进行其他操作', choices=[
                '继续使用', '打开文件夹', '关闭程序'])
            if else_mode == '关闭程序':  # 循环调用
                break
            elif else_mode == '打开文件夹':
                os.system("explorer 音乐\n")
    except:
        easygui.msgbox(
            msg='出现bug，程序将退出\n如有需要，请把debug_mode的值更改为True来打开调试模式以查看详情')
else:
    while(1):
        download()
        else_mode = easygui.choicebox(msg='本次操作已完成，是否进行其他操作', choices=[
            '继续使用', '打开文件夹', '关闭程序'])
        if else_mode == '关闭程序':  # 循环调用
            break
        elif else_mode == '打开文件夹':
            os.system("explorer 音乐\n")
    os.system('pause')
