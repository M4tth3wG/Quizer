from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path
from quiz import Quiz
import questions
from functools import partial
import exceptions
from PyQt6.QtGui import QFont
from QuizBuilder import QuizBuilder

class QuizCreatorWindow(QMainWindow):
    
    def __init__(self, main_window):
        super(QuizCreatorWindow, self).__init__()
        uic.loadUi(Path('quiz_creator_gui.ui'), self)

        self.quiz_builder = QuizBuilder()
        self.answer_layouts_list = []
        self.main_window = main_window

        self.quit_btn.clicked.connect(self.close)
        self.quit_btn.clicked.connect(self.main_window.show)
        self.add_answer_btn.clicked.connect(self.create_answer_input)
        self.multiple_answer_question_check_box.stateChanged.connect(self.update_correct_answers_check_boxes)
        self.previous_question_btn.clicked.connect(self.load_previous_question)
        self.next_question_btn.clicked.connect(self.load_next_question)
        self.edit_question_btn.clicked.connect(self.edit_current_question)
        self.save_question_btn.clicked.connect(self.save_current_question)
        self.add_question_btn.clicked.connect(self.add_new_question)
        self.save_quiz_btn.clicked.connect(self.save_quiz)

    def create_answer_input(self):
        answer_line_edit = QLineEdit()
        delete_answer_btn = QPushButton()
        correct_answer_check_box = QCheckBox()

        delete_answer_btn.setText('-')
        font = QFont("Arial", 12)
        font.setBold(True)
        delete_answer_btn.setFont(font)

        answer_horizontal_layout = QHBoxLayout()

        answer_horizontal_layout.addWidget(correct_answer_check_box)
        answer_horizontal_layout.addWidget(answer_line_edit)
        answer_horizontal_layout.addWidget(delete_answer_btn)

        delete_answer_btn.clicked.connect(partial(self.delete_answer, answer_horizontal_layout))
        correct_answer_check_box.stateChanged.connect(self.relock_correct_answers_check_boxes)

        self.answer_layouts_list.append(answer_horizontal_layout)
        self.answer_vertical_layout.addLayout(answer_horizontal_layout)
        self.relock_correct_answers_check_boxes()

        return answer_horizontal_layout

    def delete_answer(self, answer_layout):
        self.answer_vertical_layout.removeItem(answer_layout)
        self.answer_layouts_list.remove(answer_layout)
        
        while answer_layout.count():
            widget = answer_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        answer_layout.deleteLater()
        self.relock_correct_answers_check_boxes()

    def update_correct_answers_check_boxes(self):
        if self.multiple_answer_question_check_box.isChecked():
            self.unlock_correct_answers_check_boxes()
        else:
            self.clear_correct_answers_check_boxes()

    def clear_correct_answers_check_boxes(self):
        for layout in self.answer_layouts_list:
            layout.itemAt(0).widget().setChecked(False)

    def relock_correct_answers_check_boxes(self):
        buttons = [layout.itemAt(0).widget() for layout in self.answer_layouts_list]
        
        if self.multiple_answer_question_check_box.isChecked():
            return
        elif not any(button.isChecked() for button in buttons):
            self.unlock_correct_answers_check_boxes()
        else:
            self.lock_correct_answers_check_boxes()

    def lock_correct_answers_check_boxes(self):
        for layout in self.answer_layouts_list:
            button =  layout.itemAt(0).widget()
            if not button.isChecked():
                button.setEnabled(False)

    def unlock_correct_answers_check_boxes(self):
        for layout in self.answer_layouts_list:
            layout.itemAt(0).widget().setEnabled(True)

    def update_action_buttons(self):
        pass

    def load_question(self, question):
        self.question_text_edit.setText(question.content)
        self.multiple_answer_question_check_box.setChecked(isinstance(question, questions.MultipleChoiceQuestion))

        for answer in question.answers:
            answer_layout = self.create_answer_input()
            answer_layout.itemAt(1).widget().setText(answer)

        for correct_answer in question.get_correct_answers():
            self.answer_layouts_list[correct_answer].itemAt(0).widget().setChecked(True)

        # lock question


    def load_previous_question(self):
        pass

    def load_next_question(self):
        pass

    def edit_current_question(self):
        pass

    def save_current_question(self):
        pass

    def add_new_question(self):
        pass

    def save_quiz(self):
        pass

    
        

    