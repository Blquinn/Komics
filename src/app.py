import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene
from PyQt5 import QtGui
from ui.main import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    """MainWindow is the boilerplate for our gui"""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scene = QGraphicsScene()
        self.progress = 0
        self.main()

    def main(self):
        """main is responsible for setting up the gui"""
        self.buttons()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.show()

    def quit(self):
        """quit exits the application gracefully"""
        print('Komics exited properly.')
        sys.exit()

    def buttons(self):
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.actionOpen.triggered.connect(self.openFile)

        # Page Controls
        self.ui.btnArchivePrevious.clicked.connect(self.archivePrevious)
        self.ui.btnArchiveBeggining.clicked.connect(self.archiveBeggining)
        self.ui.btnPageBack.clicked.connect(self.pageBack)
        self.ui.btnPageGoTo.clicked.connect(self.pageGoTo)
        self.ui.btnPageForward.clicked.connect(self.pageForward)
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
        self.okayMessageBox('You pressed archive end')
        self.showProgress()

    def archiveBeggining(self):
        self.okayMessageBox('You pressed archive begginging')
        self.showProgress()

    def archiveNext(self):
        self.okayMessageBox('You pressed archive next')
        self.showProgress()

    def archivePrevious(self):
        self.okayMessageBox('You pressed Previous Archive')
        self.showProgress()

    def pageBack(self):
        self.okayMessageBox('You pressed page back')
        self.showProgress()

    def pageForward(self):
        self.okayMessageBox('You pressed page forward')
        self.showProgress()

    def pageGoTo(self):
        self.okayMessageBox('You pressed page goto')
        self.showProgress()

    def viewWidthFit(self):
        self.okayMessageBox('You pressed Width fit')
        self.showProgress()

    def viewHeightFit(self):
        self.okayMessageBox('You pressed height fit')
        self.showProgress()

    def viewFitToSize(self):
        self.okayMessageBox('You pressed fit to size')
        self.showProgress()

    def viewManualZoom(self):
        self.okayMessageBox('You pressed manual zoom')
        self.showProgress()

    def layoutDoublePage(self):
        self.okayMessageBox('You pressed double page')
        self.showProgress()

    """End Buttons"""

    def showProgress(self):
        self.progress = 0
        while self.progress < 100:
            self.progress += 0.00001
            self.ui.progressBar.setValue(self.progress)

    def okayMessageBox(self, message, title='Message'):
        """Mixin"""
        QtWidgets.QMessageBox.question(self,
                                       title,
                                       message,
                                       QtWidgets.QMessageBox.Ok)


    def openFile(self):
        diag = QFileDialog()
        options = QFileDialog.options(diag)
        fileName, _ = QFileDialog.getOpenFileName(diag, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            image = QtGui.QPixmap(fileName)
            self.scene.addPixmap(image)
            self.ui.graphicsView.setScene(self.scene)