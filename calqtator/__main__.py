import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from calqtator import CalQtator


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('CalQtator')
    calqtator = CalQtator()
    calqtator.show()
    app.exec_()


if __name__ == '__main__':
    main()
