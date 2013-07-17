# -*- coding: utf-8 -*-

#Author: Jason Hou

#Date: 2013/07/17

############################ CHANGE HISTORY ############################

# VERSION : 2.2 Twenty-second Release 17-Jul-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION	1. add snapshot operation before raising some exception;
#				2. update favor method

# VERSION : 2.1 Twenty-first Release 10-Jul-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. use class inheritance instead of importing module

# VERSION : 2.0 Nineteenth Release 09-Jul-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. reorganize the code and migrate the common operation to common module
#				2. refactor goList module

# VERSION : 1.9 Nineteenth Release 08-Jul-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. Refactor addContact method;
#				2. update isReady, delete and sortAndViewAs method

# VERSION : 1.8 Eighteenth Release 07-Jul-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. Add configuraion file support function by Jack;
#				2. Add touch method and update slide method to avoid the getXY bug in 4.1.2;
#				3. Fix nullpoint bug if key value is None in editContact relevant method;
#				4. update menu and scroll method to sleep 2 seconds;
#				5. update logPath retrieve and logFile naming method

# VERSION : 1.7 seventeenth Release 06-Jul-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. update goEdit to support to go to Edit view of exist contacts;
#				2. update menu, scroll method;
#				3. refactor the editDetails relevant module

# VERSION : 1.6 sixteenth Release 04-Jul-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. refactor the editDetails relevant module by Robin
#				2. update scroll method

# VERSION : 1.5 Fifteenth Release 04-Jul-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. refactor the addContact module
#				2. refactor delete and getCounter module by Faure

# VERSION : 1.4 Fourteenth Release 02-Jul-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. refactor the getCounter and delete method by Faure

# VERSION : 1.3 Thirteenth Release 29-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. fix bug scroll trace info wrong;
#				2. merge the search and sortAndViewAs method refactorred by Donner

# VERSION : 1.2 Twelveth Release 27-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. fix bug cannot slide to left or right in list view
#				2. update scroll() method to support touching highlight item

# VERSION : 1.1 Eleventh Release 26-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. new add meun() and scroll() method

# VERSION : 1.0 Tenth Release 25-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. update slide() method to support sliding in specified view

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

__version__ = '2.2'

import os,sys,ConfigParser
try:
	for p in os.environ['PYTHONPATH'].split(';'):
		if not p in sys.path:
			sys.path.append(p)
except:
	pass
	
from com.android.monkeyrunner import MonkeyRunner
import common

package = 'com.android.contacts'
activity = '.activities.PeopleActivity'
componentName = package + '/' + activity

action=common.action

