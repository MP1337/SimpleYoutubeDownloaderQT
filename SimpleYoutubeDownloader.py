from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAction, QPushButton, QLabel,QLineEdit, \
                            QProgressBar,QFileDialog, QStyleFactory, QListWidget
import clipboard
import pytube
from urllib import request
import sys
from os import getcwd

class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('app.ui', self)
        self.show()
        #Buttons
        buttonBrowse = self.findChild(QPushButton, 'buttonBrowse')
        buttonBrowse.clicked.connect(self.buttonBrowseHandler)

        buttonPaste = self.findChild(QPushButton, 'buttonPaste')
        buttonPaste.clicked.connect(self.buttonPasteHandler)

        buttonDownload = self.findChild(QPushButton, 'buttonDownload')
        buttonDownload.clicked.connect(self.buttonDownloadHandler)

        actionInfo = self.findChild(QAction, 'actionInfo')
        actionInfo.triggered.connect(self.actionInfoHandler)

        actionClose = self.findChild(QAction, 'actionClose')
        actionClose.triggered.connect(self.actionCloseHandler)

        #list Widget
        self.listWidget = self.findChild(QListWidget, 'listWidget')

        #Labels
        self.labelVideo = self.findChild(QLabel, 'labelVideo')
        self.labelImage = self.findChild(QLabel, 'labelImage')
        img = QPixmap("default_thumb.jpg")
        self.labelImage.setPixmap(img)

        #QlineEdits
        self.editTarget  = self.findChild(QLineEdit, 'editTarget')
        self.editTarget.setText(getcwd())

        self.editLink = self.findChild(QLineEdit, 'editLink')

        #Progressbar
        self.pbar  = self.findChild(QProgressBar)
        self.pbar.setValue(0)

################################################################################################

    def buttonBrowseHandler(self):
        filename = str(QFileDialog.getExistingDirectory(None))
        self.editTarget.setText(filename)

    def buttonPasteHandler(self):
        clip = str(clipboard.paste())
        self.editLink.setText(clip)
        clip = self.editLink.text()
        
        if 'youtube' in clip and 'watch' in clip:
            yttitle = pytube.YouTube(clip)
            self.labelVideo.setText(yttitle.title)
            url = yttitle.thumbnail_url #url for thumbnail
            request.urlretrieve(url,'thumb.jpg')
            pixmap = QPixmap("thumb.jpg").scaled(650,400)
            self.labelImage.setPixmap(pixmap)
        else:
            QMessageBox.about(self,"Warning", "No YouTube link!")
    
    def buttonDownloadHandler(self):
        try:
            ytdown = pytube.YouTube(str(self.editLink.text()),on_progress_callback=self.progress_function)
            ytdown.streams.first().download(self.editTarget.text())
            self.listWidget.addItem(ytdown.title)
            self.download_finished()
        except:
            print(ex)
        
    
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
