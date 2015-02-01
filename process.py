#!/usr/bin/env python

import subprocess, os, signal, sys

def launchvideo(url):
	try:
		if url[0:14] in ("https://youtu.", "http://youtu.b", "https://www.yo", "http://www.you", "http://youtub", "http://youtube") :
			print "Youtube, setting to 360p"
			command = "youtube-dl -f 18 -g "
		elif url[0:12] in ("https://vime", "http://vimeo") :
			print "Vimeo, setting to 360p"
			command = "youtube-dl -f h264-sd -g "
		else :
			command = "youtube-dl -g "
	
		proc = subprocess.Popen(command+url, stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		print "program output:", out	
		#os.system('echo "Video link is ' + out + '" | wall')
		out = out.rstrip()
	
		try: 
                        os.killpg(omxplay.pid, signal.SIGTERM)

		except:
			print "No videos currently playing"
			pass

		omx = "omxplayer -b -o local '"+out+"' < /tmp/cmd"
		print omx
		omxplay = subprocess.Popen(omx, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

		os.system("echo . > /tmp/cmd")

	except (KeyboardInterrupt, SystemExit):
		try:
			os.system("echo -n q > /tmp/cmd")
			os.killpg(omxplay.pid, signal.SIGTERM)
			os.system("killall omxplayer.bin")
		except:
			pass
                exit()

