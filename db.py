import sqlite3
from getpass import getuser
try:
    from my_instances import *
except ImportError:
    from instances import *

# A class specifically for database operations
class DB_drone:
        def routines_insert(self, database, table, *routines):
            # Connect to the database and establish a cursor
            conn = sqlite3.connect(database, isolation_level=None)
            cursor = conn.cursor()

            result = cursor.fetchall()

            cursor.execute('''CREATE TABLE {0} (Routine TEXT PRIMARY KEY);'''.format(table))

            # Insert name and location into database
            for items in routines:
                # Enable for debugging
                print('Adding {0} to table {1}'.format(items, table))
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

        def invalid_choice(self):
            print('\nThat is not a valid choice. Please try again.\n')
            input()        

        # Generates a menu for use in the command prompt/bash shell and allows a user to select a syncing routine
        def create_menu(self, database, just_view=False):
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

            if just_view == True:
                return tables

            # Selection section
            print('\nPlease select from the following routines, or press 0 to exit:\n')

            for numbers, items in enumerate(tables):
                print(str(numbers+1) + '.' + ' ' + items)

            try:
                choice = int(input('\nChoice: ')) - 1
                if choice == -1:
                    exit()
                print('\nYou chose: ' + tables[choice] + '\n' + 'Press any key to continue...\n')
                input()
            except IndexError:
                self.invalid_choice()
                self.create_menu(database)    
            except ValueError:
                self.invalid_choice()
                self.create_menu(database)    
            except SyntaxError:
                pass
            finally:
                pass
            # Execute the routine, then return to the main menu (even if there are problems)
            self.run("routines.db", tables[choice])
            self.create_menu(database)

"""
Database worker instance
"""
DB = DB_drone()
