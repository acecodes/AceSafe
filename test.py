import unittest
from os import system
from dirobj import DirObject
from getpass import getuser

user = getuser()

testdir = "/home/%s/dev/testing" % (user)

class Tester(unittest.TestCase):

	def test_db_build(self):
		system("""python3 my_build.py""")

	def test_compare_dirs(self):
		DirTest1 = DirObject('Test1', "/home/%s/dev/testing/1" % (user))
		DirTest2 = DirObject('Test2', "/home/%s/dev/testing/2" % (user))
		DirTest1.routine(DirTest2)

if __name__ == '__main__':
	unittest.main()