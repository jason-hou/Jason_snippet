# -*- coding: utf-8 -*-

#Author: Jason Hou

#Date: 2013/06/24

############################ CHANGE HISTORY ############################

# VERSION : 0.9 Ninth Release 25-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. new add favor() method

# VERSION : 0.8 Seventh Release 24-Jun-13 Glen Fan
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION :	1. new add goEditExistContact(), slideByView(), editCompany(),\
#				editAnotherField(),editDetails() method

# VERSION : 0.7 Seventh Release 24-Jun-13 Faure Zhang
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION :	1. new add delete() method
#				2. rewrite getCounter() method	

# VERSION : 0.6 Sixth Release 24-Jun-13 Donner Li
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION :	1. new add search(), sortAndViewAs() method

# VERSION : 0.5 Fiveth Release 24-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION :	1. rewrite goEdit() method
#				2. fix 'Content is not allowed in prolog' bug

# VERSION : 0.4 Fourth Release 21-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. fix the bug in wipe() method;
#				2. update the start(), goEdit(), snapshot() method;
#				3. extend getView() method to support findViewWithAttributeThatMatches();
#				4. new add isEmpty(), getCounter() method;
#				5. new add addContact() method demo
#

# VERSION : 0.3 Third Release 20-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. add more trace info
#				2. update getView method, add 'dump' parameter 
#				3. update goEdit method and return current contacts counter
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


__version__ = '0.9'

