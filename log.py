# -*- coding: utf-8 -*-

#Author: Jason Hou
#Date: 2013/06/09

############################ CHANGE HISTORY ############################

# VERSION : 0.4 Third Release 09-Jun-13 Jason Hou
# REASON : Fix bug
# REFERENCE : 
# DESCRIPTION : 1. fix bug Illegal character in file 'log.py' for encoding 'utf-8' which is imported in the third release 

# VERSION : 0.3 Third Release 09-Jun-13 Jason Hou
# REASON : Update document and Fix bug
# REFERENCE : 
# DESCRIPTION : 1. add document description How to import module user defined in monkeyrunner;
#				2. add the "change history" section;
#				3. fix the bug timestamp(False) failes when class trace init with True, vice versa: 

# VERSION : 0.2 Second Release 08-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. change the logFile type from file object to file path;
#				2. change the default verbose and echo value from False to True;
#				3. filter the the last three bit time due to display unusefull 000 or 999.

# VERSION : 0.1 First Release 07-Jun-13 Jason Hou
# REASON : First implementation
# REFERENCE : 
# DESCRIPTION : 1. Create the first trace log module

############################ CHANGE HISTORY ############################

'''Trace log handle library
This module is an trace log handle library that: 
	-output the trace log info with time stamp

How to import module user defined in monkeyrunner?
1. Set user variable PYTHONPATH with value (path contain user defined module, separated with semicolons)
2. Add below code in your code start section:

import os,sys
try:
    for p in os.environ['PYTHONPATH'].split(';'):
       if not p in sys.path:
          sys.path.append(p)
except:
    pass

3. Now you can import the module user defined and use in monkeyrunner

from log import trace
trace=trace(logFile).trace
......
trace('code start...')

'''

__version__ = '0.2'
__all__ = ['trace']

from datetime import datetime

class trace:
	
	''' the clase is used to output the tracelog info '''	
	
	def __init__(self,logFile,verbose=True,echo=True):
		'''
		logFile:	 specify the logFile with full path;
		verbose:	 if False, output less time detail(without date);
		echo:		 if False, trace info won't display in command line.
		'''
		self.logFile=logFile
		self.verbose=verbose
		self.echo=echo
	
	def timestamp(self,verbose):
		'''return the current timestamp string'''
		if not verbose:
			return str(datetime.now())[-15:-3]
		else:
			return str(datetime.now())[:-3]

	def trace(self,str):
		'''add str as log info to logfile'''
		logInfo=(self.timestamp(self.verbose) + '\t' + str + '\n')
		if self.echo:
			print logInfo
		f=open(self.logFile,'a+')
		try:
			f.write(logInfo)
		except:
			print "file I/O error"
		finally:
			f.close()

if __name__ == 	'__main__':
	t=trace('main_test.txt')
	trace=t.trace
	trace('*' * 40)
	trace('start' + '\t' + t.timestamp(0))
	trace('this is a test')
	trace('end' + '\t' + t.timestamp(1))
	trace('*' * 40)