#!/usr/bin/env python

from config import *
import logging, os, sys

#Setting log
logging.basicConfig(filename='RaspberryCast.log', format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%m-%d %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger("RaspberryCast")

#Creating handler to print messages on stdout
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

if new_log == True:
    os.system("sudo fbi -T 1 --noverbose -a  images/ready.jpg &")

from bottle import *
from process import *
import urllib

setState("0")
logger.info('Server successfully started!')

app = Bottle()

SimpleTemplate.defaults["get_url"] = app.get_url

@app.route('/static/<filename>', name='static')
def server_static(filename):
	return static_file(filename, root='static')

@app.route('/')	
@app.route('/remote')
def remote():
	logger.debug('Remote page requested.')
	return template('remote')

@app.route('/stream')	
def stream(): 
	response.headers['Access-Control-Allow-Origin'] = '*'
	url = request.query['url']	
	logger.debug('Received URL to cast: '+url)

	try :
		if 'subtitles' in request.query:
			subtitles = request.query['subtitles']
			logger.debug('Subtitles link is '+subtitles)
			urllib.urlretrieve(subtitles, "subtitle.srt")
			launchvideo(url, True, False)
		else:
			logger.debug('No subtitles for this stream')
			if 'slow' in request.query:
				if request.query['slow'] in ["True", "true"]:
					launchvideo(url, False, True)
					return "1"
			
			launchvideo(url, False, False)
			return "1"
	except Exception, e:
		logger.error('Error in launchvideo function or during downlading the subtitles')
		logger.exception(e)
		return "0"

@app.route('/queue')
def queue():
	response.headers['Access-Control-Allow-Origin'] = '*'
	url = request.query['url']

	with open('state.tmp', 'r') as f:
		currentState = f.read().replace('\n', '')
	
	if currentState != "0" :
		logger.info('Adding URL to queue: '+url)
		with open('video.queue', 'a') as f:
			f.write(url+'\n')
			return "1"
	else :
		logger.info('No video currently playing, playing url : '+url)
		try :
			launchvideo(url, False, True)
			return "1"
		except Exception, e:
			logger.error('Error in launchvideo function !')
			logger.exception(e)
			return "0"

@app.route('/video')
def video():
	response.headers['Access-Control-Allow-Origin'] = '*'
	control = request.query['control']
	if control == "pause" :
		logger.info('Command : pause')
		os.system("echo -n p > /tmp/cmd &")
		return "1"
	elif control in ["stop", "next"] :
		logger.info('Command : stop video')
		os.system("echo -n q > /tmp/cmd &")
		return "1"
	elif control == "right" :
		logger.info('Command : forward')
		os.system("echo -n $'\x1b\x5b\x43' > /tmp/cmd &")
		return "1"
	elif control == "left" :
		logger.info('Command : backward')
		os.system("echo -n $'\x1b\x5b\x44' > /tmp/cmd &")
		return "1"

@app.route('/sound')
def sound():
	response.headers['Access-Control-Allow-Origin'] = '*'
	vol = request.query['vol']
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
	with open('state.tmp', 'r') as f:
		currentState = f.read().replace('\n', '')
	logger.debug("RUNNING: Running state as been asked : "+currentState)
	return currentState
		
run(app, reloader=False, host='0.0.0.0', debug=True, quiet=True, port=2020)
