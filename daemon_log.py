#!/usr/bin/env python

import subprocess, re
from process import *
from time import sleep
import logging
logger = logging.getLogger(" | RaspberryCast | ")

#
# Functionality/file not used at the moment.
#

sleep(1)

f = open('RaspberryCast.log', 'r')
size = os.path.getsize('RaspberryCast.log')

while 1:
    #Log management
	if os.path.getsize('RaspberryCast.log') == size:
		line = f.readline()
		if line:
			print "Log: " + line
			size = os.path.getsize('RaspberryCast.log')
	sleep(0.2)