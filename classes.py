import os
import json
from filecmp import dircmp

##
## Tasks:
## 1. Convert copy functions to classes - Done!
## 2. Implement GUI
## 3. Take over the world. Bwaha....bwa..bwahaha...BWAHAHHAHAHAHA!


"""
Set JSON configuration file and related variables.
The JSON file contains all of the directories that will be used in this script.
"""

JSONopen = open('config.json')
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
            
        
    # Function for copying from one directory to another. Utilizes batch commands for simplification.
    def copy_dirs(self, dst, src='', subs='', dst_sub='', del_dst_dir='', Fresh=False):
        if src == '':
            src = self.src
        if subs != '':
            src = src + '\\' + subs
            dst = dst + '\\' + subs
        if dst_sub != '':
            dst = dst + '\\' + dst_sub
        print('Source: %s' % src)
        print('Destination: %s' % dst)
        if del_dst_dir != '':
            os.system("""rmdir "{0}" /S /Q """.format(dst + '\\' + del_dst_dir))
        if Fresh == False:
            os.system("""xcopy /I /E /Y /D "{0}" "{1}" """.format(src, dst))
        elif Fresh == True:
            os.system("""rmdir "{0}" /S /Q """.format(dst))
            os.system("""xcopy /I /E /Y /D "{0}" "{1}" """.format(src, dst))
            
    # Function for comparing two directories, which can be utilized with compare_delete to get rid of extra folders in a destination
    def dir_compare(self, dst, return_src=False):
        src = self.src
        comparison1 = dircmp(src, dst)
        if return_src == False:
            return comparison1.right_only
        elif return_src == True:
            return comparison1.left_only
        
    # Deletes directories that do not exist in a source directory
    def compare_delete(self, dst, src_sub='', dst_sub=''):
        src = self.src
        if src_sub != '':
            src = src + '\\' + src_sub
        if dst_sub != '':
            dst = dst + '\\' + dst_sub
        folder_differences = self.dir_compare(dst)
        for folders in folder_differences:
            os.system("""rmdir "{0}" /S /Q""".format(dst + '\\' + folders))
            #map(os.system("""rmdir "{0}" /S /Q""".format(dst + '\\' + folders)), folder_differences)
            
    # Message confirming end of copy activity
    def finished(self):
        print("\nAll done!  Returning to main menu...\n")
        input()

    # Warning before copying
    def copy_warn(self, dst):
        print('\n%s files are about to be copied..' % dst)
        print('Press any key to continue...\n')
        input()


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
            copy_dirs(Dirs[directory], subs='Browsers\\Chrome', Fresh=True)
        self.finished()

class Server(DirObject):
    def __init__(self):
        DirObject.__init__(self, Sources['Server'])

    def backup(self):
        copy_warn = self.copy_warn
        copy_dirs = self.copy_dirs
        copy_warn('Server')
        for directory in Dirs:
            copy_dirs(Dirs[directory], subs='Documents\\Server', Fresh=True)
        self.finished()
            
class Apps(DirObject):
    def __init__(self):
        DirObject.__init__(self, Sources['Apps'])
    
    def backup(self):
        copy_warn = self.copy_warn
        copy_dirs = self.copy_dirs
        copy_warn('Apps')
        for directory in Dirs:
            copy_dirs(Dirs[directory], dst_sub='Apps', Fresh=True)
        self.finished()

class Books(DirObject):
    def __init__(self):
        DirObject.__init__(self, Sources['Books'])

    def refresh(self, copy_configs=False):
        copy_dirs = self.copy_dirs
        compare_delete = self.compare_delete
        # Look for folders that do not match the home book folder, delete them and then replace with any new folders
        for directory in Dirs:
            compare_delete(Dirs[directory], dst_sub='Books\\Calibre')
            copy_dirs(Dirs[directory], dst_sub='Books\\Calibre')
        # Copy Calibre configuration files
        if copy_configs == True:
            for directory in Dirs:
                copy_dirs(Dirs[directory], src=Sources['Calibre Config'], dst_sub='Books\\Config', fresh=True)

class Flashcards(DirObject):
    def __init__(self):
        DirObject.__init__(self, Sources['Anki'])

    def choice(self):
        number = int(input('Press 1 to copy only new files.\nPress 2 to refresh folders (delete all, then copy files): '))
        if number == 1:
            self.backup(new=False)
        elif number == 2:
            self.backup(new=True)

    def backup(self, new=False):
        copy_warn = self.copy_warn
        copy_dirs = self.copy_dirs
        copy_warn('Anki')
        if new == False:
            for directory in Dirs:
                copy_dirs(Dirs[directory], dst_sub='Flashcards\\Anki', del_dst_dir='backups')
        elif new == True:
            for directory in Dirs:
                copy_dirs(Dirs[directory], dst_sub='Flashcards\\Anki', del_dst_dir='backups', Fresh=True)
        self.finished()

"""
Instances
"""
MyFlashcards = Flashcards()
MyBrowser = Browser()
MyServer = Server()
MyApps = Apps()
MyExternals = ExternalHDs()
MyBooks = Books()
MyDropbox = Dropbox()




JSONopen.close()


