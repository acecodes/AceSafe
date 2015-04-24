# AceSafe
# By Ace Eddleman, 2014

# Compatability imports that allow usage in Python 2 & 3
from __future__ import print_function

import db
import os.path
from os import system
from sys import argv, platform
from dirobj import DirObject

if os.path.exists('my_build.py') == True:
    build = 'my_build.py'
else:
    build = 'build.py'

# User name for welcome message
name = 'User'


def welcome(name=name):
    """Welcome message"""
    print('\nWelcome to your file management program, {0}!'.format(name))

"""
Command-line arguments
"""

help_text = """
        Arguments available for AceSafe:

        run - Run a specific routine, i.e. "python acesafe.py run Dropbox"
        view-routines - View routines in your database file
        dirs - Takes two dirs (source and destination) and runs a comparison
        menu - Creates a numbered menu out of your routines

        For example:
        python acesafe.py dirs ~/user1/downloads ~/user2/downloads

        This command would compare the contents of user1/downloads to the
        contents of user2/downloads, then delete or add files as needed
        between them. If there are files in user2/downloads that
        do not exist in user1/downloads, they will be deleted from user2.
        If there are files in user1/downloads that do no exist in
        user2/downloads, they will be copied from user1 to user2.

        AceSafe runs in both Python 2.x and 3.x

        Visit www.acecodes.net or github.com/acecodes/acesafe
        for more information.
        """

if 'help' in argv or len(argv) == 1:
    print(help_text)
    exit()

run_args = argv[2:]

# Rebuild database
if argv[1] == 'db':
    try:
        system("""rm routines.db""")
    except:
        pass
    system("""python %s""" % build)
    exit()

# Run a specific routine, bypassing menu system

# Collect arguments in case user wants to run more than one
# This option skips the menu entirely


if argv[1] == 'run':
    for argv[1] in run_args:
        db.DB.run('routines.db', argv[1])
    exit()

if argv[1] == 'run-sleep':
    for argv[1] in run_args:
        db.DB.run('routines.db', argv[1])
    print("\nRoutines completed, going to sleep...")
    if platform == 'win32':
        pass
        # Not implemented for Windows platforms yet
    else:
        try:
            system("sudo pm-suspend")
        except:
            print(
                "\nThe suspend command is not supported by your OS.\n")
    exit()

if argv[1] == 'view-routines':
    print('\nYour currently accessible routines:\n')
    for items in db.DB.create_menu("routines.db", just_view=True):
        print(items)
    print(
        """
        If you would like to run these without the
        menu system, use the "run" argument
        """)
    exit()

if argv[1] == 'dirs':
    src = DirObject('source', argv[2])
    dst = DirObject('destination', argv[3])
    if os.path.exists(argv[2]) and os.path.exists(argv[3]):
        print(
            '\nCopying files from {0} to {1} - press any key to continue...'.format(src.src, dst.src))
        try:
            input()
        except SyntaxError:
            pass
        src.copy_dirs(dst.src)
    else:
        print('\nThose paths are invalid, please try again.\n')
    exit()

if argv[1] == 'menu':
    welcome()
    db.DB.create_menu("routines.db")
