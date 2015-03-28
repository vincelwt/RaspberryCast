#!/usr/bin/env python

from bottle import *
from process import *
from json import dumps
import os
import logging

#Setting log
logging.basicConfig(filename='RaspberryCast.log',level=logging.DEBUG)

#Trying to create the FIFO if it is the 1st time
os.system("mkfifo /tmp/cmd >/dev/null 2>&1")

#os.system("cat images/cast.asc | wall")
logging.info('RaspberryCast started.')

app = Bottle()

SimpleTemplate.defaults["get_url"] = app.get_url

@app.route('/static/<filename>', name='static')
def server_static(filename):
	return static_file(filename, root='static')
	
@app.route('/remote')
def remote():
	return template('remote')


@app.route('/stream')	
def stream(): 
	response.headers['Access-Control-Allow-Origin'] = '*'
	url = request.query['url']	
	logging.info('Casting URL: '+url)
	try :
		launchvideo(url, False)
	except :
		logging.error('Error in launchvideo function.')
		#os.system("cat images/error.asc | wall")
	return "1"

@app.route('/queue')
def queue():
	response.headers['Access-Control-Allow-Origin'] = '*'
	url = request.query['url']
	
	if is_running() == True :
		logging.info('Adding to queue: '+url)

		#Writing url to file
		with open('video.queue', 'a') as f:
			f.write(url+'\n')
		return "1"
	else :
		logging.info('Casting URL (no video in queue): '+url)
		try :
			launchvideo(url, False)
		except :
			logging.error('Error in launchvideo function.')
			#os.system("cat images/error.asc | wall")
		return "1"
	

@app.route('/popcorn')
def popcorn():
	response.headers['Access-Control-Allow-Origin'] = '*'
	logging.info('Starting popcorntime function.')

	url = request.query['url']
	logging.info('URL is :'+url)

	ip = request.environ['REMOTE_ADDR']
	logging.info('IP is :'+ip)

	port = url.split(":")[2]
	logging.info('Port is:'+port)

	url = "http://"+ip+":"+port
	logging.info('Final url:'+url)

	# Try to remove subtitle
	os.system("rm subtitle.srt &")
		
	try :
		os.system("wget http://"+ip+":9999/subtitle.srt")
		logging.info('Success with Wget ! Starting with subtitles.')
		try :
			launchvideo(url, True)
		except :
			logging.error('Error in launchvideo function (with subtitles).')
			#os.system("cat images/error.asc | wall")
	except :
		logging.info('Error with Wget, starting without subtitles.')
	
		try :
			launchvideo(url, False)
		except :
			logging.error('Error in launchvideo function (without subtitles).')
			#os.system("cat images/error.asc | wall")
	
	return "1"

@app.route('/video')
def video():
	response.headers['Access-Control-Allow-Origin'] = '*'
	control = request.query['control']
	if control == "pause" :
		logging.info('Command : pause')
		os.system("echo -n p > /tmp/cmd &")
		return "1"
	elif control == "stop" :
		logging.info('Command : stop')
		os.system("echo -n q > /tmp/cmd &")
		#os.system("cat images/stop.asc | wall")
		logging.info('Command : empty queue file')
		#Empty queue file
		open('video.queue', 'w').close()
		return "1"
	elif control == "right" :
		logging.info('Command : forward')
		os.system("echo -n $'\x1b\x5b\x43' > /tmp/cmd &")
		return "1"
	elif control == "left" :
		logging.info('Command : backward')
		os.system("echo -n $'\x1b\x5b\x44' > /tmp/cmd &")
		return "1"

@app.route('/sound')
def sound():
	response.headers['Access-Control-Allow-Origin'] = '*'
	vol = request.query['vol']
	print vol + " volume"
	if vol == "more" :
		logging.info('Command : Sound ++')
		os.system("echo -n + > /tmp/cmd &")
	elif vol == "less" :
		logging.info('Command : Sound --')
		os.system("echo -n - > /tmp/cmd &")
	return "1"

@app.route('/shutdown')
def shutdown():
	response.headers['Access-Control-Allow-Origin'] = '*'
	time = request.query['time']
	if time == "cancel":
		os.system("shutdown -c")
		logging.info("Shutdown canceled.")
		return "1"
	else:	
		try:
			time = int(time)
			if (time<400 and time>=0):
				shutdown_command = "shutdown -h +" + str(time) + " now &"
				os.system(shutdown_command)
				logging.info("Shutdown should be successfully programmed")
		except:
			logging.error("Error in shutdown command parameter")
		return "1"

@app.route('/settings')
def settings():
	response.headers['Access-Control-Allow-Origin'] = '*'
	sound_output = request.query['audioout']
	print "Audio setting is :"+sound_output
	mode_slow = request.query['modeslow']
	print "Mode slow setting is :"+mode_slow
	os.system("sed -i '/low_mode/c\low_mode = "+mode_slow+"' config.py &")
	os.system("sed -i '/audio_output/c\sound_output = \""+sound_output+"\"' config.py &")
	return "1"

@app.route('/status')
def getlog():
	response.headers['Access-Control-Allow-Origin'] = '*'
	f = open('RaspberryCast.log', 'r')
	line = f.readline()[-1]
	if line:
		last_log = line
	return last_log

		
run(app, reloader=False, host='0.0.0.0', debug=True, port=2020)
