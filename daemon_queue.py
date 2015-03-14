#!/usr/bin/env python

import subprocess, re
from process import *
from time import sleep

while 1:
	if is_running("omxplayer.bin") == False:
		with open('video.queue', 'r') as f:
			first_line = f.readline()
			if first_line != "" :
				print "Lancement de la video ! "+first_line
				launchvideo(first_line)
				with open('video.queue', 'r') as fin:
					data = fin.read().splitlines(True)
				with open('video.queue', 'w') as fout:
   					 fout.writelines(data[1:])				
	sleep(1)
