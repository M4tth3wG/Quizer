import os, random, json, copy
from questions import Question
from attempt import Attempt
from itertools import repeat
from exceptions import NotPreparedQuizException, BlockedQuizException, QuizException, DuplicatedQuizNameException
from database_support import load_score_to_base, create_empty_db, find_all_scores_for_quiz, check_quiz_exists, check_quiz
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
from dataclasses import dataclass


DEFAULT_PATH_TO_SAVE_ATTEMPT= r'.\default_attempt.json'

GENTLE_MODE = 1
RELENTLESS_MODE = 0

RESULT_DATABASE_FILE = r'scores_database.db'
RESULT_DATABASE_FOLDER = r'./quiz_results'

@dataclass
class Quiz:

    def __init__(self, name, questions_bank: list[Question], number_of_question_repetition = 1, mode = GENTLE_MODE, shuffle=False):
        if number_of_question_repetition <= 0:
            raise ValueError("Number of question repetition must be positive number!!!")

        self._name = name
        self._questions_bank = questions_bank
        self._last_attempt = Attempt()
        self._mode = mode
        self._shuffle = shuffle
        self._is_ready = False
        self._is_blocked = True
        self._number_of_question_repetition = number_of_question_repetition

    @staticmethod
    def create_new_quiz(name, questions_bank: list[Question], number_of_question_repetition = 1, mode = GENTLE_MODE, shuffle=False):
        if check_quiz_exists(name):
            raise DuplicatedQuizNameException(f'Quiz with name: {name} has already existed!!!')
        
        return Quiz(name, questions_bank, number_of_question_repetition, mode, shuffle)


    def clear_question_bank(self):
        self._questions_bank = []
        self.reset_quiz()

    def reset_quiz(self):
        self._last_attempt = Attempt()
        self._is_ready = False
        self._is_blocked = True


    def clear_questions(self):
        self._last_attempt.add_question_list([])

    def add_question(self, new_question):
        self._questions_bank.append(new_question)


    def prepare_quiz(self):
        self._last_attempt.add_question_list([question for question in self._questions_bank for _ in repeat(None, self._number_of_question_repetition)])
        if self.shuffle:
            random.shuffle(self._last_attempt._questions)
        self._is_ready, self._is_blocked = True, False


    def get_question(self):
        if self._is_blocked:
            raise BlockedQuizException('The quiz did not receive an answer to the previous question!!!')
        elif self._is_ready:
            self._is_blocked = True
            return self._last_attempt.peek_next_question()
        else:
            raise NotPreparedQuizException('Quiz has not been prepared!!!')
        

    def check_answer(self, input_answer):
        if self._is_blocked:
            # last_question: Question = self.questions.pop(0)
            last_question = self._last_attempt.pop_next_question()
            self._is_blocked = False
            if self.check_emptiness_question_list():
                 self._is_ready, self._is_blocked = False, True
            self._last_attempt.add_answer(input_answer)
            return last_question.get_correct_answers()
        else:
            raise QuizException('Question has already been answered!!!')
        
    
    def check_emptiness_question_list(self):
        return len(self._last_attempt._questions) == 0

    
    @property
    def number_of_question_repetition(self):
        return self._number_of_question_repetition
    
    @number_of_question_repetition.setter
    def number_of_question_repetition(self, new_number):
        if new_number <= 0:
            raise ValueError("Number of question repetition must be positive number!!!")
        self._number_of_question_repetition = new_number

    @property
    def shuffle(self):
        return self._shuffle
    
    @shuffle.setter
    def shuffle(self, new_shuffle):
        self._shuffle = new_shuffle

    @property
    def questions_bank(self):
        return copy.copy(self._questions_bank)
    
    def get_score(self):
        return self._last_attempt._actual_score
    
    def get_actual_max_points(self):
        return self._last_attempt._actual_max_points
    
    def get_actual_index(self):
        return self._last_attempt._index
    
    def get_number_of_question(self):
        return self._last_attempt.get_length_of_questions()
    
    def get_total_max_points(self):
        return self._last_attempt.get_max_points()
    
    def save_scores(self):
        if not os.path.join(RESULT_DATABASE_FOLDER, RESULT_DATABASE_FILE):
            create_empty_db(RESULT_DATABASE_FOLDER, RESULT_DATABASE_FILE)

        load_score_to_base(self._name, self.get_score(), self.get_total_max_points(), f'{RESULT_DATABASE_FOLDER}{os.sep}{RESULT_DATABASE_FILE}')

    def read_scores(self):
        scored_points, max_points, dates = [],[],[]

        for score in find_all_scores_for_quiz(self._name, f'{RESULT_DATABASE_FOLDER}{os.sep}{RESULT_DATABASE_FILE}'):
            scored_points.append(score.scored_points)
            max_points.append(score.max_points)
            dates.append(score.date)

        plt.plot(dates, scored_points, marker='o', linestyle='-', label='Punkty zdobyte')
        plt.plot(dates, max_points, marker='o', linestyle='-', label='Maksymalne punkty')
        plt.xlabel('Data')
        plt.ylabel('Liczba punktów')
        plt.title('Postęp w nauce')
        plt.legend()

        date_formatter = DateFormatter('%Y-%m-%d')
        plt.gca().xaxis.set_major_formatter(date_formatter)
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(5))

        plt.tight_layout()
        plt.show()

    @staticmethod   
    def load_from_json(path):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.loads(file.read())

            name = data['name']
            questions_bank = [Question.read_from_dict(q_dict) for q_dict in data['question_bank']]
            mode = data['mode']
            shuffle = data['shuffle']
            isReady = data['isReady'] 
            isBlocked = data ['isBlocked']
            number_of_question_repetition = data['number_of_question_repetition']

            return_quiz = Quiz(name, questions_bank, mode, shuffle, number_of_question_repetition)
            return_quiz.is_ready = isReady
            return_quiz.is_blocked = isBlocked

            return return_quiz
        

        

    def load_attempt_from_json(self, path, path_to_save_current_attempt=DEFAULT_PATH_TO_SAVE_ATTEMPT):
        self.save_attempt_to_json(path_to_save_current_attempt)
        self._last_attempt = Attempt.load_from_json(path)



    def to_json(self):
        quiz_dict = {
            'name': self._name,
            'question_bank': [question.__dict__() for question in self._questions_bank],
            'mode': self._mode,
            'shuffle': self._shuffle,
            'isReady': False, 
            'isBlocked': True,
            'number_of_question_repetition': self._number_of_question_repetition
        }
        return json.dumps(quiz_dict, indent=4, ensure_ascii=False)