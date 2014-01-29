# PyFile
# By Ace Eddleman, 2014

import os
import sys
import functions


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
        functions.ext_HDs()
        welcome()
    elif selection == welcome_choices.index('Copy bulk files to Dropbox')+1:
        functions.dropbox()
        welcome()
    elif selection == welcome_choices.index('Copy Anki files')+1:
        functions.anki()
        welcome()
    elif selection == welcome_choices.index('Copy browser files')+1:
        functions.chrome()
        welcome()
    elif selection == welcome_choices.index('Copy server files')+1:
        functions.server()
        welcome()
    elif selection == welcome_choices.index('Sync book files')+1:
        config_choice = int(input('\nPress 2 if you would like to copy Calibre config files as well\nOtherwise, press 1: '))
        if config_choice == 1:
            functions.books()
        elif config_choice == 2:
            functions.books(copy_configs=True)
        welcome()
    elif selection == welcome_choices.index('Sync apps')+1:
        functions.sync_apps()
        welcome()
    elif selection == welcome_choices.index('Exit')+1:
        sys.exit()

# Menu choices
welcome_choices = ['Copy files to external hard drives',
           'Copy bulk files to Dropbox',
           'Copy Anki files',
           'Copy browser files',
           'Copy server files',
           'Sync book files',
           'Sync apps',
           'Exit']

"""Start of program"""
if __name__ == '__main__':
    welcome()
