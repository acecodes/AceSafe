# AceSafe

This is a program I built out of the carcass of my horrendously unfashionable batch file backup system. The primary purpose of this program is to send files that are valued the most to your various backup sources. First, AceSafe builds some objects that each correspond with a path on the user's hard drive. Then each path is turned into an class object and customized so that their files can be manipulated with copying methods. Once that is done, the program builds a database file that consists of several tables, with each table containing syncing routines.

The most powerful feature of this program is its copying method, which checks the source directory (defined in the <code>DirObject</code>'s <code>__init__</code>) and then compares its contents to the contents of the destination directory. If there are files that exist only in the destination, they will be deleted. Then new and updated files are copied over. This process ensures a 1-to-1 sync between files and their backups, with no extra files lingering on forever because file names or paths have been changed.

AceSafe has saved me boatloads of time, particularly with the addition of the "check and delete" feature. I used to have to manually delete files every time I changed a filename or something, otherwise I would end up with copies of the same files that only differed in filenames. For example, if I had a file called "readme_old.txt" and then renamed it "readme_new.txt", I would end up with both files. Now, only the "readme_new.txt" will remain.

## Instructions

If you would like to use this script on your computer, simply open up the <code>instances.py</code> and <code>build.py</code> files in an editor and follow the instructions I've left in the comments.

Once you've done that, run the following at the command line:

    python acesafe.py db

This will create a "routines.db" SQLite file that contains DirObject routines you created in <code>build.py</code>. Once you've done this inital build, you won't need to do it again unless you make changes to either <code>instances.py</code> or <code>build.py</code>.

So, for the sake of clarification, <i>once you've built your initial database file, you don't need to use the <code>db</code> command when running the script</i>. You only need to run it again if you've changed the <code>instances.py</code> or <code>build.py</code> files.

Now all you have to do is run the script with Python:

    python acesafe.py
    
This will generate a menu system based on the routines you created in the <code>build.py</code> file.
    
## Command-line use

If you'd prefer to just run a single routine (or a set of routines at once), you can now (as of 5/16/2014) use the command line to skip the menu system.

You will still have to run the <code>db</code> command mentioned above, but once you've done that, you can send commands straight to the script via the database. To accomplish this, you need to use the <code>run</code> argument when invoking the script. For example:

    python acesafe.py run Dropbox
    
This would look for a database table called <code>Dropbox</code> (specified in the <code>build.py</code> file) and run a routine using DirObjects you created in the <code>instances.py</code> file.

You can also run multiple routines at once. For example:

    python acesafe.py run Dropbox ExtHD1 ExtHD2
    
This would run the routines <code>Dropbox</code>, <code>ExtHD1</code> and <code>ExtHD2</code> back-to-back.

You can also just do a quick and dirty comparison between two directories without utilizing a menu system or database file. This can be accomplished using the <code>dirs</code> like so:

    python acesafe.py dirs "<source>" "<destination>"

For example:
    
    python acesafe.py dirs "/home/user/downloads" "/home/user/files"
    
For now, this feature only supports comparisons between two directories, but the ability to string together destinations for comparison is in the works.

You can also use the <code>help</code> argument in case you forgot which commands do what.

    python acesafe.py help

If you'd like to run a routine and then have your computer go to sleep, use <code>run-sleep</code> instead of the standard <code>run</code> command.

## Find out more

A fuller explanation of why I made AceSafe and what it does can be found [here][1].


  [1]: http://www.acecodes.net/?p=72