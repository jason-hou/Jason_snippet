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

device=MonkeyRunner.waitForConnection(5,'0a78310541615517')
if not device:
	print >> sys.stderr,"connection failed"
	sys.exit(1)
c=contacts.contacts(device,'0a78310541615517')
c.start()
contactTest={
	'Name':'Tom',
	'Phone':'12453',
	'Website':'cctv',
	'Notes':'test'
}

class test_demo(unittest.TestCase):

	def test_favor(self):
		c.favor('Tom')

	def test_delete(self):
		before=c.getCounter()
		c.delete('jason')
		after=c.getCounter()
		self.assertEqual(before-after,1)

	def test_add(self):
		before=c.getCounter()
		c.addContact(**contactTest)
		after=c.getCounter()
		self.assertEqual(after-before,1)

	def test_edit(self):
		c.editDetails('Tom',Phone='10086')

	def test_sort(self):
		c.sortAndViewAs(sort=True,first=False)

	def test_view(self):
		c.sortAndViewAs(sort=False,first=False)

	def test_snap(self):
		c.snapshot('test')

if __name__ == '__main__':

	# suite = unittest.TestLoader().loadTestsFromTestCase(test_demo)
	# unittest.TextTestRunner(verbosity=2).run(suite)

	# suite=unittest.TestSuite()
	# suite.addTests([unittest.defaultTestLoader.loadTestsFromTestCase(test_demo)])
	# unittest.TextTestRunner(verbosity=2).run(suite)
	suite=unittest.TestSuite()
	# suite.addTest(test_demo("test_favor"))
	# suite.addTest(test_demo("test_delete"))
	suite.addTest(test_demo("test_snap"))
	unittest.TextTestRunner(verbosity=2).run(suite)
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
