from abc import ABC, abstractmethod
import string

# MAIN_INDICATOR = '(a)'


class Question(ABC):

    def __init__(self, content, answers : list, number_of_points=1):
        self.content = content
        self.number_of_points = number_of_points
        self.answers : dict = self.convert_to_show_form(answers)

    def __str__(self):
        result = f'{self.content}\n'
        for answer in self.answers.values():
            result += f'\t {answer}\n'
        return result

    @abstractmethod
    def convert_to_file_form(self):
        pass

    @abstractmethod
    def check_answer(self, input_answer):
        pass

    def convert_to_show_form(self, answers):
        answers_dict = {}
        for answer, letter in zip(answers, list(string.ascii_uppercase)):
            answers_dict[letter] = f'{letter}) {answer}'

        return answers_dict
    
    def show_answers(self):
        print(self.answers)
        
    @abstractmethod
    def get_correct_answers(self):
        pass



class SingleChoiceQuestion(Question):

    def __init__(self, content, answers : list, correct_answer: int, number_of_points=1):
        super().__init__(content, answers, number_of_points)
        self.correct_answer = correct_answer


    def convert_to_file_form(self):
        result = 'SQ '

        for answer_index in range(1, len(self.answers)+1):
            if self.correct_answer == answer_index:
                result += '1' 
            else :
                result += '0'

        result += f'\n{self.content}\n'

        for index, answer in enumerate(self.answers):
            result += f'\t {index+1}. {answer}\n'

        return result
    
    def check_answer(self, input_answer):

        if len(input_answer) == 1:
            return self.number_of_points if self.correct_answer == input_answer[0] else 0
        else:
            return 0
        

    def get_correct_answers(self):
        return [self.correct_answer]

 


class MultipleChoiceQuestion(Question):

    def __init__(self, content, answers : list, correct_answers, number_of_points : int = 1):
        super().__init__(content, answers, number_of_points)
        self.correct_answers = correct_answers

    def convert_to_file_form(self):
        result = 'MQ '

        for answer_index in range(1, len(self.answers)+1):
            digit_to_concat = '0'
            for correct_answer_index in self.correct_answers:
                if correct_answer_index == answer_index:
                    digit_to_concat = '1'
                    break
            result += digit_to_concat

        result += f'\n{self.content}\n'

        for index, answer in enumerate(self.answers):
            result += f'\t {index+1}. {answer}\n'

        return result
    
    def check_answer(self, input_answers):
        if len(input_answers) > len(self.correct_answers):
            return 0
        actual_correct_answers = 0
        for correct_answer in self.correct_answers:
            if correct_answer in input_answers:
                actual_correct_answers += 1
            
        # return actual_correct_answers/max(len(self.correct_answers), len(input_answers)) * self.number_of_points
        return actual_correct_answers/len(self.correct_answers)* self.number_of_points
    
    
    def get_correct_answers(self):
        return self.correct_answers.copy()