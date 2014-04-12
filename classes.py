import os
import filecmp
import shutil
import zipfile
import sys
import sqlite3

##
## Tasks:
## 1. Convert copy functions to classes - Done!
## 2. Implement GUI
## 3. Take over the world. Bwaha....bwa..bwahaha...BWAHAHHAHAHAHA!


"""
Classes
"""

class DirObject:
    """
    A directory object that represents a location on the hard drive.
    The argument 'src' represents that location and is required for all instances.
    """

    def __init__(self, name, src):
        self.name = name
        self.src = src
        # self.db_source_insert() - Disabled until I reinstate database functionality

    def __str__(self):
        return self.src

    def __dict__(self):
        return dict({self.name:self.dst})

    # A big thank you goes out to Pi Marillion (on StackOverflow) for helping me work out the mechanics of this method
    def copy_dirs(self, dst, subs='', src_sub='', dst_sub=''):
        """Searches for and deletes files not found in the source, then copies any new files to the destination
        """
        # Join paths (if specified)
        src = self.src
        if subs:
            src = os.path.join(src, subs)
            dst = os.path.join(dst, subs)
        if dst_sub:
            dst = os.path.join(dst, dst_sub)
        if src_sub:
            src = os.path.join(src, src_sub)
        print('\nComparing...\n')
        print('\nSource: %s' % src)
        print('Destination: %s\n' % dst)
        for src_root, src_dirs, src_files in os.walk(src, topdown=True):
            dst_root = os.path.join(dst, os.path.relpath(src_root, src))
            dirs = filecmp.dircmp(src_root, dst_root)
            # Find old files and delete them from destination
            for item in dirs.right_only:
                try:
                    print('Removing ' + item)
                except UnicodeEncodeError:
                    print('Removing file (Unicode error)') # Prevents the program from stopping in the event of an awkward file name
                dst_path = os.path.join(dst_root, item)
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)
                else:
                    os.remove(dst_path)
            # Find new files and add them to destination
            for item in dirs.left_only:
                try:
                    print('Adding ' + item)
                except UnicodeEncodeError:
                    print('Adding file (Unicode error)') # Prevents the program from stopping in the event of an awkward file name
                src_path = os.path.join(src_root, item)
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, os.path.join(dst_root, item))
                else:
                    shutil.copy2(src_path, os.path.join(dst_root, item))
        # Once clearing and adding has completed, update existing files
        print('\nUpdating: ')
        os.system("""xcopy /I /E /Y /D "{0}" "{1}" """.format(src, dst))

    def routine(self, *dirobjs,**copy_args):
        for dirs in dirobjs:
            self.copy_dirs(dirs.src, **copy_args)

    # Warning before copying
    def copy_warn(self, dst):
        print('\n%s files are about to be copied..' % dst)
        print('Press any key to continue...\n')
        input()

    # Compress a DirObject into a zip file
    def compress(self, dst):
        """Zip everything in a folder (including subfolders).
        """
        src = self.src
        parent = os.path.dirname(src)
        # Walk through the source directory
        contents = os.walk(src)
        try:
            zipper = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
            for root, folders, files in contents:
                # Ensure that subs are included
                for folder_name in folders:
                    absolute_path = os.path.join(root, folder_name)
                    relative_path = absolute_path.replace(parent + '\\', '')
                    print('Adding contents of %s to %s...' % (absolute_path, dst))
                for file_name in files:
                    absolute_path = os.path.join(root, file_name)
                    relative_path = absolute_path.replace(parent + '\\', '')
                    zipper.write(absolute_path, relative_path)
            print('%s created successfully.' % dst)
        except IOError:
            sys.exit(1)
        except OSError:
            sys.exit(1)
        except zipfile.BadZipFile:
            sys.exit(1)
        finally:
            zipper.close()


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


"""
Object factory
"""

def factory(Parent_Class, *pargs, **kargs):
       return Parent_Class(*pargs, **kargs)

"""
Instances
"""
Apps = DirObject('Apps', 'D:\\Dropbox\\Apps')
Browser = DirObject('Browser', 'C:\\Users\\User1\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
Dropbox = DirObject('Dropbox', 'D:\\Dropbox')
ExternalHD1 = DirObject('ExternalHD1', 'G:\\Files')
ExternalHD2 = DirObject('ExternalHD2', 'H:\\Files')
Files = DirObject('Files', 'D:\\Files')
Flashcards = DirObject('Flashcards', 'D:\\User\\Documents\\Anki\\User 1')
Music = DirObject('Music', 'D:\\Dropbox\\Music')
Server = DirObject('Server', 'C:\\XAMPP\\htdocs')
Thumb = DirObject('Thumb', 'F:\\')

DB = DB_drone()


# Build routines and insert them into the database
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
    "Server.routine(Files, Dropbox, ExternalHD1, ExternalHD2, Thumb, dst_sub='Documents\\Server')")

if __name__ == '__main__':
    pass
