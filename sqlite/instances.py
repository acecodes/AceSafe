from dirobj import DirObject
from getpass import getuser

user = getuser()

user = getuser()

"""
DirObject instances
"""
""""
Create DirObjects for the directories you want to backup using the following syntax:
Name = DirObject('Name', 'location')
These represent directories that can then be compared to other directories.

Examples:
Pictures = DirObject('Pictures', 'C:\Pictures')
Dropbox = DirObject('Dropbox', 'F:\Dropbox')
Movies = DirObject('Movies', 'D:\Media\Movies')
"""

### PLACE DIROBJECTS BELOW: