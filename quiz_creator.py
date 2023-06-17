from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path
from quiz import Quiz
import questions
from functools import partial
import exceptions

class QuizCreatorWindow(QMainWindow):
    
    def __init__(self, main_window):
        super(QuizCreatorWindow, self).__init__()
        uic.loadUi(Path('quiz_creator_gui.ui'), self)

        self.main_window = main_window
        self.quit_btn.clicked.connect(self.close)
        self.quit_btn.clicked.connect(self.main_window.show)        