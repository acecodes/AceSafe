# AceSafe
# By Ace Eddleman, 2014

# Compatability imports that allow usage in Python 2 & 3
from __future__ import print_function
from __future__ import unicode_literals

import db
import dirobj
import os.path
from os import system

if os.path.exists('my_build.py') == True:
    build = 'my_build.py'
else:
    build = 'build.py'

# User name for welcome message
name = 'User'

# Welcome message
def welcome(name=name):
    print('\nWelcome to your file management program, {0}!'.format(name))
    try:
        rebuild = int(input('\nWould you like to rebuild the database before you begin?\nPress 1 for yes, anything else for no:  '))
        if rebuild == 1:
            try:
                system("""rm routines.db""")
            except:
                pass
            system("""python %s""" % build)
        else:
            pass
    except ValueError:
        pass
    except SyntaxError:
        pass


"""Start of program"""
if __name__ == '__main__':
    welcome()
    db.DB.create_menu("routines.db")