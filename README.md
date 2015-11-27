# RaspberryCast 0.2
> Transform your Raspberry Pi into a streaming device.
Cast YouTube/Vimeo videos from mobile devices or computers with the Chrome extension.

[![Android app on Google Play](https://developer.android.com/images/brand/en_app_rgb_wo_60.png)](https://play.google.com/store/apps/details?id=com.kiwiidev.raspberrycast)
[![Extension in Chrome web store](https://developer.chrome.com/webstore/images/ChromeWebStore_BadgeWBorder_v2_206x58.png)](https://chrome.google.com/webstore/detail/raspberrycast/aikmhmnmlebhcjjdbjilohbpfljioeak)


Demo video with the Chrome extension:

[![Video 1](http://img.youtube.com/vi/0wEcYPSm_f8/0.jpg)](http://www.youtube.com/watch?v=0wEcYPSm_f8)

Demo video with an Android (also works on iOS):

[![Video 2](http://img.youtube.com/vi/ZafqI4ZtJkI/0.jpg)](http://www.youtube.com/watch?v=ZafqI4ZtJkI)

## Supported services
Works with all youtube-dl supported websites: http://rg3.github.io/youtube-dl/supportedsites.html (YouTube, SoundCloud, Dailymotion, Vimeo, etc...) and also any direct link to mp3, mp4, avi and mkv file.

## How to install (RaspberryPi side)

```
wget https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/setup.sh && sudo sh setup.sh
```
That's it.

The installation script will:
- Install RaspberryCast and the necessary dependencies
- Autostart RaspberryCast at boot (added to /etc/rc.local)
- Reboot (necessary to print logs on first use)
You can review the [install script](https://github.com/vincent-lwt/RaspberryCast/blob/master/setup.sh).

# Remote control (mobile devices)
![alt tag](https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/images/android.png)

On any device connected to the same network as you Pi, you can visit the page:
```
http://<your-Pi-ip>:2020/remote
```
Note that you can "Add to homescreen" this link
 
You can also use the Android application (link to Playstore at the top of the page)

## Chrome extension (computers)
![alt tag](https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/images/extension.png)

![alt tag](https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/images/rightclick.png)

You can configure RaspberryCast settings in the extension option page.

## Todo
- Playlist support
- Subtitles support
- Live stream supports
- Torrent by magnet
- Firefox extension
- iOS app for control & sharing
- HDMI-CEC support

## PopcornTime integration
On your computer, use the following version: https://popcorntime.io/

You need to enable the PopcornTime support in the extension options.

1. On computer, when the selected movie/show is playing press "u" (keyboard).
2. Open your browser, click on the extension and paste the URL in the textbox (ctrl-v).
3. Press enter, and wait a few seconds.

Keep Popcorntime running during play.

##Uninstall
Remove reference to RaspberryPi.sh in /etc/rc.local
Delete the /home/pi/RaspberryCast/ folder.

##Tips

**Update:**

```
cd /RaspberryCast
git pull
sudo ./RasberryCast.sh stop
./RasberryCast.sh start
```

**Restart RaspberryCast (i.e. adress already in use):**

```
cd /RaspberryCast
sudo ./RasberryCast.sh stop
./RasberryCast.sh start
```

**If you want to enable autologin at boot:**

```
sed -i '/1:23/c\1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1' /etc/inittab
```

##License
Code released under the MIT license. 

You are welcome to contribute to the project.
