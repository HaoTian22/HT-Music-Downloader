import os
import requests
import Netease
import KuGou
import ytmusic
import eyed3

def search(provider, search_value):
    if provider == "Netease":
        return Netease.search(search_value)
    elif provider == "KuGou":
        return KuGou.search(search_value)
    elif provider == "QQ":
        pass
    elif provider == "YTMusic":
        return ytmusic.search(search_value)
    else:
        return []
    
def get_url(provider, song_id,quality="higher"):
    if provider == "Netease":
        return Netease.get_url(song_id,quality)
    elif provider == "KuGou":
        return KuGou.get_url(song_id)
    elif provider == "QQ":
        pass
    elif provider == "YTMusic":
        return ytmusic.get_url(song_id)
        # return 'https://www.youtube.com/watch?v='+song_id
    else:
        return None
    
def get_mp3(provider,url,filename, music_dir):
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)

    if provider != "YTMusic":
        mp3_content = requests.get(url).content
        if os.path.exists(f"{music_dir}/{filename}.mp3"):
            print("File already exists")
            return
        with open(f"{music_dir}/{filename}.mp3", "wb") as file:
            file.write(mp3_content)
    else:
        ytmusic.download(url, filename, music_dir)
    return

def write_id3(provider, songid, filename, music_dir):
    if provider == "Netease":
        info = Netease.get_info(songid)
        lyric = Netease.get_lyric(songid)
        pic = requests.get(info["pic_url"]).content
    elif provider == "KuGou":
        info = KuGou.get_info(songid)
        lyric = KuGou.get_lyric(songid)
    elif provider == "QQ":
        pass
    elif provider == "YTMusic":
        info = ytmusic.get_info(songid)
        lyric = None
    else:
        return
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
    if os.path.exists(f"{music_dir}/{filename}.mp3"):
        audiofile = eyed3.load(f"{music_dir}/{filename}.mp3")
        audiofile.tag.title = info["song_name"]
        audiofile.tag.artist = info["song_singer"]
        if "song_album" in info:
            audiofile.tag.album = info["song_album"]
        # audiofile.tag.album_artist = info["song_singer"]
        if "pic_url" in info:
            audiofile.tag.images.set(3, pic, "image/jpeg")
        if lyric != None:
            audiofile.tag.lyrics.set(lyric)
            with open(f"{music_dir}/{filename}.lrc", "w", encoding='utf-8') as file:
                file.write(lyric)
        audiofile.tag.save(version=(2, 3, 0))

    return

def get_info(provider, songid):
    if provider == "Netease":
        return Netease.get_info(songid)
    elif provider == "KuGou":
        return KuGou.get_music_info(songid)
    elif provider == "QQ":
        pass
    elif provider == "YTMusic":
        return ytmusic.get_info(songid)
    else:
        return None
    
def get_lyric(provider, songid):
    if provider == "Netease":
        return Netease.get_lyric(songid)
    elif provider == "KuGou":
        return KuGou.get_lyric(songid)
    elif provider == "QQ":
        pass
    elif provider == "YTMusic":
        return ytmusic.get_lyric(songid)
    else:
        return None