class contacts(action):
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
		action.__init__(self,device,'Contacts',devID)
		
		#get the API Level of the connected device
		API_LEVEL = int(device.getProperty('build.version.sdk'))
		#read the configuration file
		if API_LEVEL == 17:
			configFile = 'API-17.conf'
		elif API_LEVEL == 16:
			configFile = 'API-16.conf'
		else:
			raise EnvironmentError('Not available configuration to support your device')
		sysConfigFile = common.configPath + '\\' + configFile
		cf=ConfigParser.ConfigParser()
		cf.read(sysConfigFile)

		self.AllContacts		= cf.get('Contacts','AllContacts')
		self.AddNew				= cf.get('Contacts','AddNew')
		self.CreateNewContact	= cf.get('Contacts','CreateNewContact')
		self.NoContacts			= cf.get('Contacts','NoContacts')
		self.KeepLocal			= cf.get('Contacts','KeepLocal')
		self.IsReady			= cf.get('Contacts','IsReady')

		self.sample				= sample
		self.contactCounter		= 0
		#the status which indicate whether the contacts activity is started
		self.startStatus		= False

	def start(self):
		'''
		start the contacts activity and set the startStatus True if contacts is ready.
		'''
		self.startComponent(componentName)
		self.startStatus = self.goList()
		self.trace('Contacts is started, checking the contacts status...')
		self.isReady()

	def stop(self):
		'''
		stop the contacts activity and set the startStatus False
		'''
		self.stopPackage(package)
		self.startStatus = False

	def isReady(self):
		'''
		check whether the contacts is ready.
		
		@return: True
		'''
		while True:
			view=self.getView(self.IsReady)
			if not view:
				self.trace('Contacts is ready')
				self.sleep(2)
				break
			else:
				self.trace('Contacts is not ready, please wait!')
				self.sleep(4)
		return True

	def isEmpty(self):
		'''
		check whether the contacts is empty

		@return: True or False
		'''
		self.check()
		#view=self.getView('No contacts.')
		view=self.getView(self.NoContacts)
		if view:
			self.trace('Contacts list is empty')
			return True
		else:
			self.trace('Contacts list is not empty')
			return False

	def getCounter(self):
		'''
		get the contacts counter
		
		@return: the current contacts counter
		'''
		if self.isEmpty():
			self.contactCounter=0
		else:
			while True:
				try:
					self.contactCounter = int(self.getView('\d+ contacts?',regex=True).getText().split()[0])
					break
				except AttributeError:
					self.slide('down')
					self.sleep(1)
		self.trace('current contacts counter is %d' % self.contactCounter)
		return self.contactCounter

	def goList(self):
		'''
		check whether the screen is in contacts list view, if not, go list view via pressing back key
		
		@return: True
		'''
		while True:
			try:
				self.getView(self.AllContacts,cD=True).touch()
				self.sleep(3)
				break
			except AttributeError:
				self.back()
				self.sleep(3)
		self.trace('Goto contacts list view')
		return True

	def goEdit(self,searchInfo=None):
		'''
		check whether the contacts is empty, then select adding and go to edit view.
		if searchInfo is specified, then go to Edit view of exist contact
		
		@type searchInfo: str
		@param searchInfo: information of contacts
		
		@return: True
		'''
		self.check()
		if searchInfo:
			try:
				self.search(searchInfo).touch()
			except AttributeError:
				self.trace('No matched contact found, operation failed!')
				self.snapshot('NoMatched')
				raise SyntaxError('No such contact info: %s to edit' % searchInfo)
			self.sleep(3)
			self.menu()
			self.scroll(1)
		else:
			try:
				self.getView(self.AddNew,cD=True,dump=False).touch()
				self.trace('Touch ' + self.AddNew)
				self.sleep(5)
				return True
			except AttributeError: pass
			try:
				self.getView(self.CreateNewContact,dump=False).touch()
				self.trace('Touch "Create a new contact"')
				self.sleep(5)
				#self.getView('Keep local').touch()
				self.touch(self.getView(self.KeepLocal))
				self.trace('Select "Keep local"' )
				self.sleep(2)
			except AttributeError: pass
		return True

	def check(self):
		'''
		check whether the contacts is started before other operation about contacts
		
		@return: True
		'''
		if not self.startStatus:
			self.trace("Wrong code! please start contacts firstly in you code")
			raise SyntaxError('Contacts should be start firstly!')
		return True

	def addContact(self,**editInfo):
		'''
		add new contact
		
		@type editInfo: collecting parameters
		@param editInfo: valid key value should be 'Name','Phone','Email','Address','Company','Website','Nickname','Notes'

		@return: True
		'''
		self.editDetails(None,**editInfo)

	def editName(self,name):
		'''
		edit Name details of contacts
		
		@type name: str
		@param name: content of Name
		
		@return: True
		'''
		view = self.getView('id/no_id/27',iD=True)
		self.wipe(view)
		if name:
			self.type(name)
			self.trace("Type Name: %s" % name)
			self.sleep(2)
			self.touch(view)
		else:
			self.trace("Erase Name")
		return True

	def editCompany(self,company):
		'''
		edit Company details of contacts
		@type company: str
		@param company: content of Company
		
		@return: True
		'''
		try:
			self.getView('Add organization').touch()
			self.sleep(1)
		except AttributeError:
			view = self.getView('id/no_id/42',iD=True)
			self.wipe(view)
		if company:
			self.type(company)
			self.trace('Type Company: %s' % company)
		else:
			self.trace('Erase Company')
		return True

	def editOther(self,fieldName,content):
		'''
		edit details of other field
		
		@type fieldName: str
		@param fieldName: name of field
		@type content: str
		@param content: edit content
	
		@return: True
		'''
		while True:
			try:
				viewId = self.getView(fieldName).getId()
				view2Id = viewId[:-2]+str(int(viewId[-2:])+6)
				view2=self.getView(view2Id,iD=True)
				self.wipe(view2)
				if content:
					self.type(content)
					self.trace('Type %s: %s' %(fieldName,content))
				else:
					self.trace('Erase %s' % fieldName)
				break
			except AttributeError:
				try:
					self.getView('Add another field').touch()
					self.sleep(1)
					while True:
						try:
							self.touch(self.getView(fieldName))
							break
						except AttributeError:
							view2 = self.getView('id/no_id/2',iD=True,dump=False)
							self.slide('up',view2)
							self.sleep(1)
					if content:
						self.type(content)
						self.trace('Type %s: %s' %(fieldName,content))
					break
				except AttributeError:
					pass
			self.slide('up')
			self.sleep(2)
		return True

	def editDetails(self,contactsInfo,**editInfo):
		'''
		edit details of contact with add or update
		
		@type contactsInfo: str
		@param contactsInfo: information of contacts
		@type action: str
		@param action: 'add' or 'update' details
		@type editInfo: collecting parameters
		@param editInfo: valid key value should be 'Name','Phone','Email','Address','Company','Website','Nickname','Notes'
	
		@return: True
		'''
		for fieldName in editInfo:
			if fieldName not in ['Name','Phone','Email','Address','Company','Website','Nickname','Notes']:
				raise SyntaxError("Wrong parameter: fieldName choose from 'Name','Phone','Email','Address','Company','Website','Nickname','Notes'")
		self.goEdit(contactsInfo)
		try:
			try:
				self.editName(editInfo['Name'])
				editInfo.pop('Name')
			except KeyError: pass
			try:
				self.editCompany(editInfo['Company'])
				editInfo.pop('Company')
			except KeyError: pass
			keyNumber = editInfo.__len__()
			for updateField in editInfo:
				self.editOther(updateField, editInfo[updateField])
				self.getView('Done').touch()
				self.trace('Click Done')
				keyNumber -= 1
				self.trace('KeyNumber: %i' % keyNumber)
				if keyNumber:
					self.sleep(3)
					self.menu()
					self.scroll(1)
		finally:
			self.sleep(3)
			self.goList()

	def search(self,str):
		'''
		search contact by keyword
		
		@type str: str
		@param str: specify the search keyword
		
		@return: the view of search result if search result is not null, else return False
		'''
		self.trace("Start searching...")
		try:
			self.getView("Search",True).touch()
			self.sleep(2)
			self.type(str)
			self.trace("Search keyword is: "+str)
		except AttributeError:
			if self.isEmpty():
				self.trace("No contacts exist")
			else:
				self.trace("No contacts searched")
			return False
		#the id of 1st search result is always 27
		return self.getView("id/no_id/27",iD=True)

	def sortAndViewAs(self, sort=True, first=True):
		'''
		sort and view contact name
		
		@type sort: boolean
		@param sort: whether sort contact name or view contact  
		@type first: boolean
		@param first: whether sort and view contact by first name or last name
		
		@return: boolean
		'''
		self.trace("Start sorting...")
		self.menu()
		self.scroll(4)
		sortOrView="Sort list by" if sort else "View contact names as"
		firstOrLast="First name*" if first else "Last name*"
		try:
			self.touch(self.getView(sortOrView))
			self.touch(self.getView(firstOrLast,regex=True))
			return True
		except AttributeError:
			return False
		finally:
			self.goList()

	def favor(self,str,favor=True):
		'''
		add or cancel contact to favorites
		
		@type str: str
		@param str: specify the search string
		@type favor: boolean
		@param favor: add if True
		
		@return: boolean
		'''
		aim, action = ('Add to favorites', 'add') if favor else ('Remove from favorites', 'remov')
		try:
			self.search(str).touch()
			self.sleep(3)
			try:
				self.touch(self.getView(aim, cD=True))
				self.trace('%s successfully' % aim)
				return True
			except AttributeError:
				self.trace('%s has been %sed in favorites, not have to %s repeatedly' % (str, action, action))
				return False
		except AttributeError:
			self.trace('No matched contact found, operation failed!')
			self.snapshot('NoMatchedToFavor')
			raise SyntaxError('No such contact info: %s to favor' % str)
			return False
		finally:
			self.goList()

	def delete(self,str):
		'''delete one contact
		@type str: string
		@param str: keyword which contact to be delete, if none,delete first contact
		@return: True if operate sucess, False if operate fail.
		'''
		if self.isEmpty():
			self.trace('Empty contact list, operation failed!')
			self.snapshot('NoMatchedToDelete')
			raise SyntaxError('Could not find any contact data,no record!')
			return False
		find = self.search(str) if str else self.getView('id/no_id/27',iD=True,dump=False)
		try:
			find.touch()
			self.sleep(4)
			self.menu()
			self.scroll(3)
			self.trace('Choose delete contact')
			self.touch(self.getView('OK'))
			return True
		except AttributeError:
			self.trace('No matched contact found, operation failed!')
			self.snapshot('NoMatchedToDelete')
			raise SyntaxError('No such contact info: %s to delete' % str)
			return False
		finally:
			self.goList()

