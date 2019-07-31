# This Python file uses the following encoding: utf-8
import sys
import wget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QMessageBox, QComboBox
from PySide2.QtCore import QFile, QObject

from distutils.spawn import find_executable

LATEX_DIFF_EXEC = ''
OUTPUT_FILE_NAME = 'output.tex'


# helper function for checking empty or blank strings
def isNotBlank(s): return (s and s.strip())

# helper function for showing a message box
def showMsg(msg, title='Warning', icon=QMessageBox.Question):
    dialog = QMessageBox()
    dialog.setText(msg)
    dialog.setWindowTitle(title)
    dialog.setIcon(icon)
    dialog.exec_()

def findTool():
    global LATEX_DIFF_EXEC
    # first check if latexdiff is installed on the system as an executable 
    LATEX_DIFF_EXEC = find_executable('latexdiff')
    if LATEX_DIFF_EXEC:
        return
    else:
        LATEX_DIFF_EXEC = 'latexdiff'
    
    # TODO: download from http://mirrors.ctan.org/support/latexdiff.zip
    print('Beginning to download latex-diff with wget...')
    url = 'http://mirrors.ctan.org/support/latexdiff.zip'
    wget.download(url, '.')

class Form(QWidget): 
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)

        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
 
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
 
        self.leOldFile = self.window.findChild(QLineEdit, 'leOldFile')
        self.leNewFile = self.window.findChild(QLineEdit, 'leNewFile')
 
        pbOldFile = self.window.findChild(QPushButton, 'pbOldFile')
        pbOldFile.clicked.connect(self.pbOldFile_handler)

        pbNewFile = self.window.findChild(QPushButton, 'pbNewFile')
        pbNewFile.clicked.connect(self.pbNewFile_handler)

        pbExit = self.window.findChild(QPushButton, 'pbExit')
        pbExit.clicked.connect(self.pbExit_handler)

        pbRun = self.window.findChild(QPushButton, 'pbRun')
        pbRun.clicked.connect(self.pbRun_handler)

        self.window.show()
 
    def tr(self, text):
        return QObject.tr(self, text)

    def pbOldFile_handler(self):
        fileName = QFileDialog.getOpenFileName(self,
            self.tr("Open Tex Source Code"), self.tr("/home"), self.tr("Tex Files (*.tex)"))
        if fileName[0] != "" :
            self.leOldFile.setText(fileName[0])
    
    def pbNewFile_handler(self):
        fileName = QFileDialog.getOpenFileName(self,
            self.tr("Open Tex Source Code"), self.tr("/home"), self.tr("Tex Files (*.tex)"))
        if fileName[0] != "" :
            self.leNewFile.setText(fileName[0])
    
    def pbExit_handler(self):
        sys.exit()

    def pbRun_handler(self):
        global LATEX_DIFF_EXEC

        if not isNotBlank(self.leOldFile.text()):
            showMsg('Old file path is empty. Please check.')
            return

        if not isNotBlank(self.leNewFile.text()):
            showMsg('New file path is empty. Please check.')
            return
        
        cbMarkupStyle = self.window.findChild(QComboBox, 'cbMarkupStyle')
        option = cbMarkupStyle.currentText().upper()

        #latexdiff -t CTRADITIONAL draft.tex revision.tex > diff.tex
        oldFileName = self.leOldFile.text()
        newFileName = self.leNewFile.text()
        cmd = '%s -t %s %s %s > %s' % (LATEX_DIFF_EXEC, option, oldFileName, newFileName, OUTPUT_FILE_NAME)

        showMsg(cmd)
        print(cmd)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    findTool()

    form = Form('mainwindow.ui')

    sys.exit(app.exec_())
