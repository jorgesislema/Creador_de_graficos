# main.py
# Entry point de la GUI principal

import sys
from PySide6.QtWidgets import QApplication
from chart_maker.app.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