if __name__ == '__main__':
	device=MonkeyRunner.waitForConnection(5,'emulator-5554')
	c=contacts(device,'emulator-5554')
	c.start()
	c.trace('pass')
	# trace('complete contacts activity starting')
	############################ add contact case Beginning ############################
	
	# c.favor('jason1')
	'''
	# for i in range(5):
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
	
	# c.favor('jason')
	# c.favor('jason')
	# c.favor('jason',False)
	# c.favor('jason',False)
	
	c.editDetails('222',action='add', Website='www')
	c.editDetails('222',action='update', Website='mmm')
	c.editDetails('222',action='add', Nickname='nick')
	c.editDetails('222',action='add', Company='teleca')
	c.editDetails('222',action='add', Phone='123456789')
	
	# c.sortAndViewAs(True,True)
	# c.sortAndViewAs(False,True)
	# c.sortAndViewAs(True,False)
	# c.sortAndViewAs(False,False)
	c.delete(None)
	c.stop()
	'''
	# c.addContact(Name='jason',Website='dotcom')
	# c.editDetails(None, Name='Jason',Website='www',Nickname='tom',Company='teleca',Phone='7654321')
	# c.editDetails('7654321', Website='wap',Nickname='jerry',Company='symphonyteleca',Phone='1234567',Name='222')
	# c.editDetails('Jason', Name=None,Company=None,Phone='1234',Nickname=None)
	# c.editDetails('123', Name='Jason',Company='symphonyteleca',Phone=None)
	c.stop()
	# trace('end testing')
	############################ add contact case Finished ############################
	