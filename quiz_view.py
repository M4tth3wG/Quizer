from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path
from quiz import Quiz
import quiz
import questions
from functools import partial
import exceptions
import os
from path_constants import GUI_RESOURCES, DEFAULT_DIRECTORY

class QuizWindow(QMainWindow):

    def __init__(self, quiz: Quiz, main_window):
        super(QuizWindow, self).__init__()
        uic.loadUi(Path(GUI_RESOURCES).joinpath('quiz_gui.ui'), self)

        self.current_question = None
        self.answer_btns = []
        self.quiz = quiz
        self.main_window = main_window
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.quiz_window_views.setCurrentIndex(0)
        self.quiz_name_label.setText(quiz._name)
        self.question_repetition_line_edit.setText('1')

        self.start_quiz_btn.clicked.connect(self.start_quiz)
        self.quit_btn.clicked.connect(self.close)
        self.quit_btn.clicked.connect(self.main_window.show)
        self.quiz_back_to_menu_btn.clicked.connect(self.close)
        self.quiz_back_to_menu_btn.clicked.connect(self.main_window.show)
        self.back_to_menu_btn.clicked.connect(self.close)
        self.back_to_menu_btn.clicked.connect(self.main_window.show)
        self.confirm_btn.clicked.connect(self.confirm_answer)
        self.next_question_btn.clicked.connect(self.load_question)
        self.quiz_repeat_btn.clicked.connect(self.repeat_quiz)

    def start_quiz(self):
        try:
            self.quiz.number_of_question_repetition = int(self.question_repetition_line_edit.text())
        except:
            self.main_window.show_error_message('Nieprawidłowa liczba powtórzeń pytania!')
            return

        self.quiz.shuffle = self.question_shuffle_check_box.isChecked()
        self.quiz.shuffle_answers = self.answer_shuffle_check_box.isChecked()
        self.quiz.mode = quiz.RELENTLESS_MODE if self.restrictive_mode_check_box.isChecked() else quiz.GENTLE_MODE
        
        self.quiz.prepare_quiz()
        self.quiz_window_views.setCurrentIndex(1)
        self.load_question()

    def load_question(self):
        try:
            self.next_question_btn.setEnabled(False)
            self.current_question = self.quiz.get_question()
            self.question_text_edit.setPlainText(self.current_question._content)
            self.update_quiz_progress_label()
            self.update_question_type_label()
            self.load_answers()
        except exceptions.EndQuestionException:
            self.quiz_window_views.setCurrentIndex(2)
            self.display_final_score()

    def update_quiz_progress_label(self):
        self.quiz_progress_label.setText(f'{self.quiz.get_actual_index() + 1}/{self.quiz.get_number_of_question()}')

    def update_current_score_label(self):
        self.current_score_label.setText(f'{round(self.quiz.get_score(), 2)}/{self.quiz.get_actual_max_points()}')

    def update_question_type_label(self):
        if isinstance(self.current_question, questions.SingleChoiceQuestion):
            self.question_type_label.setText('Pytanie jednokrotnego wyboru')
        else:
            self.question_type_label.setText('Pytanie wielokrotnego wyboru')

    def load_answers(self):
        self.clear_answers()

        if isinstance(self.current_question, questions.SingleChoiceQuestion):
            self.load_single_choice_answers()
        else:
            self.load_multiple_choice_answers()

    def load_single_choice_answers(self):
        answers_dict = self.current_question._answers

        for answer in answers_dict.values():
            answer_btn = QPushButton()
            answer_btn.setText(answer)
            answer_btn.setStyleSheet("text-align: left;")
            answer_btn.setCheckable(True)
            answer_btn.clicked.connect(partial(self.update_buttons, button = answer_btn))
            answer_btn.clicked.connect(self.update_confirm_button)

            self.answer_layout.insertWidget(self.answer_layout.count() - 1, answer_btn)
            self.answer_btns.append(answer_btn)

    def load_multiple_choice_answers(self):
        answers_dict = self.current_question._answers

        for answer in answers_dict.values():
            answer_btn = QPushButton()
            answer_btn.setText(answer)
            answer_btn.setStyleSheet("text-align: left;")
            answer_btn.setCheckable(True)
            answer_btn.clicked.connect(self.update_confirm_button)

            self.answer_layout.insertWidget(self.answer_layout.count() - 1, answer_btn)
            self.answer_btns.append(answer_btn)
        
    def update_buttons(self, button):
        if button.isChecked():
            self.lock_answer_buttons()
        else:
            self.unlock_answer_buttons()
        
    def lock_answer_buttons(self):
        for btn in self.answer_btns:
            if not btn.isChecked():
                btn.setEnabled(False)

    def unlock_answer_buttons(self):
        for btn in self.answer_btns:
            if not btn.isEnabled():
                btn.setEnabled(True)

    def update_confirm_button(self):
        if any(btn.isChecked() for btn in self.answer_btns):
            self.confirm_btn.setEnabled(True)
        else:
            self.confirm_btn.setEnabled(False)

    def confirm_answer(self):
        self.quiz.check_answer(self.get_answers_from_buttons())
        self.display_correct_answers()
        self.update_current_score_label()
        self.confirm_btn.setEnabled(False)

    def display_correct_answers(self):
        for btn in self.answer_btns:
            btn.setEnabled(False)

            if btn.isChecked():
                btn.setStyleSheet(btn.styleSheet() + "background-color: #ff0000;")

        for index in self.current_question.get_correct_answers():
            btn = self.answer_btns[index]

            if btn.isChecked():
                btn.setStyleSheet(btn.styleSheet() + "background-color: #008000;")
            else:
                btn.setStyleSheet(btn.styleSheet() + "background-color: #ffff00;")

        self.next_question_btn.setEnabled(True)

    def get_answers_from_buttons(self):
        answers_list = []
        for index, button in enumerate(self.answer_btns):
            if button.isChecked():
                answers_list.append(index)

        return answers_list

    
    def clear_answers(self):
        for btn in self.answer_btns:
            self.answer_layout.removeWidget(btn)
            btn.deleteLater()

        self.answer_btns.clear()

    def repeat_quiz(self):
        self.quiz_window_views.setCurrentIndex(0)
        self.current_score_label.setText('0')
        self.quiz.reset_quiz()

    def display_final_score(self):
        self.final_score_label.setText(f'{round(self.quiz.get_score(),2)}/{self.quiz.get_total_max_points()}')