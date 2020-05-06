from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAction, QPushButton, QLabel,QLineEdit, \
                            QProgressBar,QFileDialog, QStyleFactory, QListWidget
import clipboard
import pytube
from urllib import request
import sys
from os import getcwd
#import pprint

class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('app.ui', self)

        #print(self.__dict__)
        
        #Buttons
        self.buttonBrowse.clicked.connect(self.buttonBrowseHandler)
        self.buttonPaste.clicked.connect(self.buttonPasteHandler)
        self.buttonDownload.clicked.connect(self.buttonDownloadHandler)
        self.actionInfo.triggered.connect(self.actionInfoHandler)
        self.actionClose.triggered.connect(self.actionCloseHandler)

        img = QPixmap("default_thumb.jpg")
        self.labelImage.setPixmap(img)

        #QlineEdits
        self.editTarget.setText(getcwd())
        #Progressbar
        self.progressBar.setValue(0)

        self.show()

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
        except pytube.exceptions.PytubeError as err:
            print(err)
        
    
    def progress_function(self, stream, chunk, bytes_remaining):
        percent = round((1-bytes_remaining/stream.filesize)*100)
        self.progressBar.setValue(percent)            

    def download_finished(self):
        QMessageBox.information(self, "Download Completed", "YouTube download completed!")

    def actionInfoHandler(self):
        QMessageBox.information(self, "Info", "Created by Peter Mazela")

    def actionCloseHandler(self):
        QApplication.instance().quit()

def main():
    app = QApplication(sys.argv)
    ex = AppWindow()
    sys.exit(app.exec_())

################################################################################################

if __name__ == '__main__':
    main()
