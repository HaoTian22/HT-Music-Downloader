from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
import mutagen
import os
import requests

mp3file = "D:\code\python\项目\kugou-spider\音乐\郑伊健 - 友情岁月.mp3"
songFile = mutagen.File(mp3file, easy=True)
# songFile = ID3(mp3file)
picData2 = requests.get(
    "http://imge.kugou.com/stdmusic/20150715/20150715190438230801.jpg").content

with open('C:/Users/Hao_Tian/Downloads/20150715190438230801.jpg', 'rb') as f:
    picData = f.read()
    songFile['APIC'] = APIC(  # 插入封面
        encoding=3,
        mime='image/jpeg',
        type=3, 
        desc=u'Cover',
        data=picData2
)
songFile.save()
