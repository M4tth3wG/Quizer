
from exceptions import EmptyListException, UnexpectedEventException, NoQuizArgumentsException
from quiz import Quiz

class QuizBuilder:

    def __init__(self):
        self._question_list = []
        self._actual_index = 0
        self._quiz_args = 5 * [None]

    @property
    def current_index(self):
        return self._actual_index

    @property
    def current_question(self):
        if not self.is_empty():
            return self._question_list[self._actual_index]
        else:
            return None
    
    @current_question.setter
    def current_question(self, question):
        if not self.is_empty():
            self._question_list[self._actual_index] = question
        elif self._actual_index == 0:
            self._question_list.append(question)
        else:
            raise UnexpectedEventException('Something is wrong!')


    def add_question(self, question):
        if not self.is_empty():
            if not self.current_index == 0:
                self._actual_index += 1
        self._question_list.insert(self._actual_index, question)


    def insert(self, index, question):
        if index < 0 or index > len(self._question_list):
            raise IndexError()
        self._actual_index = index
        self._question_list.insert(index, question)
        

    def has_previous(self):
        return self._actual_index > 0

    def has_next(self):
        return self._actual_index < len(self._question_list)-1

    def prev(self):
        if self.has_previous():
            self._actual_index -= 1
            return self._question_list[self._actual_index]
        else:
            raise IndexError()

    def next(self):
        if self.has_next():
            self._actual_index += 1
            return self._question_list[self._actual_index]
        else:
            raise IndexError()
        
    def is_empty(self):
        return self._question_list == []
    
    def get_length(self):
        return len(self._question_list)
        
    def drop_current_question(self):
        if not self.is_empty():
            self._question_list.pop(self._actual_index)
            if self._actual_index >= 1:
                self._actual_index -= 1
        else: 
            raise EmptyListException("Question list is empty!!!")
    
    def create_quiz(self):
        if None in self._quiz_args:
            raise NoQuizArgumentsException(f'Found: {self._quiz_args}')
        return Quiz(self._quiz_args[0], self._question_list, self._quiz_args[1], self._quiz_args[2], self._quiz_args[3], self._quiz_args[4])
    
    @property
    def quiz_args(self):
        return self._quiz_args.copy()
    
    @quiz_args.setter
    def quiz_args(self, new_args):
        if len(new_args) == 5:
            for arg, typ in zip(new_args, [str, int, int, bool, bool]):
               if type(arg) != typ:
                   raise TypeError(f'Found: {type(arg)}  Expected: {typ}')
            self._quiz_args = new_args
        else:
            raise ValueError()
    


    def save_to_quiz_to_json(self, path):
        return self.create_quiz().save_quiz_to_json(path)


    def load_quiz_from_json(self, path):
        load_quiz = Quiz.load_from_json(path)
        if load_quiz != None:
            self._current_index = 0
            self._question_list = load_quiz.questions_bank
            self._quiz_args = [load_quiz.name, load_quiz.number_of_question_repetition, load_quiz.mode, load_quiz.shuffle, load_quiz.shuffle_answers]
            return True
        else:
            return False



