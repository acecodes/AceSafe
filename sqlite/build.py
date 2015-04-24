from db import DB_drone
from dirobj import DirObject


"""
Database worker instance - DO NOT MODIFY!
"""
DB = DB_drone()

"""
Build routines and insert them into the database using the following syntax:
DB.routines_insert("routines.db", "DirObject.routine(routine)", "DirObject.routine(routine, flags)")

An example:

DB.routines_insert("routines.db", "Dropbox", "Files.routine(Dropbox, subs='Documents')")

This creates a routine called "Dropbox" (which will show up on the main menu) and runs by looking at the 
'Files' DirObject, then compares it to the 'Dropbox' DirObject. The 'subs' flag indicates that the comparison is happening on the subdirectory called 'Documents' in both the source and destination directories.

"""

### PLACE ROUTINES BELOW:
