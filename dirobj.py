import os
import filecmp
import shutil
import zipfile
import sys

plat = sys.platform

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
        if plat != 'win32':
            os.system("""rsync -v -r "{0}"/* "{1}" """.format(src, dst))
        else:
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




"""
Object factory
"""
def factory(Parent_Class, *pargs, **kargs):
       return Parent_Class(*pargs, **kargs)