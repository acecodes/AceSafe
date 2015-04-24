# AceSafe
#### Last updated: 4/24/2015
##### This update is a complete overhaul that utilizes JSON instead of a SQLite database file. It's much cleaner and simpler, but if you prefer the old version for whatever reason, just look at the <code>sqlite</code> subfolder.
This is a program I built out of the carcass of my horrendously unfashionable batch file backup system. The primary purpose of this program is to send files that are valued the most to your various backup sources. First, AceSafe builds some objects that each correspond with a path on the user's hard drive. Then each path is turned into an class object and customized so that their files can be manipulated with copying methods. Once that is done, the program builds a database file that consists of several tables, with each table containing syncing routines.

The most powerful feature of this program is its copying method, which checks the source directory and then compares its contents to the contents of the destination directory. If there are files that exist only in the destination, they will be deleted. Then new and updated files are copied over. This process ensures a 1-to-1 sync between files and their backups, with no extra files lingering on forever because file names or paths have been changed.

AceSafe has saved me boatloads of time, particularly with the addition of the "check and delete" feature. I used to have to manually delete files every time I changed a filename or something, otherwise I would end up with copies of the same files that only differed in filenames. For example, if I had a file called "readme_old.txt" and then renamed it "readme_new.txt", I would end up with both files. Now, only the "readme_new.txt" will remain.

## Instructions

The first step is to open up the <code>test_json.json</code> file. You'll see that some sample entries for directories and routines have already been filled in. Here is a layout of the file itself and some additional instructions:

    {
      "locations": {
       # These are base directories
        "test1": "/home/username/tmp/test1",
        "test2": "/home/username/tmp/test2",
        "test3": "/home/username/tmp/test3"
      },
      "routines": {
      # This is a routine
        "test": {
        # Here you define critical information for the routine
          "setup": {
            "description": "Test routine",
            "baseDirectory": "test1",
            # These two arguments are optional, and specify subdirectories
            # in either the source or destination directories
            "srcSub": "test4",
            "dstSub": "test5"
          },
          # These are the steps in the routine, using the names of the 
          # base directories you defined in 'locations'
          "1": "test2",
          "2": "test3"
        }
      }
    }

You can either use this file or create your own. If you want to use your own, simply drop it into the directory that AceSafe lives in (ensuring that your file has the same formatting as the test_json file) and then define an environment variable called <code>ACESAFE_JSON</code>. When defining this variable, don't include the <code>.json</code> extension.

For example, if you had a file called <code>my_json_file.json</code>, you would create the environment variable like so:

    $ export ACESAFE_JSON=my_json_file

 