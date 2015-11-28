#!/usr/bin/env python

from gi.repository import Gtk, GdkPixbuf, Gdk
import urllib, urllib2, os, thread, socket, base64
from bottle import route, run, static_file

TARGET_TYPE_URI_LIST = 80

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
localip = s.getsockname()[0]
s.close()

def serve(path, a):
    @route('/<filename>')
    def static(filename):
        fileN = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        return static_file(base64.b32decode(fileN)+extension, root=os.path.split(path)[0])

    run(host='0.0.0.0', port=8080, debug=True)

def entryChange(widget):
    with open('.raspberrycastIP', 'w+') as f:
        f.write(widget.get_text())

def get_file_path_from_dnd_dropped_uri(uri):
    # get the path to file
    path = ""
    if uri.startswith('file:\\\\\\'): # windows
        path = uri[8:] # 8 is len('file:///')
    elif uri.startswith('file://'): # nautilus, rox
        path = uri[7:] # 7 is len('file://')
    elif uri.startswith('file:'): # xffm
        path = uri[5:] # 5 is len('file:')

    path = urllib.url2pathname(path) # escape special chars
    path = path.strip('\r\n\x00') # remove \r\n and NULL

    return path

def on_drag_data_received(widget, context, x, y, selection, target_type, timestamp):
    if target_type == TARGET_TYPE_URI_LIST:
        uri = selection.get_data().strip('\r\n\x00')
        print 'uri', uri
        uri_splitted = uri.split() # we may have more than one file dropped
        for uri in uri_splitted:
            path = get_file_path_from_dnd_dropped_uri(uri)
            print 'path to open', path
            if os.path.isfile(path): # is it file?
                data = file(path).read()
                #print data
            thread.start_new_thread( serve, (path, 1) )
            filename = os.path.splitext(os.path.split(path)[1])[0]
            extension = os.path.splitext(path)[1]
            encoded_string = urllib.quote_plus("http://"+localip+":8080/"+base64.b32encode(filename)+extension)
            full_url = "http://"+w.entry.get_text()+":2020/stream?url="
            if os.path.isfile(os.path.splitext(path)[0]+".srt"):
                urllib2.urlopen(full_url+encoded_string+"&subtitles="+urllib.quote_plus("http://"+localip+":8080/"+base64.b32encode(os.path.splitext(os.path.split(path)[1])[0]))+".srt").read()
            else: 
                urllib2.urlopen(full_url+encoded_string).read()

w = Gtk.Window(title="RaspberryCast", border_width=10)

vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
w.add(vbox)

w.text = Gtk.Label("Drag and drop a media file\n\nKeep this window open while \nthe media is playing", justify=Gtk.Justification.CENTER)
w.entry = Gtk.Entry()

try:
    with open('.raspberrycastIP', 'r') as f:
        w.entry.set_text(f.read())
except:
    w.entry.set_text("192.168.0.0")

w.entry.connect("changed", entryChange)
vbox.add(w.text)
vbox.add(w.entry)

w.connect('drag_data_received', on_drag_data_received)
w.connect("destroy", Gtk.main_quit, "WM destroy")

w.drag_dest_set( Gtk.DestDefaults.MOTION|
                  Gtk.DestDefaults.HIGHLIGHT | Gtk.DestDefaults.DROP,
                  [Gtk.TargetEntry.new("text/uri-list", 0, 80)], Gdk.DragAction.COPY)


w.show_all()
Gtk.main()
