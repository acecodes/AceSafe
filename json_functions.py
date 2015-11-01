import json
import os
import subprocess
import filecmp
import shutil
import sys

plat = sys.platform


class JSONRunner:

    @staticmethod
    def copy_dirs(src, dst,
                  subs=None,
                  src_sub=None,
                  dst_sub=None,
                  logging=False):
        """
        Searches for and deletes files not found in the source,
        then copies any new files to the destination
        """
        # Join paths (if specified)
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
            log_items = []

            # Find old files and delete them from destination
            for item in dirs.right_only:
                try:
                    print('Removing ' + item)
                except UnicodeEncodeError:
                    # Prevents the program from stopping in the event of an
                    # awkward file name
                    print('Removing file (Unicode error)')
                dst_path = os.path.join(dst_root, item)
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)
                else:
                    os.remove(dst_path)
                if logging:
                    log_items.append((item, 'Removed'))

            # Find new files and add them to destination
            for item in dirs.left_only:
                try:
                    print('Adding ' + item)
                except UnicodeEncodeError:
                    # Prevents the program from stopping in the event of an
                    # awkward file name
                    print('Adding file (Unicode error)')
                src_path = os.path.join(src_root, item)
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, os.path.join(dst_root, item))
                else:
                    shutil.copy2(src_path, os.path.join(dst_root, item))
                if logging:
                    log_items.append((item, 'Added'))

        if logging:
            with open('acesafe.log', 'w') as logfile:
                for item in log_items:
                    logfile.write(item)

        # Once clearing and adding has completed, update existing files
        print('\nUpdating: ')
        if plat != 'win32':
            if logging is True:
                print('Saving updates to log file...')
                with open('acesafe.log', 'a') as logfile_update:
                    subprocess.call("""rsync -r -u -v --links "{0}"/* "{1}" """.format(src, dst), shell=True, stdout=logfile_update)
            else:
                subprocess.call("""rsync -r -u -v --links "{0}"/* "{1}" """.format(src, dst), shell=True)
        else:
            subprocess.call("""xcopy /I /E /Y /D "{0}" "{1}" """.format(src, dst))

    @staticmethod
    def routine(JSON_Source, routine, logging=False):
        """
        Run a backup routine from a JSON file
        Keep in mind that subdirectories MUST exist ahead of time!
        Use absolute paths in your JSON file - don't use ~/
        """

        try:

            dir_errors = []

            with open(JSON_Source + '.json') as data_file:
                dir_obj = json.load(data_file)

            src = dir_obj[routine]['src']
            dst = dir_obj[routine]['dst']

            JSONRunner.copy_dirs(src, dst, logging=logging)

        except KeyboardInterrupt:
            print('\nYou have elected to exit the program, goodbye!\n')
            exit()
        # except KeyError:
        #     print('That routine does not exist. Please try again.')
        except IOError:
            print('That JSON file is invalid. Please try again.')
        if len(dir_errors) > 0:
            print('\nThese directories experienced errors:')
            for i in dir_errors:
                print(i)
