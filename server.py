#!/usr/bin/env python

from bottle import *
from process import *
import os 

#Trying to create the FIFO is it is the 1st time
os.system("mkfifo /tmp/cmd")

app = Bottle()

@app.route('/')
def index():
	return '''
	<a href='/video?control=pause'><button type='button'>Pause</button></a>  <a href='/video?control=stop'><button type='button'>Stop</button></a><br>
	<a href='/video?control=left'><button type='button'>&lt;</button></a>  <a href='/video?control=right'><button type='button'>&gt;</button></a><br><br>
	<a href='/sound?vol=more'><button type='button'>+</button></a>  <a href='/sound?vol=less'><button type='button'>-</button></a>'''


@app.route('/stream')	
def stream(): 
	url = request.query['url']	
	print url
	launchvideo(url)

@app.route('/video')
def video():
	control = request.query['control']
	if control == "pause" :
		os.system("echo -n p > /tmp/cmd")
	elif control == "stop" :
		os.system("echo -n q > /tmp/cmd")
	elif control == "right" :
		os.system("echo -n $'\x1b\x5b\x43' > /tmp/cmd")
	elif control == "left" :
		os.system("echo -n $'\x1b\x5b\x44' > /tmp/cmd")

@app.route('/sound')
def sound():
	vol = request.query['vol']
	print vol + " volume"
	if vol == "more" :
		os.system("amixer set PCM playback 3db+")
		os.system("echo -n + > /tmp/cmd")
	elif vol == "less" :
		os.system("amixer set PCM playback 3db-")
		os.system("echo -n - > /tmp/cmd")
	
run(app, reloader=False, host='0.0.0.0', debug=True, port=2020)

