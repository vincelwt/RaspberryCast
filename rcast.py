#!/usr/bin/env python

import urllib
import urllib2
import os
import sys
import thread
import signal
import socket
import SimpleHTTPServer
import SocketServer
import time
import json


def signal_handler(signal, frame):
        print(
            'You pressed Ctrl+C, stopping. Casting may continue for some time.'
        )
        sys.exit(0)


# No need for advanced logging options since rcast.py is to be run manually
def log(output):

    # If file exist, open it and append to file.
    # If file does not exist, create it.
    try:
        file = open(sys.path[0] + "/rcast.log", "a")
    except IOError:
        file = open(sys.path[0] + "/rcast.log", "w")

    file.write(time.strftime('%a %H:%M:%S') + "  " + output + "\n")
    file.close()
    print output

# Catch SIGINT via Ctrl + C
signal.signal(signal.SIGINT, signal_handler)

# Handle incorrect number of arguments
if(len(sys.argv) > 3 or len(sys.argv) < 2):
    log("""Incorrect number of arguments given. Program expects 1-2 arguments.
A playable video file, and an optional subtitle file.""")
    sys.exit(0)

# Attempt to load and read configuration file.
# If no file is found, use default values.
try:
    with open(sys.path[0] + "/raspberrycast.conf") as f:
        config = json.load(f)

        # Read configuration file.
        # If no values exists (or if it's empty), use default values.
        if config["pi_hostname"] and config["pi_hostname"] is not "":
            ip = config["pi_hostname"] + ".local" + ":2020"
        else:
            ip = ip = "raspberrypi.local:2020"

        if config["subtitle_search"] and config["subtitle_search"] is not "":
            search_for_subtitles = config["subtitle_search"]
        else:
            search_for_subtitles = False

# If an IOException is caught, the file could not be found.
# We then use the default values for the hostname and sub_search
except IOError as e:
    log("""INFO: Configuration file 'raspberrycast.conf' not found.
Using default values.""")
    ip = "raspberrypi.local:2020"
    search_for_subtitles = False

# -- MAIN PROGRAM START -- #

tocast = sys.argv[1]
subtitle_path = ""

log("-----------------------------")
log("Attempting to cast " + tocast)
log("-----------------------------")

if not os.path.isfile(tocast):
    log("File not found!")
    sys.exit(0)

if(len(sys.argv) == 3):
    subtitle_path = sys.argv[2]

    # If two arguments are given, but in the wrong order, sort them out.
    if not subtitle_path.endswith(".srt"):
        subtitle_path = sys.argv[1]
        tocast = sys.argv[2]

    log("Subtitle path is " + subtitle_path)


# Assuming user wants to search for subtitles, but no specific file was given
if search_for_subtitles and len(sys.argv) == 2:

    file_path = sys.argv[1]

    filename = os.path.split(file_path)[1]
    base_path = os.path.split(file_path)[0]

    # We have to assume that the subtitle file has the same name as the file
    # This line "trims" the file extenstion, and appends "srt."
    default_subtitle = filename[:(filename.rfind("."))] + ".srt"

    files = [file for file in os.listdir(base_path)]
    for f in files:
        if default_subtitle == file:
            log("Subtitle match was found at " + file)
            subtitle_path = default_subtitle


# Handle case where rcast is run from another directory
path = os.path.split(tocast)[0]

if(path is not ""):
    os.chdir(path)

filename = os.path.split(tocast)[1]
subtitle_path = os.path.split(subtitle_path)[1]

PORT = 8080


class MyTCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = MyTCPServer(("", PORT), Handler)

thread.start_new_thread(httpd.serve_forever, ())

encoded_string = urllib.quote_plus("http://localhost:8080/"+filename)

log("The encoded string is " + encoded_string)

full_url = "http://"+ip+"/stream?url="+encoded_string

# If subtitle exists, append it to the URL to send.
if subtitle_path is not "":
    sub_string = urllib.quote_plus("http://localhost:8080/" + subtitle_path)
    full_url += "&subtitles=" + sub_string


log("-----------------------------")
log("Do not close this program while playing the file")
log("Press Ctrl+C to stop")
log("-----------------------------")

urllib2.urlopen(full_url).read()
# We don't want to quit directly, pause until Ctrl+C
signal.pause()
