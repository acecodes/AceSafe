# AceSafe

This is the script I built (out of the carcass of my horrendously unfashionable batch file system). The primary purpose of this program is to send files I value the most to my various backup sources. The script first builds some objects that each correspond with a path on the user's hard drive. Then each path is turned into an class object and customized so that their files can be manipulated with copying methods. Once that is done, the program builds a database file that consists of several tables, with each table containing syncing routines.

The most powerful feature of this program is its copying method, which checks the source directory (defined in the DirObject's __init__) and then compares its contents to the contents of the destination directory. If there are files that exist only in the destination, they will be deleted. Then new and updated files are copied over. This process ensures a 1-to-1 sync between files and their backups, with no extra files lingering on forever because file names or paths have been changed.

AceSafe has saved me boatloads of time, particularly with the addition of the "check and delete" feature. I used to have to manually delete files every time I changed a filename or something, otherwise I would end up with copies of the same files that only differed in filenames. For example, if I had a file called "readme_old.txt" and then renamed it "readme_new.txt", I would end up with both files. Now, only the "readme_new.txt" will remain.

If you would like to use this script on your computer, simply open up the "instances.py" and "build.py" files in an editor and follow the instructions I've left in the comments.

Once you've done that, run the following at the command line:

    python acesafe.py

And when asked whether you want to rebuild the database, press 1. This will create a "routines.db" SQLite file that contains DirObject routines you created in "build.py." Once you've done this inital build, you won't need to do it again unless you make changes to either "instances.py" or "build.py."

A fuller explanation of why I made AceSafe and what it does can be found <a href="http://www.acecodes.net/?p=72">here</a>.
