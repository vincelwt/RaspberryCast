# RaspberryCast
Streaming popular videos-website to Raspberry Pi, and control it via a web interface
> Chromecast-like

## Still in Alpha !

## How to install

We recommend you a fresh Raspbian install

>sudo apt-get install python-pip fim git
>sudo pip install youtube-dl
>git clone https://github.com/vincent-lwt/RaspberryCast.git

In your computer, clone the project too. Open chrome(ium), go to the extension page and pack the folder /chrome.
 

## How to use

Go to the 
Edit the config file : config.py
Start the server:
>./server.py &

Or add it to the startup

## Knows bugs

When the server is closed, and you try to restart it, there is an "adress already in use" bug.
You can install lsof :
>sudo apt-get install lsof
Then locate the problematic pid :
>lsof -i :2020
And then kill the pid
>kill <pid>

## For those who want to help :

**Todo**

- Cleaner/better code
- "Add to queue" function
- Firefox extension
- Beautiful responsive web interface
- Visualisation of queue into web interface
- Installation script 
- Android/Ios app for control & sharing

Please contribute to the project :)
