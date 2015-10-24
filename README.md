# AceSafe
#### Last updated: 4/24/2015
##### This update is a complete overhaul that utilizes JSON instead of a SQLite database file. It's much cleaner and simpler, but if you prefer the old version for whatever reason, just look at the <code>sqlite</code> subfolder.
This is a program I built out of the carcass of my horrendously unfashionable batch file backup system. The primary purpose of this program is to send files that are valued the most to your various backup sources. First, AceSafe builds some objects that each correspond with a path on the user's hard drive. Then each path is turned into an class object and customized so that their files can be manipulated with copying methods. Once that is done, the program builds a database file that consists of several tables, with each table containing syncing routines.

The most powerful feature of this program is its copying method, which checks the source directory and then compares its contents to the contents of the destination directory. If there are files that exist only in the destination, they will be deleted. Then new and updated files are copied over. This process ensures a 1-to-1 sync between files and their backups, with no extra files lingering on forever because file names or paths have been changed.

AceSafe has saved me boatloads of time, particularly with the addition of the "check and delete" feature. I used to have to manually delete files every time I changed a filename or something, otherwise I would end up with copies of the same files that only differed in filenames. For example, if I had a file called "readme_old.txt" and then renamed it "readme_new.txt", I would end up with both files. Now, only the "readme_new.txt" will remain.

## Instructions

The first step is to open up the <code>test_json.json</code> file. You'll see that there's a sample routine setup for your benefit.

    
    {
      "testRoutine": {
        "src": "/Users/yourUser/test1",
        "dst":"/Users/yourUser/test2"
      }
    }

`testRoutine` is the name of the routine you want to use, `src` is the folder you want to backup, and `dst` is the place where you want your files to be copied to. AceSafe will compare the contents of `src` with the contents of `dst` and delete anything that isn't in `src` while also copying any files that are only in `src`.
    

You can either use this file or create your own. If you want to use your own, simply drop it into the directory that AceSafe lives in (ensuring that your file has the same formatting as the test_json file) and then define an environment variable called <code>ACESAFE_JSON</code>. When defining this variable, don't include the <code>.json</code> extension.

For example, if you had a file called <code>my_json_file.json</code>, you would create the environment variable like so:

    $ export ACESAFE_JSON=my_json_file

 