import os,sys,re
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
		
		#define the point coordinate used to slide screen
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
		trace('Starting activity ...')
		self.device.startActivity(component=componentName)
		sleep(2)
		self.startStatus = self.goList()
		trace('Contacts is started, checking the contacts status...')
		self.isReady()
		sleep(2)
		
			
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
		sleep(2)
		
	def getView(self,str,cD=False,iD=False,dump=True,regex=False):
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
		
		if cD:
			view=self.vc.findViewWithContentDescription(str)
			trace('Query view with content description: %s, return is %s' % (str, view is not None))
			return view
		elif iD:
			view=self.vc.findViewById(str)
			trace('Query view by id: %s, return is %s' % (str, view is not None))
			return view
		elif regex:
			view=self.vc.findViewWithAttributeThatMatches('text',re.compile(str))
			trace('Query view that match attribute: %s, return is %s' % (str, view is not None))
			return view
		else:
			view=self.vc.findViewWithText(str)
			trace('Query view with text: %s, return is %s ' % (str, view is not None))
			return view
			
	def isReady(self):
		'''
		check whether the contacts is ready.
		@return: True
		'''
		while True:
			view=self.getView('Contacts list is being updated to reflect the change of language.')
			if not view:
				trace('Contacts is ready')
				break
			else:
				trace('Contacts is not ready, please wait!')
				sleep(2)
		return True
	
	def isEmpty(self):
		'''
		check whether the contacts is empty

		@return: True or False
		'''
		self.check()
		view=self.getView('No contacts.')
		if view:
			trace('Contacts list is empty')
			return True
		else:
			trace('Contacts list is not empty')
			return False
	def getCounter(self):
		'''
		get the contacts counter
		
		@return: the current contacts counter
		'''
		self.goList()
		if self.isEmpty():
			self.contactCounter=0
		else:
			while not self.getView('\d+ contacts?',regex=True):
				self.slide('down')
				sleep(3)
			self.contactCounter = int(self.getView('\d+ contacts?',regex=True,dump=False).getText().split()[0])
		trace('current contacts counter is %d' % self.contactCounter)
		return self.contactCounter

	def goList(self):
		'''
		check whether the screen is in contacts list view, if not, go list view via pressing back key
		
		@return: True
		'''
		while True:
			view=self.getView("All contacts",cD=True)
			if not view:
				self.back()
				sleep(3)
			else:
				if not view.isSelected():
					trace('Touch "All contacts"')
					view.touch()
				break
		trace('Goto contacts list view')
		return True
		
	def goEdit(self):
		'''
		check whether the contacts is empty, then select adding and go to edit view.
		
		@return: True
		'''
		self.check()
		try:
			self.getView('Add Contact',cD=True,dump=False).touch()
			trace('Touch "Add Contact"')
			sleep(5)
			return True
		except AttributeError: pass
		try:
			self.getView('Create a new contact',dump=False).touch()
			trace('Touch "Create a new contact"')
			sleep(5)
			self.getView('Keep local').touch()
			trace('Select "Keep local"')
			sleep(5)
			return True
		except AttributeError: pass
						
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
		snapFolder = 'snapshot'
		os.system('if not exist %s\\%s mkdir %s\\%s' % (logPath, snapFolder, logPath, snapFolder))
		snapFile = logPath + '\\' + snapFolder + '\\' + snapName
		result = self.device.takeSnapshot().getSubImage(self.snap_rect)
		trace('take snapshot without the statusbar')
		result.writeToFile(snapFile,'png')
		trace('save the snapshot to file: %s ' % snapFile)
		return result
	
	def wipe(self,view):
		'''
		wipe the text in specified view
		'''
		try:
			self.device.drag(view.getXY(),view.getXY(),1,1)
			trace('wipe text: %s' % str(view.getText()))
			self.device.press('KEYCODE_DEL','DOWN_AND_UP')
		except:
			Exception('wipe failed')
	
	def addContact(self,name='',phone='',email='',address=''):
		self.goEdit()
		try:
			offset = 0
			if name:
				view=self.getView('id/no_id/27',iD=True)
				trace('type %s' % name)
				view.type(name)
				view.touch()
			if phone:
				view=self.getView('id/no_id/46',iD=True,dump=False)
				trace('type %s' % phone)
				view.type(phone)
				offset += 4
				sleep(2)
			if email:
				view=self.getView('id/no_id/' + str(57 + offset), iD=True)
				trace('type %s' % email)
				view.type(email)
				offset += 4
				sleep(2)
			if address:
				view=self.getView('id/no_id/' + str(68 + offset), iD=True)
				trace('type %s' % address)
				view.type(address)
				sleep(2)
			view=self.getView('Done',dump=False)
			view.touch()
			trace('Touch Done')						
		finally:
			sleep(5)
			self.goList()

	def goEditExistContact(self,str):
		trace('Search a contact to edit')
		view=self.search(str)
		if not view:
			raise SyntaxError('No '+str+' contact to edit')
		view.touch()
		sleep(4)
		self.device.press('KEYCODE_MENU')
		sleep(2)
		self.device.press('KEYCODE_DPAD_DOWN')
		sleep(1)
		self.device.press('KEYCODE_ENTER')
		sleep(3)	

	def slideByView(self,view):
		trace('SlideByView')
		startp=(view.getX()+view.getWidth()-10,view.getY()+view.getHeight()-10)
		endpoint=(view.getX()+view.getWidth()-10,view.getY()+10)
		self.device.drag(startp,endpoint,0.5,1)   
		sleep(1)

	def editCompany(self,company,action):
		view=self.getView('Add organization')
		if view:
			trace('Step: add a organization info')
			view.touch()
			sleep(1)
			trace('add the company info')
			self.device.type(company)
			sleep(1)
			view=self.getView('Title')
			trace("add a company's Title")
			view.type(company)
		else:
			trace('Step: Edit the organization info')  
			view=self.getView('id/no_id/42',iD=True)
			self.wipe(view)
			trace('Edit the company info')
			self.device.type(company)
			view=self.getView('id/no_id/43',iD=True)
			trace("Edit the company's Title")
			self.wipe(view)
			self.device.type(company)

	def editAnotherField(self,fieldName,content,action):
		find=1
		view=self.getView(fieldName)
		view2=self.getView('Add another field')
		while not view:
			self.device.drag((440,760),(440,160),2,5)
			sleep(1)
			view=self.getView(fieldName)
			view2=self.getView('Add another field')
			if view2:
				if not view:
					find=0
					break
		if 0==find:
			trace('Step: add field '+fieldName+' info')
			view2.touch()
			trace('Click Add another field')
			sleep(2)
			view=self.getView(fieldName)
			if not view:
				view2=self.getView('id/no_id/2',iD=True)
				self.slideByView(view2)
				view=self.getView(fieldName)
			view.touch()
			sleep(1)
			#view=self.getView(fieldName)
			#view2=self.getView(view.getId()[:-2]+str(int(view.getId()[-2:])+6),iD=True)
			#view2.type(content)
			sleep(1)
			self.device.type(content)
			sleep(2)
		else:
			trace('Step: Edit field '+fieldName+' info')
			view2=self.getView(view.getId()[:-2]+str(int(view.getId()[-2:])+6),iD=True)
			self.wipe(view2)
			sleep(1)
			view2.type(content)
			sleep(1)
			   
	def editDetails(self,nameOrNumber,company='',website='',nickname='',notes='',action='add'):
		'''
		
		'''
		self.goEditExistContact(nameOrNumber)
		if not company=='':
			self.editCompany(company,action)
		if not website=='':
			self.editAnotherField('Website',website,action)
		if not nickname=='':
			self.editAnotherField('Nickname',nickname,action)        
		if not website=='':
			self.editAnotherField('Notes',notes,action)          
		view=self.getView('Done')
		trace('Click Done')
		view.touch()
		sleep(3)
		self.goList()

	def search(self,str):
		'''
		@type str: str
		@param str: specify the search keyword
		##@return: the view of search result if search result is not null, else return None
		'''		
		trace("start searching...")
		self.goList()
		
		searchView=self.getView("Search",True)
		searchView.touch()
		sleep(2)
		self.device.type(str)
		trace("search keyword is: "+str)
		#the id of 1st search result is always 28
		if self.getView("No contacts"):
			trace("No contact searched")
			return None
		else:
			return self.getView("id/no_id/28",iD=True)  
		
	def sortAndViewAs(self, sortByFirstName=True, viewAsFirstNameFirst=True):
		'''
		sort contact name
		@type sortByFirstName: boolean
		@param sortByFirstName: whether sort contact name by first name  
		@type viewAsFirstNameFirst: boolean
		@param viewAsFirstNameFirst: whether view contact by first name first              
		'''
		self.goList()              
		
		trace("start sorting...")
		self.device.press("KEYCODE_MENU","DOWN_AND_UP")                
		settingsView=self.getView("Settings")
		settingsView.touch()
		sleep(2)
		
		self.getView("Sort list by").touch()
		
		if sortByFirstName:                        
			self.getView("First name").touch()
			sleep(2)
			self.getView("View contact names as").touch()
			sleep(2)
			if viewAsFirstNameFirst:
				self.getView("First name first").touch()
			else:
				self.getView("Last name first").touch()
		else:
			self.getView("Last name").touch()
			sleep(2)
			self.getView("View contact names as").touch()
			sleep(2)
			if viewAsFirstNameFirst:
				self.getView("First name first").touch()
			else:
				self.getView("Last name first").touch()
		sleep(2)       
		
	def favor(self,str,favor=True):
		'''
		add or cancel contact to favorites
		
		@type str: str
		@param str: specify the search string
		@type favor: boolean
		@param favor: add if True
		'''
		try:
			self.search(str).touch()
			sleep(3)
		except AttributeError:
			trace('no matched contact found, operation failed!')
			self.goList()
			return False
		aim, action = ('Add to favorites', 'add') if favor else ('Remove from favorites', 'remov')
		try:
			self.getView(aim, cD=True).touch()
			trace('%s successfully' % aim)
		except AttributeError:
			trace('%s has been %sed in favorites, not have to %s repeatedly' % (str, action, action))
		sleep(3)
		self.goList()
		return True
		
	def delete(self,kwd = ''):
        
		'''delete one contact
		@type kwd: string
		@param kwd: keyword which contact to be delete, if none,delete first contact
		@return: 
		'''
		#self.start()
		#trace('launch on contact application')

		self.goList()
		if self.isEmpty():
			trace('Could not find any contact data,no record!')
			raise SyntaxError('Could not find any contact data,no record!')

		if not kwd :
			# keyword is empty,delete first contact
			trace('keyword is none, first contact with be delete')
			find = self.getView('id/no_id/27',iD=True,dump=False)
			#if find != None:
		else :
			# keyword is not none
			# search specifying contact by keyword
			find = self.search(kwd)
			trace('')
			# if find != None:
		if not find :
			trace('Could not find the contact : ' + kwd)
			raise SyntaxError('Could not find the contact : ' + kwd)
		else:
			# delete operate 
			find.touch()
			sleep(3)
			trace('show contact detail information')
			sleep(1)
			self.device.press('KEYCODE_MENU')
			sleep(4)
			delete_menu = self.getView('Delete')
			trace('choose delete contact')
			delete_menu.touch()
			
			# confirm delete operate
			ok_menu = self.getView('OK')
			ok_menu.touch()
			sleep(3)
			
		# if current activity is not Main Activity back to Main Activity
		self.goList()
		
		if 0 == self.getCounter() :
			trace(' all contacts has been deleted, no record!')
		trace('operation success.')
if __name__ == '__main__':
	device=MonkeyRunner.waitForConnection()
	trace('=' * 80)
	trace('start testing...')
	c=contacts(device)
	trace('complete init')
	c.start()
	trace('complete contacts activity starting')
	############################ add contact case Beginning ############################
	c.favor('jason1')
	'''
	for i in range(5):
		result='failed'
		try:	
			before=c.getCounter()
			c.addContact(name='jason',phone='123',email='a@b.c',address='softwarepark')
			after=c.getCounter()
			if after - before == 1:
				result='passed'
		# except	Exception,e:
			# result='unknown'
			# details=str(e)
		finally:
			trace("*" * 20 + " case %d is %s " % (i + 1, result) + "*" * 20)
			# if 'unknown' == result:
				# trace('Exception details: ' + details)
			sleep(5)
	'''
	c.favor('jason')
	c.favor('jason')
	c.favor('jason',False)
	c.favor('jason',False)
	trace('end testing')
	############################ add contact case Finished ############################