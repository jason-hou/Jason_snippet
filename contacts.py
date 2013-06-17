# -*- coding: utf-8 -*-

#Author: Jason Hou
#Date: 2013/06/16
import os,sys
try:
    for p in os.environ['PYTHONPATH'].split(';'):
       if not p in sys.path:
          sys.path.append(p)
except:
    pass

from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage
from com.dtmilano.android.viewclient import ViewClient
from log import trace

logPath = r'C:\Users\Jason\Desktop'
logName = 'case_log.txt'
logFile = logPath + '\\' + logName

trace = trace(logFile).trace

package = 'com.android.contacts'
activity = '.activities.PeopleActivity'
componentName = package + '/' + activity
	
def sleep(duration = 1):
	MonkeyRunner.sleep(duration)

class contacts:
	def __init__(self, device, devID='emulator-5554',sample = False):
		'''if sample is True, take snapshot as expected result.'''
		self.device=device
		self.sample=sample
		self.vc=ViewClient(device, devID)
		#use below code to remove the status bar from the snapshot
		width = int(device.getProperty('display.width'))
		height = int(device.getProperty('display.height'))
		density = device.getProperty('display.density')
		if density == .75:
			statusBarHeight = 19
		elif density == 1.5:
			statusBarHeight = 38
		elif density == 2.0:
			statusBarHeight = 50
		else:
			statusBarHeight = 25
		self.snap_rect = 0, statusBarHeight, width, height - statusBarHeight

	def start(self):
		self.device.startActivity(component=componentName)
	
	def getView(self,str,ContentDescription=False):
		self.vc.dump()
		if not contentDescription:
			return self.vc.getViewWithText(str)
		else:
			return self.vc.findViewWithContentDescription(str)
			
	def isReady(self):
		while True:
			view=self.getView('Contact list is being updated to reflect the change of language.')
			if not view: break
			sleep(2)
		return True
	
	def isEmpty(self):
		view=self.getView('Create a new contact')
		if view:
			view.touch()
			view=self.getView('Keep local')
			if view:
				view.touch()
				return True
			else:
				return True
		else:
			view=self.getView('Add Contact',True)
			view.touch()
			return True
	def snapshot(self,title):
		snapName = title + '.png' 
		snapFile = logPath + '\\' + snapName
		result = self.device.takeSnapshot().getSubImage(self.snap_rect)
		result.writeToFile(snapFile,'png')
	
	def addContact(self):
		trace('start...')
		self.start()
		sleep(3)
		trace('take snapshot')
		self.snapshot('contact_snap')
		
	def editDetails(self):
		pass
	
	def search(self):
		pass
	
	def sort(self):
		pass
		
	def favorite(self):
		pass
		
if __name__ == '__main__':
	device=MonkeyRunner.waitForConnection()
	print 'test'
	c=contacts(device)
	c.addContact()