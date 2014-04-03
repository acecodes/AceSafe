<h1>
PyFile
</h2>

<h2>
Description:
</h2>

This is the script I built (out of the carcass of my horrendously unfashionable batch file system). The primary purpose of this program is to send files I value the most to my various backup sources. The script starts by reading a JSON file of paths. These paths are folders of files I want to backup. Then each path is turned into an class object and customized so that their files can be manipulated with copying methods.

Additionally, the copying method checks the source directory (defined in the DirObject's __init__) and then checks that against the destination. If there are files that exist only in the destination, they will be deleted. Then new and updated files are copied over. This process ensures a 1-to-1 sync between my files and their backups.

PyFile has saved me boatloads of time, particularly with the addition of the "check and delete" feature. I used to have to manually delete files every time I changed a filename or something, otherwise I would end up with copies of the same files that only differed in filenames. For example, if I had a file called "readme_old.txt" and then renamed it "readme_new.txt", I would end up with both files. Now, only the "readme_new.txt" will remain.

A fuller explanation of why I made PyFile and what it does can be found <a href="http://www.acecodes.net/?p=72">here</a>.