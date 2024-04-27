from ytmusicapi import YTMusic
import yt_dlp
# import json

ytmusic_tool = YTMusic()

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'music/%(uploader)s - %(title)s.%(ext)s',
    # 'logger': MyLogger(),
    # 'progress_hooks': [my_hook],
}

def search(keyword):
    search_results = ytmusic_tool.search(keyword)
    song_list = []
    for song in search_results:
        if song["category"] == "Videos":
            song_list.append({
            "song_name": song["title"],
            "song_id": song["videoId"],
            "song_album": '',
            "song_singer": song["artists"][1]["name"],
            "song_album_id":0,
            "song_auxiliary":''
            })
            continue
        if song["category"] != "Songs":
            continue
        song_list.append({
            "song_name": song["title"],
            "song_id": song["videoId"],
            "song_album": song["album"]["name"] if "album" in song else "",
            "song_singer": song["artists"][0]["name"],
            "song_album_id":0,
            "song_auxiliary":''
        })
    return song_list

def get_url(song_id):
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    # ydl.geturl(['https://www.youtube.com/watch?v=lYBUbBu4W08'])
    info = ydl.extract_info("https://www.youtube.com/watch?v="+song_id, download=False) 
    format_list = ydl.sanitize_info(info)
    for format in format_list["formats"]:
        if format["ext"] == "m4a":
            url = format["url"]
            break
    # url = youtube_dl.geturl('https://www.youtube.com/watch?v='+song_id)
    return url

def download(url, filename):
    ydl_opts["outtmpl"] = "music/"+filename
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    ydl.download([url])