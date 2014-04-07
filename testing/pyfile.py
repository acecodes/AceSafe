# PyFile
# By Ace Eddleman, 2014

import os
import sys
import classes


"""Functions"""

# Welcome message
def welcome(name='Brochacho Dawg'):
    print('\nWelcome to your file management program, %s!\n' % name)
    print('What would you like to do?\n')
    x = 1 # Starting point for iterator
    for i in welcome_choices:
        print(x, i, sep='. ')
        x += 1
    try:
        choice = int(input('\nPlease make a selection: '))
        select(choice)
    except:
        print('That is not a valid choice.')
        choice = int(input('\nPlease make a selection: '))
        select(choice)

# Function that executes choices from main menu
def select(selection):
    if selection == welcome_choices.index('Copy files to external hard drives')+1:
        classes.MyExternals.backup()
        welcome()
    elif selection == welcome_choices.index('Copy bulk files to Dropbox')+1:
        classes.MyDropbox.backup()
        welcome()
    elif selection == welcome_choices.index('Copy Anki files')+1:
        classes.MyFlashcards.backup()
        welcome()
    elif selection == welcome_choices.index('Copy browser files')+1:
        classes.MyBrowser.backup()
        welcome()
    elif selection == welcome_choices.index('Copy server files')+1:
        classes.MyServer.backup()
        welcome()
    elif selection == welcome_choices.index('Sync apps')+1:
        classes.MyApps.backup()
        welcome()
    elif selection == welcome_choices.index('Exit')+1:
        sys.exit()

# Menu choices
welcome_choices = ['Copy files to external hard drives',
           'Copy bulk files to Dropbox',
           'Copy Anki files',
           'Copy browser files',
           'Copy server files',
           'Sync apps',
           'Exit']

"""Start of program"""
if __name__ == '__main__':
    welcome()