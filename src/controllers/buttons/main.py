import sys, os
sys.path.insert(0, os.path.abspath('..')) # Path hack
from PyQt5 import QtCore

from ui.main import Ui_MainWindow

def quit():
    Ui_MainWindow.btnQuit.connect(QtCore.QCoreApplication.instance().quit)
