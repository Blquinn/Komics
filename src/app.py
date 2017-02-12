import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from ui.main import Ui_MainWindow



# from src.mixins.files import Files


class MainWindow(QtWidgets.QMainWindow):
    """MainWindow is the boilerplate for our gui"""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main()
        self.ui = None
        self.pixmap = None
        self.label = None

    def main(self):
        """main is responsible for setting up the gui"""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.buttons()
        self.show()

    def quit(self):
        """quit exits the application gracefully"""
        print('Komics exited properly.')
        sys.exit()

    def buttons(self):
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.actionOpen.triggered.connect(self.openFile)


    def openFile(self):
        diag = QFileDialog()
        options = QFileDialog.options(diag)
        fileName, _ = QFileDialog.getOpenFileName(diag, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            # self.label = QLabel('Cool pics')
            # self.pixmap = QPixmap(fileName)
            # self.label.setPixmap(pixmap)
            # self.ui.graphicsView.
            # scene = QGraphicsScene()
            # image = QPixmap(fileName)
            # item = QGraphicsPixmapItem(image)
            # scene.addItem(item)
            # self.ui.graphicsView.items(scene)