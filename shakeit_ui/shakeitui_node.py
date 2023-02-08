import sys

from PyQt5.QtWidgets import QApplication
from shakeit_ui.Main import MainWindow

def hallo():
    print("hallo world!")

def main():
    print('Hi from shakeit_ui.')
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
