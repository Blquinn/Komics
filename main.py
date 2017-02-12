import sys, os, subprocess
PATH = os.path.dirname(os.path.realpath(__name__))

from PyQt5 import QtWidgets

"""
Setup
"""
def run():
    """Boilerplate function to instantiate MainWindow"""
    if '-b' in sys.argv:
        print('Building UI files...')
        buildUI()
        from src.app import MainWindow
    else:
        from src.app import MainWindow

    app = QtWidgets.QApplication(sys.argv)
    gui = MainWindow()
    print('Running application...')
    sys.exit(app.exec_())

def buildUI():
    if sys.platform == 'win32':
        output = subprocess.getoutput('pyuic5 ' + PATH + '\\mainwindow.ui -o ' + PATH + '\\ui\\main.py')
        rc_output = subprocess.getoutput('pyrcc5.exe {} -o {}'.format((PATH + '\\icons.qrc'), (PATH + '\\icons_rc.py')))
    else:
        output = subprocess.getoutput('pyuic5' + PATH + '/mainwindow.ui -o ' + PATH + '/ui/main.py')
        rc_output = subprocess.getoutput('pyrcc5 {} -o {}'.format((PATH + '/icons.qrc'), (PATH + '/icons_rc.py')))

    if output:
        print(output)
        print('Failure building ui files')
        sys.exit(1)

    if rc_output:
        print(rc_output)
        print('Failure building resources')
        sys.exit(1)

if __name__ == "__main__":
    run()
