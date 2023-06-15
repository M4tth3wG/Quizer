import os, random
from questions import Question
from attempt import Attempt
from itertools import repeat
from exceptions import NotPreparedQuizException, BlockedQuizException, QuizException


GENTLE_MODE = 1
RELENTLESS_MODE = 0


class Quiz:

    def __init__(self, questions_bank: list[Question], number_of_question_repetition = 1, mode = GENTLE_MODE, shuffle=False):
        self.questions_bank = questions_bank
        self.last_attempt = Attempt()
        self.mode = mode
        self.shuffle = shuffle
        self.is_ready = False
        self.is_blocked = True
        self.number_of_question_repetition = number_of_question_repetition

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


    def save_quiz_to_file(name, path=r'.') :
        ...
        # file = open(f'{path}{os.sep}{name}.txt')


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
        


    @staticmethod
    def read_quiz_from_folder(path_to_file):
        loaded_questions = []
        ...
        return Quiz(loaded_questions)
    
    def check_emptiness_question_list(self):
        return len(self.last_attempt.questions) == 0
    
    def get_score(self):
        return self.last_attempt.get_total_score()