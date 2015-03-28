#!/usr/bin/env python

import subprocess, re
from process import *
from time import sleep

while 1:
    #Playlist management
	if is_running() == False:
		with open('video.queue', 'r') as f:
			first_line = f.readline()
			if first_line != "" :
				print "No video currently playing, starting next into queue. "+first_line
				launchvideo(first_line, False)
				with open('video.queue', 'r') as fin:
					data = fin.read().splitlines(True)
				with open('video.queue', 'w') as fout:
   					 fout.writelines(data[1:])				    
	sleep(1)
