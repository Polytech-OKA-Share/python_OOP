import sys
from PyQt6.QtWidgets import QApplication
from othello_gui.main_window import MainWindow

def main():
    """
    GUIアプリケーションを起動する
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
