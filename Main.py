import os,sys
try:
	for p in os.environ['PYTHONPATH'].split(os.pathsep):
		if not p in sys.path:
			sys.path.append(p)
except:
	pass
from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage
import contacts
import HTMLTestRunner
import unittest

HTML_SUPPORT = False

rootPath = os.path.dirname(os.path.abspath(__file__))
reportFile = rootPath + os.sep + 'TestReport.html'

device=MonkeyRunner.waitForConnection(5,'045070c5429fb317')
if not device:
	print >> sys.stderr,"connection failed"
	sys.exit(1)

contactTest={
	'Name':'Jason',
	'Phone':'1234567890',
	'Website':'www.baidu.com',
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
		for i in range(3):
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
		c.snapshot('snaptest')
        
    @classmethod
    def setUpClass(cls):
        c=contacts.contacts(device,'045070c5429fb317')
        c.start()
    
    @classmethod
    def tearDownClass(cls):
        c.stop()

if __name__ == '__main__':

	suite=unittest.TestSuite()
	# suite.addTest(test_demo("test_add"))
	# suite.addTest(test_demo("test_favor"))
	# suite.addTest(test_demo("test_delete"))
	# suite.addTest(test_demo("test_snap"))
	# suite.addTests([unittest.defaultTestLoader.loadTestsFromTestCase(test_demo)])
	# suite = unittest.TestLoader().loadTestsFromTestCase(test_demo)
	if not HTML_SUPPORT:
		unittest.TextTestRunner(verbosity=2).run(suite)
	else:
		outfile = open(reportFile, "w")
		runner = HTMLTestRunner.HTMLTestRunner(
				stream=outfile,
				title='Test Report',
				description='Test'
				)
		print 'Now start testing ...'
		runner.run(suite)
		print 'Testing completed, press any key to exit!'
