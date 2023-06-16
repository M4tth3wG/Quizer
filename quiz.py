import os, random, json
from questions import Question
from attempt import Attempt
from itertools import repeat
from exceptions import NotPreparedQuizException, BlockedQuizException, QuizException
from database_support import load_score_to_base, create_empty_db, find_all_scores_for_quiz
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
from dataclasses import dataclass


GENTLE_MODE = 1
RELENTLESS_MODE = 0

RESULT_DATABASE_FILE = r'scores_database.db'
RESULT_DATABASE_FOLDER = r'./quiz_results'

@dataclass
class Quiz:

    def __init__(self, name, questions_bank: list[Question], number_of_question_repetition = 1, mode = GENTLE_MODE, shuffle=False):
        self.name = name
        self.questions_bank = questions_bank
        self.last_attempt = Attempt()
        self.mode = mode
        self.shuffle = shuffle
        self.is_ready = False
        self.is_blocked = True
        self.number_of_question_repetition = number_of_question_repetition

    @staticmethod
    def read_quiz_from_folder(path_to_file):
        loaded_questions = []
        ...
        return Quiz(loaded_questions)
    
    
    def save_quiz_to_file(file_name, path=r'.') :
        ...
        # file = open(f'{path}{os.sep}{name}.txt')

    def clear_question_bank(self):
        self.questions_bank = []
        self.reset_quiz()

    def reset_quiz(self):
        self.last_attempt = Attempt()
        self.is_ready = False
        self.is_blocked = True


    def clear_questions(self):
        self.last_attempt.add_question_list([])

    def add_question(self, new_question):
        self.questions_bank.append(new_question)


    def prepare_quiz(self):
        self.last_attempt.add_question_list([question for question in self.questions_bank for _ in repeat(None, self.number_of_question_repetition)])
        if self.shuffle:
            random.shuffle(self.question)
        self.is_ready, self.is_blocked = True, False


    def get_question(self):
        if self.is_blocked:
            raise BlockedQuizException('The quiz did not receive an answer to the previous question!!!')
        elif self.is_ready:
            self.is_blocked = True
            return self.last_attempt.peek_next_question()
        else:
            raise NotPreparedQuizException('Quiz has not been prepared!!!')
        

    def check_answer(self, input_answer):
        if self.is_blocked:
            # last_question: Question = self.questions.pop(0)
            last_question = self.last_attempt.pop_next_question()
            self.is_blocked = False
            if self.check_emptiness_question_list():
                 self.is_ready, self.is_blocked = False, True
            self.last_attempt.add_answer(input_answer)
            return last_question.get_correct_answers()
        else:
            raise QuizException('Question has already been answered!!!')
        
    
    def check_emptiness_question_list(self):
        return len(self.last_attempt.questions) == 0
    
    def get_score(self):
        return self.last_attempt.get_total_score()
    
    def get_max_points(self):
        return self.last_attempt.get_max_points()
    
    def save_scores(self):
        if not os.path.join(RESULT_DATABASE_FOLDER, RESULT_DATABASE_FILE):
            create_empty_db(RESULT_DATABASE_FOLDER, RESULT_DATABASE_FILE)

        load_score_to_base(self.name, self.get_score(), self.get_max_points(), f'{RESULT_DATABASE_FOLDER}{os.sep}{RESULT_DATABASE_FILE}')

    def read_scores(self):
        scored_points, max_points, dates = [],[],[]

        for score in find_all_scores_for_quiz(self.name, f'{RESULT_DATABASE_FOLDER}{os.sep}{RESULT_DATABASE_FILE}'):
            scored_points.append(score.scored_points)
            max_points.append(score.max_points)
            dates.append(score.date)

        # Tworzenie wykresu
        plt.plot(dates, scored_points, marker='o', linestyle='-', label='Punkty zdobyte')
        plt.plot(dates, max_points, marker='o', linestyle='-', label='Maksymalne punkty')
        plt.xlabel('Data')
        plt.ylabel('Liczba punktów')
        plt.title('Postęp w nauce')
        plt.legend()

        # Konfiguracja osi czasu
        date_formatter = DateFormatter('%Y-%m-%d')
        plt.gca().xaxis.set_major_formatter(date_formatter)
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(5))

        # Wyświetlanie wykresu
        plt.tight_layout()
        plt.show()

    def to_json(self):
        quiz_dict = {
            'name': self.name,
            'question_bank': [question.__dict__() for question in self.questions_bank],
            'mode': self.mode,
            'shuffle': self.shuffle,
            'isReady': False, 
            'isBlocked': True,
            'number_of_question_repetition': self.number_of_question_repetition
        }
        return json.dumps(quiz_dict, indent=4, ensure_ascii=False)