# -*- coding: utf-8 -*-

#Author: Jason Hou
#Date: 2013/06/20

############################ CHANGE HISTORY ############################

# VERSION : 0.3 Third Release 20-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. add more trace info
#				2. update getView method, add 'dump' parameter 
#				3. update goEdit method and return current contact counter
#				4. new add stop, slide, goList and wipe method

# VERSION : 0.2 Second Release 18-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. add change history and function document string
#				2. update getView(), isReady() method
#				3. update the isEmpty() to goEdit() to avoid the misunderstanding
#				4. new add back, check method

# VERSION : 0.1 First Release 16-Jun-13 Jason Hou
# REASON : First implementation
# REFERENCE : 
# DESCRIPTION : 1. Create the basic contacts module framework
#				2. encapsulate the findView method using method getView()

############################ CHANGE HISTORY ############################

__version__ = '0.3'

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

logPath = r'C:\Users\cninjaho\Desktop'
logName = 'case_log.txt'
logFile = logPath + '\\' + logName

trace = trace(logFile).trace

package = 'com.android.contacts'
activity = '.activities.PeopleActivity'
componentName = package + '/' + activity
	
def sleep(duration = 1):
	'''
	Monkey sleep
	
	@type duration: int
	@param duration: how long to sleep
	'''
	MonkeyRunner.sleep(duration)
	
