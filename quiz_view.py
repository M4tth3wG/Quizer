from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path

class QuizWindow(QMainWindow):
    def __init__(self, quiz):
        super(QuizWindow, self).__init__()
        uic.loadUi(Path('quiz_gui.ui'), self)

        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.quiz_window_views.setCurrentIndex(0)

        self.start_quiz_btn.clicked.connect(self.start_quiz)
        self.quit_btn.clicked.connect(self.close)

    def start_quiz(self):
        self.quiz_window_views.setCurrentIndex(1)