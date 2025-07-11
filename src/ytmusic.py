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
    }, {
        'key': 'EmbedThumbnail',
    }],
    'writethumbnail': True,
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
            "song_singer": song["artists"][0]["name"],
            "song_album_id":0,
            "song_auxiliary":'Video/MV'
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
            "song_auxiliary":'Song'
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

def download(url, filename, music_dir):
    ydl_opts["outtmpl"] = f"{music_dir}/{filename}.mp3"
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    ydl.download([url])

def get_info(song_id):
    # song_info = ytmusic_tool.get_song(song_id)["videoDetails"]
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    song_info = ydl.extract_info("https://www.youtube.com/watch?v="+song_id, download=False)
    # song_info = info["title"]
    if "artist" not in song_info:
        song_info["artist"] = song_info["uploader"]

    return {
        "song_name": song_info["title"],
        "song_id": song_id,
        "song_album": song_info["album"] if "album" in song_info else None,
        "song_singer": song_info["artist"][0] if type(song_info["artist"]) == list else song_info["artist"],
        # "song_album_id":0,
        # "pic_url": song_info["thumbnails"][0]["url"]
    }