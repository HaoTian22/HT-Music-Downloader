import flet
import json
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
import os
import requests
from flet import (
    Checkbox,
    Column,
    Theme,
    FloatingActionButton,
    IconButton,
    TextButton,
    Icon,
    OutlinedButton,
    Page,
    theme,
    Row,
    Card,
    Tabs,
    Text,
    TextField,
    UserControl,
    AlertDialog,
    colors,
    icons,
    Container,
    ListTile
)
# from download import *

# App作为一个类
class App(UserControl):
    # 初始化控件
    def build(self):
        self.search = TextField(
            hint_text="Search from KuGou", expand=True,on_submit=self.search_song)
        self.songs = Column()

        return Column(
            width=600,
            controls=[
                Row(
                    controls=[
                        self.search,
                        FloatingActionButton(
                            icon=icons.SEARCH, on_click=self.search_song),
                    ],
                ),
                self.songs,
            ],
        )

    # 通过名字搜索歌曲
    def search_song(self, e):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'}
        url = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery11240770641348037286_1566198223730&keyword={}&page=1&pagesize=50&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1'.format(self.search.value)
        page = requests.get(url=url, headers=headers).text
        self.song_json = eval(page[41:-2])
        print(1)
        self.songs.controls = []
        print(2)
        # 提取歌曲有关信息
        for song in self.song_json['data']['lists']:
            file_name = song['FileName'].replace(
                '<em>', '').replace('</em>', '').replace('<\\/em>', '')
            file_hash = song['FileHash']
            AlbumName = song['AlbumName'].replace(
                '<em>', '').replace('</em>', '').replace('<\\/em>', '')
            song_name = song['SongName'].replace(
                '<em>', '').replace('</em>', '').replace('<\\/em>', '')
            singer = song['SingerName']
            album = song['AlbumID']

            song = Song(file_name, song_name, file_hash, AlbumName, singer,album)
            # print(self.songs)
            self.songs.controls.append(song)
        self.update()

# 每首歌作物有个类
class Song(UserControl):
    def __init__(self, filename, name, hash, AlbumName, singer, AlbumID):
        super().__init__()
        self.filename = filename
        self.name = name
        self.hash = hash
        self.album = AlbumName
        self.singer = singer
        self.albumID = AlbumID

    # 渲染控件
    def build(self):
        # self.display_name = Text(value=self.name, expand=1)
        self.download_state = IconButton(
            icon=icons.DOWNLOAD_ROUNDED,
            tooltip="Download this song",
            on_click=self.download,
        )
        self.display_view = Card(
            content=Container(
                padding=10,
                content=Column(
                    [
                        ListTile(
                            leading=Icon(icons.MUSIC_NOTE_ROUNDED),
                            title=Text(self.name),
                            subtitle=Text('Singer:{}      Album:{}'.format(
                                self.singer, self.album)),
                        ),
                        Row([
                            IconButton(
                                icon=icons.PLAY_ARROW_ROUNDED,
                                tooltip="Play",
                                on_click=self.play,
                            ), self.download_state],
                            alignment="end",
                            ),
                    ]
                )
            )
        )
        return self.display_view

    # 下载音乐
    def download(self, *e):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'}
        cookies1 = 'kg_mid=f82cfe86ec1c5fc11436ebd5e6bb5dad; kg_dfid=4XTEXw318YJm49LxBP1Lad3C; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; kg_mid_temp=f82cfe86ec1c5fc11436ebd5e6bb5dad'
        cookies_list = cookies1.replace(' ', '').split(';')
        cookies={}
        for str1 in cookies_list:
            key, values = str1.split('=', 1)
            cookies[key] = values
        
        # 获取歌曲地址
        hash_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19107707606997391536_1606614033664&hash={}&album_id={}'.format(
            self.hash,str(self.albumID))
        self.song_json = json.loads(requests.get(
            url=hash_url, headers=headers,cookies=cookies).text[41:-2])
        if self.song_json['status'] == 0:
            os.system("start https://www.kugou.com/song/")
            self.err()
        song_url = self.song_json['data']['play_url'].replace('\\', '')
        song_free = self.song_json['data']['is_free_part']
        img_url = self.song_json['data']['img']
        if song_url == '':  # 检测歌曲是否能下载
            self.err('下载失败','该歌曲无版权或者需要付费')
        else:
            # try:  # 检测是否存在已下载文件
                if song_free == 1:  # 试听歌曲检测
                    notice = '⚠歌曲为试听版，请核实'
                    self.err('提示',notice)
                with open('音乐/' + self.filename + '.mp3', 'xb') as f:  # 检测歌曲是否已经存在，不存在则写入歌曲
                    song = requests.get(url=song_url, headers=headers,cookies=cookies)
                    f.write(song.content)
                self.get_lyrics()
                self.download_state.icon=icons.DOWNLOAD_DONE_ROUNDED
                try:  # 写入歌曲封面
                    mp3file = '音乐/' + self.filename + '.mp3'
                    songFile = MP3(mp3file, ID3=ID3)
                    try:  # 给没有ID3 tag的歌曲加入tag
                        songFile.add_tags()
                    except:
                        pass
                    picData = requests.get(
                        url=img_url, headers=self.headers).content
                    songFile.tags.add(
                        APIC(  # 插入封面
                            encoding=3,
                            mime='image/jpeg',
                            type=3,
                            desc=u'Cover',
                            data=picData
                        )
                    )
                    songFile.save()
                except:
                    self.err('提示',"歌曲封面写入失败")

            # except:  # 歌曲存在的替换
            #     self.err('下载失败','歌曲已存在')

    def get_lyrics(self):
        self.lyrics=self.song_json['data']['lyrics']
        if str(self.lyrics).find('纯音乐，请欣赏') != -1:
            self.err('提示','✔已检测到纯音乐，不需要歌词')
        elif self.lyrics == '':
            self.err('提示','❌此歌曲无歌词')
        else:
            with open('音乐/' + self.song_json['data']['audio_name'] + '.lrc', 'w', encoding='utf-8') as f:
                f.write(self.lyrics.replace('\ufeff', '').replace('\r', ''))
            print('歌词下载完成')

    # 调用ffplay先下载再播放
    def play(self, *e):
        self.download()
        os.system('ffplay -i "音乐/'+self.filename+'.mp3"')
#        player = MediaPlayer("音乐/{}.mp3".format(self.filename))
#        pass

    # 报错
    def err(self, title='Opps...', content='Oh no! Something went wrong. :('):
        error_msg = AlertDialog(
            title=Text(title),
            content=Text(content),
            actions=[TextButton("OK",on_click=self.close_dia)],
            actions_alignment="end",
        )
        error_msg.open = True
        self.dialog=error_msg
        self.controls.append(error_msg)
        self.update()

    # 关闭报错
    def close_dia(self,e):
        self.dialog.open = False
        self.update()


# 主程序
def main(page: Page):
    page.title = "HT's Music Downloader"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.fonts = {
        "opposans": "/OPPOSans-M.ttf",
    }
    page.theme_mode='light'
    page.theme = Theme(font_family='opposans',
                       use_material3=True, color_scheme_seed='blue')
    page.update()

    # create application instance
    app = App()

    # add application's root control to the page
    page.add(app)
    
try:  # 检测音乐文件夹，没有则新建
    os.mkdir('音乐')
except:
    print('检测到音乐文件夹已存在')
try:
    os.mkdir('数据')
except:
    print('检测到数据文件夹已存在')
flet.app(target=main,port=80,assets_dir="assets")
