import unittest
from os import system
from dirobj import DirObject
from getpass import getuser
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = getuser()

testdir = "/home/%s/dev/testing" % (user)

Base = declarative_base()

engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)


class Routine(Base):
	# Placeholder because SQLAlchemy requires that this be declared for any ORM class
	__tablename__ = 'Rename This'

	def __init__(self, name):
		self.name = name
		__tablename__ = name

	Routines = Column(String, primary_key=True)

	def __repr__(self):
		return "Routine Table Name: {0}".format(self.__tablename__)

	def add_routines(self, *routines):
		session = Session()
		session.add(self(Routines=routines))
		session.commit()
		# Add code for inserting routines into database here



#class Tester(unittest.TestCase):

Dropbox = Routine('Dropbox')

if __name__ == '__main__':
	#unittest.main()
	print(Dropbox)
	print(Dropbox.__table__)