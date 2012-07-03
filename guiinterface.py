'''
    This file is part of youget.

    youget is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    youget is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with youget. If not, see <http://www.gnu.org/licenses/>.
'''
from PySide import QtCore, QtGui
import Youtube
import urllib.request
import time

class interface(QtGui.QMainWindow):
    def __init__(self):
        super(interface, self).__init__()

        global ToolName

        youtubeurllabel = QtGui.QLabel("Youtube URL or ID:")
        self.youtubeurlbox = QtGui.QLineEdit()

        youtubeurllayout = QtGui.QHBoxLayout()
        youtubeurllayout.addWidget(youtubeurllabel)
        youtubeurllayout.addWidget(self.youtubeurlbox)

        cleardatabutton = QtGui.QPushButton('Clear Data')
        cleardatabutton.clicked.connect(self.cleardata)
        getdatabutton = QtGui.QPushButton('Get Data')
        getdatabutton.clicked.connect(self.getdata)

        databuttonlayout = QtGui.QHBoxLayout()
        databuttonlayout.addWidget(getdatabutton)
        databuttonlayout.addWidget(cleardatabutton)

        titlelabel = QtGui.QLabel("Name:")
        self.titlebox = QtGui.QLineEdit()
        self.titlebox.setReadOnly(True)

        authorlabel = QtGui.QLabel("Author:")
        self.authorbox = QtGui.QLineEdit()
        self.authorbox.setReadOnly(True)

        datelabel = QtGui.QLabel("Upload date:")
        self.datebox = QtGui.QLineEdit()
        self.datebox.setReadOnly(True)

        viewslabel = QtGui.QLabel("Views:")
        self.viewsbox = QtGui.QLineEdit()
        self.viewsbox.setReadOnly(True)

        AUVlayout = QtGui.QHBoxLayout()
        AUVlayout.addWidget(authorlabel)
        AUVlayout.addWidget(self.authorbox)
        AUVlayout.addWidget(datelabel)
        AUVlayout.addWidget(self.datebox)
        AUVlayout.addWidget(viewslabel)
        AUVlayout.addWidget(self.viewsbox)

        likeslabel = QtGui.QLabel("Likes:")
        self.likesbox = QtGui.QLineEdit()
        self.likesbox.setReadOnly(True)

        dislikeslabel = QtGui.QLabel("Dislikes:")
        self.dislikesbox = QtGui.QLineEdit()
        self.dislikesbox.setReadOnly(True)

        ratinglayout = QtGui.QHBoxLayout()
        ratinglayout.addWidget(likeslabel)
        ratinglayout.addWidget(self.likesbox)
        ratinglayout.addWidget(dislikeslabel)
        ratinglayout.addWidget(self.dislikesbox)

        titlelayout = QtGui.QHBoxLayout()
        titlelayout.addWidget(titlelabel)
        titlelayout.addWidget(self.titlebox)

        descriptionlabel = QtGui.QLabel("Description:")
        self.descriptionbox = QtGui.QTextEdit()
        self.descriptionbox.setReadOnly(True)

        descriptionlayout = QtGui.QVBoxLayout()
        descriptionlayout.addWidget(descriptionlabel)
        descriptionlayout.addWidget(self.descriptionbox)

        urltablelabel = QtGui.QLabel("Video URL Table:")

        self.urltable = QtGui.QTableWidget(0, 5)
        self.urltable.setHorizontalHeaderLabels(("Quality", "Size (in bytes)", "Type", "Codecs", "URL"))
        self.urltable.horizontalHeader().setResizeMode(4, QtGui.QHeaderView.Stretch)
        self.urltable.setShowGrid(True)
        self.urltable.verticalHeader().hide()
        self.urltable.itemDoubleClicked.connect(self.displayitem)

        commandlabel = QtGui.QLabel("Launch URL with command:")

        self.commanddict = None

        self.commandfilepath = QtGui.QLineEdit()
        self.commandfilepath.setReadOnly(True)

        commandfileload = QtGui.QPushButton('Specify a file')
        commandfileload.clicked.connect(self.getcommandfilepath)

        commandfilereload = QtGui.QPushButton('Load file')
        commandfilereload.clicked.connect(self.loadcommandfile)

        self.commandcombo = QtGui.QComboBox()

        commandfilelayout = QtGui.QHBoxLayout()
        commandfilelayout.addWidget(self.commandfilepath)
        commandfilelayout.addWidget(commandfilereload)
        commandfilelayout.addWidget(commandfileload)

        commandlaunch = QtGui.QPushButton('Launch command')
        commandlaunch.clicked.connect(self.sendcommand)

        advancedlayout = QtGui.QVBoxLayout()
        advancedlayout.addWidget(commandlabel)
        advancedlayout.addLayout(commandfilelayout)
        advancedlayout.addWidget(self.commandcombo)
        advancedlayout.addWidget(commandlaunch)

        advancedlayoutbutton = QtGui.QPushButton('Advanced Options')
        advancedlayoutbutton.clicked.connect(self.toggleadvancedlayout)

        downloadvideobutton = QtGui.QPushButton('Download selected URL')
        downloadvideobutton.clicked.connect(self.downloadvideo)

        self.advancedlayoutwidget = QtGui.QWidget()
        self.advancedlayoutwidget.setLayout(advancedlayout)
        self.advancedlayoutwidget.hide()

        self.advancedlayouthidden = True

        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setRange(0, 100)
        self.progressbar.setValue(0)
        self.progressbar.hide()

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addLayout(youtubeurllayout)
        mainlayout.addLayout(databuttonlayout)
        mainlayout.addLayout(titlelayout)
        mainlayout.addLayout(AUVlayout)
        mainlayout.addLayout(ratinglayout)
        mainlayout.addLayout(descriptionlayout)
        mainlayout.addWidget(urltablelabel)
        mainlayout.addWidget(self.urltable)
        mainlayout.addWidget(downloadvideobutton)
        mainlayout.addWidget(advancedlayoutbutton)
        mainlayout.addWidget(self.advancedlayoutwidget)
        mainlayout.addWidget(self.progressbar)

        mainlayoutwidget = QtGui.QWidget()
        mainlayoutwidget.setLayout(mainlayout)

        statusbarwelcome = ''.join(["Welcome to ", ToolName])
        self.statusBar().showMessage(statusbarwelcome)

        self.setCentralWidget(mainlayoutwidget)
        self.setWindowTitle(ToolName)

    def updatedownload(self, count, blockSize, totalSize):
        percent = int(count*blockSize*100/totalSize)
        self.progressbar.setValue(percent)
        self.setWindowTitle(''.join([ToolName, " - Downloading Video, ", str(percent), "%"]))
        if percent >= 100:
            time.sleep(1)
            self.progressbar.setValue(0)
            self.setWindowTitle(ToolName)
            self.progressbar.hide()

    def updatedata(self, completed, message, total):
        global ToolName
        percent = int((completed/total)*100)
        self.progressbar.setValue(percent)
        self.setWindowTitle(''.join([ToolName, " - ", str(message)]))
        if percent >= 100:
            time.sleep(1)
            self.progressbar.setValue(0)
            self.setWindowTitle(ToolName)
            self.progressbar.hide()

    def cleardata(self):
        self.titlebox.setText('')
        self.authorbox.setText('')
        self.datebox.setText('')
        self.viewsbox.setText('')
        self.likesbox.setText('')
        self.dislikesbox.setText('')
        self.descriptionbox.setText('')
        self.urltable.clearContents()
        self.urltable.setRowCount(0)

    def getdata(self):
        self.progressbar.show()
        TotalStages = 3
        Stage = 0
        self.cleardata()
        self.updatedata(Stage, "Downloading Youtube page", TotalStages)
        videoid = Youtube.getvideoid(self.youtubeurlbox.text())
        if videoid == None:
            self.progressbar.hide()
            self.progressbar.setValue(0)
            self.setWindowTitle(ToolName)
            QtGui.QMessageBox.critical(self, "Error while retrieving page", "The input in the URL/ID box could not be processed.", QtGui.QMessageBox.Ok)
            return None
        self.youtubeurlbox.setText(videoid)
        pagedata = Youtube.downloadpage(videoid)
        if pagedata == 'Error_OpeningURL':
            self.progressbar.hide()
            self.progressbar.setValue(0)
            self.setWindowTitle(ToolName)
            QtGui.QMessageBox.critical(self, "Error while retrieving page", "Could not connect to server with current URL.\nThe operation has aborted.", QtGui.QMessageBox.Ok)

        elif pagedata == 'Error_ReadingData':
            self.progressbar.hide()
            self.progressbar.setValue(0)
            self.setWindowTitle(ToolName)
            QtGui.QMessageBox.critical(self, "Error while retrieving page", "Could not download the page.\nThe operation has aborted.", QtGui.QMessageBox.Ok)

        elif pagedata == 'Error_DecodingData':
            self.progressbar.hide()
            self.progressbar.setValue(0)
            self.setWindowTitle(ToolName)
            QtGui.QMessageBox.critical(self, "Error while processing page", "Could not decode the page.\nThe operation has aborted.", QtGui.QMessageBox.Ok)

        else:
            Stage = Stage + 1
            self.updatedata(Stage, "Retrieving metadata", TotalStages)
            metalist = Youtube.getmeta(pagedata)
            self.titlebox.setText(metalist[0])
            self.authorbox.setText(metalist[2])
            self.datebox.setText(metalist[3])
            self.viewsbox.setText(metalist[4])
            self.likesbox.setText(metalist[5])
            self.dislikesbox.setText(metalist[6])
            self.descriptionbox.setText(metalist[1])

            Stage = Stage + 1
            self.updatedata(Stage, "Retrieving Youtube video URLs and data", TotalStages)
            urldict = Youtube.getvideourl(Youtube.getflashvars(pagedata))
            i = 0
            NumURLs = len(list(urldict))
            if NumURLs == 0:
                progressincrement = 1
            else:
                progressincrement = 1/NumURLs
            for URL in iter(urldict):
                self.updatedata(Stage, ''.join(["Inserting URL #", str(i+1), " of ", str(NumURLs)]), TotalStages)
                URLItem = QtGui.QTableWidgetItem(str(URL))
                TypeItem = QtGui.QTableWidgetItem(str((urldict[URL])[0]))
                CodecItem = QtGui.QTableWidgetItem(str((urldict[URL])[1]))
                videosize = Youtube.getvideosize(URL)
                QualityItem = QtGui.QTableWidgetItem(str((urldict[URL])[2]))
                if videosize == None:
                    videosize = "N\A"
                else:
                    videosize = "{0:,d}".format(int(videosize))
                SizeItem = QtGui.QTableWidgetItem(str(videosize))
                URLItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                TypeItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                CodecItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                SizeItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                QualityItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

                self.urltable.insertRow(i)
                self.urltable.setItem(i, 0, QualityItem)
                self.urltable.setItem(i, 1, SizeItem)
                self.urltable.setItem(i, 2, TypeItem)
                self.urltable.setItem(i, 3, CodecItem)
                self.urltable.setItem(i, 4, URLItem)
                Stage = Stage + progressincrement
                i = i+1
            self.updatedata(TotalStages, "Done", TotalStages)
            QtGui.QMessageBox.information(self, "Operation completed", "The Youtube video data has been retrieved sucessfully.")

    def displayitem(self):
        self.displayitemdialog = DisplayText(self.urltable.currentItem().text())

    def getcommandfilepath(self):
        newpath = QtGui.QFileDialog.getOpenFileName(self, "Choose the command text file", '', "All Files (*);;Text Files (*.txt)")
        if newpath[0]:
            self.commandfilepath.setText(newpath[0])

    def loadcommandfile(self):
        self.commanddict = Youtube.loadlaunchcommand(self.commandfilepath.text())
        if self.commanddict:
            self.clearcommandcombo()
            self.populatecommandcombo()
        else:
            self.clearcommandcombo()
            QtGui.QMessageBox.critical(self, "Error while loading command text file", "Unable to load the file from the current path.\nThe operation has aborted.", QtGui.QMessageBox.Ok)

    def sendcommand(self):
        try:
            URL = self.urltable.item(self.urltable.currentRow(), 4).text()
        except:
            QtGui.QMessageBox.critical(self, "Error while launching command", "No URL selected.\nThe operation has aborted.", QtGui.QMessageBox.Ok)
            return None
        if self.commanddict:
            Command = self.commanddict[self.commandcombo.currentText()]
            Command = Command.replace("{URL}", URL)
            Youtube.launchcommand(Command)
        else:
            QtGui.QMessageBox.critical(self, "Error while launching command", "The launch command file needs to be loaded.\nThe operation has aborted.", QtGui.QMessageBox.Ok)

    def populatecommandcombo(self):
        i = 0
        for commandname in iter(self.commanddict):
            self.commandcombo.insertItem(i, commandname)
            i = i+1

    def clearcommandcombo(self):
        self.commandcombo.clear()

    def toggleadvancedlayout(self):
        if self.advancedlayouthidden:
            self.advancedlayouthidden = False
            self.advancedlayoutwidget.show()
        else:
            self.advancedlayouthidden = True
            self.advancedlayoutwidget.hide()

    def downloadvideo(self):
        try:
            URL = self.urltable.item(self.urltable.currentRow(), 4).text()
        except:
            QtGui.QMessageBox.critical(self, "Error while downloading video", "No URL selected.\nThe operation has aborted.", QtGui.QMessageBox.Ok)
            return None
        newpath = QtGui.QFileDialog.getSaveFileName(self, "Choose a location to save the video", '', "All Files (*)")
        if newpath[0]:
            newpath = newpath[0]
            try:
                newfile = open(newpath, mode='w')
                newfile.close()
            except:
                QtGui.QMessageBox.critical(self, "Error while downloading video", "Could not save the video to the specified location.\nThe operation has aborted.", QtGui.QMessageBox.Ok)
                return None
            self.progressbar.show()
            try:
                urllib.request.urlretrieve(URL, filename=newpath, reporthook=self.updatedownload)
            except:
                self.progressbar.hide()
                self.progressbar.setValue(0)
                self.setWindowTitle(ToolName)
                QtGui.QMessageBox.critical(self, "Error while downloading video", "The operation failed while downloading.\nThe operation has aborted.", QtGui.QMessageBox.Ok)

