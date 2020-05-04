from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAction
import clipboard
import pytube
import urllib.request  
import sys
import os

class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('app.ui', self)
        self.show()
        #Buttons
        buttonBrowse = self.findChild(QtWidgets.QPushButton, 'buttonBrowse')
        buttonBrowse.clicked.connect(self.buttonBrowseHandler)

        buttonPaste = self.findChild(QtWidgets.QPushButton, 'buttonPaste')
        buttonPaste.clicked.connect(self.buttonPasteHandler)

        buttonDownload = self.findChild(QtWidgets.QPushButton, 'buttonDownload')
        buttonDownload.clicked.connect(self.buttonDownloadHandler)

        actionInfo = self.findChild(QtWidgets.QAction, 'actionInfo')
        actionInfo.triggered.connect(self.actionInfoHandler)

        actionClose = self.findChild(QtWidgets.QAction, 'actionClose')
        actionClose.triggered.connect(self.actionCloseHandler)

        #Labels
        self.labelVideo = self.findChild(QtWidgets.QLabel, 'labelVideo')
        self.labelImage = self.findChild(QtWidgets.QLabel, 'labelImage')
        img = QPixmap("default_thumb.jpg")
        self.labelImage.setPixmap(img)

        #QlineEdits
        self.editTarget  = self.findChild(QtWidgets.QLineEdit, 'editTarget')
        self.editTarget.setText(os.getcwd())

        self.editLink = self.findChild(QtWidgets.QLineEdit, 'editLink')

        #Progressbar
        self.pbar  = self.findChild(QtWidgets.QProgressBar)
        self.pbar.setValue(0)

################################################################################################

    def buttonBrowseHandler(self):
        filename = str(QtWidgets.QFileDialog.getExistingDirectory(None))
        self.editTarget.setText(filename)

    def buttonPasteHandler(self):
        clip = str(clipboard.paste())
        self.editLink.setText(clip)
        clip = self.editLink.text()
        
        if 'youtube' in clip:
            yttitle = pytube.YouTube(clip)
            self.labelVideo.setText(yttitle.title)
            url = yttitle.thumbnail_url #url for thumbnail
            urllib.request.urlretrieve(url,'thumb.jpg')
            pixmap = QPixmap("thumb.jpg")
            self.labelImage.setPixmap(pixmap)
    
    def buttonDownloadHandler(self):
        ytdown = pytube.YouTube(str(self.editLink.text()),on_progress_callback=self.progress_function)
        ytdown.streams.first().download(self.editTarget.text())
        self.download_finished()
        
    
    def progress_function(self, stream, chunk, bytes_remaining):
        percent = round((1-bytes_remaining/stream.filesize)*100)
        if( percent%1 == 0):
            self.pbar.setValue(percent)            

    def download_finished(self):
        QMessageBox.information(self, "Download Completed", "YouTube download completed!")

    def actionInfoHandler(self):
        QMessageBox.information(self, "Info", "Created by Peter Mazela")

    def actionCloseHandler(self):
        QApplication.instance().quit()

################################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppWindow()
    sys.exit(app.exec_())
