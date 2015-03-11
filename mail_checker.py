#!/usr/bin/env python
 
import feedparser, time, subprocess, os, signal
from process import * 

USERNAME = "gmailbefore@"
PASSWORD = "gmailpassword"
d = feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom")
NEWMAIL_OFFSET = int(d.feed.fullcount)
MAIL_CHECK_FREQ = 5

os.system('echo "---------------------------- Waiting for new mails. ------------------------" | wall')
 
while 1:
	try:

		d = feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom")

		newmails = int(d.feed.fullcount)

		if newmails > NEWMAIL_OFFSET:
			print "New message"
			os.system('echo "New message" | wall')
			content = d.entries[0].summary_detail.value
			print content
			where_to_cut = content.find("http")
			content = content[where_to_cut:]
			url = content.split(" ")[0]
			print url
			os.system('echo "URL: ' + url + '" | wall')
			launchvideo(url)
			
			NEWMAIL_OFFSET = newmails
		
		else:
			print "No new messages."

		time.sleep(MAIL_CHECK_FREQ)
	
	except (KeyboardInterrupt, SystemExit):
        	os.system("echo -n q > /tmp/cmd") 
                os.killpg(omxplay.pid, signal.SIGTERM)
                os.system("killall omxplayer.bin")

		exit()
