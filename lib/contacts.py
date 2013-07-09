# -*- coding: utf-8 -*-

#Author: Jason Hou

#Date: 2013/07/09

############################ CHANGE HISTORY ############################

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

__version__ = '1.9'

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
		self.action = common.action(device,'Contacts',devID)
		
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
		self.action.start(componentName)
		self.action.sleep(2)
		self.startStatus = self.goList()
		self.action.trace('Contacts is started, checking the contacts status...')
		self.isReady()
		self.action.sleep(2)

	def stop(self):
		'''
		stop the contacts activity and set the startStatus False
		'''
		self.action.stop(package)
		self.startStatus = False

	def isReady(self):
		'''
		check whether the contacts is ready.
		
		@return: True
		'''
		while True:
			view=self.action.getView(self.IsReady)
			if not view:
				self.action.trace('Contacts is ready')
				break
			else:
				self.action.trace('Contacts is not ready, please wait!')
				self.action.sleep(4)
		return True

	def isEmpty(self):
		'''
		check whether the contacts is empty

		@return: True or False
		'''
		self.check()
		#view=self.action.getView('No contacts.')
		view=self.action.getView(self.NoContacts)
		if view:
			self.action.trace('Contacts list is empty')
			return True
		else:
			self.action.trace('Contacts list is not empty')
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
			while True:
				try:
					self.contactCounter = int(self.action.getView('\d+ contacts?',regex=True).getText().split()[0])
					break
				except AttributeError:
					self.action.slide('down')
					self.action.sleep(1)
		self.action.trace('current contacts counter is %d' % self.contactCounter)
		return self.contactCounter

	def goList(self):
		'''
		check whether the screen is in contacts list view, if not, go list view via pressing back key
		
		@return: True
		'''
		while True:
			try:
				self.action.getView(self.AllContacts,cD=True).touch()
				break
			except AttributeError:
				self.action.back()
				self.action.sleep(3)
		self.action.trace('Goto contacts list view')
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
				raise SyntaxError('No such contact info: %s to edit' % searchInfo)
			self.action.sleep(3)
			self.action.menu()
			self.action.scroll(times=1)
		else:
			try:
				self.action.getView(self.AddNew,cD=True,dump=False).touch()
				self.action.trace('Touch ' + self.AddNew)
				self.action.sleep(5)
				return True
			except AttributeError: pass
			try:
				self.action.getView(self.CreateNewContact,dump=False).touch()
				self.action.trace('Touch "Create a new contact"')
				self.action.sleep(5)
				#self.action.getView('Keep local').touch()
				self.action.touch(self.action.getView(self.KeepLocal))
				self.action.trace('Select "Keep local"' )
				self.action.sleep(2)
			except AttributeError: pass
		return True

	def check(self):
		'''
		check whether the contacts is started before other operation about contacts
		
		@return: True
		'''
		if not self.startStatus:
			self.action.trace("Wrong code! please start contacts firstly in you code")
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
		view = self.action.getView('id/no_id/27',iD=True)
		self.action.wipe(view)
		if name:
			self.action.type(name)
			self.action.trace("Type Name: %s" % name)
			self.action.sleep(2)
			self.action.touch(view)
		else:
			self.action.trace("Erase Name")
		return True

	def editCompany(self,company):
		'''
		edit Company details of contacts
		@type company: str
		@param company: content of Company
		
		@return: True
		'''
		try:
			self.action.getView('Add organization').touch()
			self.action.sleep(1)
		except AttributeError:
			view = self.action.getView('id/no_id/42',iD=True)
			self.action.wipe(view)
		if company:
			self.action.type(company)
			self.action.trace('Type Company: %s' % company)
		else:
			self.action.trace('Erase Company')
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
				viewId = self.action.getView(fieldName).getId()
				view2Id = viewId[:-2]+str(int(viewId[-2:])+6)
				view2=self.action.getView(view2Id,iD=True)
				self.action.wipe(view2)
				if content:
					self.action.type(content)
					self.action.trace('Type %s: %s' %(fieldName,content))
				else:
					self.action.trace('Erase %s' % fieldName)
				break
			except AttributeError:
				try:
					self.action.getView('Add another field').touch()
					self.action.sleep(1)
					while True:
						try:
							self.action.touch(self.action.getView(fieldName))
							break
						except AttributeError:
							view2 = self.action.getView('id/no_id/2',iD=True,dump=False)
							self.action.slide('up',view2)
							self.action.sleep(1)
					if content:
						self.action.type(content)
						self.action.trace('Type %s: %s' %(fieldName,content))
					break
				except AttributeError:
					pass
			self.action.slide('up')
			self.action.sleep(2)
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
				self.action.getView('Done').touch()
				self.action.trace('Click Done')
				keyNumber -= 1
				self.action.trace('KeyNumber: %i' % keyNumber)
				if keyNumber:
					self.action.sleep(3)
					self.action.menu()
					self.action.scroll(times=1)
		finally:
			self.action.sleep(3)
			self.goList()

	def search(self,str):
		'''
		search contact by keyword
		
		@type str: str
		@param str: specify the search keyword
		
		@return: the view of search result if search result is not null, else return False
		'''
		self.action.trace("start searching...")
		try:
			self.action.getView("Search",True).touch()
			self.action.sleep(2)
			self.action.type(str)
			self.action.trace("search keyword is: "+str)
		except AttributeError:
			if self.isEmpty():
				self.action.trace("No contacts exist")
			else:
				self.action.trace("No contacts searched")
			return False
		#the id of 1st search result is always 27
		return self.action.getView("id/no_id/27",iD=True)

	def sortAndViewAs(self, sort=True, first=True):
		'''
		sort and view contact name
		
		@type sort: boolean
		@param sort: whether sort contact name or view contact  
		@type first: boolean
		@param first: whether sort and view contact by first name or last name
		
		@return: boolean
		'''
		self.action.trace("start sorting...")
		self.action.menu()
		self.action.scroll(times=4)
		sortOrView="Sort list by" if sort else "View contact names as"
		firstOrLast="First name*" if first else "Last name*"
		try:
			self.action.touch(self.action.getView(sortOrView))
			self.action.touch(self.action.getView(firstOrLast,regex=True))
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
		try:
			self.search(str).touch()
			self.action.sleep(3)
		except AttributeError:
			self.action.trace('no matched contact found, operation failed!')
			self.goList()
			return False
		aim, action = ('Add to favorites', 'add') if favor else ('Remove from favorites', 'remov')
		try:
			self.action.touch(self.action.getView(aim, cD=True))
			self.action.trace('%s successfully' % aim)
			return True
		except AttributeError:
			self.action.trace('%s has been %sed in favorites, not have to %s repeatedly' % (str, action, action))
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
			self.action.trace('Could not find any contact data,no record!')
			return False
		find = self.search(str) if str else self.action.getView('id/no_id/27',iD=True,dump=False)
		try:
			find.touch()
			self.action.sleep(4)
			self.action.menu()
			self.action.scroll(times=3)
			self.action.trace('choose delete contact')
			self.action.touch(self.action.getView('OK'))
			return True
		except AttributeError:
			return False
		finally:
			self.goList()

if __name__ == '__main__':
	device=MonkeyRunner.waitForConnection(5,'emulator-5554')
	# trace('=' * 80)
	# trace('start testing...')
	c=contacts(device,'emulator-5554')
	# trace('complete init')
	c.start()
	# trace('complete contacts activity starting')
	############################ add contact case Beginning ############################
	
	c.favor('jason1')
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
	c.addContact(Name='jason',Website='dotcom')
	# c.editDetails(None, Name='Jason',Website='www',Nickname='tom',Company='teleca',Phone='7654321')
	# c.editDetails('7654321', Website='wap',Nickname='jerry',Company='symphonyteleca',Phone='1234567',Name='222')
	c.editDetails('Jason', Name=None,Company=None,Phone='1234',Nickname=None)
	c.editDetails('123', Name='Jason',Company='symphonyteleca',Phone=None)
	c.stop()
	# trace('end testing')
	############################ add contact case Finished ############################