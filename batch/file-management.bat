@echo off

REM Section for setting variables.
set anki=User\Documents\Anki\User 1
set books=Files\Books
set calibre=Files\Books\Calibre
set chrome=C:\Users\User1\AppData\Local\Google\Chrome\User Data\Default
set DLs=User\Downloads
set dropbox=Dropbox
set dropbox_photos=Camera Uploads
set dropbox_photos_backup=Photos\To Be Sorted\Dropbox
set echocopy=Echo You will now be returned to the copy menu.
set echodl=Echo You will now be returned to the download menu.
set exthd1=G:
set exthd2=H:
set file_drive=D:
set files=Files
set flash=F:
set linebreak=Echo ---------------------------------
set music=Music
set name=Bro Montana
set python=C:\Python33
set storage_docs=E:\Storage\Documents

:MENU

REM Clears all text.
CLS

REM Introduction.
Echo Hello, %name%.
Echo Welcome to the file management batch file.
Pause

REM Provide the user with a menu of choices.
%linebreak%
Echo Press 1 to copy/upload files to various locations.
Echo Press 2 to download files from various locations.
Echo Press 3 to exit.
%linebreak%
CHOICE /C:123 /M "Please make a choice."
%linebreak%

If errorlevel ==3 GOTO MainExit
If errorlevel ==2 GOTO Download
If errorlevel ==1 GOTO Copy

REM This section is dedicated to copying files to backup sources.
:COPY
REM Clears all previous text.
CLS

%linebreak%
Echo Press 1 to copy files to the external hard drives.
Echo Press 2 to copy files to the thumb drive.
Echo Press 3 to copy files to Dropbox.
Echo Press 4 to copy Anki files.
Echo Press 5 to copy browser files.
Echo Press 6 to go back to the main menu.
Echo Press 7 to exit.
%linebreak%

CHOICE /C:1234567 /M "Please decide which files you would like to copy."

%linebreak%

If errorlevel ==7 GOTO CopyExit
If errorlevel ==6 GOTO BackToMM
If errorlevel ==5 GOTO Browser
If errorlevel ==4 GOTO Anki
If errorlevel ==3 GOTO Dropbox
If errorlevel ==2 GOTO Thumb
If errorlevel ==1 GOTO ExternalHDs

:ExternalHDs
Echo You pressed 1. %files% will be copied to the external hard drives. 
Pause

xcopy /E /Y /D %file_drive%\%files% %exthd1%\%files%
xcopy /E /Y /D "%file_drive%\%dropbox%\%dropbox_photos%" "%exthd1%\%files%\%dropbox_photos_backup%"
xcopy /E /Y /D "%file_drive%\%dropbox%\%dropbox_photos%" "%exthd2%\%files%\%dropbox_photos_backup%"
xcopy /E /Y /D %storage_docs% %exthd1%\Storage
xcopy /E /Y /D %file_drive%\%files% %exthd2%\%files%
xcopy /E /Y /D %storage_docs% %exthd2%\Storage
xcopy /E /Y /D %file_drive%\%dropbox%\Music %file_drive%\%files%\Music
xcopy /E /Y /D "%file_drive%\%files%\Music" %exthd1%\%files%\Music
xcopy /E /Y /D "%file_drive%\%files%\Music" %exthd2%\%files%\Music

%echocopy%
Pause
GOTO Copy

:Thumb
Echo You pressed 2. %files% will be copied to the thumb drive.
Pause

xcopy /E /Y /D "%file_drive%\%books%" %flash%\Books
xcopy /E /Y /D "%file_drive%\%files%\Documents" %flash%\Documents
xcopy /E /Y /D "%file_drive%\%files%\Utilities\Work" %flash%\Utilities
xcopy /E /Y /D "%file_drive%\%files%\Programming" %flash%\Programming
copy /Y /D "%file_drive%\%files%\Flashcards\Anki Archive\ACE-system-changelog.txt" "%flash%\Documents\Anki Archive"

%echocopy%
Pause
GOTO Copy

:Dropbox
Echo You pressed 3. %files% will be copied to Dropbox.
Pause

xcopy /E /Y /D "%file_drive%\%files%\Documents\*.*" "%file_drive%\%dropbox%\Documents"
xcopy /E /Y /D "%file_drive%\%files%\Programming\*.*" "%file_drive%\%dropbox%\Programming"
xcopy /E /Y /D %file_drive%\%calibre% %file_drive%\%dropbox%\Books 
xcopy /Y /D "%file_drive%\%files%\Flashcards\Anki Archive\ACE-system-changelog.txt" "%file_drive%\%dropbox%\Anki\"
xcopy /E /Y /D %file_drive%\%music% %file_drive%\%dropbox%\Music

%echocopy%
Pause
GOTO Copy

:Anki
Echo You pressed 4. Anki files will be backed up.
Pause

REM This is the menu for managing my Anki files.
:ANKIMENU

REM Provide the user with a menu of choices.
%linebreak%
Echo Press 1 to copy all new files only.
Echo Press 2 to delete old files and copy all new files.
Echo Press 3 to return to the copy menu.
Echo Press 4 to exit.
%linebreak%

CHOICE /C:1234 /M "Please make a choice."

%linebreak%

REM Instructions for each choice.

