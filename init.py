import flet
import json
import logging
import yaml
import eyed3
from pathlib import Path
import requests
from pygame import mixer
from flet import (
    Column,
    Theme,
    FloatingActionButton,
    NavigationRail,
    Switch,
    NavigationRailDestination,
    Divider,
    VerticalDivider,
    IconButton,
    TextButton,
    Icon,
    icons,
    Page,
    theme,
    Row,
    Card,
    Text,
    Stack,
    TextField,
    UserControl,
    AlertDialog,
    colors,
    icons,
    Container,
    ListTile
)

# App作为一个类


class App(UserControl):
    # 初始化控件
    def build(self):
        self.side_rail = NavigationRail(selected_index=0)
        self.side_rail = NavigationRail(
            selected_index=0,
            label_type="all",
            min_width=100,
            # height=650,
            min_extended_width=400,
            # leading=Icon(icons.QUEUE_MUSIC_ROUNDED),
            group_alignment=-1,
            destinations=[
                NavigationRailDestination(
                    icon=icons.HOME_OUTLINED, selected_icon=icons.HOME_ROUNDED, label="Home"
                ),
                NavigationRailDestination(
                    icon_content=Icon(icons.LIBRARY_MUSIC_OUTLINED),
                    selected_icon_content=Icon(icons.LIBRARY_MUSIC_ROUNDED),
                    label="Local",
                ),
                NavigationRailDestination(
                    icon=icons.SETTINGS_OUTLINED,
                    selected_icon_content=Icon(icons.SETTINGS_ROUNDED),
                    label_content=Text("Settings"),
                ),
            ],
            on_change=self.change_page
        )
        # self.change_page()
        self.main_page = self.build_main_page()
        self.local_page = self.build_local_page()
        self.settings_page = self.build_settings_page()
        self.current_page = self.main_page
        return Row(controls=[self.side_rail, VerticalDivider(width=1), self.current_page], height=650, expand=True)

    def change_page(self, *e):  # 切换页面
        if self.side_rail.selected_index == 0:
            logger.info("change page to main page")
            self.current_page = self.main_page
        elif self.side_rail.selected_index == 1:
            logger.info("change page to local page")
            self.current_page = self.local_page
        elif self.side_rail.selected_index == 2:
            logger.info("change page to settings page")
            self.current_page = self.settings_page
        self.controls = [Row(controls=[self.side_rail, VerticalDivider(
            width=1), self.current_page], height=650, expand=True)]
    # 更新控件
        self.update()

    def build_main_page(self):  # 主页面
        self.search = TextField(
            hint_text="Search from KuGou", expand=True, on_submit=self.search_song)
        self.play_state = True
        self.play_button = FloatingActionButton(
            icon=icons.PAUSE_ROUNDED,
            on_click=self.change_play_state,
            right=10,
            bottom=5,
        )
        self.songs = Column(scroll="auto", width=1000, height=600, horizontal_alignment="center")
        page = Stack(controls=[
            Column(
                width=1000,
                height=650,
                controls=[
                    Row(
                        controls=[
                            self.search,
                            FloatingActionButton(
                                icon=icons.SEARCH, on_click=self.search_song),
                        ],
                    ),
                    # Container(self.songs,padding=padding.symmetric(horizontal=200)),
                    Row(controls=[self.songs]),
                ]
            ),
            self.play_button,
        ])
        # self.main_page=page
        logger.info("build main page")
        return page

    def build_local_page(self):  # 本地音乐页面
        logger.info("build local page")
        return Text("Local Music Page\n Under Construction")

    def build_settings_page(self):  # 设置页面
        theme_setting = Card(
            content=Container(
                padding=10,
                content=Row([
                    Icon(icons.COLOR_LENS),
                    Text("Theme-Color", expand=True),
                    VerticalDivider(width=420),
                    IconButton(icon=icons.CIRCLE, icon_color='red', tooltip='red', on_click=lambda e:self.change_theme('red')),
                    IconButton(icon=icons.CIRCLE, icon_color='pink', tooltip='pink', on_click=lambda e:self.change_theme('pink')),
                    IconButton(icon=icons.CIRCLE, icon_color='orange', tooltip='orange', on_click=lambda e:self.change_theme('orange')),
                    IconButton(icon=icons.CIRCLE, icon_color='yellow', tooltip='yellow', on_click=lambda e:self.change_theme('yellow')),
                    IconButton(icon=icons.CIRCLE, icon_color='green', tooltip='green', on_click=lambda e:self.change_theme('green')),
                    IconButton(icon=icons.CIRCLE, icon_color='blue', tooltip='blue', on_click=lambda e:self.change_theme('blue')),
                    IconButton(icon=icons.CIRCLE, icon_color='purple', tooltip='purple', on_click=lambda e:self.change_theme('purple')),
                    IconButton(icon=icons.CIRCLE, icon_color='brown', tooltip='brown', on_click=lambda e:self.change_theme('brown')),
                ])

            ),
        )
        global config
        debug_setting = Card(
            content=Container(
                padding=10, 
                # height=200,
                content=Row([
                    Icon(icons.BUG_REPORT_ROUNDED),
                    Text("Debug-Mode", expand=True),
                    VerticalDivider(width=750),
                    Switch(on_change=self.change_debug_mode, value=config['debug'])
                ])
            )
        )

        settings = Column(
            width=1000,
            height=650,
            scroll="auto",
            controls=[
                Text("Settings"),
                theme_setting,
                debug_setting,
            ]
        )
        logger.info("build settings page")
        return settings

    def change_theme(self, color):
        global config
        # self.page.theme.color_scheme_seed=color
        self.page.theme = Theme(font_family='opposans',use_material3=True, color_scheme_seed=color)
        self.page.update()

        config['theme'] = color
        with open('config.yml', "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True)
        logger.info("change theme to %s" % color)

    # Debug设置
    def change_debug_mode(self, e):
        global config
        config['debug'] = True if e.data == 'true' else False
        with open('config.yml', "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True)
        logger.info("change debug mode to %s" % e.data)

    # 通过名字搜索歌曲

    def search_song(self, e):
        logger.info("search song")
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'}
        url = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery11240770641348037286_1566198223730&keyword={}&page=1&pagesize=50&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1'.format(self.search.value)
        page = requests.get(url=url, headers=headers).text
        self.song_json = eval(page[41:-2])
        logger.debug(self.song_json)
        self.songs.controls = []
        # 提取歌曲有关信息
        for song in self.song_json['data']['lists']:
            file_name = song['FileName'].replace('<em>', '').replace('</em>', '').replace('<\\/em>', '')
            file_hash = song['FileHash']
            AlbumName = song['AlbumName'].replace('<em>', '').replace('</em>', '').replace('<\\/em>', '')
            song_name = song['SongName'].replace('<em>', '').replace('</em>', '').replace('<\\/em>', '')
            singer = song['SingerName'].replace('<em>', '').replace('</em>', '').replace('<\\/em>', '')
            album = song['AlbumID']

            song = Song(file_name, song_name, file_hash, AlbumName, singer, album)
            self.songs.controls.append(song)
        self.update()

    def change_play_state(self, *e):
        self.play_state = not self.play_state
        self.play_button.icon = icons.PAUSE_ROUNDED if self.play_state else icons.PLAY_ARROW_ROUNDED
        mixer.music.unpause() if self.play_state else mixer.music.pause()
        logger.info("change play state to %s" % self.play_state)
        self.update()


# 每首歌作为一个类
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
        logger.info("build song"+self.filename)
        self.download_state = IconButton(
            icon=icons.DOWNLOAD_ROUNDED,
            tooltip="Download this song",
            on_click=self.download
        )
        self.display_view = Card(
            content=Container(
                padding=10,
                width=600,
                content=Column(
                    [
                        ListTile(
                            leading=Icon(icons.MUSIC_NOTE_ROUNDED),
                            title=Text(self.name),
                            subtitle=Text('Singer:{}      Album:{}'.format(self.singer, self.album)),
                        ),
                        Row([
                            IconButton(
                                icon=icons.PLAY_ARROW_ROUNDED,
                                tooltip="Play",
                                on_click=self.play
                            ),
                            self.download_state
                        ],
                            alignment="end"
                        )
                    ]
                )
            )
        )
        return self.display_view

    # 下载音乐
    def download(self, *e):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'}
        cookies1 = 'kg_mid=f82cfe86ec1c5fc11436ebd5e6bb5dad; kg_dfid=4XTEXw318YJm49LxBP1Lad3C; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; kg_mid_temp=f82cfe86ec1c5fc11436ebd5e6bb5dad'
        cookies_list = cookies1.replace(' ', '').split(';')
        cookies = {}
        for str1 in cookies_list:
            key, values = str1.split('=', 1)
            cookies[key] = values

        # 获取歌曲地址
        hash_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19107707606997391536_1606614033664&hash={}&album_id={}'.format(self.hash, str(self.albumID))
        self.song_json = json.loads(requests.get(
            url=hash_url, headers=headers, cookies=cookies).text[41:-2])
        if self.song_json['status'] == 0:
            # os.system("start https://www.kugou.com/song/")
            logger.error("download error")
            self.err()
        song_url = self.song_json['data']['play_url'].replace('\\', '')
        song_free = self.song_json['data']['is_free_part']
        img_url = self.song_json['data']['img']
        logger.debug(self.song_json)
        logger.info("download song"+self.filename)
        # 下载歌曲
        if song_url == '':  # 检测歌曲是否能下载
            logger.warning('song url is empty')
            self.err('下载失败', '该歌曲无版权或者需要付费')
        else:
            try:  # 检测是否存在已下载文件
                if song_free == 1:  # 试听歌曲检测
                    notice = '⚠歌曲为试听版，请核实'
                    self.err('提示', notice)
                    logger.warning('song is trial')
                with open('音乐/' + self.filename + '.mp3', 'xb') as f:  # 检测歌曲是否已经存在，不存在则写入歌曲
                    song = requests.get(
                        url=song_url, headers=headers, cookies=cookies)
                    f.write(song.content)
                self.get_lyrics()
                self.download_state.icon = icons.DOWNLOAD_DONE_ROUNDED
                self.update()
                # try:  # 写入歌曲信息ID3 v2.3
                logger.info("write id3")
                mp3file = '音乐/' + self.filename + '.mp3'
                audio = eyed3.load(mp3file)
                old_image = None
                if audio.tag.images._fs[b'APIC']:
                    desc = audio.tag.images._fs[b'APIC'][0].description
                    old_image = audio.tag.images.get(desc)
                # audio.initTag(version=(2, 3, 0))
                if audio.tag.artist is None:
                    audio.tag.artist = self.singer
                if audio.tag.album is None:
                    audio.tag.album = self.album
                if audio.tag.title is None:
                    audio.tag.title = self.name
                if old_image is None:
                    audio.tag.images.set(3, requests.get(
                        url=img_url, headers=headers, cookies=cookies).content, 'image/jpeg', u'Cover')
                if len(audio.tag.lyrics) == 0:
                    audio.tag.lyrics.set(self.lyrics)

                audio.tag.save(version=(2, 3, 0))
                # except:
                #     logger.warning('Fail to write song cover')
                #     self.err('提示',"歌曲封面写入失败")

            except FileExistsError:  # 歌曲已存在
                self.err('下载失败', '歌曲已存在')
                logger.warning('song {} is exist'.format(self.filename))
                self.download_state.icon = icons.DOWNLOAD_DONE_ROUNDED
                self.update()

    def get_lyrics(self):  # 获取歌词
        self.lyrics = self.song_json['data']['lyrics']
        if str(self.lyrics).find('纯音乐，请欣赏') != -1:
            logger.warning('song is pure music')
            self.err('提示', '✔已检测到纯音乐，不需要歌词')
        elif self.lyrics == '':
            logger.warning('song has no lyrics')
            self.err('提示', '❌此歌曲无歌词')
        else:
            with open('音乐/' + self.song_json['data']['audio_name'] + '.lrc', 'w', encoding='utf-8') as f:
                f.write(self.lyrics.replace('\ufeff', '').replace('\r', ''))
            logger.info('Download lyrics success')

    # 调用ffplay先下载再播放
    def play(self, e):
        self.download()
        # os.system('ffplay -i "音乐/'+self.filename+'.mp3"')
        mixer.music.load('音乐/{}.mp3'.format(self.filename))
        e.page.controls[0].play_state = False
        e.page.controls[0].change_play_state()
        mixer.music.play()

    # 报错
    def err(self, title='Opps...', content='Oh no! Something went wrong. :('):
        error_msg = AlertDialog(
            title=Text(title),
            content=Text(content),
            actions=[TextButton("OK", on_click=self.close_dia)],
            actions_alignment="end",
        )
        error_msg.open = True
        self.controls.append(error_msg)
        self.update()

    # 关闭报错
    def close_dia(self, e):
        # 隐藏最新弹窗
        self.controls[-1].open = False
        self.update()
        # 删除弹窗
        self.controls.pop()




# 主程序
def main(page: Page):
    page.title = "HT's Music Downloader"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.scroll = "adaptive"
    page.fonts = {"opposans": "/OPPOSans-M.ttf", }
    global config
    color = config['theme']
    page.theme = Theme(font_family='opposans',
                       use_material3=True, color_scheme_seed=color)
    page.window_width = 1200
    page.window_height = 720
    page.update()

    # create application instance
    app = App()

    # add application's root control to the page
    page.add(app)


# start the application
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S', filename='log.log', filemode="w")
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler("log.log", mode="w")
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setFormatter(formatter)

logger.setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(console)

try:  # 检测音乐文件夹，没有则新建
    path = Path('音乐')
    path.mkdir()
except:
    logger.warning('Music Directory Exists')

logger.info('Initializing config...')
config_file = Path('config.yml')
config_file.touch(exist_ok=True)
with open('config.yml', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)
    if config == None:
        config = {}
    if 'theme' not in config:
        config['theme'] = 'blue'
    if 'debug' not in config:
        config['debug'] = False
if config['debug']:
    logger.setLevel(logging.INFO)
mixer.init()
flet.app(target=main, port=4000, assets_dir="assets")
