# -*- coding: utf-8 -*-

#Author: Jason Hou
#Date: 2013/06/07
import os,sys
try:
    for p in os.environ['PYTHONPATH'].split(';'):
       if not p in sys.path:
          sys.path.append(p)
except:
    pass

from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage
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
	def __init__(self, device, sample = False):
		'''if sample is True, take snapshot as expected result.'''
		self.device=device
		self.sample=sample
		
	def start(self):
		self.device.startActivity(component=componentName)
	
	def snapshot(self,title):
		snapName = title + '.png' 
		snapFile = logPath + '\\' + snapName
		result = self.device.takeSnapshot()
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