If errorlevel ==4 GOTO End
If errorlevel ==3 GOTO Copy
If errorlevel ==2 GOTO AnkiDelete
If errorlevel ==1 GOTO AnkiNew

:AnkiNew
Echo Only new Anki files will be copied now.
Pause

del "%file_drive%\%files%\Flashcards\Anki\backups\*.*" /S /Q
xcopy /E /Y /I /D "%file_drive%\%anki%" "%file_drive%\%files%\Flashcards\Anki\"
del "%file_drive%\%dropbox%\Anki\Deck\backups\*.*" /S /Q
xcopy /E /Y /I /D "%file_drive%\%anki%" "%file_drive%\%dropbox%\Anki\Deck\"
xcopy /E /Y /I /D "%file_drive%\%files%\Flashcards\Anki Archive\ACE-system-changelog.txt" "%file_drive%\%dropbox%\Anki\"
del "%exthd1%\%files%\Flashcards\Anki\backups\*.*" /S /Q
xcopy /E /Y /I /D "%file_drive%\%anki%" "%exthd1%\%files%\Flashcards\Anki\"
del "%exthd2%\%files%\Flashcards\Anki\backups\*.*" /S /Q
xcopy /E /Y /I /D "%file_drive%\%anki%" "%exthd2%\%files%\Flashcards\Anki\"
del "%flash%\Anki\backups\*.*" /S /Q
xcopy /E /Y /I /D "%file_drive%\%anki%" "%flash%\Anki\"

%echocopy%
Pause
GOTO Copy

:AnkiDelete
Echo All old Anki files will be deleted and replaced with new files.
Pause

rmdir "%file_drive%\%files%\Flashcards\Anki" /S /Q
xcopy /E /Y /I "%file_drive%\%anki%" "%file_drive%\%files%\Flashcards\Anki\"
rmdir "%file_drive%\%dropbox%\Anki\Deck" /S /Q
xcopy /E /Y /I "%file_drive%\%anki%\" "D:\Dropbox\Anki\Deck\"
xcopy /E /Y /I "%file_drive%\%files%\Flashcards\Anki Archive\ACE-system-changelog.txt" "%file_drive%\%dropbox%\Anki\"
rmdir "%exthd1%\%files%\Flashcards\Anki" /S /Q
xcopy /E /Y /I "%file_drive%\%anki%" "%exthd1%\%files%\Flashcards\Anki\"
rmdir "%exthd2%\%files%\Flashcards\Anki" /S /Q
xcopy /E /Y /I "%file_drive%\%anki%" "%exthd2%\%files%\Flashcards\Anki\"
rmdir "%flash%\Anki" /S /Q
xcopy /E /Y /I "%file_drive%\%anki%" "%flash%\Anki\"

%echocopy%
Pause
GOTO Copy

:Browser
Echo You pressed 5.  Browser files will be backed up.
Pause

rmdir "%file_drive%\%dropbox%\Browsers\Chrome" /S /Q
rmdir "%file_drive%\%files%\Browsers\Chrome" /S /Q

xcopy /E /Y /I "%chrome%\*" "%file_drive%\%dropbox%\Browsers\Chrome"
xcopy /E /Y /I "%chrome%\*" "%file_drive%\%files%\Browsers\Chrome"

rmdir "%exthd1%\%files%\Browsers\Chrome" /S /Q
rmdir "%exthd2%\%files%\Browsers\Chrome" /S /Q

xcopy /E /Y /I "%chrome%\*" "%exthd1%\%files%\Browsers\Chrome"
xcopy /E /Y /I "%chrome%\*" "%exthd2%\%files%\Browsers\Chrome"

rmdir "%flash%\Browsers\Chrome" /S /Q
xcopy /E /Y /I "%chrome%\*" "%flash%\Browsers\Chrome"

%echocopy%
Pause
GOTO Copy

:BackToMM
Echo You pressed 6.  You will now be returned to the main menu.
GOTO Menu

:CopyExit
Echo You pressed 7.  You will now exit.
GOTO End

REM This is the section dedicated to downloading files from Dropbox.
:Download
CLS
Echo Please select which files you would like to download from Dropbox.
Echo Press 1 for books.
Echo Press 2 for programming files.
Echo Press 3 for application installers.
Echo Press 4 to return to the main menu.
%linebreak%
CHOICE /C:1234 /M "Please make a choice."
%linebreak%

If errorlevel ==4 GOTO Menu
If errorlevel ==3 GOTO AppDownload
If errorlevel ==2 GOTO ProgDownload
If errorlevel ==1 GOTO BookDownload

:BookDownload
Echo You pressed 1. Books will now be downloaded from Dropbox.
Pause
xcopy /E /Y /D %file_drive%\%dropbox%\Books "%file_drive%\%files%\%calibre%"
%echodl%
Pause
GOTO Download

:ProgDownload
Echo You pressed 2. Programming files will now be downloaded from Dropbox.
Pause
xcopy /E /Y /D %file_drive%\%dropbox%\Programming %file_drive%\%files%\Programming
%echodl%
Pause
GOTO Download

:AppDownload
Echo You pressed 3. Installer files will now be downloaded from Dropbox.
Pause
xcopy /E /Y /D %file_drive%\%dropbox%\Apps %file_drive%\%DLs%\Apps
%echodl%
Pause
GOTO Download

:MainExit
GOTO End


:END