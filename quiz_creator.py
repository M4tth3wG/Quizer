from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path
from quiz import Quiz
import questions
from functools import partial
import exceptions
from PyQt6.QtGui import QFont

class QuizCreatorWindow(QMainWindow):
    
    def __init__(self, main_window):
        super(QuizCreatorWindow, self).__init__()
        uic.loadUi(Path('quiz_creator_gui.ui'), self)

        self.answer_layouts_list = []
        self.main_window = main_window
        self.quit_btn.clicked.connect(self.close)
        self.quit_btn.clicked.connect(self.main_window.show)
        self.add_answer_btn.clicked.connect(self.create_answer_input)
        self.multiple_answer_question_check_box.stateChanged.connect(self.update_correct_answers_check_boxes)

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
        correct_answer_check_box.stateChanged.connect(self.update_buttons)

        self.answer_layouts_list.append(answer_horizontal_layout)
        self.answer_vertical_layout.addLayout(answer_horizontal_layout)
        self.update_buttons()

    def delete_answer(self, answer_layout):
        self.answer_vertical_layout.removeItem(answer_layout)
        self.answer_layouts_list.remove(answer_layout)
        
        while answer_layout.count():
            widget = answer_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        answer_layout.deleteLater()
        self.update_buttons()

    def update_correct_answers_check_boxes(self):
        if self.multiple_answer_question_check_box.isChecked():
            self.unlock_correct_answers_check_boxes()
        else:
            self.clear_correct_answers_check_boxes()

    def clear_correct_answers_check_boxes(self):
        for layout in self.answer_layouts_list:
            layout.itemAt(0).widget().setChecked(False)

    def update_buttons(self):
        buttons = [layout.itemAt(0).widget() for layout in self.answer_layouts_list]
        
        if self.multiple_answer_question_check_box.isChecked():
            return
        elif not any(button.isChecked() for button in buttons):
            self.unlock_correct_answers_check_boxes()
        else:
            self.lock_correct_answers_check_boxes()

    def update_buttons_after_deletion(self):
        buttons = [layout.itemAt(0).widget() for layout in self.answer_layouts_list]
        
        if not any(button.isChecked() for button in buttons):
            self.unlock_correct_answers_check_boxes()

    def lock_correct_answers_check_boxes(self):
        for layout in self.answer_layouts_list:
            button =  layout.itemAt(0).widget()
            if not button.isChecked():
                button.setEnabled(False)

    def unlock_correct_answers_check_boxes(self):
        for layout in self.answer_layouts_list:
            layout.itemAt(0).widget().setEnabled(True)
        

    