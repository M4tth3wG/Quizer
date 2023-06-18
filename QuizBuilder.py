
from exceptions import EmptyListException, UnexpectedEventException

class QuizBuilder:

    def __init__(self):
        self._question_list = []
        self._actual_index = 0

    @property
    def current_index(self):
        return self._actual_index

    @property
    def current_question(self):
        if not self.is_empty():
            return self._question_list[self._actual_index]
        else:
            raise EmptyListException()
    
    @current_question.setter
    def current_question(self, question):
        if not self.is_empty():
            self._question_list[self._actual_index] = question
        elif self._actual_index == 0:
            self._question_list.append(question)
        else:
            raise UnexpectedEventException()


    def add_question(self, question):
        if not self.is_empty():
            self._actual_index += 1
        self._question_list.append(question)


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
        
    def drop_current_question(self):
        if not self.is_empty():
            self._question_list = self._question_list.pop(self._actual_index)
            if self._actual_index >= 1:
                self._actual_index -= 1
        else: 
            raise IndexError()
    




