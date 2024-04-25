import flet as ft
import logging


def main(page: ft.Page):
    page.title = "HT's Music Downloader"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.scroll = "adaptive"
    page.fonts = {"opposans": "/OPPOSans-M.ttf", }
    if not page.client_storage.contains_key("debug"):
        page.client_storage.set("debug", False)
        page.client_storage.set("color", 'Blue')

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

    def change_debug_mode(e):
        page.client_storage.set("debug", e.control.value)
        page.update()

    def change_theme(color):
        page.client_storage.set('color', color)
        page.theme.color_scheme_seed=color
        # page.theme = Theme(font_family='opposans',use_material3=True, color_scheme_seed=color)
        logger.info("Change theme to %s" % color)
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

    player = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Playing...", width=200),
                ft.IconButton(ft.icons.PLAY_ARROW_ROUNDED), 
                ft.IconButton(ft.icons.SKIP_PREVIOUS_ROUNDED),
                ft.Slider(width=300,secondary_active_color=ft.colors.GREY,secondary_track_value=1),
            ],
            height=38,
            width=1020,
        ),
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_radius=10,
        padding=ft.padding.symmetric(vertical=3, horizontal=10),
        alignment=ft.alignment.center,
    )

    def search_song(e):
        # 搜索歌曲
        pass

    class APP_Page:

        def build_search_page(self):  # 搜索页面
            self.search = ft.TextField(
                hint_text="Search from KuGou", expand=True, on_submit=search_song)
            self.songs = ft.Column(scroll="auto", width=1000, height=600, horizontal_alignment="center")
            page = ft.Container(content=
                ft.Column(
                    width=1030,
                    height=600,
                    controls=[
                        ft.Row(
                            controls=[
                                self.search,
                                ft.FloatingActionButton(
                                    icon=ft.icons.SEARCH, on_click=search_song),
                            ],
                        ),
                        # Container(self.songs,padding=padding.symmetric(horizontal=200)),
                        # ft.Row(controls=[self.songs]),
                    ]
                ),
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

            settings = ft.Column(
                width=1000,
                height=600,
                scroll="auto",
                controls=[
                    ft.Text("Settings"),
                    theme_setting,
                    debug_setting,
                ]
            )
            logger.info("Build settings page")
            return settings

        def __init__(self) -> None:
            self.search_page = self.build_search_page()
            self.local_page = self.build_local_page()
            self.settings_page = self.build_settings_page()

    app_page = APP_Page()
    main_page = app_page.search_page

    if debug_mode:
        logger.setLevel(logging.INFO)

    page.add(ft.Row(controls=[nav, ft.VerticalDivider(width=1), ft.Column(controls=[main_page, player])], height=650, width=1200, expand=True))


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
logger.setLevel(logging.INFO)

ft.app(target=main,assets_dir="./assets")
