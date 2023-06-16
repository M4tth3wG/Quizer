from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path
from quiz import Quiz
import questions
from functools import partial

class QuizWindow(QMainWindow):
    current_question = None
    answer_btns = []
    
    def __init__(self, quiz: Quiz):
        super(QuizWindow, self).__init__()
        uic.loadUi(Path('quiz_gui.ui'), self)

        self.quiz = quiz
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.quiz_window_views.setCurrentIndex(0)

        self.start_quiz_btn.clicked.connect(self.start_quiz)
        self.quit_btn.clicked.connect(self.close)
        self.confirm_btn.clicked.connect(self.confirm_answer)

    def start_quiz(self):
        self.quiz_window_views.setCurrentIndex(1)
        self.load_question()

    def load_question(self):
        #current_question = self.quiz.get_question()
        self.current_question = questions.SingleChoiceQuestion(
    'Jaki jest cel komunikatów ICMP?',
    [
        'Zapewniają poprawne dostarczanie pakietu IP do odbiorcy',
        'Dostarczają informacji zwrotnych o transmisjach pakietów IP',
        'Monitorują proces zamiany adresów domenowych na adresy IP',
        'Informują routery o zmianach topologii sieci'
    ],
    2
)
        self.question_text_edit.setPlainText(self.current_question.content)
        self.load_answers()

    def load_answers(self):
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

    def get_answers_from_buttons(self):
        return [index for index, button in enumerate(self.answer_btns)]