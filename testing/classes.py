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

    # -- BEGIN FILE OPERATION FUNCTIONS -- #

    # A big thank you goes out to Pi Marillion (on StackOverflow) for helping me work out the mechanics of this method
    def copy_dirs(self, dst, src='', subs='', dst_sub=''):
        """Searches for and deletes files not found in the source, then copies any new files to the destination
        """

        if not src:
            src = self.src
        if subs:
            src = os.path.join(src, subs)
            dst = os.path.join(dst, subs)
        if dst_sub:
            dst = os.path.join(dst, dst_sub)
        print('\nSource: %s' % src)
        print('Destination: %s\n' % dst)
        for src_root, src_dirs, src_files in os.walk(src, topdown=True):
            dst_root = os.path.join(dst, os.path.relpath(src_root, src))
            dirs = filecmp.dircmp(src_root, dst_root)
            # Find old files and delete them from destination
            for item in dirs.right_only:
                try:
                    print('Removing ' + item)
                except:
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
                except:
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
            self.copy_dirs(dirs, **copy_args)

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
        
    # -- END FILE OPERATION FUNCTIONS -- #

    # -- BEGIN DATABASE FUNCTIONS -- #

    def db_source_insert(self, table=''):
        # Connect to the database and establish a cursor
        conn = sqlite3.connect('settings.db', isolation_level=None)
        cursor = conn.cursor()
        info = (self.name, self.src)

        result = cursor.fetchall()

        if table == '':
            table = 'Sources'

        try:
            # Create table if it doesn't exist
            cursor.execute('''CREATE TABLE {0} (Name text PRIMARY KEY, Location text)'''.format(table))
            print('Table does not exist, creating one...')
        except:
            pass

        try:
            # Insert name and location into database
            cursor.execute('''INSERT INTO {0} VALUES (?, ?)'''.format(table), info)
        except sqlite3.IntegrityError:
            print('The unique key "{0}" already exists, moving on...'.format(self.name))
            pass
            
        # Commit and close connection to database
        conn.commit()    
        cursor.close()
        conn.close()

    def db_update(self, location, table=''):
        # Connect to the database and establish a cursor
        conn = sqlite3.connect('settings.db', isolation_level=None)
        cursor = conn.cursor()

        print('Updating database with new object location for {0}...'.format(self.name))

        self.src = location

        if table == '':
            table = 'Sources'

        cursor.execute('''UPDATE {0} SET Location = ? WHERE Name = ?'''.format(table), (location, self.name))

        print('Database updated, {0} new location is: {1}'.format(self.name, self.src))

        # Commit and close connection to database
        conn.commit()    
        cursor.close()
        conn.close()

    # Function for pulling the path of an object from the database
    def db_path(self, table):
        # Connect to the database and establish a cursor
        conn = sqlite3.connect('settings.db')
        cursor = conn.cursor()

        # View table
        cursor.execute('SELECT * FROM {0}'.format(table))
        # Convert table to dictionary
        Table = dict(cursor.fetchall())
        # Create path variable from matching object name in table
        path = Table[self.name]

        # Commit and close connection to database
        conn.commit()    
        cursor.close()
        conn.close()

        return path

        # -- END DATABASE FUNCTIONS -- #
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
ExternalHD1 = DirObject('ExternalHD1', 'G:\\')
ExternalHD2 = DirObject('ExternalHD2', 'H:\\')
Files = DirObject('Files', 'D:\\Files')
Flashcards = DirObject('Flashcards', 'D:\\User\\Documents\\Anki\\User 1')
Music = DirObject('Music', 'D:\\Dropbox\\Music')
Server = DirObject('Server', 'C:\\XAMPP\\htdocs')
Testing = DirObject('Testing', 'C:\\Temp')
Testing2 = DirObject('Testing 2', 'C:\\Temp 2')
Testing3 = DirObject('Testing 3', 'C:\\Temp 3')
Thumb = DirObject('Thumb', 'F:\\')

if __name__ == '__main__':
    Testing.routine(Testing2.src, Testing3.src, subs='2')
    pass