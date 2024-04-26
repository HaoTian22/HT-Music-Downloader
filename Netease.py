import requests
import logging

import flet as ft
from NeteaseCloudMusic import NeteaseCloudMusicApi, api_help, api_list

netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API
version_result = netease_cloud_music_api.request("inner_version")
# print(
    # f'当前使用NeteaseCloudMusicApi版本号：{version_result["NeteaseCloudMusicApi"]}\n当前使用NeteaseCloudMusicApi_V8版本号：{version_result["NeteaseCloudMusicApi_V8"]}')  # 退出登录

def search(search_value):
    # search_value = input("请输入要搜索的内容：")  # 输入搜索内容
    response = netease_cloud_music_api.request("/cloudsearch",{"keywords":search_value})  # 请求API
    print(response)  # 打印返回结果
    ''''''
    songs_list = response["data"]["result"]["songs"]  # 获取歌曲列表
    song_objects = ft.Column(controls=[],scroll="auto",height=520,width=1020,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    for song in songs_list:
        song_name = song["name"]
        song_id = song["id"]
        song_album = song["al"]["name"]
        song_singer = song["ar"][0]["name"]
        song_album_id = song["al"]["id"]
        song_auxiliary = song["alia"][0] if ("alia" in song and len(song["alia"])>0) else ""
        song_objects.controls.append(Song(song_name, song_id, song_album, song_singer, song_album_id, song_auxiliary).ui)
    # Only UI
    return song_objects

class Song:

    def __init__(self, name, id, AlbumName, singer, AlbumID, Auxiliary):
        super().__init__()
        self.name = name
        self.id = id
        self.album = AlbumName
        self.singer = singer
        self.albumID = AlbumID
        self.Auxiliary = Auxiliary
        self.ui = self.build()


    def play(self):
        response = netease_cloud_music_api.request("/song/url/v1",{"id":self.id,"level":"higher"})
        url = response["data"]["data"][0]["url"]
        from HT_Music_Downloader import music_player
        music_player.load_audio(url)
        return url
        # print(response)


    # 渲染控件
    def build(self):
        # self.display_name = Text(value=self.name, expand=1)
        print("Building song: "+self.name)
        self.download_state = ft.IconButton(
            icon=ft.icons.DOWNLOAD_ROUNDED,
            tooltip="Download this song",
            # on_click=self.download
        )
        Auxiliary = '\nAuxiliary: '+self.Auxiliary if self.Auxiliary != '' else ''
        singer = 'Singer: '+self.singer+'    ' if len(self.singer)<=12 and len(self.album) <= 12 else 'Singer: '+self.singer+'\n'
        album = 'Album: '+self.album if self.album != '' else ''
        basicinfo = singer+album+Auxiliary
        self.display_view = ft.Card(
            content=ft.Container(
                padding=10,
                width=600,
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.MUSIC_NOTE_ROUNDED),
                            title=ft.Text(self.name),
                            subtitle=ft.Text(basicinfo),
                        ),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.PLAY_ARROW_ROUNDED,
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