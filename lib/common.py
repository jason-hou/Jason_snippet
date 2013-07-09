# -*- coding: utf-8 -*-

#Author: Jason Hou

#Date: 2013/07/09

############################ CHANGE HISTORY ############################

# VERSION : 0.1 First Release 09-Jul-13 Jason Hou
# REASON : First implementation
# REFERENCE : 
# DESCRIPTION : 1. encapsulate the common method

############################ CHANGE HISTORY ############################

__version__ = '0.1'

import os,sys,re,ConfigParser,datetime
try:
	for p in os.environ['PYTHONPATH'].split(';'):
		if not p in sys.path:
			sys.path.append(p)
except:
	pass

from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage
from com.dtmilano.android.viewclient import ViewClient
from log import trace

DEBUG = True

nowPath = os.path.dirname(os.path.abspath(__file__))
rootPath = '\\'.join(nowPath.split('\\')[:-1])
configPath = rootPath + '\\' + 'config'
configName = 'UserDefine.conf'
userConfigFile = configPath + '\\' + configName
cP = ConfigParser.ConfigParser()
cP.read(userConfigFile)
logPath = cP.get('Path','logPath')
logName = ''.join(re.split('\W+',str(datetime.datetime.now())[:-7])) + '.log'
logFile = logPath + '\\' + logName

mTrace = trace(logFile).trace

class action:
	def __init__(self,device,feature,devID='emulator-5554'):
		'''
		constructor
		
		@type device: MonkeyDevice
		@param device: The device or emulator connected
		@type feature: str
		@param feature: feature name, use to mark in trace log
		@type devID: str
		@param serialno: the serial number of the device or emulator to connect to
		'''
		if not device:
			raise Exception('Cannot connect to device')
		self.device = device
		self.feature = feature
		
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
		
		self.trace('Before instance')
		self.vc=ViewClient(device, devID)
		self.trace('After instance')

	def trace(self,str):
		'''
		trace
		
		@type str: str
		@param str: specified trace info
		'''
		mTrace('[%s]:%s'%(self.feature,str))

	def sleep(self,duration=1):
		'''
		Monkey sleep
		
		@type duration: int
		@param duration: how long to sleep
		'''
		MonkeyRunner.sleep(duration)

	def menu(self):
		'''
		press menu
		'''
		self.device.press('KEYCODE_MENU','DOWN_AND_UP')
		self.trace('Press menu')
		self.sleep(2)

	def scroll(self,times=1,down=True):
		'''
		scoll up or down for some times then touch the highlight submenu item
		
		@type down: boolead
		@param down: scroll down if True or scroll up
		@type times: int
		@param times: how many times to scroll
		'''
		keycode = 'KEYCODE_DPAD_DOWN' if down else 'KEYCODE_DPAD_UP'
		for i in range(times):
			self.device.press(keycode,'DOWN_AND_UP')
			self.trace('Scroll %s' % keycode.split('_')[-1].lower())
		self.device.press('KEYCODE_ENTER','DOWN_AND_UP')
		self.trace('Press Enter')
		self.sleep(2)

	def back(self):
		'''
		press back
		'''
		self.device.press('KEYCODE_BACK','DOWN_AND_UP')
		self.trace('Press back')

	def start(self,componentName):
		'''
		start activity
		
		@type componentName: str
		@param componentName: component name
		'''
		self.device.startActivity(component=componentName)
		self.trace('Start component: %s' % componentName)

	def stop(self,package):
		'''
		stop activity
		
		@type package: str
		@param package: package name
		'''
		self.device.shell('am force-stop %s' % package)
		self.trace('Force stop contacts package %s' % package)

	def type(self,str):
		'''
		type
		
		@type str: str
		@param str: strings to type
		'''
		self.device.type(str)
		self.trace('Type %s' % str)

	def slide(self,str,view=None):
		'''
		slide the screen
		
		@type: str
		@param: 'left','right','up','down'
		@type view: view
		@param view: specify the view, default to None  
		'''
		if str not in ['left','right','up','down']:
			raise SyntaxError("Wrong Parameter: choose from 'left','right','up' or 'down'")
		try:
			cX = view.getX()
			cY = view.getY()
			width = view.getWidth()
			height = view.getHeight()
			cL = cX + width/4, cY + height/2
			cR = cX + width/4*3, cY + height/2
			cU = cX + width/2, cY + height/4
			cD = cX + width/2, cY + height/4*3
		except AttributeError:
			pass
		(left, right, up, down) = (cL, cR, cU, cD) if view else (self.left, self.right, self.up, self.down)
		nav = {
			'left':{'start':right,'end':left},
			'right':{'start':left,'end':right},
			'up':{'start':down,'end':up},
			'down':{'start':up,'end':down}
			}
		self.device.drag(nav[str]['start'], nav[str]['end'], 0.1, 10)
		self.trace('Slide the screen from %s to %s ' % (nav[str]['start'],nav[str]['end']))
		self.sleep(2)

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
			if DEBUG: self.trace('Before dump')
			self.vc.dump()
			if DEBUG: self.trace('After dump')
		if cD:
			view=self.vc.findViewWithContentDescription(str)
			self.trace('Query view with content description: %s, return is %s' % (str, view is not None))
			return view
		elif iD:
			view=self.vc.findViewById(str)
			self.trace('Query view by id: %s, return is %s' % (str, view is not None))
			return view
		elif regex:
			view=self.vc.findViewWithAttributeThatMatches('text',re.compile(str))
			self.trace('Query view that match attribute: %s, return is %s' % (str, view is not None))
			return view
		else:
			view=self.vc.findViewWithText(str)
			self.trace('Query view with text: %s, return is %s ' % (str, view is not None))
			return view

	def touch(self,view):
		'''
		touch the specified view
		
		@type view: view
		@param view: specified view

		@return: True
		'''
		x = view.getX()
		y = view.getY()
		w = view.getWidth()
		h = view.getHeight()
		self.device.touch(x + w/2, y + h/2,'DWON_AND_UP')
		self.trace('Touch (%d,%d)' % (x + w/2, y + h/2))
		self.sleep(3)
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
		self.trace('Take snapshot without the statusbar')
		result.writeToFile(snapFile,'png')
		self.trace('Save snapshot to file: %s ' % snapFile)
		return result

	def wipe(self,view):
		'''
		wipe the text in specified view
		
		@type view: view
		@param view: specified view
		'''
		try:
			self.device.drag(view.getXY(),view.getXY(),1,1)
			self.trace('Wipe text: %s' % str(view.getText()))
			self.device.press('KEYCODE_DEL','DOWN_AND_UP')
		except:
			Exception('Wipe failed')