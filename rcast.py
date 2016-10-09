#!/usr/bin/env python

import urllib, urllib2, os, sys, thread, base64, signal, socket, SimpleHTTPServer, SocketServer

def signal_handler(signal, frame):
        print('You pressed Ctrl+C, stopping. Casting may continue for some time.')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ip = 'raspberrypi.local:2020'

tocast = sys.argv[1]

print "-----------------------------"
print "Casting "+tocast
print "-----------------------------"

if not os.path.isfile(tocast):
    print "File not found!"
    sys.exit(0)

print "Do not close this program while playing the file"
print "Press Ctrl+C to stop"
print "-----------------------------"

PORT = 8080

class MyTCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = MyTCPServer(("", PORT), Handler)

thread.start_new_thread( httpd.serve_forever, ())

filename = os.path.split(tocast)[1]

encoded_string = urllib.quote_plus("http://localhost:8080/"+filename)

full_url = "http://"+ip+"/stream?url="+encoded_string

#print "Calling "+full_url

urllib2.urlopen(full_url).read()

# We don't want to quit directly, pause until Ctrl+C
signal.pause()