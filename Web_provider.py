import Netease

def search(provider, search_value):
    if provider == "Netease":
        return Netease.search(search_value)
    else:
        return None
    
def get_url(provider, song_id):
    if provider == "Netease":
        return Netease.get_url(song_id)
    else:
        return None