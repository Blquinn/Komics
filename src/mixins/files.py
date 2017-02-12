from PyQt5.QtWidgets import QFileDialog, QLabel
from PyQt5.QtGui import QPixmap

class Files():
    def openFile(self):
        diag = QFileDialog()
        options = QFileDialog.options(diag)
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.ui.label = QLabel(self)
            self.ui.pixmap = QPixmap(fileName)
            self.ui.label.setPixmap(pixmap)


    def openFileNamesDialog(self):
        diag = QFileDialog()
        options = QFileDialog.Options(diag)
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)