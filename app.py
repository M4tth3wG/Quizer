from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path
import sys
from path_constants import GUI_RESOURCES, DEFAULT_DIRECTORY
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

        self.quit_btn.clicked.connect(sys.exit)
        self.load_quiz_btn.clicked.connect(self.load_quiz)
        self.create_new_quiz_btn.clicked.connect(partial(self.open_quiz_creator, None))
        self.edit_quiz_btn.clicked.connect(self.edit_quiz)

    def load_quiz(self):
        try:
            file_path = QFileDialog.getOpenFileName(directory=str(DEFAULT_DIRECTORY))[0]
            
            if file_path == '':
                return
            
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
            file_path = QFileDialog.getOpenFileName(directory=str(DEFAULT_DIRECTORY))[0]
            
            if file_path == '':
                return

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

    try:
        window = MenuWindow(Path(GUI_RESOURCES).joinpath("main_window.ui"))
        window.show()
    except:
        sys.stderr.write("Quitting app")

    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()