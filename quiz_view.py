from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path

class QuizWindow(QMainWindow):
    def __init__(self, quiz):
        super(QuizWindow, self).__init__()
        uic.loadUi(Path('quiz_gui.ui'), self)

        self.setFixedWidth(800)
        self.setFixedHeight(600)