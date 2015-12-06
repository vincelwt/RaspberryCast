#!/usr/bin/env python

from bottle import *
from process import *
from daemon_state import *
import os
import logging
import sys
import urllib

#Setting log
logging.basicConfig(filename='RaspberryCast.log',level=logging.DEBUG)
logger = logging.getLogger(" | RaspberryCast | ")

if new_log == False :
	#Creating handler to print messages on stdout
	root = logging.getLogger()
	root.setLevel(logging.DEBUG)

	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	ch.setFormatter(formatter)
	root.addHandler(ch)
else :
	StartDialogLog()


#Reset log
os.system("rm RaspberryCast.log >/dev/null 2>&1")
os.system("touch RaspberryCast.log")

logger.info('START: RaspberryCast successfully started!')

app = Bottle()

SimpleTemplate.defaults["get_url"] = app.get_url

@app.route('/static/<filename>', name='static')
def server_static(filename):
	return static_file(filename, root='static')

@app.route('/')	
@app.route('/remote')
def remote():
	logger.debug('REMOTE: Template requested.')
	return template('remote')

@app.route('/stream')	
def stream(): 
	response.headers['Access-Control-Allow-Origin'] = '*'
	url = request.query['url']	
	logger.debug('STREAM: Successfully received URL to cast: '+url)

	try :
		if 'subtitles' in request.query:
			subtitles = request.query['subtitles']
			logger.debug('STREAM: Subtitles link is '+subtitles)
			urllib.urlretrieve(subtitles, "subtitle.srt")
			launchvideo(url, True, False)
		else:
			logger.debug('STREAM: No subtitles for this stream')
			if 'slow' in request.query:
				if request.query['slow'] == "True":
					launchvideo(url, False, True)
					return "1"
			
			launchvideo(url, False, False)
			return "1"
	except Exception, e:
		logger.error('STREAM: Error in launchvideo function or during downlading the subtitles')
		logger.exception(e)
		return "0"

@app.route('/queue')
def queue():
	response.headers['Access-Control-Allow-Origin'] = '*'
	url = request.query['url']
	
	if state() != "0" :
		logger.info('QUEUE: Adding URL to queue: '+url)

		#Writing url to queue file
		with open('video.queue', 'a') as f:
			f.write(url+'\n')
			return "1"
	else :
		logger.info('QUEUE: No video currently playing, casting URL: '+url)
		try :
			launchvideo(url, False, True)
			return "1"
		except Exception, e:
			logger.error('QUEUE: Error in launchvideo function.')
			logger.exception(e)
			#os.system("cat images/error.asc | wall")
			return "0"

@app.route('/video')
def video():
	response.headers['Access-Control-Allow-Origin'] = '*'
	control = request.query['control']
	if control == "pause" :
		logger.info('REMOTE: Command : pause')
		os.system("echo -n p > /tmp/cmd &")
		return "1"
	elif control == "stop" :
		logger.info('REMOTE: Command : stop video')
		os.system("echo -n q > /tmp/cmd &")
		#os.system("cat images/stop.asc | wall")
		logger.debug('REMOTE: Command : empty queue file')
		#Empty queue file
		open('video.queue', 'w').close()
		return "1"
	elif control == "right" :
		logger.info('REMOTE: Command : forward')
		os.system("echo -n $'\x1b\x5b\x43' > /tmp/cmd &")
		return "1"
	elif control == "left" :
		logger.info('REMOTE: Command : backward')
		os.system("echo -n $'\x1b\x5b\x44' > /tmp/cmd &")
		return "1"
	elif control == "next" :
		logger.info('REMOTE: Command : next video in queue')
		os.system("echo -n q > /tmp/cmd &")
		return "1"

@app.route('/sound')
def sound():
	response.headers['Access-Control-Allow-Origin'] = '*'
	vol = request.query['vol']
	logger.info("REMOTE: Change requested: " + vol)
	
	if vol == "more" :
		logger.info('REMOTE: Command : Sound ++')
		os.system("echo -n + > /tmp/cmd &")
	elif vol == "less" :
		logger.info('REMOTE: Command : Sound --')
		os.system("echo -n - > /tmp/cmd &")
	return "1"

@app.route('/shutdown')
def shutdown():
	response.headers['Access-Control-Allow-Origin'] = '*'
	time = request.query['time']
	if time == "cancel":
		os.system("shutdown -c")
		logger.info("SHUTDOWN: Shutdown canceled.")
		return "1"
	else:	
		try:
			time = int(time)
			if (time<400 and time>=0):
				shutdown_command = "shutdown -h +" + str(time) + " &"
				os.system(shutdown_command)
				logger.info("SHUTDOWN: Shutdown should be successfully programmed")
				return "1"
		except:
			logger.error("SHUTDOWN: Error in shutdown command parameter")
			return "0"
			
@app.route('/running')
def webstate():
	response.headers['Access-Control-Allow-Origin'] = '*'
	logger.debug("RUNNING: Running state as been asked.")
	return state()
		
run(app, reloader=False, host='0.0.0.0', debug=True, quiet=True, port=2020)
