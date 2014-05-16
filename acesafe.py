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

"""
Command-line arguments
"""

# Rebuild database
if argv[1] == 'db':
    try:
        system("""rm routines.db""")
    except:
        pass
    system("""python %s""" % build)

# Run a specific routine, bypassing menu system

# Collect arguments in case user wants to run more than one
# This option skips the menu entirely
run_args = argv[2:]

if argv[1] == 'run':
    for args in run_args:
        db.DB.run('routines.db', args)


# Welcome message
def welcome(name=name):
    print('\nWelcome to your file management program, {0}!'.format(name))


"""Start of program"""
if __name__ == '__main__':
    welcome()
    db.DB.create_menu("routines.db")