import sys
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene
from PyQt5 import QtGui, QtWidgets, QtCore
from ui.main import Ui_MainWindow
import os
import re
import rarfile

# Local
from src.photoviewer import PhotoViewer

IMAGE_REGEX = re.compile(r".*\.(jpg|png|gif)$")
FILE_TYPES = ('All Files (*)',
              'JPEG Files (*.jpg)',
              'GIF Files (*.gif)',
              'PNG Files (*.png)',
              'CBZ Archives (*.cbz)',
              'CBR Archives (*.cbr)',
              'CBT Archives (*.cbt)',
              'CBA Archives (*.cba)',
              'CB7 Archives (*.cb7)')


class MainWindow(QtWidgets.QMainWindow):
    """MainWindow is the boilerplate for our gui"""
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.progress = 0
        self.collections = None
        self.workingDirectory = None
        self.workingFiles = None
        self.workingFileType = None  # Should be ( archive | dir )
        self.workingFileIndex = 0
        self.scene = QGraphicsScene()
        self.ui.progressBar.hide()
        self.ui.graphicsView = PhotoViewer(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.graphicsView.sizePolicy().hasHeightForWidth())
        self.ui.graphicsView.setSizePolicy(sizePolicy)
        self.ui.graphicsView.setObjectName("graphicsView")
        self.ui.gridLayout.addWidget(self.ui.graphicsView, 1, 0, 1, 1)

        self.main()
    # def resize(self, event):
    #     print(event)
        # self.ui.graphicsView.scale(self.width(), self.height())

    def main(self):
        """main is responsible for setting up the gui"""
        self.buttons()
        self.setWindowIcon(QtGui.QIcon(':/images/assets/icons/36/icon.png'))
        self.show()

    def quit(self):
        """quit exits the application gracefully"""
        print('Komics exited properly.')
        sys.exit()

    def closeEvent(self, event):
        print("Komics exited with x button.")
        event.accept()
        sys.exit()

    def buttons(self):
        # Actions
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.actionOpen.triggered.connect(self.openFile)
        self.ui.actionOpen_Directory.triggered.connect(self.openDirectory)
        self.ui.actionNext_Page.triggered.connect(self.loadNext)
        self.ui.actionPrevious_Page.triggered.connect(self.loadPrev)
        self.ui.actionEnd_of_Collection.triggered.connect(self.archiveEnd)
        self.ui.actionStart_of_Collection.triggered.connect(self.archiveBeggining)
        self.ui.actionClose_Collection.triggered.connect(self.closeCollection)
        self.ui.actionGoTo_Page.triggered.connect(self.pageGoTo)
        self.ui.actionPrevious_Collection.triggered.connect(self.archivePrevious)
        self.ui.actionNext_Collection.triggered.connect(self.archiveNext)
        self.ui.actionZoom_In.triggered.connect(self.ui.graphicsView.zoomInKeys)
        self.ui.actionZoom_Out.triggered.connect(self.ui.graphicsView.zoomOutKeys)
        self.ui.actionScroll_Forward.triggered.connect(self.scrollHalfScreen)
        self.ui.actionFull_Screen.triggered.connect(self.viewFullScreen)

        # Page Controls
        self.ui.btnArchivePrevious.clicked.connect(self.archivePrevious)
        self.ui.btnArchiveBeggining.clicked.connect(self.archiveBeggining)
        self.ui.btnPageBack.clicked.connect(self.loadPrev)
        self.ui.btnPageGoTo.clicked.connect(self.pageGoTo)
        self.ui.btnPageForward.clicked.connect(self.loadNext)
        self.ui.btnArchiveEnd.clicked.connect(self.archiveEnd)
        self.ui.btnArchiveNext.clicked.connect(self.archiveNext)

        # View controls
        self.ui.btnViewWidthFit.clicked.connect(self.viewWidthFit)
        self.ui.btnViewHeightFit.clicked.connect(self.viewHeightFit)
        self.ui.btnViewFitToSize.clicked.connect(self.viewFitToSize)
        self.ui.btnViewManualZoom.clicked.connect(self.viewManualZoom)

        # Layout controls
        self.ui.btnPageDoublePage.clicked.connect(self.layoutDoublePage)

    """Start Buttons"""
    def archiveEnd(self):
        if self.workingFiles:
            self.workingFileIndex = len(self.workingFiles) - 1
            self.loadImage(self.workingFiles[self.workingFileIndex])
        else:
            self.okayMessageBox("Please load a collection")

    def archiveBeggining(self):
        if self.workingFiles:
            self.workingFileIndex = 0
            self.loadImage(self.workingFiles[self.workingFileIndex])
        else:
            self.okayMessageBox("Please load a collection")

    def archiveNext(self):
        self.okayMessageBox('You pressed archive next')

    def archivePrevious(self):
        self.okayMessageBox('You pressed Previous Archive')

    def pageGoTo(self):
        self.okayMessageBox('You pressed page goto')

    def viewWidthFit(self):
        self.okayMessageBox('You pressed Width fit')

    def viewHeightFit(self):
        self.okayMessageBox('You pressed height fit')

    def viewFitToSize(self):
        self.okayMessageBox('You pressed fit to size')

    def viewManualZoom(self):
        self.okayMessageBox('You pressed manual zoom')

    def layoutDoublePage(self):
        self.okayMessageBox('You pressed double page')

    def closeCollection(self):
        self.workingFiles = None
        self.workingFileIndex = 0
        self.ui.graphicsView.setScene(None)
        self.rf = None

    """End Buttons"""

    """Start Actions"""
    def viewFullScreen(self):
        self.ui.graphicsView.showFullScreen()

    def showFullScreen(self):
        self.ui.centralWidget.hide()
        # self.ui.menuBar.hide()
        # self.ui.graphicsView.showFullScreen()
    """End Actions"""

    def showProgress(self):
        self.ui.progressBar.show()
        self.progress = 0
        while self.progress < 100:
            self.progress += 0.00001
            self.ui.progressBar.setValue(self.progress)
        self.ui.progressBar.hide()

    def okayMessageBox(self, message, title='Message'):
        """Mixin"""
        QtWidgets.QMessageBox.question(self,
                                       title,
                                       message,
                                       QtWidgets.QMessageBox.Ok)

    def scrollHalfScreen(self):
        end = self.ui.graphicsView.scrollHalf()
        if end:
            self.loadNext()

    def loadImage(self, image):
        self.scene.clear()
        if type(image) is str:
            pm = QtGui.QPixmap(image)
            # self.scene.addPixmap(pm)
            # self.ui.graphicsView.setScene(self.scene)
            self.ui.graphicsView.setPhoto(pm)
        elif type(image) is rarfile.Rar3Info:
            im_type = image.filename.split('.')[-1].strip().upper()
            bts = self.rf.read(image)
            pm = QtGui.QPixmap()
            pm.loadFromData(bts, im_type)
            self.ui.graphicsView.setPhoto(pm)
            # self.scene.addPixmap(pm)
            # self.ui.graphicsView.setScene(self.scene)
        else:
            self.okayMessageBox("Invalid image format")

    def loadPrev(self):
        if self.workingFiles:
            if self.workingFileIndex - 1 >= 0:
                self.workingFileIndex -= 1
                self.loadImage(self.workingFiles[self.workingFileIndex])
            else:
                self.workingFileIndex = 0
                self.okayMessageBox("You've reached the begining of the collection")
        else:
             self.okayMessageBox("Please open a file or archive.")

    def loadNext(self):
        if self.workingFiles:
            if self.workingFileIndex + 1 < len(self.workingFiles):
                self.workingFileIndex += 1
                self.loadImage(self.workingFiles[self.workingFileIndex])
            else:
                self.workingFileIndex = 0
                self.okayMessageBox("You've reached the end :(")
        else:
            self.okayMessageBox("Please open a file or archive.")

    def openDirectory(self):
        diag = QFileDialog()
        path = QFileDialog.getExistingDirectory(diag, "Select Directory")
        if path:
            if os.path.isdir(path):
                self.workingFileIndex = 0
                self.workingFiles = [
                    os.path.join(path, file)
                    for file in os.listdir(path)
                    if IMAGE_REGEX.match(file)
                ]
            if not self.workingFiles:
                self.okayMessageBox('No valid files found in directory')
            else:
                self.loadImage(self.workingFiles[self.workingFileIndex])


    # types: JPEG GIF PNG CBZ CBR CBT CBA CB7
    def openFile(self):
        diag = QFileDialog()
        options = QFileDialog.options(diag)
        path, _ = QFileDialog.getOpenFileName(diag, "QFileDialog.getOpenFileName()", "", ';;'.join(FILE_TYPES), options=options)
        filename, file_ext = os.path.splitext(path)
        if path:
            if file_ext in '.jpg .gif .png':
                self.workingFileIndex = 0
                self.workingFiles = [
                    os.path.dirname(path) + '/' + file
                    for file in os.listdir(os.path.dirname(path))
                    if IMAGE_REGEX.match(file)
                ]
                for i, file in enumerate(self.workingFiles):
                    if file == path:
                        self.workingFileIndex = i
                        break

                if not self.workingFiles:
                    self.okayMessageBox('No valid files found in directory')
                else:
                    self.loadImage(self.workingFiles[self.workingFileIndex])
            elif file_ext == '.cbr':
                # Unrar and open as directory
                self.rf = rarfile.RarFile(path, mode='r')
                self.workingFiles = [
                    f for f in self.rf.infolist()
                    if IMAGE_REGEX.match(f.filename)
                ]
                self.loadImage(self.workingFiles[0])
            else:
                self.okayMessageBox("Please use a valid filetype")
