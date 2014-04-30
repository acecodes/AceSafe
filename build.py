#### IMPORTANT: RENAME THIS SCRIPT TO my_build.py BEFORE USE! ####

# Database building script
from db import DB_drone
from dirobj import DirObject


"""
Database worker instance
"""
DB = DB_drone()
if __name__ == '__main__':
# Build routines and insert them into the database using the following syntax:
# DB.routines_insert("routines.db", "DirObject.routine(routine)", "DirObject.routine(routine, flags)")


# An example:
# DB.routines_insert("routines.db", "Dropbox", "Files.routine(Dropbox, subs='Documents')")