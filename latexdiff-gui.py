# This Python file uses the following encoding: utf-8
import sys
import os, platform
import subprocess
import datetime

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QMessageBox, QComboBox, QListWidget, QListWidgetItem
from PySide2.QtCore import QFile, QObject, Qt


from distutils.spawn import find_executable

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

import zipfile
try:
    import wget
except:
    install('wget')
    import wget

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

def solveHighRes():
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

def findTool():
    global LATEX_DIFF_EXEC
    # first check if latexdiff is installed on the system as an executable 
    LATEX_DIFF_EXEC = find_executable('latexdiff')
    if not LATEX_DIFF_EXEC:
        if platform.system().lower() == 'windows':
            print('latexdiff has not been found on your computer. \
                   If you have installed CTEX or TexLive or other \
                   TeX document production system, please use the \
                   package manager to install `latexdiff`.        \
                   If you have not installed any TeX document     \
                   production system, please do so. After all, you\
                   need it to build your tex source file.')
            sys.exit()
        elif platform.system().lower() == 'linux':
            # check if the latexdiff script has already been downloaded
            if os.path.isfile('./latexdiff/latexdiff'):
                LATEX_DIFF_EXEC = ' '.join(['perl', './latexdiff/latexdiff'])
                return
            
            # if not found, download it & extract it
            print('latex-diff executable not found... Solving...')
            
            try:
                # Download from http://mirrors.ctan.org/support/latexdiff.zip
                print('Beginning to download latex-diff with wget...')
                url = 'http://mirrors.ctan.org/support/latexdiff.zip'
                wget.download(url, '.')
                print('Finished to download latex-diff.')

                with zipfile.ZipFile('./latexdiff.zip', 'r') as zip_ref:
                    zip_ref.extractall('.')
                
                LATEX_DIFF_EXEC = ' '.join(['perl', './latexdiff/latexdiff'])
            except:
                print('Error occurred during the installation of \
                       latex-diff. The program will not work properly \
                       and has to exit.')
                sys.exit()
        else:
            print('Currently your OS is not supported. Exit.')
            sys.exit()
    else:
        pass
        # LATEX_DIFF_EXEC = [LATEX_DIFF_EXEC]

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

        self.lwMsg = self.window.findChild(QListWidget, 'listWidget')
 
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

    def lwWriteMsg(self, msg):
        currentDT = datetime.datetime.now()
        tim = currentDT.strftime("%Y-%m-%d %H:%M:%S")

        msg = '[%s] %s' % (tim, msg)

        item = QListWidgetItem(msg)
        self.lwMsg.insertItem(0, item)

    def pbOldFile_handler(self):
        fileName = QFileDialog.getOpenFileName(self,
            self.tr("Open Tex Source Code"), self.tr("."), self.tr("Tex Files (*.tex)"))
        if fileName[0] != "" :
            self.leOldFile.setText(fileName[0])
            self.lwWriteMsg('Old file selected.')
    
    def pbNewFile_handler(self):
        fileName = QFileDialog.getOpenFileName(self,
            self.tr("Open Tex Source Code"), self.tr("."), self.tr("Tex Files (*.tex)"))
        if fileName[0] != "" :
            self.leNewFile.setText(fileName[0])
            self.lwWriteMsg('New file selected.')
    
    def pbExit_handler(self):
        sys.exit()

    def pbRun_handler(self):
        global LATEX_DIFF_EXEC

        if not isNotBlank(self.leOldFile.text()):
            msg = 'Old file path is empty. Please check.'
            showMsg(msg)
            self.lwWriteMsg(msg)
            return

        if not isNotBlank(self.leNewFile.text()):
            msg = 'New file path is empty. Please check.'
            showMsg(msg)
            self.lwWriteMsg(msg)
            return
        
        cbMarkupStyle = self.window.findChild(QComboBox, 'cbMarkupStyle')
        option = cbMarkupStyle.currentText().upper()

        #latexdiff -t CTRADITIONAL draft.tex revision.tex > diff.tex
        oldFileName = self.leOldFile.text()
        newFileName = self.leNewFile.text()
        cmd = '%s -t %s %s %s > %s' % (LATEX_DIFF_EXEC, option, oldFileName, newFileName, OUTPUT_FILE_NAME)

        # showMsg(cmd)
        self.lwWriteMsg('Executing command: %s' % cmd)

        result = os.system(cmd)

        self.lwWriteMsg('Command executed with return value: %d.' % result)


if __name__ == "__main__":
    solveHighRes()
    findTool()

    app = QApplication(sys.argv)

    form = Form('mainwindow.ui')

    sys.exit(app.exec_())
