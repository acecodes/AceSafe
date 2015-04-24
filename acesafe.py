# AceSafe
# By Ace Eddleman, 2014

# Compatability imports that allow usage in Python 2 & 3
from __future__ import print_function

import json
from os import environ
from sys import argv
from json_functions import JSONRunner

try:
    json_file = environ['ACESAFE_JSON']
except KeyError:
    json_file = 'test_json'

"""
Command-line arguments
"""

help_text = """
        Arguments available for AceSafe:

        run - Run a specific routine, i.e. "python acesafe.py run Dropbox"
        view-routines - View routines in your database file

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
    for argv[1] in run_args:
        JSONRunner.routine(json_file, argv[1])
    exit()

if argv[1] == 'view-routines':
    with open(json_file + '.json') as data_file:
        json_routines = json.load(data_file)
    print("\nCurrently available routines:\n")
    for keys in json_routines['routines'].items():
        print(keys[0], ' - ', keys[1]['setup']['description'])
    print()
    exit()
