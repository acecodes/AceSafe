#!/usr/bin/env python

# Compatability imports that allow usage in Python 2 & 3
from __future__ import print_function

import json
from os import environ
from sys import argv
from json_functions import JSONRunner

"""
AceSafe
An easy-to-use backup utility by Ace Eddleman.
"""

try:
    json_file = environ['ACESAFE_JSON']
except KeyError:
    json_file = 'test_json'

"""
Command-line arguments
"""

help_text = """
        Arguments available for AceSafe:

        run - Run a specific routine from your JSON file
        Syntax:
        For example: ./acesafe.py run dropbox
        (Runs a routine called "dropbox" that is defined within your JSON file)

        view-routines - View routines in your JSON file
        Syntax: ./acesafe.py view-routines

        compare - Compare two directories without using a JSON file
        Syntax: compare {source} {destination}
        Example: ./acesafe.py compare /home/user1/test1 /home/user1/test2

        generate - Generate JSON for a routine (for insertion into your JSON file).
        Syntax: generate {routine title} {source} {destination}
        Example: ./acesafe.py generate testRoutine /home/user1/test1 /home/user1/test2

        log - Output a log file.
        Syntax: run {routine_1} {routine_n} log
        Example: ./acesafe.py run test_routine test_routine2 log
        Note: log MUST be placed as the LAST argument to work correctly!

        This program runs with a JSON file, which by default is test_json.json.
        If you want a different JSON file to be used, create it, place it in
        this directory, then set the "json_file" environment variable.

        AceSafe runs in both Python 2.x and 3.x

        Visit www.acecodes.net or github.com/acecodes/acesafe
        for more information.
        """

if 'help' in argv or len(argv) == 1:
    print(help_text)
    exit()

run_args = argv[2:]

# Collect arguments in case user wants to run more than one
if argv[1] == 'run':
    log = False
    if argv[-1] == 'log':
        log = True
    for argv[1] in run_args:
        if argv[1] == 'log':
            pass
        else:
            JSONRunner.routine(json_file, argv[1], logging=log)
    exit()

if argv[1] == 'view-routines':
    with open(json_file + '.json') as data_file:
        json_routines = json.load(data_file)
    print("\nCurrently available routines:\n")
    for i in json_routines.keys():
        print(i)
    print()
    exit()

if argv[1] == 'compare':
    src = argv[2]
    dst = argv[3]
    log = False
    if 'log' in argv:
        log = True
    JSONRunner.copy_dirs(src, dst, logging=log)
    exit()

if argv[1] == 'generate':
    title = argv[2]
    src = argv[3]
    dst = argv[4]
    print("Here's your JSON:")
    print(json.loads(JSONRunner.routine_json(title, src, dst)))
