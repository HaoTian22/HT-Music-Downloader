import requests

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'}

def get_music_info(keyword):
    url = 'http://songsearch.kugou.com/song_search_v2?keyword={}&page=1&pagesize=1'.format(keyword)
    response = requests.get(url)
    data = response.json()
    if data['status'] == 1:
        music_info = data['data']['lists'][0]
        music_name = music_info['SongName']
        music_singer = music_info['SingerName']
        music_hash = music_info['FileHash']
        return music_name, music_singer, music_hash
    else:
        return None, None, None
    
def get_url(hash):
    # url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash={}'.format(hash)
    # https://wwwapi.kugou.com/play/songinfo?srcappid=2919&clientver=20000&clienttime=1714149355081&mid=ebbbacfd400d240e8579adf29daddf5b&uuid=ebbbacfd400d240e8579adf29daddf5b&dfid=11SO492aSG2c0wiD5D0UDn2D&appid=1014&platid=4&encode_album_audio_id=9d1b3j23&token=&userid=0&signature=b2b53498b20c54ffc041c5dde4aa7bd0
    # url = 'https://kugou-music-api2.vercel.app/song/url?hash={}'.format(hash)
    # url = 'https://wwwapi.kugou.com/play/songinfo?srcappid=2919&clientver=20000&clienttime=1714149355081&mid=ebbbacfd400d240e8579adf29daddf5b&uuid=ebbbacfd400d240e8579adf29daddf5b&dfid=11SO492aSG2c0wiD5D0UDn2D&appid=1014&platid=4&encode_album_audio_id={}&token=&userid=0&signature=b2b53498b20c54ffc041c5dde4aa7bd0'.format(hash)
    # data = response.json()
    # if data['status'] == 2:
    #     # qr_code_base64 = requests.get("https://kugou-music-api2.vercel.app/login/qr/key").json()['data']['qrcode_img']
    #     # return qr_code_base64
    #     return {"status":0,"error":data['error']}
    # else:
    #     return None
    # 上面的方法貌似都不行，只能用下面的方法
    url = 'http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash={}'.format(hash)
    response = requests.get(url, headers=headers).json()
    # print(response)
    if response['status'] == 0:
        return {"status":0,"error":response['error']}
    return response["url"]
    
def search(keyword):
    # http://songsearch.kugou.com/song_search_v2?keyword={}&page=1&pagesize=30
    # http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword={}&page=1&pagesize=30&showtype=1
    # https://complexsearch.kugou.com/v2/search/song?callback=callback123&srcappid=2919&clientver=1000&clienttime=1714149224569&mid=ebbbacfd400d240e8579adf29daddf5b&uuid=ebbbacfd400d240e8579adf29daddf5b&dfid=11SO492aSG2c0wiD5D0UDn2D&keyword={}&page=1&pagesize=30&bitrate=0&isfuzzy=0&inputtype=0&platform=WebFilter&userid=0&iscorrection=1&privilege_filter=0&filter=10&token=&appid=1014&signature=7859548cb460955df753942c64e3e82c
    result = requests.get('http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword={}&page=1&pagesize=30&showtype=1'.format(keyword)).json()
    result_list = result['data']['info']
    songs_list = []
    for song in result_list:
        song_name = song['songname']
        song_id = song['hash']
        song_album = song['album_name']
        song_singer = song['singername']
        song_album_id = song['album_id']
        song_auxiliary = song['topic'] if 'topic' in song else ''
        songs_list.append({"song_name":song_name,"song_id":song_id,"song_album":song_album,"song_singer":song_singer,"song_album_id":song_album_id,"song_auxiliary":song_auxiliary})
    return songs_list