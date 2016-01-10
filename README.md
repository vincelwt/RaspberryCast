# RaspberryCast 3.0
> Transform your Raspberry Pi into a streaming device.
Cast videos from mobile devices or computers to your TV.

[![Android app on Google Play](http://vincelwt.github.io/RaspberryCast/images/android_banner.png)](https://play.google.com/store/apps/details?id=com.kiwiidev.raspberrycast)
[![Extension for Chrome](http://vincelwt.github.io/RaspberryCast/images/chrome_banner.png)](https://chrome.google.com/webstore/detail/raspberrycast/aikmhmnmlebhcjjdbjilohbpfljioeak)
[![Extension for Firefox](http://vincelwt.github.io/RaspberryCast/images/firefox_banner.png)](https://addons.mozilla.org/firefox/addon/raspberrycast/)


Demo video with the Chrome extension:

[![Video 1](http://img.youtube.com/vi/0wEcYPSm_f8/0.jpg)](http://www.youtube.com/watch?v=0wEcYPSm_f8)

Demo video with an Android (also works on iOS):

[![Video 2](http://img.youtube.com/vi/ZafqI4ZtJkI/0.jpg)](http://www.youtube.com/watch?v=ZafqI4ZtJkI)

## Supported services
Works with all youtube-dl supported websites: http://rg3.github.io/youtube-dl/supportedsites.html (YouTube, SoundCloud, Dailymotion, Vimeo, etc...) and also any direct link to mp3, mp4, avi and mkv file.

You can also cast playlists from Youtube or Soundcloud.

## How to install (Raspberry Pi side)

```
wget https://raw.githubusercontent.com/vincelwt/RaspberryCast/master/setup.sh && sudo sh setup.sh
```
That's it.

The installation script will:
- Download RaspberryCast and install the necessary dependencies
- Autostart RaspberryCast at boot (added to /etc/rc.local)
- Reboot

You can review the [install script](https://github.com/vincelwt/RaspberryCast/blob/master/setup.sh).

# Remote control (mobile devices)
![The remote on Android](http://vincelwt.github.io/RaspberryCast/images/android.png)

On any device connected to the same network as you Pi, you can visit the page:
```
http://raspberrypi.local:2020/remote
```
Note that you can "Add to homescreen" this link
 
You can also use the Android application (link to Playstore at the top of the page)

## Chrome & Firefox extension
![alt tag](http://vincelwt.github.io/RaspberryCast/images/extension.png)

![alt tag](http://vincelwt.github.io/RaspberryCast/images/rightclick.png)

You can configure RaspberryCast settings in the extension option page.

## Drag and drop videos from computer

![alt tag](http://vincelwt.github.io/RaspberryCast/images/draganddrop.png)

Download for [Windows](http://vincelwt.github.io/RaspberryCast/dist/DragDrop-linux), [Windows](http://vincelwt.github.io/RaspberryCast/dist/DragDrop-windows.exe), OSX (coming really soon)

**To execute it on Linux :**

```
chmod +x DragDrop-linux
./DragDrop-linux
```

If subtitles corresponding to the video you are casting are found, they will be automatically loaded.

## Uninstall
Remove reference to RaspberryCast.sh in /etc/rc.local

Delete the /home/pi/RaspberryCast/ folder.

## License
Code released under the MIT license. 

You are welcome to contribute to the project.
