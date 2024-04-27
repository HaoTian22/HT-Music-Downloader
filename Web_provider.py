import os
import requests
import Netease
import KuGou
import ytmusic

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
    
def get_url(provider, song_id):
    if provider == "Netease":
        return Netease.get_url(song_id)
    elif provider == "KuGou":
        return KuGou.get_url(song_id)
    elif provider == "QQ":
        pass
    elif provider == "YTMusic":
        return ytmusic.get_url(song_id)
        # return 'https://www.youtube.com/watch?v='+song_id
    else:
        return None
    
def get_mp3(provider,url,filename):
    if not os.path.exists("./Music"):
        os.makedirs("Music")

    if provider != "YTMusic":
        mp3_content = requests.get(url).content
        if os.path.exists("./Music/"+filename+".mp3"):
            print("File already exists")
            return
        with open("./Music/"+filename+".mp3", "wb") as file:
            file.write(mp3_content)
    else:
        ytmusic.download(url, filename)
    return