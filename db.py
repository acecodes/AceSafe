import sqlite3
from dirobj import *

# A class specifically for database operations
class DB_drone:
        def routines_insert(self, database, table, *routines):
            # Connect to the database and establish a cursor
            conn = sqlite3.connect(database, isolation_level=None)
            cursor = conn.cursor()

            result = cursor.fetchall()

            try:
                # Delete table if it exists, then recreate it with fresh data
                self.drop(database, table)
                cursor.execute('''CREATE TABLE {0} (Routine TEXT PRIMARY KEY);'''.format(table))
                #print('Table {0} did not exist, created it...'.format(name))
            except:
                # Create the table if it doesn't exist to begin with
                cursor.execute('''CREATE TABLE {0} (Routine TEXT PRIMARY KEY);'''.format(table))

            # Insert name and location into database
            for items in routines:
                # Enable for debugging
                #print('Adding {0} to table {1}'.format(items, name))
                try:
                    cursor.execute('''INSERT INTO {0} (Routine) VALUES (?)'''.format(table), (items,))
                except sqlite3.IntegrityError:
                    # Enable for debugging
                    # print('Unique key {0} already exists, moving on...'.format(items))
                    continue
                
            # Commit and close connection to database
            conn.commit()    
            cursor.close()
            conn.close()

        # Delete table from database
        def drop(self, database, table, echo=False):
            # Connect to the database and establish a cursor
            conn = sqlite3.connect(database, isolation_level=None)
            cursor = conn.cursor()

            if echo == True:
                print('Deleting table {0} from {1}...'.format(table, database))

            try:
                cursor.execute('''DROP TABLE {0}'''.format(table))
                if echo == True:
                    print('Deleted...')
            except:
                print('Table not deleted...')
            # Commit and close connection to database
            conn.commit()    
            cursor.close()
            conn.close()

        # Run routines from database
        def run(self, database, table):
            print('Running routine for {0}...\n'.format(table))
            # Connect to the database and establish a cursor
            conn = sqlite3.connect(database, isolation_level=None)
            cursor = conn.cursor()

            data = cursor.execute('''SELECT * FROM {0}'''.format(table))

            routine_list = []
            for routines in data:
                routine_list.append(list(routines))

            for items in routine_list:
                eval(items[0])

            # Commit and close connection to database
            conn.commit()    
            cursor.close()
            conn.close()


        # Generates a menu for use in the command prompt/bash shell and allows a user to select a syncing routine
        def create_menu(self, database):
            # Connect to the database and establish a cursor
            conn = sqlite3.connect(database, isolation_level=None)
            cursor = conn.cursor()

            # sqlite_master calls all tables from a single database file, as opposed to a normal "SELECT * FROM (table)" call
            data = cursor.execute('''SELECT * FROM sqlite_master''')

            tables = []

            for items in data:
                tables.append(items[2])

            tables = sorted(tables[0::2])

            # Commit and close connection to database
            conn.commit()    
            cursor.close()
            conn.close()

            # Selection section
            print('\nPlease select from the following routines:\n')

            for numbers, items in enumerate(tables):
                print(str(numbers+1) + '.' + ' ' + items)

            try:
                choice = int(input('\nChoice: ')) - 1
                print('\nYou chose: ' + tables[choice] + '\n' + 'Press any key to continue...\n')
                input()
            except IndexError:
                print('\nThat is not a valid choice. Please try again.\n')
                input()
                self.create_menu(database)
            except ValueError:
                print('\nThat is not a valid choice. Please try again.\n')
                input()
                self.create_menu(database)

            # Execute the routine, then return to the main menu (even if there are problems)
            try:
                self.run("routines.db", tables[choice])
                self.create_menu(database)
            except PermissionError:
                print('\nThat file or directory is being used and cannot be copied.\nShut down the program using it and try again.\n')
                input()
                self.create_menu(database)

"""
Database worker instance
"""
DB = DB_drone()

# Build routines and insert them into the database
def rebuild_db():
    DB.routines_insert("routines.db", "ExternalHDs",
        "Music.routine(Files, dst_sub='Music')",
        "Files.routine(ExternalHD1, ExternalHD2)",
        "Files.routine(Thumb, subs='Documents')",
        "Files.routine(Thumb, subs='Books\\Calibre')",
        "Files.routine(Thumb, subs='Programming')")

    DB.routines_insert("routines.db", "Dropbox",
        "Files.routine(Dropbox, subs='Documents')",
        "Files.routine(Dropbox, subs='Books\\Calibre')",
        "Files.routine(Dropbox, subs='Programming')",
        "Files.routine(Dropbox, subs='Photos')")

    DB.routines_insert("routines.db", "Flashcards",
        "Flashcards.routine(Files, dst_sub='Flashcards\\Anki')",
        "Files.routine(Dropbox, ExternalHD1, ExternalHD2, Thumb, subs='Flashcards\\Anki')")

    DB.routines_insert("routines.db", "Browser",
        "Browser.routine(Files, Dropbox, ExternalHD1, ExternalHD2, Thumb, dst_sub='Browsers\\Chrome')")

    DB.routines_insert("routines.db", "Server",
        "Server.routine(Files, Dropbox, ExternalHD1, ExternalHD2, Thumb, dst_sub='Documents\\Server')")

    DB.routines_insert("routines.db", "Apps",
         "Apps.routine(Files, Dropbox, ExternalHD1, ExternalHD2, Thumb, dst_sub='Apps')")