import requests
import base64

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
    
def get_info(hash):
    # https://wwwapi.kugou.com/play/songinfo?srcappid=2919&clientver=20000&clienttime=1760168982908&mid=84f5d26eb3a790ec6ac1f0f11a8e86a5&uuid=84f5d26eb3a790ec6ac1f0f11a8e86a5&dfid=2mVQCE2IvWni1H84b122yf0q&appid=1014&platid=4&encode_album_audio_id=d5joa5f8&token=afc9fb1f98acd0ca56a63f824dc5a10763b513fb5d85b7993c2b183baa4d15bb&userid=399348742&signature=358512511cc25087c1b94e3d3aeb8f8c
    # https://gateway.kugou.com/tracker/v6/priv_url?appid=1001&clienttime=1760170358&clientver=20061&dfid=1nkrJe1JC0wQ3RORGB2srOfr&mid=3fa044cf10eab25a244bf1cb00abab8f&signature=d1c79c859dbfc32ac160642308e9ca21&token=52bba9dd1f66890be99712c3c5ec7fa7626b9e518d38de02c439dca47b137d40&userid=399348742&uuid=307FB215A4ED34EDEDAA3D7CF9F67C5D
    # url = 'https://wwwapi.kugou.com/play/songinfo?srcappid=2919&clientver=20000&clienttime=1760168982908&mid=84f5d26eb3a790ec6ac1f0f11a8e86a5&uuid=84f5d26eb3a790ec6ac1f0f11a8e86a5&dfid=2mVQCE2IvWni1H84b122yf0q&appid=1014&platid=4&encode_album_audio_id={}&token=afc9fb1f98acd0ca56a63f824dc5a10763b513fb5d85b7993c2b183baa4d15bb&userid=399348742&signature=358512511cc25087c1b94e3d3aeb8f8c'.format(hash)
    # https://m.kugou.com/app/i/getSongInfo.php?hash=034A79E54C345156E34176E771632210&cmd=playInfo
    url = 'http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash={}'.format(hash)
    response = requests.get(url, headers=headers).json()
    if response['status'] == 0:
        return {"status":0,"error":response['error']}
    # info = {"song_name":response_data["name"],"song_id":songid,"song_album":response_data["al"]["name"],"song_singer":response_data["ar"][0]["name"],"song_album_id":response_data["al"]["id"],"pic_url":response_data["al"]["picUrl"]}
    # {"authors":[{"birthday":"1992-09-29","is_publish":1,"author_name":"周深","author_id":169967,"language":"华语","identity":47,"country":"中国","avatar":"http:\/\/singerimg.kugou.com\/uploadpic\/softhead\/{size}\/20230531\/20230531160722881.jpg","type":1}],"hash":"034A79E54C345156E34176E771632210","author_name":"周深、HOYO-MiX","imgUrl":"http:\/\/singerimg.kugou.com\/uploadpic\/softhead\/{size}\/20230531\/20230531160722881.jpg","status":1,"audio_id":93897610,"ctype":1009,"errcode":0,"req_albumid":"41539533","fileHead":0,"fail_process":0,"pay_type":0,"store_type":"audio","128privilege":0,"mvhash":"","fileName":"周深、HOYO-MiX - Rubia","intro":"","songName":"Rubia","320privilege":0,"extName":"mp3","album_category":1,"privilege":0,"backup_url":["https:\/\/sharefs.kugou.com\/202510111807\/d2d02279ccb2a337314e9e2981afd393\/v3\/034a79e54c345156e34176e771632210\/yp\/full\/ap1000_us0_pi409_s3486383194.mp3"],"req_hash":"034A79E54C345156E34176E771632210","old_cpy":1,"q":0,"time":1760177263,"area_code":"1","singerHead":"","timeLength":194,"album_audio_id":293161173,"topic_remark":"","albumid":41539533,"album_img":"http:\/\/imge.kugou.com\/stdmusic\/{size}\/20240129\/20240129181003171581.jpg","error":"","trans_param":{"ogg_128_hash":"E598176640EEFC39D63C28D6F2A410D7","classmap":{"attr0":234881032},"all_quality_free":1,"language":"英语","cpy_attr0":58720256,"musicpack_advance":0,"display":0,"display_rate":0,"union_cover":"http:\/\/imge.kugou.com\/stdmusic\/{size}\/20240129\/20240129181003171581.jpg","qualitymap":{"attr0":1061142645,"attr1":136380416},"ogg_320_filesize":7473218,"ogg_320_hash":"BA89FA5407D00637AD151A13AC99FEC8","cid":247499232,"ogg_128_filesize":2219158,"cpy_grade":5,"ipmap":{"attr0":1090523140},"appid_block":"3124","hash_multitrack":"FC3627CBF0D5BD4EE4BAC3036C7676CF","pay_block_tpl":1,"cpy_level":1},"choricSinger":"周深、HOYO-MiX","stype":11323,"climax_info":{"timelength":"28500","start_time":"101600","end_time":"130100","audio_id":"93897610"},"url":"https:\/\/sharefs.tx.kugou.com\/202510111807\/14ef8e10a1f240b5953bd3f57da96faa\/v3\/034a79e54c345156e34176e771632210\/yp\/full\/ap1000_us0_pi409_s3486383194.mp3","publish_self_flag":0,"highprivilege":0,"sqprivilege":0,"fileSize":3114027,"audio_group_id":354539026,"topic_url":"","bitRate":128,"extra":{"320hash":"5D2B778D428486A17D0129AC3E3CC5A4","128timelength":194586,"sqfilesize":20882496,"sqhash":"BCABBF76900C9220EC7023352D38B888","320timelength":194586,"sqtimelength":194558,"sqbitrate":858,"highhash":"E4BCA39DD26E33978564930D793244A3","128bitrate":128,"hightimelength":194558,"320filesize":7784721,"highfilesize":38016006,"highbitrate":1562,"128hash":"034A79E54C345156E34176E771632210","128filesize":3114027},"singerId":169967,"singerName":"周深"}
    info = {"song_name":response["songName"],"song_id":hash,"song_album":response["req_albumid"],"song_singer":response["author_name"],"song_album_id":response["albumid"],"pic_url":response["album_img"].replace('{size}','400')}
    return info

