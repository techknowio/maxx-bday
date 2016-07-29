#!/usr/bin/env python2.7
import pyinotify
import requests
mask = pyinotify.IN_CLOSE_WRITE
wm = pyinotify.WatchManager()

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        print "Creating:", event
	payload = {'party': 'maxx'}
        r = requests.post('http://thephotobooth.io/upload.php', files={'file': open(event.pathname, 'rb')},data=payload)

    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname

handler = EventHandler()
notifier = pyinotify.Notifier(wm,handler)
wm.add_watch('/home/pi/maxx-bday/images', mask,rec=True)
notifier.loop()
