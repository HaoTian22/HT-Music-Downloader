from email import header
from ssl import AlertDescription
from turtle import onclick
import flet
import json
import os
import requests
from flet import (
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    TextButton,
    Icon,
    OutlinedButton,
    Page,
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


class App(UserControl):
    def build(self):
        self.search = TextField(
            hint_text="Search from KuGou", expand=True)
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

    def search_song(self, e):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'}
        url = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery11240770641348037286_1566198223730' \
            '&keyword={}&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection' \
            '=1&privilege_filter=0&_=1566198223734'.format(self.search.value)
        page = requests.get(url=url, headers=headers).text
        song_json = eval(page[41:-2])
        print(1)
        self.songs.controls = []
        print(2)
        for song in song_json['data']['lists']:
            file_name = song['FileName'].replace(
                '<em>', '').replace('</em>', '').replace('<\\/em>', '')
            file_hash = song['FileHash']
            AlbumName = song['AlbumName'].replace(
                '<em>', '').replace('</em>', '').replace('<\\/em>', '')
            song_name = song['SongName'].replace(
                '<em>', '').replace('</em>', '').replace('<\\/em>', '')
            singer = song['SingerName']

            song = Song(file_name, song_name, file_hash, AlbumName, singer)
            # print(self.songs)
            self.songs.controls.append(song)
        self.update()


class Song(UserControl):
    def __init__(self, filename, name, hash, AlbumName, singer):
        super().__init__()
        self.filename = filename
        self.name = name
        self.hash = hash
        self.album = AlbumName
        self.singer = singer

    def build(self):
        # self.display_name = Text(value=self.name, expand=1)
        self.display_view = Card(
            content=Container(
                padding=10,
                content=Column(
                    [
                        ListTile(
                            leading=Icon(icons.MUSIC_NOTE),
                            title=Text(self.name),
                            subtitle=Text('Singer:{}      Album:{}'.format(
                                self.singer, self.album)),
                        ),
                        Row([
                            IconButton(
                                icon=icons.PLAY_ARROW,
                                tooltip="Play",
                                on_click=self.play,
                            ), IconButton(
                                icon=icons.DOWNLOAD,
                                tooltip="Download this song",
                                on_click=self.download,
                            ), ],
                            alignment="end",
                            ),
                    ]
                )
            )
        )
        return self.display_view

    def download(self, e):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'}
        hash_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19107707606997391536_1606614033664&hash={}'.format(
            self.hash)
        main_json = json.loads(requests.get(
            url=hash_url, headers=headers).text[41:-2])
        if main_json['status'] == 0:
            os.system("start https://www.kugou.com/song/")
        # if main_json['data']['have_album'] == 0:
        if 1:
            self.error_msg.open = True
            self.update()

    def play(self, e):
        error_msg = AlertDialog(
            title=Text('Opps...'),
            content=Text('Oh no! Something went wrong. :('),
            actions=[TextButton("OK",on_click=self.close_dia)],
            actions_alignment="end",
        )
        self.dialog = error_msg
        error_msg.open = True
        self.update()
        # print(1)

    def close_dia(self,e):
        self.dialog.open = False
        self.update()


def main(page: Page):
    page.title = "KuGou Download"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.update()

    # create application instance
    app = App()

    # add application's root control to the page
    page.add(app)

    def err():
        error_msg = AlertDialog(
            title=Text('Opps...'),
            content=Text('Oh no! Something went wrong. :('),
            actions=[TextButton("OK",on_click=close_dia)],
            actions_alignment="end",
        )
        page.dialog = error_msg
        error_msg.open = True

    def close_dia():
        page.dialog.open = False
        page.update()


flet.app(target=main, view=flet.WEB_BROWSER, port=80)
