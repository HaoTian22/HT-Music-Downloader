# HT's Music Downloader v4

🎶一个简单的Material Design 3的音乐下载器  
🌏中文 | [English](https://github.com/HaoTian22/HT-Music-Downloader/blob/master/README.md)

## 特性

✅完整支持 | ☑️部分支持 | ❌不支持 | 🕑计划中

---

✅支持根据歌曲名称搜索下载  
🕑自动嵌入歌曲信息/歌词/封面  
☑️多平台Win/Mac/Linux（Linux理论上可以，但是构建bin会报错）  
🕑lrc歌词下载  
✅自定义主题  
☑️多种网络音源（KuGou/Netease/Youtube Music），更多其他源有空可能会加（懒）  
✅简单的播放支持
🕑酷狗码歌单导入  
🕑本地音乐播放  
🕑多选/批量下载  
🕑播放时显示歌词  
❌付费歌曲的所有功能  

*酷狗源只限极少部分歌曲，网易源由[NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)提供，Youtube Music由[yt-dlp](https://github.com/yt-dlp/yt-dlp)提供

## 如何使用

### 方法A（推荐）

1. 克隆仓库：`git clone https://github.com/HaoTian22/HT-Music-Downloader.git`
2. 安装所需包：`pip install -r requirements.txt`
3. 运行程序：`python HT_Music_Downloader.py`

### 方法B

注意：不推荐使用此方法，因为EXE程序基本上不可用
已知问题：

+ yt-dlp在下载歌曲时报`403 forbidden`
+ 无法处理网易云音乐API的响应
+ 相对路径设置为`%temp%/ht_music_downloader-1.0.0-1`文件夹，可能会导致错误
+ 无法在搜索框中输入本地URL播放音乐

~~（所以几乎什么都不好使）~~

步骤：

1. 从[发布页面](https://github.com/HaoTian22/HT-Music-Downloader/releases)下载最新版本
2. 解压文件
3. 双击`HT_Music_Downloader.exe`运行程序

## 已知问题

+ EXE程序大部分功能都不可用，建议使用源码运行，正在尝试解决

## 屏幕截图

V4
![image](https://user-images.githubusercontent.com/48882584/180126365-dd758718-0ef1-4ff8-b4b5-1c521382eacc.png)
![image](https://user-images.githubusercontent.com/48882584/180126578-412ba782-e112-4b1c-a57b-b0bddbe08237.png)
V4.5
![Screenshot 2024-04-27 163212](https://github.com/HaoTian22/HT-Music-Downloader/assets/48882584/9a9083a9-8178-4980-8aca-d05a6f42f7ec)
![1714207476510](https://github.com/HaoTian22/HT-Music-Downloader/assets/48882584/3a5b67d5-c83b-49c3-bd76-7968fac8a761)

## 对开发者

欢迎为这个项目做出贡献！

## 许可

[Apache License](https://github.com/HT-Music/HT-Music-Downloader/blob/master/LICENSE)  

## 鸣谢

Powered By:  
[Python](https://python.org) | [Flutter](https://flutter.dev) | [Flet](https://flet.dev) | [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi) | [yt-dlp](https://github.com/yt-dlp/yt-dlp)
