#!/usr/bin/env python

from bottle import *
from process import *
from json import dumps
import os
import logging

#Setting log
logging.basicConfig(filename='RaspberryCast.log',level=logging.DEBUG)
logger = logging.getLogger(" | RaspberryCast | ")

#Printing-like log
os.system("rm RaspberryCast.log >/dev/null 2>&1")
os.system("touch RaspberryCast.log")
os.system("tail -f RaspberryCast.log &")

#Trying to create the FIFO if it is the 1st time
os.system("mkfifo /tmp/cmd >/dev/null 2>&1")

#os.system("cat images/cast.asc | wall")
logger.info('START: RaspberryCast web server started.')

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
	logger.info('STREAM: Successfully received URL to cast: '+url)
	try :
		launchvideo(url, False)
		return "1"
	except Exception, e:
		logger.error('STREAM: Error in launchvideo function.')
		logger.exception(e)
		#os.system("cat images/error.asc | wall")
		return "0"

@app.route('/queue')
def queue():
	response.headers['Access-Control-Allow-Origin'] = '*'
	url = request.query['url']
	
	if is_running() == True :
		logger.info('QUEUE: Video currently playing, adding URL to queue: '+url)

		#Writing url to queue file
		with open('video.queue', 'a') as f:
			f.write(url+'\n')
			return "1"
	else :
		logger.info('QUEUE: No video currently playing, casting URL: '+url)
		try :
			launchvideo(url, False)
			return "1"
		except Exception, e:
			logger.error('QUEUE: Error in launchvideo function.')
			logger.exception(e)
			#os.system("cat images/error.asc | wall")
			return "0"
	

@app.route('/popcorn')
def popcorn():
	response.headers['Access-Control-Allow-Origin'] = '*'
	logger.info('POPCORN: Starting popcorntime function.')

	url = request.query['url']
	logger.info('POPCORN: URL is :'+url)

	ip = request.environ['REMOTE_ADDR']
	logger.info('POPCORN: IP is :'+ip)

	port = url.split(":")[2]
	logger.info('POPCORN: Port is:'+port)

	url = "http://"+ip+":"+port
	logger.info('POPCORN: Final url:'+url)

	# Try to remove subtitle
	os.system("rm subtitle.srt &")
		
	try :
		os.system("wget http://"+ip+":9999/subtitle.srt")
		logger.info('POPCORN: Success with Wget ! Starting with subtitles.')
		try :
			launchvideo(url, True)
		except :
			logger.error('POPCORN: Error in launchvideo function (with subtitles).')
			#os.system("cat images/error.asc | wall")
	except :
		logger.info('POPCORN: Error with Wget, starting without subtitles.')
	
		try :
			launchvideo(url, False)
		except :
			logger.error('POPCORN: Error in launchvideo function (without subtitles).')
			#os.system("cat images/error.asc | wall")
	
	return "1"

@app.route('/video')
def video():
	response.headers['Access-Control-Allow-Origin'] = '*'
	control = request.query['control']
	if control == "pause" :
		logger.info('REMOTE: Command : pause')
		os.system("echo -n p > /tmp/cmd &")
		return "1"
	elif control == "stop" :
		logger.info('REMOTE: Command : stop')
		os.system("echo -n q > /tmp/cmd &")
		#os.system("cat images/stop.asc | wall")
		logger.info('REMOTE: Command : empty queue file')
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
				shutdown_command = "shutdown -h +" + str(time) + " now &"
				os.system(shutdown_command)
				logger.info("SHUTDOWN: Shutdown should be successfully programmed")
				return "1"
		except:
			logger.error("SHUTDOWN: Error in shutdown command parameter")
			return "0"

@app.route('/settings')
def settings():
	response.headers['Access-Control-Allow-Origin'] = '*'
	sound_output = request.query['audioout']
	logger.info("SETTINGS: Audio setting is :"+sound_output)
	mode_slow = request.query['modeslow']
	logger.info("SETTINGS: Mode slow setting is :"+mode_slow)
	os.system("sed -i '/low_mode/c\low_mode = "+mode_slow+"' config.py &")
	os.system("sed -i '/sound_output/c\sound_output = \""+sound_output+"\"' config.py &")
	return "1"

@app.route('/status')
def getlog():
	response.headers['Access-Control-Allow-Origin'] = '*'
	f = open('RaspberryCast.log', 'r')
	line = f.readline()[-1]
	if line:
		last_log = line
	return last_log

		
run(app, reloader=False, host='0.0.0.0', debug=True, quiet=True, port=2020)
