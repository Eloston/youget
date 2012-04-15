from PyQt4 import QtCore, QtGui
import Youtube

class interface(QtGui.QMainWindow):
    def __init__(self):
        super(interface, self).__init__()

        global ToolName

        youtubeurllabel = QtGui.QLabel("Youtube URL:")
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

        self.urltable = QtGui.QTableWidget(0, 4)
        self.urltable.setHorizontalHeaderLabels(("Size (in bytes)", "Type", "Codecs", "URL"))
        self.urltable.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.Stretch)
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

        commandlayout = QtGui.QHBoxLayout()
        commandlayout.addWidget(self.commandfilepath)
        commandlayout.addWidget(commandfilereload)
        commandlayout.addWidget(commandfileload)

        commandlaunch = QtGui.QPushButton('Launch command')
        commandlaunch.clicked.connect(self.sendcommand)

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addLayout(youtubeurllayout)
        mainlayout.addLayout(databuttonlayout)
        mainlayout.addLayout(titlelayout)
        mainlayout.addLayout(descriptionlayout)
        mainlayout.addWidget(urltablelabel)
        mainlayout.addWidget(self.urltable)
        mainlayout.addWidget(commandlabel)
        mainlayout.addLayout(commandlayout)
        mainlayout.addWidget(self.commandcombo)
        mainlayout.addWidget(commandlaunch)

        mainlayoutwidget = QtGui.QWidget()
        mainlayoutwidget.setLayout(mainlayout)

        statusbarwelcome = ''.join(["Welcome to ", ToolName])
        self.statusBar().showMessage(statusbarwelcome)

        self.setCentralWidget(mainlayoutwidget)
        self.setWindowTitle(ToolName)

    def cleardata(self):
        self.titlebox.setText('')
        self.descriptionbox.setText('')
        self.urltable.clearContents()
        self.urltable.setRowCount(0)

    def getdata(self):
        self.cleardata()
        pagedata = Youtube.downloadpage(self.youtubeurlbox.text())
        if pagedata == 'Error_OpeningURL':
            QtGui.QMessageBox.critical(self, "Error while retrieving page", "Could not connect to server with current URL.\nThe operation has aborted.", "OK")

        elif pagedata == 'Error_ReadingData':
            QtGui.QMessageBox.critical(self, "Error while retrieving page", "Could not download the page.\nThe operation has aborted.", "OK")

        elif pagedata == 'Error_DecodingData':
            QtGui.QMessageBox.critical(self, "Error while processing page", "Could not decode the page.\nThe operation has aborted.", "OK")

        else:
            metalist = Youtube.getmeta(pagedata)
            if metalist[0] == None:
                self.titlebox.setText("N/A")
            else:
                self.titlebox.setText(metalist[0])
            if metalist[1] == None:
                self.descriptionbox.setText("N/A")
            else:
                self.descriptionbox.setText(metalist[1])

            urldict = Youtube.getvideourl(Youtube.getflashvars(pagedata))
            i = 0
            for URL in iter(urldict):
                URLItem = QtGui.QTableWidgetItem(str(URL))
                TypeItem = QtGui.QTableWidgetItem(str((urldict[URL])[0]))
                CodecItem = QtGui.QTableWidgetItem(str((urldict[URL])[1]))
                videosize = Youtube.getvideosize(URL)
                if videosize == None:
                    videosize = "N\A"
                else:
                    videosize = "{0:,d}".format(int(videosize))
                SizeItem = QtGui.QTableWidgetItem(str(videosize))
                URLItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                TypeItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                CodecItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                SizeItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

                self.urltable.insertRow(i)
                self.urltable.setItem(i, 0, SizeItem)
                self.urltable.setItem(i, 1, TypeItem)
                self.urltable.setItem(i, 2, CodecItem)
                self.urltable.setItem(i, 3, URLItem)
                i = i+1
            QtGui.QMessageBox.information(self, "Operation completed", "The youtube video data has been retrieved sucessfully.")

    def displayitem(self):
        self.displayitemdialog = DisplayText(self.urltable.currentItem().text())

    def getcommandfilepath(self):
        if QtGui.QFileDialog.getOpenFileName(self, "Choose the command text file", '', "All Files (*);;Text Files (*.txt)"):
            self.commandfilepath.setText()

    def loadcommandfile(self):
        self.commanddict = Youtube.loadlaunchcommand(self.commandfilepath.text())
        self.clearcommandcombo()
        self.populatecommandcombo()

    def sendcommand(self):
        try:
            URL = self.urltable.item(self.urltable.currentRow(), 3).text()
        except:
            QtGui.QMessageBox.critical(self, "Error while launching command", "No URL selected or unable to launch command.\nThe operation has aborted.", "OK")
            return None
        if self.commanddict:
            Command = self.commanddict[self.commandcombo.currentText()]
            Command = Command.replace("{URL}", URL)
            Youtube.launchcommand(Command)
        else:
            QtGui.QMessageBox.critical(self, "Error while launching command", "The launch command file needs to be loaded.\nThe operation has aborted.", "OK")

    def populatecommandcombo(self):
        i = 0
        for commandname in iter(self.commanddict):
            self.commandcombo.insertItem(i, commandname)
            i = i+1

    def clearcommandcombo(self):
        self.commandcombo.clear()

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

ToolName = "Youtube Video URLs"

ExceptionDialog = None

if __name__ == '__main__':
    import sys

    sys.excepthook = exceptionhookstart

    app = QtGui.QApplication(sys.argv)

    Interface = interface()
    Interface.commandfilepath.setText(Youtube.programfile_path('launchcommand.txt'))
    Interface.show()

    sys.exit(app.exec_())