class DisplayText(QtGui.QDialog):
    def __init__(self, Message):
        super(DisplayText, self).__init__()

        messagelabel = QtGui.QLabel("The item's value is shown below:")
        messagebox = QtGui.QLineEdit()
        messagebox.setReadOnly(True)
        messagebox.setText(Message)

        buttonFiller = QtGui.QWidget()
        buttonFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

        closebutton = QtGui.QPushButton('Close')
        closebutton.clicked.connect(self.close)

        closelayout = QtGui.QHBoxLayout()
        closelayout.addWidget(buttonFiller)
        closelayout.addWidget(closebutton)

        messagelayout = QtGui.QVBoxLayout()
        messagelayout.addWidget(messagelabel)
        messagelayout.addWidget(messagebox)
        messagelayout.addLayout(closelayout)

        self.setLayout(messagelayout)

        self.setWindowTitle("Display Item's Value")

        self.show()

class GeneralExceptiondialog(QtGui.QDialog):
    def __init__(self, *args):
        super(GeneralExceptiondialog, self).__init__()

        import traceback
        ExceptionDetails = ''.join(traceback.format_exception(*args))
        global ToolName

        self.ErrorMessage = QtGui.QLabel(''.join([ToolName, " has encountered an error. The details are below:"]))
        self.MissingList = QtGui.QTextEdit()
        self.MissingList.setPlainText(ExceptionDetails)
        self.MissingList.setReadOnly(True)
        self.ErrorMessageBottom = QtGui.QLabel("If you want to report this error, please submit these details to the developer.")
        self.closebutton = QtGui.QPushButton("Close")
        self.closebutton.clicked.connect(self.close)

        buttonFiller = QtGui.QWidget()
        buttonFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(buttonFiller)
        buttonLayout.addWidget(self.closebutton)

        self.Layout = QtGui.QVBoxLayout()
        self.Layout.addWidget(self.ErrorMessage)
        self.Layout.addWidget(self.MissingList)
        self.Layout.addWidget(self.ErrorMessageBottom)
        self.Layout.addLayout(buttonLayout)

        self.setLayout(self.Layout)

        self.setWindowTitle(''.join([ToolName, " - Error"]))

def exceptionhookstart(*args):
    global ExceptionDialog
    QtGui.qApp.closeAllWindows()
    ExceptionDialog = GeneralExceptiondialog(*args)
    ExceptionDialog.show()

ToolName = "Youget"

ExceptionDialog = None

if __name__ == '__main__':
    import sys

    sys.excepthook = exceptionhookstart

    app = QtGui.QApplication(sys.argv)

    Interface = interface()
    Interface.commandfilepath.setText(Youtube.programfile_path('launchcommand.txt'))
    Interface.show()

    sys.exit(app.exec_())
