import os
import json
import filecmp
import shutil
import zipfile
import sys

##
## Tasks:
## 1. Convert copy functions to classes - Done!
## 2. Implement GUI
## 3. Take over the world. Bwaha....bwa..bwahaha...BWAHAHHAHAHAHA!


"""
Set JSON configuration file and related variables.
The JSON file contains all of the directories that will be used in this script.
"""

JSONopen = open('D:\\Files\\Programming\\Python\\my_projects\\PyFile\\config.json')
JSONdata = json.load(JSONopen)

Sources = JSONdata['Sources']
Dirs = JSONdata['Dirs']
Dropbox_Dirs = JSONdata['Dropbox Dirs']

"""
Classes
"""

class DirObject:
    """
    A directory object that represents a location on the hard drive.
    The argument 'src' represents that location and is required for all instances.
    """
    
    def __init__(self, src):
        self.src = src

    def __str__(self):
        return 'This object\'s home directory is: %s' % (self.src)

    def __dict__(self):
        return dict({self.name:self.dst})

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
                print('Removing ' + item)
                dst_path = os.path.join(dst_root, item)
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)
                else:
                    os.remove(dst_path)
            # Find new files and add them to destination
            for item in dirs.left_only:
                print('Adding ' + item)
                src_path = os.path.join(src_root, item)
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, os.path.join(dst_root, item))
                else:
                    shutil.copy2(src_path, os.path.join(dst_root, item))
        # Once clearing and adding has completed, update existing files
        print('\nUpdating: ')
        os.system("""xcopy /I /E /Y /D "{0}" "{1}" """.format(src, dst))

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
        

            
    # Message confirming end of copy activity
    def finished(self):
        print("\nAll done!  Returning to main menu...\n")
        input()

    # Warning before copying
    def copy_warn(self, dst):
        print('\n%s files are about to be copied..' % dst)
        print('Press any key to continue...\n')
        input()

"""
Directory Objects
"""

class Testing(DirObject):
    def __init__(self):
        DirObject.__init__(self, 'C:\\Temp\\1')


class Dropbox(DirObject):
    def __init__(self):
        DirObject.__init__(self, Dirs['Dropbox'])
        
    def backup(self):
        copy_warn = self.copy_warn
        copy_dirs = self.copy_dirs
        copy_warn('Dropbox')
        for directory in Dropbox_Dirs:
            copy_dirs(Dirs['Dropbox'], src=Dirs['Files'], subs=Dropbox_Dirs[directory])
        self.finished()

class ExternalHDs(DirObject):
    def __init__(self):
        DirObject.__init__(self, Dirs['Files'])

    def backup(self):
        copy_warn = self.copy_warn
        copy_dirs = self.copy_dirs
        copy_warn('External backups')
        copy_dirs(Dirs['External HD 1'])
        copy_dirs(Dirs['External HD 2'])
        copy_dirs(Dirs['Thumb Drive'], subs='Books\\Calibre')
        copy_dirs(Dirs['Thumb Drive'], subs='Documents')
        copy_dirs(Dirs['Thumb Drive'], subs='Programming')
        self.finished()

class Browser(DirObject):
    def __init__(self):
        DirObject.__init__(self, Sources['Chrome'])

    def backup(self):
        copy_warn = self.copy_warn
        copy_dirs = self.copy_dirs
        copy_warn('Browser')
        for directory in Dirs:
            copy_dirs(Dirs[directory], dst_sub='Browsers\\Chrome')
        self.finished()

class Server(DirObject):
    def __init__(self):
        DirObject.__init__(self, Sources['Server'])

    def backup(self):
        copy_warn = self.copy_warn
        copy_dirs = self.copy_dirs
        copy_warn('Server')
        for directory in Dirs:
            copy_dirs(Dirs[directory], dst_sub='Documents\\Server')
        self.finished()
            
class Apps(DirObject):
    def __init__(self):
        DirObject.__init__(self, Sources['Apps'])
    
    def backup(self):
        copy_warn = self.copy_warn
        copy_dirs = self.copy_dirs
        copy_warn('Apps')
        for directory in Dirs:
            copy_dirs(Dirs[directory], dst_sub='Apps')
        self.finished()

class Flashcards(DirObject):
    def __init__(self):
        DirObject.__init__(self, Sources['Anki'])

    def backup(self):
        # Send Anki CSS file to GitHub repository directory
        copy_warn = self.copy_warn
        copy_dirs = self.copy_dirs
        copy_warn('Anki')
        print('\nCopying CSS file to GitHub repository...\n')
        os.system("""xcopy /I /E /Y /D "{0}" "{1}" """.format(self.src + '\\' + 'collection.media\\_CSS-Master.css', 'D:\\Files\\Programming\\CSS\\AnkiCSS'))
        for directory in Dirs:
            copy_dirs(Dirs[directory], dst_sub='Flashcards\\Anki')
        self.finished()


"""
Instances
"""
MyFlashcards = Flashcards()
MyBrowser = Browser()
MyServer = Server()
MyApps = Apps()
MyExternals = ExternalHDs()
MyDropbox = Dropbox()
Test = Testing()


JSONopen.close()