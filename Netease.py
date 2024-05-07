import requests
# import logging
# import threading
# import flet as ft
from NeteaseCloudMusic import NeteaseCloudMusicApi, api_help, api_list

netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API
version_result = netease_cloud_music_api.request("inner_version")
# print(
    # f'当前使用NeteaseCloudMusicApi版本号：{version_result["NeteaseCloudMusicApi"]}\n当前使用NeteaseCloudMusicApi_V8版本号：{version_result["NeteaseCloudMusicApi_V8"]}')  # 退出登录

def search(search_value):
    # search_value = input("请输入要搜索的内容：")  # 输入搜索内容
    response = netease_cloud_music_api.request("/cloudsearch",{"keywords":search_value})  # 请求API
    # print(response)  # 打印返回结果
    ''''''
    try:
        
        result_list = response["data"]["result"]  # 获取歌曲列表  
        if result_list["songCount"] == 0:
            return []
        result_song_list = result_list["songs"] 
        mode = 1
    except TypeError:
        response = requests.get("https://neteasecloudmusicapi.vercel.app/search?keywords="+search_value).json()
        result_list = response["result"]
        if result_list["songCount"] == 0:
            return []
        result_song_list = result_list["songs"]
        mode = 2
    # song_objects = ft.Column(controls=[],scroll="auto",height=520,width=1020,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    songs_list = []
    for song in result_song_list:
        if mode == 1:
            song_name = song["name"]
            song_id = song["id"]
            song_album = song["al"]["name"]
            song_singer = song["ar"][0]["name"]
            song_album_id = song["al"]["id"]
            song_auxiliary = song["alia"][0] if ("alia" in song and len(song["alia"])>0) else ""
        if mode == 2:
            song_name = song["name"]
            song_id = song["id"]
            song_album = song["album"]["name"]
            song_singer = song["artists"][0]["name"]
            song_album_id = song["album"]["id"]
            song_auxiliary = song["alias"][0] if ("alias" in song and len(song["alias"])>0) else ""
        songs_list.append({"song_name":song_name,"song_id":song_id,"song_album":song_album,"song_singer":song_singer,"song_album_id":song_album_id,"song_auxiliary":song_auxiliary})
        # song_objects.controls.append(Song(song_name, song_id, song_album, song_singer, song_album_id, song_auxiliary).ui)
    # Only UI
    return songs_list

def get_url(song_id):
    response = netease_cloud_music_api.request("/song/url/v1",{"id":song_id,"level":"higher"})
    url = response["data"]["data"][0]["url"]
    return url

def get_info(songid):
    response = netease_cloud_music_api.request("/song/detail",{"ids":str(songid)})
    # response = requests.get("https://neteasecloudmusicapi.vercel.app/song/detail?ids="+songid).json()
    # pic_url = response["data"]["songs"][0]["al"]["picUrl"]
    # pic = requests.get(pic_url).content
    response_data = response["data"]["songs"][0]
    info = {"song_name":response_data["name"],"song_id":songid,"song_album":response_data["al"]["name"],"song_singer":response_data["ar"][0]["name"],"song_album_id":response_data["al"]["id"],"pic_url":response_data["al"]["picUrl"]}
    return info

def get_lyric(songid):
    response = netease_cloud_music_api.request("/lyric",{"id":str(songid)})
    lyric = response["data"]["lrc"]["lyric"]
    return lyric