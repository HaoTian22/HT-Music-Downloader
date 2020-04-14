from urllib import parse
from requests import get,post

def kugou_code(code):
    # 这堆东西别瞎改，酷狗特别奇葩，data发的字符串，双引号还不能换成引号
    data2 = {"appid": 1001, "clientver": 8392, "mid": "b1422385bca909d7ac9aadb285f05541",
             "clienttime": 636307277, "key": "1bb5ba48267c0a4750ecda8d7b10368c"}
    data = '{"appid":1001,"clientver":8392,"mid":"b1422385bca909d7ac9aadb285f05541","clienttime":636307277,"key":"1bb5ba48267c0a4750ecda8d7b10368c","data":"' + code + '"}'

    # ----------------第一部分：获取用户信息----------------
    page = post(url="http://t.kugou.com/command/", data=data).text
    page = eval(page)
    # 复制前面的信息，补充后面的data
    json2 = data2
    json2["data"] = page["data"]['info']
    if json2["data"]["type"] == 4:  # 歌单酷狗码
        # 删除多余的data信息，以免出事
        del json2['data']['name'], json2['data']['username'], json2['data']['img'], json2['data']['img_size']
        json2['data']['page'] = 1
        json2['data']['pagesize'] = json2['data']['count']
        del json2['data']['count']
        # 这个我也不知道是什么，抓包抓到的是这样填的我就这样写吧
        json2['data']['type'] = 3
        print('共有' + str(json2['data']['pagesize']) + '首歌')
        # 下面的是原版的json，改崩了可以对照下(我也很崩溃的啊)
        # json2 = '{"appid":1001,"clientver":8392,"mid":"b1422385bca909d7ac9aadb285f05541","clienttime":636307277,"key":"1bb5ba48267c0a4750ecda8d7b10368c","data":{"id":8,"type":3,"userid":"399348742","collect_type":0,"page":1,"pagesize":81}}'
        json2 = str(json2).replace("\'", "\"")

        # -----------------第二部分：根据用户信息获取歌单-------------------
        json3 = post(url='http://www2.kugou.kugou.com/apps/kucodeAndShare/app/', data=json2).text
        json3 = eval(json3)
        song_list = json3['data']
        return song_list
    elif json2['data']["type"] == 1:  # 单曲酷狗码
        return page['data']['list']['hash']


def lyrics(json_list):
    if str(json_list).find('纯音乐，请欣赏') != -1:
        print('✔已检测到纯音乐，不需要歌词')
    elif json_list == None or json_list['data']['lyrics'] == '':
        print('❌此歌曲无歌词')
    else:
        with open('音乐/' + json_list['data']['audio_name'] + '.lrc', 'w', encoding='gb18030') as f:
            f.write(
                json_list['data']['lyrics'].replace('\n', '').replace('\ufeff', '').replace('[id:$00000000]',
                                                                                            '').replace('\r',
                                                                                                        '', 1))
        print('歌词下载完成')


class kugou_download:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4023.0 Safari/537.36 Edg/81.0.396.0'}
        with open('数据/cookies.txt', 'r') as f:
            cookies_dict = {}
            try:
                cookies1 = f.read()
                cookies_list = cookies1.replace(' ', '').split(';')
                for str1 in cookies_list:
                    key, values = str1.split('=', 1)
                    cookies_dict[key] = values
            except:
                cookies1 = 'kg_mid=b434c13fcd475da311e141a0cf532557; _WCMID=16477e145e53a4a7e38ece94; kg_dfid=1aJRd418KcGl0dnFZB3ucZDk; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1582544353; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e'
                cookies_list = cookies1.replace(' ', '').split(';')
                for str1 in cookies_list:
                    key, values = str1.split('=', 1)
                    cookies_dict[key] = values
            self.cookies = cookies_dict


    def download_main(self, song_hash, is_lyrics):
        hash_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191044011229047114075_1566198263706&hash={}'.format(
            song_hash)
        json = get(url=hash_url, headers=self.headers, cookies=self.cookies).text
        main_json = eval(json[42:-2])
        with open('数据/log.txt', 'w', encoding='utf-8') as log:
            log.write(str(main_json))
        if main_json['status'] == 0:
            print('cookies过期或发生其他错误，请重试')
            print('以下是错误代码:'+str(main_json))
            quit(1)
        # 傻逼文件名的检测替换
        file_name_error = ['"', '?', '/', '*', ':', '\\', '|', '<', '>']
        for file_name in file_name_error:
            if main_json['data']['audio_name'].find(file_name) != -1:
                main_json['data']['audio_name'] = main_json['data']['audio_name'].replace(file_name, ' ')
        song_url = main_json['data']['play_url'].replace('\\', '')
        song_name = main_json['data']['audio_name']
        song_length = int(main_json['data']['timelength'])
        song_free = main_json['data']['is_free_part']  # 试听歌曲为1，普通歌曲为0
        if song_url == '':  # 检测歌曲是否能下载
            return '❌歌曲<{}>无数据或需要付费下载'.format(song_name)
        else:
            try:  # 检测是否存在已下载文件
                notice_file_name = ''
                notice = ''
                if song_free == 1:  # 试听歌曲检测
                    notice = '⚠歌曲为试听版，请核实'
                    notice_file_name = '[试听]'
                with open('音乐/' + notice_file_name + song_name + '.mp3', 'xb') as f:  # 检测歌曲是否已经存在，不存在则写入歌曲
                    song = get(url=song_url, headers=self.headers, cookies=self.cookies)
                    f.write(song.content)
                song_length_format = str(int(song_length / 1000) // 60) + ":" + str(int(song_length / 1000) % 60)

                if is_lyrics:
                    lyrics(main_json)
                return '✔歌曲<{}>下载完成\n歌曲时长{}\n'.format(song_name, song_length_format) + notice
            except:  # 歌曲存在的替换
                return '⚠歌曲<' + song_name + '>已存在'

    def download_name(self, name):
        url_name = parse.quote(name)
        url_name = url_name.replace('%20', '+')
        url_json1 = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery11240770641348037286_1566198223730' \
                    '&keyword={}&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection' \
                    '=1&privilege_filter=0&_=1566198223734'.format(url_name)
        page1 = uests.get(url=url_json1, headers=self.headers).text
        song_json = eval(page1[41:-2])
        i = 0
        song_list = []
        song_dict = {}
        for song in song_json['data']['lists']:
            file_name = song['FileName'].replace('<em>', '').replace('</em>', '').replace('<\\/em>', '')
            song_dict[file_name] = i
            song_list.append(file_name)
            i += 1
        return song_json
        # i = int(song_dict[eg.choicebox(msg='请在以上结果中选择你要下载的歌曲', choices=song_list)])
        # i=int(input('请在以上结果中选择你要下载的歌曲(填数字编号)\n'))-1
        # lyrics_mode = eg.boolbox('是否下载歌词？', choices=['是', '否'])
        # if song_mode == 1:  # 流畅
        #     lyrics(download_hash(song_json['data']['lists'][i]['FileHash'], True), lyrics_mode)
        # elif song_mode == 2:  # 高品
        #     lyrics(download_hash(song_json['data']['lists'][i]['HQFileHash'], True), lyrics_mode)
        # elif song_mode == 3:  # 超高
        #     lyrics(download_hash(song_json['data']['lists'][i]['SQFileHash'], True), lyrics_mode)
        # elif song_mode == 4:  # 无损
        #     lyrics(download_hash(song_json['data']['lists'][i]['ResFileHash'], True), lyrics_mode)