class contacts:
	'''
	contacts class
	'''
	def __init__(self, device, devID='emulator-5554',sample = False):
		'''
		constructor
		
		@type device: MonkeyDevice
        @param device: The device or emulator connected
		@type devID: str
        @param serialno: the serial number of the device or emulator to connect to
		@type sample: boolean
		@param sample: whether take snapshot as an sampling
		'''
		self.device=device
		self.sample=sample
		self.contactCounter=0
		self.startStatus=False
		'''the status which indicate whether the contacts activity is started'''
		
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
		
		#define the point used to slide screen
		self.left = (width/4, height/2)
		self.right = (width/4*3, height/2)
		self.up = (width/2, height/4)
		self.down = (width/2, height/4*3)
		self.center = (width/2, height/2)
		
		trace('before instance')
		self.vc=ViewClient(device, devID)
		trace('after instance')
		
	def start(self):
		'''
		start the contacts activity and set the startStatus True if contacts is ready.
		'''
		trace('before start activity')
		self.device.startActivity(component=componentName)
		trace('contacts is starting, checking the status...')
		sleep(2)
		trace('before check status')
		self.startStatus = self.isReady()
		trace('after check status')
	
	def stop(self):
		'''
		stop the contacts activity and set the startStatus False
		'''
		self.device.shell('am force-stop %s' % package)
		trace('force stop contacts package %s' % package)
		self.startStatus = False
	
	def back(self):
		'''
		press back
		'''
		self.device.press('KEYCODE_BACK','DOWN_AND_UP')
		trace('press back')
		
	def slide(self,str):
		'''
		slide the screen
		
		@type: str
		@param: 'left','right','up','down'
		'''
		if str not in ['left','right','up','down']:
			raise SyntaxError("wrong parameter: choose from 'left','right','up' or 'down'")
		nav = {
			'left':{'start':self.right,'end':self.left},
			'right':{'start':self.left,'end':self.right},
			'up':{'start':self.down,'end':self.up},
			'down':{'start':self.up,'end':self.down}
			}
		self.device.drag(nav[str]['start'], nav[str]['end'], 0.1, 1)
		trace('slide the screen from %s to %s ' % (nav[str]['start'],nav[str]['end']))
		sleep(1)
		
	def getView(self,str,cD=False,iD=False,dump=True):
		'''
		get the view with the specified text, content description or viewId
		@type str: str
		@param str: the query string
		@type cD: boolean
		@param cD: whether handle the query str as content description
		@type iD: boolean
		@param iD: whether handle the query str as viewId
		@type dump: boolean
		@param dump: whether execute dump before findView, depending on whether the screen is changed
		
		@return: the view found
		'''
		if dump:
			trace('before dump')
			self.vc.dump()
			trace('after dump')

		if not cD:
			if not iD:
				trace('return view with text: %s' % str)
				return self.vc.findViewWithText(str)
			else:
				trace('return view with id: %s ' % str)
				return self.vc.findViewById(str)
		else:
			trace('return view with content description: %s ' % str)
			return self.vc.findViewWithContentDescription(str)
			
	def isReady(self):
		'''
		check whether the contacts is ready.
		'''
		while True:
			view=self.getView('Contact list is being updated to reflect the change of language.')
			if not view:
				trace('Contacts is ready')
				break
			else:
				trace('Contacts is not ready, please wait!')
				sleep(2)
		return True
	
	def goList(self):
		'''
		check whether the screen is in contacts list view, if not, go list view via pressing back key
		
		@return: the search Text View
		'''
		self.check()
		while True:
			view=self.getView("Search",cD=True)
			if not view:
				self.back()
				sleep(2)
			else:
				break
		return view
		
	def goEdit(self):
		'''
		check whether the contact is empty, then select adding and go to edit view.
		
		@return: current contacts counter
		'''
		self.check()
		view=self.getView('Create a new contact',dump=False)
		if view:
			self.contactCounter = 0
			view.touch()
			trace('Click "Create a new contact"')
			sleep(3) 
			view=self.getView('Keep local')
			if view:
				view.touch()
				trace('Select "Keep local"')
				sleep(2)
		else:
			self.contactCounter = int(self.getView('id/no_id/21',iD=True,dump=False).getText().split(' ')[0])
			#get the current contact counter
			view=self.getView('Add Contact',cD=True,dump=False)
			view.touch()
			trace('Click "Add Contact"')
			sleep(3)
		trace('current contacts counter is %d' % self.contactCounter)
		self.vc.dump()
		return self.contactCounter
		
	def check(self):
		'''
		check whether the contacts is started before other operation about contacts
		
		@return: True
		'''
		if not self.startStatus:
			trace("Wrong code! please start contacts firstly in you code")
			raise SyntaxError('contacts should be start firstly!')
		return True
		
	def snapshot(self,title):
		'''
		take snapshot
		@type title: str
		@param title: specify the title of snapshot
		
		@return: snapshot object
		'''
		snapName = title + '.png' 
		snapFile = logPath + '\\' + snapName
		result = self.device.takeSnapshot().getSubImage(self.snap_rect)
		trace('take snapshot without the statusbar')
		result.writeToFile(snapFile,'png')
		trace('save the snapshot to file: %s ' % snapfile)
		return result
	
	def wipe(self,view):
		'''
		wipe the text in specified view
		'''
		try:
			self.device.drag(view.getXY(),view.getXY(),1,1)
			self.device.press('KEYCODE_DEL','DOWN_AND_UP')
			trace('wipe text: %s ' % view.getText())
		except:
			Exception('wipe failed')
	
	def addContact(self,name='',phone='',email='',address=''):
		#notice firstly call self.goEdit()
		self.goEdit()
		try:
			offset = 0
			if name:
				view=self.getView('id/no_id/27',iD=True,dump=False)
				view.type(name)
				trace('type %s ' % name)
				sleep(3)
			if phone:
				view=self.getView('id/no_id/46',iD=True,dump=False)
				view.type(phone)
				trace('type %s ' % phone)
				sleep(3)
			if email:
				offset += 4 if phone else 0
				view=self.getView('id/no_id/' + str(57 + offset), iD=True)
				view.type(email)
				trace('type %s ' % email)
				sleep(3)
			if address:
				offset += 4 if phone else 0
				view=self.getView('id/no_id/' + str(68 + offset), iD=True)
				view.type(address)
				trace('type %s ' % address)
				sleep(3)
			view=self.getView('Done',dump=False)
			view.touch()
			trace('Click Done')
			sleep(2)
			self.goList()
			trace('return contact list view')
			sleep(2)
			
		except Exception,e:
			trace(str(e))
			
	def editDetails(self,phone=''):
		pass
	
	def search(self,str):
		pass
	
	def sort(self):
		pass
		
	def favorite(self,name=''):
		pass
		
if __name__ == '__main__':
	device=MonkeyRunner.waitForConnection()
	trace('start testing...')
	c=contacts(device)
	trace('complete init')
	c.slide('left')
	c.slide('right')
	c.start()
	trace('complete contacts activity starting')
	c.addContact(name='jason',phone='123',email='a@b.c')
	# c.editDetails(phone='456')
	# c.search('jason')
	# c.sort()
	# c.favorite('jason')
	trace('end testing')