import os,sys
try:
	for p in os.environ['PYTHONPATH'].split(os.pathsep):
		if not p in sys.path:
			sys.path.append(p)
except:
	pass
from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage
from log import trace
import contacts
# import HTMLTestRunner
import unittest

# rootPath = os.path.dirname(os.path.abspath(__file__))
# reportFile = rootPath + os.sep + 'TestReport.html'

device=MonkeyRunner.waitForConnection(5,'emulator-5554')
c=contacts.contacts(device,'emulator-5554')
c.start()
contactTest={
	'Name':'Tom',
	'Phone':'12453',
	'Website':'cctv',
	'Notes':'test'
}

class test_demo(unittest.TestCase):

	def test_favor(self):
		c.favor('apple')

	def test_delete(self):
		c.delete('jason')

	def test_add(self):
		c.editDetails(None,**contactTest)

	def test_edit(self):
		c.editDetails('jason',Name='apple')


# if __name__ == '__main__':

suite = unittest.TestLoader().loadTestsFromTestCase(test_demo)
# testsuite.addTests([unittest.defaultTestLoader.loadTestsFromTestCase(test_class)])
unittest.TextTestRunner(verbosity=2).run(suite)

# suite=unittest.TestSuite()
# suite.addTests([unittest.defaultTestLoader.loadTestsFromTestCase(test_demo)])
# unittest.TextTestRunner(verbosity=2).run(suite)
'''
outfile = open(reportFile, "w")
runner = HTMLTestRunner.HTMLTestRunner(
		stream=outfile,
		title='Test Report',
		description='Test'
		)
print 'Now start testing ...'
runner.run(suite)
# c.stop()
print 'Testing completed, press any key to exit!'
'''
# c.getCounter()
# c.editDetails(None, Name='thomson',Website='www',Nickname='tom',Company='teleca',Phone='7654321')
# c.favor('jason')
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
# c.getCounter()
# c.favor('jason')
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
# c.editDetails('Jason', Name=None,Company=None,Phone='1234',Nickname=None)
# c.editDetails('Jason', Name='Jason',Company='symphonyteleca',Nickname='tim',Phone='1234')
# c.delete(None)
# c.stop()
# c.addContact(name='222')
# c.editDetails(None, Name='Jason',Website='www',Nickname='tom',Company='teleca',Phone='7654321')
# c.editDetails('7654321', Website='wap',Nickname='jerry',Company='symphonyteleca',Phone='1234567',Name='222')
# c.editDetails('Jason', Name=None,Company=None,Phone='1234',Nickname=None)
# c.editDetails('123', Name='Jason',Company='symphonyteleca',Phone=None)
# trace('end testing')
############################ add contact case Finished ############################