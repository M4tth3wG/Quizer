from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path
from quiz import Quiz
import questions
from functools import partial
import exceptions

class QuizWindow(QMainWindow):
    current_question = None
    answer_btns = []
    
    def __init__(self, quiz: Quiz, main_window):
        super(QuizWindow, self).__init__()
        uic.loadUi(Path('quiz_gui.ui'), self)

        self.quiz = quiz
        self.main_window = main_window
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.quiz_window_views.setCurrentIndex(0)

        self.start_quiz_btn.clicked.connect(self.start_quiz)
        self.quit_btn.clicked.connect(self.close)
        self.quit_btn.clicked.connect(self.main_window.show)
        self.quiz_back_to_menu_btn.clicked.connect(self.main_window.show)
        self.quiz_back_to_menu_btn.clicked.connect(self.close)
        self.confirm_btn.clicked.connect(self.confirm_answer)
        self.next_question_btn.clicked.connect(self.load_question)
        self.quiz_repeat_btn.clicked.connect(self.repeat_quiz)

    def start_quiz(self):
        self.quiz.prepare_quiz()
        self.quiz_window_views.setCurrentIndex(1)
        self.load_question()

    def load_question(self):
        try:
            self.next_question_btn.setEnabled(False)
            self.current_question = self.quiz.get_question()
            self.question_text_edit.setPlainText(self.current_question.content)
            self.update_quiz_progress_label()
            self.update_question_type_label()
            self.load_answers()
        except exceptions.EndQuestionException:
            self.quiz_window_views.setCurrentIndex(2)

    def update_quiz_progress_label(self):
        self.quiz_progress_label.setText(f'{self.quiz.get_actual_index() + 1}/{self.quiz.get_number_of_question()}')

    def update_current_score_label(self):
        self.current_score_label.setText(f'{self.quiz.get_score()}/{self.quiz.get_actual_max_points()}')

    def update_question_type_label(self):
        if isinstance(self.current_question, questions.SingleChoiceQuestion):
            self.question_type_label.setText('Jednokrotnego wyboru')
        else:
            self.question_type_label.setText('Wielokrotnego wyboru')

    def load_answers(self):
        self.clear_answers()

        if isinstance(self.current_question, questions.SingleChoiceQuestion):
            self.load_single_choice_answers()
        else:
            self.load_multiple_choice_answers()

    def load_single_choice_answers(self):
        answers_dict = self.current_question.answers

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
        answers_dict = self.current_question.answers

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
        return [index for index, button in enumerate(self.answer_btns)]
    
    def clear_answers(self):
        for btn in self.answer_btns:
            self.answer_layout.removeWidget(btn)
            btn.deleteLater()
            
        self.answer_btns.clear()

    def repeat_quiz(self):
        self.quiz_window_views.setCurrentIndex(0)
        self.quiz.reset_quiz()