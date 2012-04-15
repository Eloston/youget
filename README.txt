Youget
------------------

How to use this program:
Launch Youget
Under "Youtube URL", put in the full URL to the Youtube video (ex. http://www.youtube.com/watch?v=1234567&...)
Click "Get Data". The application may freeze for a few seconds. A dialog box will pop up when it has finished retrieving all the information.
Under "Video URL Table" there will be the size of the video file (Does not always show up), the type of video file, codecs (seems to be audio codecs. Not always present), and the direct URL to that video. Double-clicking on any cell in the table will cause a dialoge box to open with that cell's text which is selectable.
Click "Clear Data" to clear all the information fields. You do not need to use this if you change Youtube URLs and click "Get Data", since the fields will update automatically.

At the bottom, the "Launch URL with command" feature will only work if a command text file is created.
In the text box will be the current path to the command text file. It will default to the location of the exe with the name "launchcommand.txt". You can change the path by clicking "Specify a file".
When you have the valid path to the command text file, click "Load file". An entry or entries will show up in the combo box below. Each entry is a command defined in your created command text file.

To specify the URL to load, click on any cell on the row containing the URL you want to use.
Then, click "Launch command" to launch your command with the specific URL.

If you want to modify the command text file, you can make your changes first then click "Load file" to retrieve the changes.

How to build this program:
You need:
Python 3.2.x
PyQt 4.9.x
cxfreeze (Get it at http://cx-freeze.sourceforge.net/)

Then run this command:
cxfreeze guiinterface.py --target-dir=build

This will build the program and place the files in the directory "build" in your current working directory.

On Windows, you will need to add the parameter "--base-name=Win32GUI" so a shell doesn't run when you run this program.
