# AceSafe
# By Ace Eddleman, 2014

# Compatability imports that allow usage in Python 2 & 3
from __future__ import print_function

import db
import os.path
from os import system
from sys import argv
from dirobj import DirObject

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
    exit()

if argv[1] == 'view-routines':
    print('\nYour currently accessible routines:\n')
    for items in db.DB.create_menu("routines.db", just_view=True):
        print(items)
    print('\nIf you would like to run these without the menu system, use the "run" argument')
    exit()

if argv[1] == 'help':
    print('\n')
    print('Arguments available for AceSafe:\nrun - Run a specific routine, i.e. "python acesafe.py run Dropbox"\nview-routines - View currently accessible routines in your database file\ndirs - Do a quick and dirty comparison between two directories (syntax is dirs "<source>"" "<destination>"')
    print('\n')
    exit()

if argv[1] == 'dirs':
    src = DirObject('source', argv[2])
    dst = DirObject('destination', argv[3])
    print('\nCopying files from {0} to {1}...'.format(src.src, dst.src))
    try:
        input()
    except SyntaxError:
        pass
    src.copy_dirs(dst.src)
    exit()


# Welcome message
def welcome(name=name):
    print('\nWelcome to your file management program, {0}!'.format(name))


"""Start of program"""
if __name__ == '__main__':
    welcome()
    db.DB.create_menu("routines.db")