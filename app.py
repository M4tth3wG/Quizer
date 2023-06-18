import PyQt6
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QFile, QTextStream
from pathlib import Path
import sys
import os
import quiz
from quiz_view import QuizWindow
from quiz_creator import QuizCreatorWindow
from functools import partial

class MenuWindow(QMainWindow):
    
    def __init__(self, ui_file):
        super(MenuWindow, self).__init__()
        uic.loadUi(ui_file, self)

        self.quiz_window = None
        self.setFixedWidth(500)
        self.setFixedHeight(250)

        self.quit_btn.clicked.connect(exit)
        self.load_quiz_btn.clicked.connect(self.load_quiz)
        self.create_new_quiz_btn.clicked.connect(partial(self.open_quiz_creator, None))
        self.edit_quiz_btn.clicked.connect(self.edit_quiz)

    def load_quiz(self):
        try:
            file_path = QFileDialog.getOpenFileName(directory=str(Path(os.path.dirname(os.path.realpath(__file__))).joinpath('Quizzes')))[0]
            loaded_quiz = quiz.Quiz.load_from_json(file_path)
            self.quiz_window = QuizWindow(loaded_quiz, self)
            self.quiz_window.show()
            self.close()
        except:
            self.show_error_message('Nieprawidłowy plik quizu!')

    def open_quiz_creator(self, quiz_path = None):
        self.quiz_creator_window = QuizCreatorWindow(self, quiz_path)
        self.quiz_creator_window.show()
        self.close()

    def edit_quiz(self):
        try:
            file_path = QFileDialog.getOpenFileName(directory=str(Path(os.path.dirname(os.path.realpath(__file__))).joinpath('Quizzes')))[0]
            self.open_quiz_creator(file_path)
        except:
            self.show_error_message('Nieprawidłowy plik quizu!')

    
    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        msg.exec()

def main():
    app = QApplication([])

    # loading custom style sheet

    """ file = QFile("MaterialDark.qss")
    file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll()) """

    try:
        window = MenuWindow(Path("main_window.ui"))
        window.show()
        sys.exit(app.exec())
    except:
        sys.stderr.write("FATAL ERROR!!!")
    

if __name__ == '__main__':
    main()