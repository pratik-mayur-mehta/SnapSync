#!/usr/bin/python

import os
import httplib2
import pprint
import datetime
import time
import logging
import watchdog
import watchdog.events
import sys
import webbrowser

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from apiclient import errors
from oauth2client.file import Storage
from Foundation import NSUserNotification
from Foundation import NSUserNotificationCenter
from Foundation import NSUserNotificationDefaultSoundName
from Foundation import NSAutoreleasePool
from optparse import OptionParser
from oauth2client.client import SignedJwtAssertionCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from apiclient import sample_tools

path = os.path.expanduser('~/Screenshots')

try:
	os.makedirs(path, 0777)

except OSError:
    if not os.path.isdir(path):
        raise

os.system("defaults write com.apple.screencapture location %s" % path)
os.system("killall SystemUIServer")

CRED_FILENAME ='credentials.json'

URL_SCOPE = 'https://www.googleapis.com/auth/urlshortener'

storage = Storage(CRED_FILENAME)

if not os.path.exists(CRED_FILENAME) :
	gauth = GoogleAuth()
	gauth.LocalWebserverAuth()

credentials = storage.get()

http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)
url_service, flags = sample_tools.init(sys.argv ,'urlshortener', 'v1', __doc__, __file__, URL_SCOPE)

def mac_notifications():
    parser = OptionParser(usage='%prog -t TITLE -m MESSAGE')
    parser.add_option('-t', '--title', action='store', default='Link Copied')
    parser.add_option('-m', '--message', action='store', default="""A Link has been Successfully Copied to Your Clipboard. Kindly Paste and Save it.""")
    parser.add_option('--no-sound', action='store_false', default=True, dest='sound')

    options, args = parser.parse_args()
                      
    pool = NSAutoreleasePool.alloc().init()
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(options.title)
    notification.setInformativeText_(options.message)
    if options.sound:
        notification.setSoundName_(NSUserNotificationDefaultSoundName)
                      
    center = NSUserNotificationCenter.defaultUserNotificationCenter()
    center.deliverNotification_(notification)
                      
    del notification
    del pool


def url_shortener(file):
	long_url = "https://docs.google.com/file/d/" + file['id']
	try:
		url = url_service.url()
		request = {
    	'longUrl': long_url
    	}
    	response = url.insert(body=request).execute()
    	print response
    	copy_to_clipboard(response)

	except client.AccessTokenRefreshError:
		print ('The credentials have been revoked or expired, please re-run' 
			'the application to re-authorize')


def copy_to_clipboard(shortened_url):
	os.system("echo %s | pbcopy" % shortened_url)
	mac_notifications()


def upload(FILENAME):
    
	title = FILENAME
    
	media_body = MediaFileUpload(path + "/" + FILENAME, mimetype='image/png', resumable=True)
	body = {
 	'title': title,
 	'description': 'Screen Shot',
 	'mimeType': 'image/png'
	}
    
	file = drive_service.files().insert(body=body, media_body=media_body).execute()
    
	new_permission = {
        'type': 'anyone',
        'role': 'reader'
	}
    
	try:
		drive_service.permissions().insert(
                                           fileId=file['id'], body=new_permission).execute()
	except errors.HttpError, error:
	    print 'An error occurred: %s' % error
    
	url_shortener(file)

def delete(FILENAME) :
	items = drive_service.files().list(q = "title = '%s'" % FILENAME).execute()['items']
	for files in items:
		fileId = files['id']
		try :
			drive_service.files().delete(fileId=fileId).execute()
		except errors.HttpError, error:
			print 'An error occurred: %s' % error


def getext(filename):
    
    return os.path.splitext(filename)[-1].lower()


class MyEventHandler (FileSystemEventHandler) :
    
	def on_created(self, event):
		if getext(event.src_path) == '.png':
			FILENAME = event.src_path
			upload(FILENAME[len(path) + 1 : ])
    
	def on_moved(self, event):
		if getext(event.dest_path) == '.png':
			FILENAME = event.dest_path
			upload(FILENAME[len(path) + 1 : ])syn
    
	def on_deleted(self, event):
		if getext(event.src_path) == '.png':
			FILENAME = event.src_path
			delete(FILENAME[len(path) + 1 : ])


if __name__ == "__main__":
    
	event_handler = MyEventHandler()
    
	observer = Observer()
	observer.schedule(event_handler, path=path, recursive=False)
	observer.start()
    
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
