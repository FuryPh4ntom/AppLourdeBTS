import sys
from PyQt6.QtWidgets import QApplication
from fonction.appli import MainWindow


if __name__ == '__main__':
    try:
        # show the app icon on the taskbar
        import ctypes
        myappid = 'yourcompany.yourproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    finally:
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec())
