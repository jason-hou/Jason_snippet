import os,sys
try:
	for p in os.environ['PYTHONPATH'].split(';'):
		if not p in sys.path:
			sys.path.append(p)
except:
	pass

from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage
from log import trace
import contacts

runLog=r'c:\runlog.txt'
trace=trace(runLog).trace

device=MonkeyRunner.waitForConnection(5,'emulator-5554')
trace('=' * 80)
trace('start testing...')
c=contacts.contacts(device,'emulator-5554')
trace('complete init')
c.start()
trace('complete contacts activity starting')

c.getCounter()
# c.editDetails(None, Name='thomson',Website='www',Nickname='tom',Company='teleca',Phone='7654321')
c.favor('jason')
############################ add contact case Beginning ############################
'''
c.favor('jason1')
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
c.getCounter()
c.favor('jason')
# c.favor('jason')
# c.favor('jason',False)
# c.favor('jason',False)
'''
c.editDetails('222',action='add', Website='www')
c.editDetails('222',action='update', Website='mmm')
c.editDetails('222',action='add', Nickname='nick')
c.editDetails('222',action='add', Company='teleca')
c.editDetails('222',action='add', Phone='123456789')
'''
# c.sortAndViewAs(True,True)
# c.sortAndViewAs(False,True)
# c.sortAndViewAs(True,False)
# c.sortAndViewAs(False,False)
c.delete(None)
c.stop()
# c.addContact(name='222')
# c.editDetails(None, Name='Jason',Website='www',Nickname='tom',Company='teleca',Phone='7654321')
# c.editDetails('7654321', Website='wap',Nickname='jerry',Company='symphonyteleca',Phone='1234567',Name='222')
# c.editDetails('Jason', Name=None,Company=None,Phone='1234',Nickname=None)
# c.editDetails('123', Name='Jason',Company='symphonyteleca',Phone=None)
trace('end testing')
############################ add contact case Finished ############################