from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path
from quiz import Quiz
import quiz
import questions
from functools import partial
import exceptions
from path_constants import GUI_RESOURCES, DEFAULT_DIRECTORY
from PyQt6.QtGui import QFont
from QuizBuilder import QuizBuilder
import os
from pathlib import Path


class QuizCreatorWindow(QMainWindow):
    
    def __init__(self, main_window, quiz_path = None):
        super(QuizCreatorWindow, self).__init__()
        uic.loadUi(Path(GUI_RESOURCES).joinpath('quiz_creator_gui.ui'), self)

        self.quiz_builder = QuizBuilder()
        self.answer_layouts_list = []
        self.main_window = main_window

        self.setFixedWidth(814)
        self.setFixedHeight(600)

        self.quit_btn.clicked.connect(self.show_quit_confirmation_dialog)
        self.add_answer_btn.clicked.connect(self.create_answer_input)
        self.multiple_answer_question_check_box.stateChanged.connect(self.update_correct_answers_check_boxes)
        self.previous_question_btn.clicked.connect(self.load_previous_question)
        self.next_question_btn.clicked.connect(self.load_next_question)
        self.edit_question_btn.clicked.connect(self.edit_current_question)
        self.save_question_btn.clicked.connect(self.save_current_question)
        self.add_question_btn.clicked.connect(self.add_new_question)
        self.save_quiz_btn.clicked.connect(self.save_quiz)
        self.select_quiz_parameters_btn.clicked.connect(self.select_quiz_parameters)
        self.back_to_creator_btn.clicked.connect(self.go_back_to_creator)
        self.delete_question_btn.clicked.connect(self.delete_current_question)

        self.stackedWidget.setCurrentIndex(0)

        if quiz_path != None:
            self.quiz_builder.load_quiz_from_json(quiz_path)
            self.current_question_exists = True
        else:
            self.current_question_exists = False

        self.load_current_question()

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
        
        for i in range(answer_layout.count()):
            widget = answer_layout.itemAt(i).widget()
            widget.deleteLater()

        answer_layout.deleteLater()
        self.relock_correct_answers_check_boxes()

    def lock_all_answers(self):
        for layout in self.answer_layouts_list:
            for i in range(layout.count()):
                layout.itemAt(i).widget().setEnabled(False)

    def unlock_all_answers(self):
        for layout in self.answer_layouts_list:
            for i in range(layout.count()):
                layout.itemAt(i).widget().setEnabled(True)

    def clear_all_answers(self):
        while len(self.answer_layouts_list) != 0:
            self.delete_answer(self.answer_layouts_list[0])

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

    def update_browsing_buttons(self):
        self.next_question_btn.setEnabled(self.quiz_builder.has_next())
        self.previous_question_btn.setEnabled(self.quiz_builder.has_previous())

    def load_question(self, question):
        self.clear_loaded_question_view()
        self.current_question_exists = True
        
        self.question_text_edit.setPlainText(question.content)
        self.multiple_answer_question_check_box.setChecked(isinstance(question, questions.MultipleChoiceQuestion))
        self.quiz_question_number_label.setText(f'{self.quiz_builder.current_index + 1}/{self.quiz_builder.get_length()}')

        for answer in question.get_plain_answers().values():
            answer_layout = self.create_answer_input()
            answer_layout.itemAt(1).widget().setText(answer)

        for correct_answer in question.get_correct_answers():
            self.answer_layouts_list[correct_answer].itemAt(0).widget().setChecked(True)

        self.lock_question()

    def load_current_question(self):
        if self.quiz_builder.current_question != None:
            self.load_question(self.quiz_builder.current_question)
        else:
            self.load_new_question_view()

    def load_previous_question(self):
        self.load_question(self.quiz_builder.prev())

    def load_next_question(self):
        self.load_question(self.quiz_builder.next())

    def edit_current_question(self):
        self.unlock_question()

    def delete_current_question(self):
        
        if self.current_question_exists:
            self.quiz_builder.drop_current_question()

        if self.quiz_builder.current_question != None:
            self.load_question(self.quiz_builder.current_question)
        else:
            self.load_new_question_view()

    def load_new_question_view(self):
        self.unlock_question()
        self.clear_loaded_question_view()
        self.current_question_exists = False
        
        if not self.quiz_builder.is_empty():
            self.quiz_question_number_label.setText(f'{self.quiz_builder.current_index + 2}/{self.quiz_builder.get_length() + 1}')
        else:
            self.quiz_question_number_label.setText('1/1')

    def save_current_question(self):
        content = self.question_text_edit.toPlainText()
        answers = [layout.itemAt(1).widget().text() for layout in self.answer_layouts_list]
        correct_answers = [index for index, layout in enumerate(self.answer_layouts_list) if layout.itemAt(0).widget().isChecked()]
        number_of_points = self.number_of_points_line_edit.text()
        
        try:
            if self.multiple_answer_question_check_box.isChecked():
                question = questions.MultipleChoiceQuestion(content, answers, correct_answers, number_of_points=int(number_of_points))
            else:
                question = questions.SingleChoiceQuestion(content, answers, correct_answers[0], number_of_points=int(number_of_points))
        except:
            self.main_window.show_error_message('Niepoprawne parametry pytania!')
            return
        
        if self.current_question_exists:
            self.quiz_builder.drop_current_question()
        elif self.quiz_builder.current_index == 0 and not self.quiz_builder.is_empty():
            self.quiz_builder.insert(1, question)
            self.lock_question()
            return

        self.quiz_builder.add_question(question)
        self.lock_question()

    def add_new_question(self):
        self.load_new_question_view()

    def save_quiz(self):
        default_directory = str(DEFAULT_DIRECTORY)
        file_filter = "JSON files (*.json)"
        file_path = QFileDialog.getSaveFileName(self, 'Zapisz quiz', directory=default_directory, filter=file_filter)[0]

        if file_path == '':
            return

        try:
            name = self.quiz_name_edit.text()
            number_of_question_repetition = int(self.quiz_number_of_question_repetition_line_edit.text())
            mode = quiz.RELENTLESS_MODE if self.quiz_restrictive_mode_check_box.isChecked() else quiz.GENTLE_MODE
            shuffle = self.quiz_shuffle_check_box.isChecked()
            shuffle_answers = self.quiz_answers_shuffle_check_box.isChecked()

            self.quiz_builder.quiz_args = [name, number_of_question_repetition, mode, shuffle, shuffle_answers]

            self.quiz_builder.save_to_quiz_to_json(file_path)
        except:
            self.main_window.show_error_message('Nieprawidłowe parametry quizu!')
        
    def lock_question(self):
        self.save_question_btn.setEnabled(False)
        self.edit_question_btn.setEnabled(True)
        self.add_question_btn.setEnabled(True)
        self.select_quiz_parameters_btn.setEnabled(True)
        self.update_browsing_buttons()

        self.question_text_edit.setReadOnly(True)
        self.multiple_answer_question_check_box.setEnabled(False)
        self.add_answer_btn.setEnabled(False)
        self.number_of_points_line_edit.setReadOnly(True)
        self.lock_all_answers()

    def unlock_question(self):
        self.save_question_btn.setEnabled(True)
        self.edit_question_btn.setEnabled(False)
        self.add_question_btn.setEnabled(False)
        self.select_quiz_parameters_btn.setEnabled(False)
        self.previous_question_btn.setEnabled(False)
        self.next_question_btn.setEnabled(False)

        self.question_text_edit.setReadOnly(False)
        self.multiple_answer_question_check_box.setEnabled(True)
        self.add_answer_btn.setEnabled(True)
        self.number_of_points_line_edit.setReadOnly(False)
        self.unlock_all_answers()

    def clear_loaded_question_view(self):
        self.question_text_edit.setPlainText('')
        self.multiple_answer_question_check_box.setChecked(False)
        self.number_of_points_line_edit.setText('1')
        self.clear_all_answers()


    def show_quit_confirmation_dialog(self):
        message = 'Spowoduje to wyjście do menu głównego. Wszystkie niezapisane postępy zostaną utracone. Czy chcesz kontynuować?'
        icon=QMessageBox.Icon.Warning
        title='Uwaga'

        cancel_button = QPushButton(text='Anuluj')
        ok_button = QPushButton(text='OK')

        dialog = QMessageBox(parent=self)
        dialog.addButton(cancel_button, QMessageBox.ButtonRole.RejectRole)
        dialog.addButton(ok_button, QMessageBox.ButtonRole.AcceptRole)
        dialog.setIcon(icon)
        dialog.setWindowTitle(title)
        dialog.setText(message)

        ok_button.clicked.connect(self.close)
        ok_button.clicked.connect(self.main_window.show)
        ok_button.clicked.connect(dialog.close)
        cancel_button.clicked.connect(dialog.close)

        dialog.exec()

    def select_quiz_parameters(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_back_to_creator(self):
        self.stackedWidget.setCurrentIndex(0)


    
        

    