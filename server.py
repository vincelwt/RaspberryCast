#!/usr/bin/env python

from bottle import *
from process import *
import os

#Trying to create the FIFO is it is the 1st time
os.system("mkfifo /tmp/cmd")

os.system("cat images/cast.asc | wall")

app = Bottle()


SimpleTemplate.defaults["get_url"] = app.get_url

@app.route('/static/<filename>', name='static')
def server_static(filename):
	return static_file(filename, root='static')
	
@app.route('/')
def index():
	return template('index')


@app.route('/stream')	
def stream(): 
	url = request.query['url']	
	print "casting now : " + url
	launchvideo(url, False)

@app.route('/queue')
def queue():
        url = request.query['url']
	if is_running() == True :
		print "adding to queue : " + url
		#Writing url to file
		with open('video.queue', 'a') as f:
			f.write(url+'\n')
	else :
		print "casting now : " + url
		launchvideo(url, False)

@app.route('/popcorn')
def queue():
        url = request.query['url']
	ip = request.environ['REMOTE_ADDR']
	port = url.split(":")[2]
	url = "http://"+ip+":"+port

	print "downloading subtitle"

	# Try to remove subtitle	
	os.system("rm subtitle.srt")
	wget = "wget http://"+ip+":9999/subtitle.srt"
	os.system(wget)

	launchvideo(url, True)

@app.route('/video')
def video():
	control = request.query['control']
	if control == "pause" :
		os.system("echo -n p > /tmp/cmd")
	elif control == "stop" :
		os.system("echo -n q > /tmp/cmd")
		os.system("cat images/stop.asc | wall")
	elif control == "right" :
		os.system("echo -n $'\x1b\x5b\x43' > /tmp/cmd")
	elif control == "left" :
		os.system("echo -n $'\x1b\x5b\x44' > /tmp/cmd")
	elif control == "emptyqueue" :
		#Empty queue file
		open('video.queue', 'w').close()

@app.route('/sound')
def sound():
	vol = request.query['vol']
	print vol + " volume"
	if vol == "more" :
		os.system("echo -n + > /tmp/cmd")
	elif vol == "less" :
		os.system("echo -n - > /tmp/cmd")
	
run(app, reloader=False, host='0.0.0.0', debug=True, port=2020)
