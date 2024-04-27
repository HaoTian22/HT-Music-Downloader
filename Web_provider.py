import requests
import Netease
import KuGou

def search(provider, search_value):
    if provider == "Netease":
        return Netease.search(search_value)
    elif provider == "KuGou":
        return KuGou.search(search_value)
    else:
        return None
    
def get_url(provider, song_id):
    if provider == "Netease":
        return Netease.get_url(song_id)
    elif provider == "KuGou":
        return KuGou.get_url(song_id)
    else:
        return None
    
def get_mp3(url):
    return requests.get(url).content