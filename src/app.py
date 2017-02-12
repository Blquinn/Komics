import sys
from PyQt5 import QtWidgets
from ui.main import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    """MainWindow is the boilerplate for our gui"""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main()
        self.ui = None

    def main(self):
        """main is responsible for setting up the gui"""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.buttons()
        self.show()

    # def buttons(self):
    #     Ui_MainWindddow.btnQuit

    def quit(self):
        """quit exits the application gracefully"""
        print('Komics exited properly.')
        sys.exit()

    def openFile(self):
        # file = QtWidgets.QFileDialog.getExistingDirectory()
        diag = QtWidgets.QFileDialog()
        # diag.setNameFilter('jpg')
        file = diag.getExistingDirectory()
        pathobject = open(file, 'r')
        print(pathobject)
        # print(file)

    def buttons(self):
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.actionOpen.triggered.connect(self.openFile)
        # self.ui.btnOpenFile.clicked.connect(self.openFile)