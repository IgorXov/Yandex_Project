# python -m PyQt6.uic.pyuic -x C:\Users\igorx\PycharmProjects\Yandex_Project\.card_widget.ui -o .venv\taskcard.py
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QFrame, QVBoxLayout
import sys

from task import *

class Second(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('edit_card.ui', self)
        self.nameEdit.setText()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"untitled.ui", self)
        # uic.loadUi(r"edit_card.ui", self)
        # uic.loadUi(r"untitled.ui", self)
        self.sec_win = None
        self.layout = QVBoxLayout(self.scrollAreaWidgetContents)
        cards = TaskManager()
        all_cards = cards.get_all_tasks()
        for card in all_cards:
            card.init_card()
            self.layout.addWidget(card)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
