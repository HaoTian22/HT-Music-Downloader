from sys import version
import eyed3
import os
import requests
mp3file = "音乐\郑伊健 - 友情岁月 - 副本.mp3"
audio = eyed3.load(mp3file)
# with open('2.jpg', 'wb') as f:
#     a = audio.tag.images._fs[b'APIC'][0].data
#     f.write(a[19:])
# audio.initTag(version=(2, 3, 0))
# audio.initTag(version=(2, 3, 0))
# assert len(audio.tag.frame_set) == 2
# del audio.tag.frame_set[b"TYER"]
# del audio.tag.frame_set[b"TDAT"]
# assert len(audio.frame_set) == 0
print(audio.tag.images)
# with open('音乐/1.jpg', 'rb') as f:
#     imagedata = f.read()
# audio.tag.images.set(3, imagedata, "image/jpeg", u"Cover")
print(audio.tag.images)
audio.tag.save(version=(2, 3, 0))
# audio.tag.lyrics[0]
