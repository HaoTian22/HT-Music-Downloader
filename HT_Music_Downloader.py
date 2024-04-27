import os
import flet as ft
import logging
import datetime
# from Netease import *
import Web_provider
# import signal
# import threading

# def handle_signal(signum, frame):
#     print("Received signal:", signum)

# # Set up signal handling in main thread
# signal.signal(signal.SIGINT, handle_signal)

def format_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


def main(page: ft.Page):
    page.title = "HT's Music Downloader"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.scroll = "adaptive"
    page.fonts = {"opposans": "/OPPOSans-M.ttf", }
    if not page.client_storage.contains_key("debug"):
        page.client_storage.set("debug", False)
        page.client_storage.set("color", 'Blue')
    if not page.client_storage.contains_key("web_provider"):
        page.client_storage.set("web_provider", "Netease")

    color = page.client_storage.get('color')
    debug_mode = page.client_storage.get('debug')
    page.theme = ft.Theme(font_family='opposans', use_material3=True, color_scheme_seed=color)
    page.window_width = 1200
    page.window_height = 720
    page.update()

    # 基本函数
    def change_page(e):
        global main_page
        if e.control.selected_index == 0:
            main_page = app_page.search_page
            logger.info("Change to search page")
        elif e.control.selected_index == 1:
            main_page = app_page.local_page
            logger.info("Change to local page")
        elif e.control.selected_index == 2:
            main_page = app_page.settings_page
            logger.info("Change to settings page")
        # 更改主页面
        page.controls[0].controls[2].controls[0] = main_page
        page.update()

    # 设置
    def change_debug_mode(e):
        page.client_storage.set("debug", e.control.value)
        page.update()

    def change_theme(color):
        page.client_storage.set('color', color)
        page.theme.color_scheme_seed=color
        # page.theme = Theme(font_family='opposans',use_material3=True, color_scheme_seed=color)
        logger.info("Change theme to %s" % color)
        page.update()

    def web_provider_change(e):
        page.client_storage.set('web_provider', e.control.value)
        logger.info("Change web provider to %s" % e.control.value)
        page.update()

    # 基本控件
    nav = ft.NavigationRail(
        selected_index=0,
        label_type="all",
        min_width=100,
        height=650,
        min_extended_width=400,
        # leading=Icon(icons.QUEUE_MUSIC_ROUNDED),
        group_alignment=-1,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME_OUTLINED,
                selected_icon=ft.icons.HOME_ROUNDED,
                label="Home",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.LIBRARY_MUSIC_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.LIBRARY_MUSIC_ROUNDED),
                label="Local",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS_ROUNDED),
                label_content=ft.Text("Settings"),
            ),
        ],on_change=change_page
    )

    class Player:
        def show_position(self):
            if(self.duration == None):
                return
            value = self.audio.get_current_position() / self.duration
            self.player.content.controls[3].value = value
            # print("Change position to "+str(value))
            self.player.content.controls[4].value = format_time(self.audio.get_current_position())
            self.player.content.controls[6].value = format_time(self.duration)
            # print("Show position "+format_time(self.audio.get_current_position()))
            page.update()

        def change_position(self, e):
            timestamp  = int(self.duration * e.control.value)
            self.audio.seek(timestamp)
            # print("Change position to "+str(timestamp))
            page.update()

        def load_audio(self,url,name=None):
            self.player.content.controls[0].value = "No song"
            self.player.content.controls[1].disabled = True
            self.player.content.controls[2].disabled = True
            self.player.content.controls[3].disabled = True
            self.player.content.controls[3].value = 0
            self.player.content.controls[4].value = "00:00"
            self.player.content.controls[6].value = "00:00"
            self.name = name if name != None else url

            page.update()
            self.audio = ft.Audio(
            src=url,
            autoplay=False,
            volume=1,
            balance=0,
            on_loaded=lambda _: self.play_audio(),
            on_duration_changed=lambda e: logger.info("Duration changed: "+str(e.data)),
            on_position_changed=lambda e: self.show_position(),
            on_state_changed=self.show_state,
            # on_seek_complete=lambda _: print("Seek complete"),
            )
            page.overlay[0] = self.audio
            page.update()
            # page.overlay[0].play()

        def play_audio(self):
            self.duration = self.audio.get_duration()
            logger.info("Duration: "+str(self.duration))
            if self.duration != None:
                self.player.content.controls[0].value = self.name
                print(self.name)
                self.player.content.controls[1].disabled = False
                self.player.content.controls[2].disabled = False
                self.player.content.controls[3].disabled = False
                self.audio.play()
                self.is_playing = True
                # self.player.content.controls[1].icon = ft.icons.PAUSE_ROUNDED
                logger.info("Start playing")
                page.update()

        def show_state(self,e):
            self.player.content.controls[1].icon = ft.icons.PAUSE_ROUNDED if e.data == "playing" else ft.icons.PLAY_ARROW_ROUNDED
            # print("State changed:", e.data)
            logger.info("State changed: "+e.data)
            page.update()

        def change_playing_status(self):
            if self.duration == None:
                return
            self.audio.pause() if self.is_playing else self.audio.resume()
            self.is_playing = not self.is_playing

            logger.info("Change playing status to "+str(self.is_playing))
            page.update()

        def __init__(self) -> None:
            self.is_playing = False
            self.name = "No song"
            self.duration = None
            self.player = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(self.name, width=200, no_wrap=True,text_align='right'),
                        ft.IconButton(
                            ft.icons.PLAY_ARROW_ROUNDED,
                            on_click=lambda e: self.change_playing_status(),
                            disabled=True,
                        ),
                        ft.IconButton(
                            ft.icons.RESTART_ALT_ROUNDED,
                            on_click=lambda e: self.audio.seek(0),
                            disabled=True,
                        ),
                        ft.Slider(
                            width=400,
                            inactive_color=ft.colors.GREY,
                            on_change=self.change_position,
                            disabled=True,
                        ),
                        ft.Text("00:00"),
                        ft.Text("/"),
                        ft.Text("00:00"),
                    ],
                    height=38,
                    width=1020,
                ),
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=10,
                padding=ft.padding.symmetric(vertical=3, horizontal=10),
                alignment=ft.alignment.center,
            )
    global music_player
    music_player = Player()

    class APP_Page:

        def build_search_page(self):  # 搜索页面
            self.search = ft.TextField(
                hint_text="Search from Web or Enter URL", expand=True, on_submit=self.search_song,text_align='center')
            self.songs = ft.Column(scroll="auto", width=1040, height=600, horizontal_alignment="center")
            page = ft.Stack(controls=
                [ft.Column(
                    width=1030,
                    height=600,
                    controls=[
                        ft.Row(
                            controls=[
                                self.search,
                                ft.FloatingActionButton(
                                    icon=ft.icons.SEARCH, on_click=self.search_song),
                            ],
                        ),
                        # Container(self.songs,padding=padding.symmetric(horizontal=200)),
                        ft.ListView(controls=[],height=520,width=1050),
                        
                    ]
                ),
                ft.AlertDialog(title=ft.Text("QR Code"))
                ],
            )
            # self.main_page=page
            logger.info("Build main page")
            return page

        def build_local_page(self):  # 本地音乐页面
            logger.info("Build local page")
            this_page = ft.Container(
                    content=ft.Text("Local Music\nComing soon..."),
                    margin=100,
                    padding=10,
                    alignment=ft.alignment.center,
                    # bgcolor=ft.colors.AMBER,
                    width=400,
                    # height=300,
                    border_radius=10,
                )
            return this_page

        def build_settings_page(self):  # 设置页面
            theme_setting = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Row([
                        ft.Icon(ft.icons.COLOR_LENS),
                        ft.Text("Theme-Color", expand=True),
                        ft.VerticalDivider(width=420),
                        ft.IconButton(icon=ft.icons.CIRCLE, icon_color='red', tooltip='red', on_click=lambda e:change_theme('red')),
                        ft.IconButton(icon=ft.icons.CIRCLE, icon_color='pink', tooltip='pink', on_click=lambda e:change_theme('pink')),
                        ft.IconButton(icon=ft.icons.CIRCLE, icon_color='orange', tooltip='orange', on_click=lambda e:change_theme('orange')),
                        ft.IconButton(icon=ft.icons.CIRCLE, icon_color='yellow', tooltip='yellow', on_click=lambda e:change_theme('yellow')),
                        ft.IconButton(icon=ft.icons.CIRCLE, icon_color='green', tooltip='green', on_click=lambda e:change_theme('green')),
                        ft.IconButton(icon=ft.icons.CIRCLE, icon_color='blue', tooltip='blue', on_click=lambda e:change_theme('blue')),
                        ft.IconButton(icon=ft.icons.CIRCLE, icon_color='purple', tooltip='purple', on_click=lambda e:change_theme('purple')),
                        ft.IconButton(icon=ft.icons.CIRCLE, icon_color='brown', tooltip='brown', on_click=lambda e:change_theme('brown')),
                    ])

                ),
            )
            debug_setting = ft.Card(
                content=ft.Container(
                    padding=10, 
                    # height=200,
                    content=ft.Row([
                        ft.Icon(ft.icons.BUG_REPORT_ROUNDED),
                        ft.Text("Debug-Mode (Need restart)", expand=True),
                        ft.VerticalDivider(width=650),
                        ft.Switch(on_change=change_debug_mode, value=page.client_storage.get("debug"))
                    ])
                )
            )

            web_provider = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.WEB),
                            ft.Text("Web Provider", expand=True),
                            ft.VerticalDivider(width=350),
                            ft.Dropdown(
                                dense=True,
                                width=200,
                                bgcolor=ft.colors.ON_INVERSE_SURFACE,
                                value=page.client_storage.get('web_provider'),
                                # filled = True,
                                options=[
                                    ft.dropdown.Option("Netease"),
                                    ft.dropdown.Option("KuGou"),
                                    ft.dropdown.Option("QQ"),
                                ],
                                on_change=web_provider_change,
                            ),
                        ]
                    ),
                )
            )

            settings = ft.Column(
                width=1040,
                height=600,
                scroll="auto",
                controls=[
                    ft.Text("Settings"),
                    theme_setting,
                    debug_setting,
                    web_provider,
                ]
            )
            logger.info("Build settings page")
            return settings

        def search_song(self,e):
            # music_player.load_audio("https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true")
            global music_player
            self.search_value = self.search_page.controls[0].controls[0].controls[0].value
            if "http" in self.search.value or ".mp3" in self.search.value:
                music_player.load_audio(self.search.value)
                logger.info("Play song: "+ self.search.value)
                return

            provider = page.client_storage.get('web_provider')
            songs_list = Web_provider.search(provider,self.search_value)
            # self.search_page.content.controls[1].controls=song_objects
            logger.info("Songs list: "+str(songs_list))
            song_objects = ft.ListView(controls=[],height=520,width=1040,padding=20,spacing=8)
            if len(songs_list) == 0:
                song_objects.controls.append(ft.Text("No result found"))

            for song in songs_list:
                song_name = song["song_name"]
                song_id = song["song_id"]
                song_album = song["song_album"]
                song_singer = song["song_singer"]
                song_album_id = song["song_album_id"]
                song_auxiliary = song["song_auxiliary"]
                song_objects.controls.append(Song(song_name, song_id, song_album, song_singer, song_album_id, song_auxiliary,provider).ui)

            self.search_page.controls[0].controls.pop()
            self.search_page.controls[0].controls.append(song_objects)
            # logger.info("Search song: "+ song.name)
            page.update()

            # logger.info("Search song: "+ self.search_page.content.controls[0].controls[0].value)
            # pass

        def __init__(self) -> None:
            self.search_page = self.build_search_page()
            self.local_page = self.build_local_page()
            self.settings_page = self.build_settings_page()

    class Song:

        def __init__(self, name, id, AlbumName, singer, AlbumID, Auxiliary,provider):
            super().__init__()
            self.name = name
            self.id = id
            self.album = AlbumName
            self.singer = singer
            self.albumID = AlbumID
            self.Auxiliary = Auxiliary
            self.ui = self.build()
            self.provider = provider

        def play(self):
            global music_player
            # response = netease_cloud_music_api.request("/song/url/v1",{"id":self.id,"level":"higher"})
            # 本地优先
            music_player.load_audio("./Music/"+self.singer+" - "+self.name+".mp3")
            duration = music_player.duration
            if duration == None:
                url = Web_provider.get_url(self.provider,self.id)
                # print(url)
                logger.info("Provider Response: "+str(url))

                if type(url) == dict:
                    app_page.search_page.controls[1].title = ft.Text("Error: ")
                    app_page.search_page.controls[1].content = ft.Text(url['error'])
                    app_page.search_page.controls[1].open = True
                    page.update()
                    return
                # if "image" in url:
                #     # dialog = ft.AlertDialog(
                #     #     title="QR Code",
                #     #     open=True,
                #     #     content=ft.Image(src_base64=url),
                #     #     # actions=[ft.DialogAction(label="Close", on_click=lambda e: dialog.close())],
                #     # )
                #     app_page.search_page.controls[1].content = ft.Image(src_base64=url[22:])
                #     app_page.search_page.controls[1].open = True
                #     page.update()
                # pass
                # from HT_Music_Downloader import web_song_loader
                # web_song_loader(url)
                # from HT_Music_Downloader import music_player
                music_player.load_audio(url,self.name)
            return url
            # print(response)

        def download(self,e):
            url = Web_provider.get_url(self.provider,self.id)
            # print(url)
            logger.info("Provider Response: "+str(url))
            if type(url) == dict:
                app_page.search_page.controls[1].title = ft.Text("Error: ")
                app_page.search_page.controls[1].content = ft.Text(url['error'])
                app_page.search_page.controls[1].open = True
                page.update()
                return

            if not os.path.exists("./Music"):
                os.makedirs("Music")
            with open("./Music/"+self.singer+" - "+self.name+".mp3", "wb") as file:
                file.write(Web_provider.get_mp3(url))
            logger.info("Downloaded: "+self.name)

            self.download_state.icon = ft.icons.DOWNLOAD_DONE_ROUNDED

        # 渲染控件
        def build(self):
            # self.display_name = Text(value=self.name, expand=1)
            # print("Building song: "+self.name)
            logger.info("Building song: "+self.name)
            self.download_state = ft.IconButton(
                icon=ft.icons.DOWNLOAD_ROUNDED,
                tooltip="Download this song",
                on_click=self.download
            )
            # Auxiliary = '\nNote: '+self.Auxiliary if self.Auxiliary != '' else ''
            # 非常抽象的UI
            Auxiliary = ft.Row([ft.Container(content=ft.Row([ft.Icon(ft.icons.MORE_ROUNDED,size=18),ft.Text(self.Auxiliary),]),bgcolor=ft.colors.PRIMARY_CONTAINER,padding=ft.padding.only(left=5, top=5, right=10, bottom=5),border_radius=30,),]) if self.Auxiliary != '' else None

            singer = 'Singer: '+self.singer+'    ' if len(self.singer)<=12 and len(self.album) <= 12 else 'Singer: '+self.singer+'\n'
            album = 'Album: '+self.album if self.album != '' else ''
            # basicinfo = singer+album+Auxiliary
            self.display_view = ft.Card(
                content=ft.Container(
                    padding=10,
                    # width=600,
                    # bgcolor=ft.colors.SURFACE_VARIANT,
                    content=ft.Row(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.MUSIC_NOTE_ROUNDED),
                                title=ft.Text(self.name, selectable=True),
                                subtitle=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Container(
                                                    content=ft.Row(
                                                        [
                                                            ft.Icon(
                                                                ft.icons.ACCOUNT_CIRCLE_ROUNDED,
                                                                size=18,
                                                            ),
                                                            ft.Text(self.singer),
                                                        ]
                                                    ),
                                                    bgcolor=ft.colors.PRIMARY_CONTAINER,
                                                    padding=ft.padding.only(
                                                        left=5,
                                                        top=5,
                                                        right=10,
                                                        bottom=5,
                                                    ),
                                                    border_radius=30,
                                                    margin=ft.margin.only(top=5),
                                                ),
                                                ft.Container(
                                                    content=ft.Row(
                                                        [
                                                            ft.Icon(
                                                                ft.icons.ALBUM_ROUNDED,
                                                                size=18,
                                                            ),
                                                            ft.Text(self.album),
                                                        ]
                                                    ),
                                                    bgcolor=ft.colors.PRIMARY_CONTAINER,
                                                    padding=ft.padding.only(
                                                        left=5,
                                                        top=5,
                                                        right=10,
                                                        bottom=5,
                                                    ),
                                                    border_radius=30,
                                                    margin=ft.margin.only(top=5),
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                                bgcolor_activated=ft.colors.ON_INVERSE_SURFACE,
                                width=830,
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.PLAY_ARROW_ROUNDED,
                                        tooltip="Play",
                                        on_click=lambda e: self.play(),
                                    ),
                                    self.download_state,
                                ],
                                alignment="end",
                            ),
                        ]
                    ),
                )
            )
            if Auxiliary != None:
                self.display_view.content.content.controls[0].subtitle.controls.append(Auxiliary)
            return self.display_view

    app_page = APP_Page()
    main_page = app_page.search_page

    if debug_mode:
        logger.setLevel(logging.INFO)

    page.add(ft.Row(controls=[nav, ft.VerticalDivider(width=1), ft.Column(controls=[main_page, music_player.player])], height=650, width=1200, expand=True))
    page.overlay.append(ft.Audio(src=" ", autoplay=False, volume=1, balance=0))


# start the application
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S', filename='log.log', filemode="w")
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler("log.log", mode="w", encoding="utf-8")
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setFormatter(formatter)

logger.setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(console)

ft.app(target=main,assets_dir="./assets")