def get_lyric(name,duration,hash):
    # http://lyrics.kugou.com/v1/search?album_audio_id=326622305&appid=1001&client=pc&clientver=20061&duration=204094&hash=4477e30030d7a2a861810b22fb09e8b6&keyword=%E8%8C%B6%E7%90%86%E7%90%86%E7%90%86%E5%AD%90%E3%80%81TetraCalyx%E3%80%81hanser%20-%20Moon%20Halo&lrctxt=1&man=yes&ver=1&vocab=1&signature=c1d2da8ec02e2adb2a594cc7855fa474
    # http://lyrics.kugou.com/search?ver=1&man=yes&client=pc&keyword=%E8%8C%B6%E7%90%86%E7%90%86%E7%90%86%E5%AD%90%E3%80%81TetraCalyx%E3%80%81hanser%20-%20Moon%20Halo&duration=204094&hash=4477e30030d7a2a861810b22fb09e8b6
    url_search = 'http://lyrics.kugou.com/search?ver=1&man=yes&client=pc&keyword={}&duration={}&hash={}'.format(name,duration,hash)

    # 找匹配的歌词
    response = requests.get(url_search, headers=headers).json()
    if response['status'] == 0:
        return {"status":0,"error":response['error']}
    if response['candidates']:
        id = response['candidates'][0]['id']
        accesskey = response['candidates'][0]['accesskey']
        # http://lyrics.kugou.com/download?ver=1&client=pc&id=197902503&accesskey=605088A1C2C5C430BEB275D2CFF8E5D6&fmt=lrc&charset=utf8
        url_download = 'http://lyrics.kugou.com/download?ver=1&client=pc&id={}&accesskey={}&fmt=lrc&charset=utf8'.format(id,accesskey)
        lyric = requests.get(url_download, headers=headers).json()['content']

        # Base64 解码
        lyric = base64.b64decode(lyric).decode('utf-8')
        return lyric

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