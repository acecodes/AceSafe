# AceSafe
# By Ace Eddleman, 2014

# Compatability imports that allow usage in Python 2 & 3
from __future__ import print_function

import db
import dirobj
import os.path
from os import system
from sys import argv

if os.path.exists('my_build.py') == True:
    build = 'my_build.py'
else:
    build = 'build.py'

# User name for welcome message
name = 'User'

# Arguments
if 'db' in argv:
    try:
        system("""rm routines.db""")
    except:
        pass
    system("""python %s""" % build)

# Welcome message
def welcome(name=name):
    print('\nWelcome to your file management program, {0}!'.format(name))


"""Start of program"""
if __name__ == '__main__':
    welcome()
    db.DB.create_menu("routines.db")