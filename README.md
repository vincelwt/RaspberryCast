# RaspberryCast
> Transform your Raspberry Pi into a streaming device.
Videos can be sent from mobile devices or computers (Chrome extension).

## Supported services

Works with all youtube-dl supported websites: 
http://rg3.github.io/youtube-dl/supportedsites.html (YouTube, SoundCloud, Dailymotion, Vimeo, etc...) but also any mp3, mp4, avi and mkv file.

RasberryCast also works with PopcornTime.

## How to install (RaspberryPi side)

```
wget https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/setup.sh && sudo sh setup.sh
```
That's it.

The installation script will:
- Install the necessary dependencies
- Install RaspberryCast
- Autostart RaspberryCast at boot

You can also configure your settings in the config.py file (audio output and video download quality).


## Chrome extension (computers)

![alt tag](https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/images/extension.png)

![alt tag](https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/images/rightclick.png)

1. Download https://github.com/vincent-lwt/RaspberryCast/tree/master/chrome
2. Visit chrome://extensions in your browser 
3. Ensure that the Developer mode checkbox in the top right-hand corner is checked.
4. Click Load unpacked extension… to pop up a file-selection dialog.
5. Navigate to the directory /RaspberryCast/chrome, and select it.
6. The option page will open, configure the Raspberry Pi ip.

Alternatively, you can drag and drop the directory where your extension files live onto chrome://extensions in your browser to load it.

# Remote control (mobile devices)

![alt tag](https://raw.githubusercontent.com/vincent-lwt/RaspberryCast/master/images/android.png)

On any device connected to the same network as you Pi, you can visit the page:
```
http://<your-Pi-ip>:2020/remote
```
To use your mobile device as a remote, you can "Add to homescreen" this page.

## Use with PopcornTime

Use the following version: https://popcorntime.io/

1. When the selected movie/show is playing click "u" (keyboard).
2. Open your browser, click on the extension and paste the URL (ctrl-v).
3. Press enter, and wait a few seconds.

Keep Popcorntime running during play.


**Update:**

```
cd /RaspberryCast
sudo git pull
sudo ./RasberryCast.sh restart
```

**Todo:**

- Better errors handling
- Firefox extension
- Android/iOS app for control & sharing
- HDMI-CEC support

You are welcome to contribute to the project.
