# RaspberryCast
> Transform your RaspberryPi into a true Chromecast

## Still in Alpha !

**Supported services:**

All youtube-dl supported websites: 
http://rg3.github.io/youtube-dl/supportedsites.html

Youtube, Soundcloud, Dailymotion, Vimeo, etc...

But also any mp3, mp4, avi, mkv file.


## How to install (RaspberryPi side)

```
wget https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/setup.sh
sudo sh setup.sh
```

This will :
- Install the necessary dependencies
- Install RaspberryCast
- Enable auto login at boot
- Autostart RaspberryCast at boot

Take a look at the config.py file to configure the audio output and the fast loading mode.

**Update:**

```
cd /RaspberryCast
sudo git pull
sudo reboot
```

## Extension

![alt tag](https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/images/extension.png)

![alt tag](https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/images/rightclick.png)

1. Visit chrome://extensions in your browser (or open up the Chrome menu by clicking the icon to the far right of the Omnibox:  The menu's icon is three horizontal bars. and select Extensions under the Tools menu to get to the same place).

2. Ensure that the Developer mode checkbox in the top right-hand corner is checked.

3. Click Load unpacked extension… to pop up a file-selection dialog.

4. Navigate to the directory /RaspberryCast/chrome, and select it.

5. The option page will open, configure the Raspberry Pi ip.

Alternatively, you can drag and drop the directory where your extension files live onto chrome://extensions in your browser to load it.

# Remote control

![alt tag](https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/images/android.png)

On any device connected to the same network as you Pi, you can visit the page :
```
http://<your-Pi-ip>:2020/
```
On Chrome for Android, we recommend you to use the "Add to homescreen" button.

## Use with PopcornTime

Use the following version : https://popcorntime.io/

1. When the selected movie/show is playing click "u" (keyboard).
2. Open your browser, click on the extension and paste the URL (ctrl-v).
3. Press enter, and wait a few seconds.

DON'T CLOSE POPCORNTIME OR SHUTDOWN YOUR COMPUTER DURING PLAY

**Todo:**

- Better handling errors (!!)
- Cleaner/better code
- Firefox extension
- Android/Ios app for control & sharing
- HDMI-CEC support

Please contribute to the project :)
