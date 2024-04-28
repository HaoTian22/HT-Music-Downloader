# HT's Music Downloader v4

🎶A simple Material Design 3 music downloader  
🌏English | [中文](https://github.com/HaoTian22/HT-Music-Downloader/blob/master/README_CN.md)

## Features

✅Full support | ☑️Partial support | ❌No support | 🕑In plan

---

✅Search for music  
🕑Embeded song info, lyrics and cover in the file  
☑️Win/Mac/Linux support(Only python/Not support build bin)  
🕑.lrc lyric download
✅Customized themes  
☑️Get songs from Music Streaming platforms online(KuGou/Netease/Youtube Music)*  
✅Play music
🕑Playlist import  
🕑Local music  
🕑Multiple choice  
🕑Show lyrics during playback  
❌All functions for paid songs  

*Limited access from KuGou, Netease is supported by [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi), Youtube Music is supported by [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## How to use

### Method A (Recommended)

1. Clone the repository by running `git clone https://github.com/HaoTian22/HT-Music-Downloader.git`
2. Install the required packages by running `pip install -r requirements.txt`
3. Run the program by running `python HT_Music_Downloader.py`

### Method B

Note: This method is not recommended, as the EXE program is basically not functional.  
Known issues:  

+ yt-dlp reports `403 forbidden` when downloading songs
+ Cannot deal with Netease Cloud Music API's response
+ Relative path is set to `%temp%/ht_music_downloader-1.0.0-1` folder, which may cause errors
+ Cannot enter local URL to search box to play music

~~(So almost nothing works)~~

Steps:

1. Download the latest release from the [releases page](https://github.com/HaoTian22/HT-Music-Downloader/releases)
2. Unzip the file
3. Run the program by double click `HT_Music_Downloader.exe`

## Known Issues

+ EXE program is basically not functional, please run the source code, trying to solve

## Screenshot

V4
![image](https://user-images.githubusercontent.com/48882584/180126365-dd758718-0ef1-4ff8-b4b5-1c521382eacc.png)
![image](https://user-images.githubusercontent.com/48882584/180126578-412ba782-e112-4b1c-a57b-b0bddbe08237.png)
V4.5
![Screenshot 2024-04-27 163212](https://github.com/HaoTian22/HT-Music-Downloader/assets/48882584/9a9083a9-8178-4980-8aca-d05a6f42f7ec)
![1714207476510](https://github.com/HaoTian22/HT-Music-Downloader/assets/48882584/3a5b67d5-c83b-49c3-bd76-7968fac8a761)

## For Developers

Welcome to contribute to this project!

## License

[Apache License](https://github.com/HT-Music/HT-Music-Downloader/blob/master/LICENSE)

## Credits

Powered By:  
[Python](https://python.org) | [Flutter](https://flutter.dev) | [Flet](https://flet.dev) | [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi) | [yt-dlp](https://github.com/yt-dlp/yt-dlp)
