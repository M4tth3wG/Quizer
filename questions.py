from abc import ABC, abstractmethod
import string, re, os, sys, json, random
from pathlib import Path
from dataclasses import asdict, dataclass
from exceptions import  IncorrectAnswersNumberException, EmptyAnswerException, EmptyContentException


SINGLE_CHOICE_QUESTION_HEADER = 'SQ'
MULTIPLE_CHOICE_QUESTION_HEADER = 'MQ'

# 
# @dataclass
class Question(ABC):

    def __init__(self, content : str, answers : list, number_of_points : int = 1):
        if content == '':
            raise EmptyContentException()
        
        if len(answers) == 0:
            raise IncorrectAnswersNumberException()
        
        for answer in answers:
            if answer == '':
                raise EmptyAnswerException()
            
        if number_of_points <= 0:
            raise ValueError("Number of points must be positive number!!!")
        
        self._content = content
        self._number_of_points = number_of_points
        self._answers : dict = self.convert_answers_to_show_form(answers)


    def __str__(self):
        result = f'{self._content}\n'
        for answer in self._answers.values():
            result += f'\t {answer}\n'
        return result[:-1]
    
    @property
    def number_of_points(self):
        return self._number_of_points

    @number_of_points.setter
    def number_of_points(self, new_number):
        if new_number <= 0:
            raise ValueError("Number of points must be positive number!!!")
        self._number_of_points = new_number

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, new_content):
        self._content = new_content

    @property
    def answers(self):
        return self._answers
    
    @answers.setter
    def answers(self, new_answers):
        self._answers = new_answers


    @abstractmethod
    def convert_to_file_form(self):
        pass


    @abstractmethod
    def check_answer(self, input_answer):
        pass


    @abstractmethod
    def get_correct_answers(self):
        pass

    @staticmethod
    def load_from_string(question_str):
        lines = question_str.splitlines()
        if re.search(r"SQ\d+", lines[0]):
            return SingleChoiceQuestion.load_from_string(lines)
        elif re.search(r"MQ\d+", lines[0]):
            return MultipleChoiceQuestion.load_from_string(lines)
        else:
            raise ValueError("Invalid input of question string")
        
    @staticmethod
    def read_question_from_file(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                loaded_text = ''
                for line in file.readlines():
                    loaded_text += line

                return Question.load_from_string(loaded_text)
        except FileNotFoundError:
            sys.stderr.write(f'File not found (Path: {path})\n')
            return None

    def convert_answers_to_show_form(self, answers):
        answers_dict = {}
        for answer, letter in zip(answers, list(string.ascii_uppercase)):
            pattern = rf'^[{letter}]\)\s.*?$'
            if re.match(pattern, answer):
                answers_dict[letter] = answer
            else: 
                answers_dict[letter] = f'{letter}) {answer}'

        return answers_dict
    
    def show_answers(self):
        print(self._answers)
        


    def save_question_into_file(self, path, file_name):
        full_path = Path(f'{path}{os.sep}{file_name}')
        try:
            with open(full_path, 'w+', encoding='utf-8') as file:
                file.write(str(self.convert_to_file_form()) + '\n')
                return True
        except FileNotFoundError:
            sys.stderr.write(f'File not found (Path: {full_path})\n')
            return False    
        
    @staticmethod
    def read_from_dict(q_dict):
        if q_dict['type'] == 'SQ':
            return SingleChoiceQuestion.read_from_dict(q_dict)
        elif q_dict['type'] == 'MQ':
            return MultipleChoiceQuestion.read_from_dict(q_dict)
        else:
            raise ValueError("Unknown type of question!!!")
        
    @abstractmethod
    def shuffle_answers():
        pass

    
    # @staticmethod
    # def make_question(content, answers, correct_answers, number_of_points, is_SQ):
    #     Question.check_question_args(content, answers, correct_answers)
    #     if is_SQ:
    #         return SingleChoiceQuestion(content, answers, correct_answers[0], number_of_points)
    #     else:
    #         return MultipleChoiceQuestion(content, answers, correct_answers, number_of_points)









@dataclass
class SingleChoiceQuestion(Question):

    def __init__(self, content : str, answers : list, correct_answer: int, number_of_points=1):
        super().__init__(content, answers, number_of_points)
        self._correct_answer = correct_answer

    def __dict__(self):
        return {
            'type': 'SQ',
            'content': self._content,
            'answers': self._answers,
            'correct_answers': self._correct_answer,
            'number_of_points': self._number_of_points
        }


    @staticmethod
    def load_from_string(lines):
        try:
            answers_as_digits = lines[0][2:]
            loaded_correct_answer_index = -1
            for index, digit in enumerate(answers_as_digits):
                if digit == '1':
                    if loaded_correct_answer_index == -1:
                        loaded_correct_answer_index = index+1
                    else:
                        raise IncorrectAnswersNumberException('Found more than one correct answer!!!')
                    
            if loaded_correct_answer_index == -1: raise ValueError("No correct answer found")


            if re.match(r'\S', lines[1].strip()):
                loaded_content = lines[1].strip()
            else:
                raise ValueError('No question found')

            loaded_answers = []

            for line in lines[2:]:   
                if re.match(r'\S', line.strip()):
                    loaded_answers.append(line.strip())
                else:
                    break

            if len(loaded_answers) != len(answers_as_digits):
                raise IncorrectAnswersNumberException('Incompatible number of answers!!!')
            
            
            return SingleChoiceQuestion(loaded_content, loaded_answers, loaded_correct_answer_index)


        except IndexError as ex:
            print(ex)
        


    def convert_to_file_form(self):
        result = SINGLE_CHOICE_QUESTION_HEADER

        for answer_index in range(len(self._answers)):
            if self._correct_answer == answer_index:
                result += '1' 
            else :
                result += '0'

        result += f'\n{self._content}\n'

        for key in self.answers.keys():
            result += f'\t{self._answers[key][3:]}\n'

        return result
    

    def check_answer(self, input_answer):

        if len(input_answer) == 1:
            return self._number_of_points if self._correct_answer == input_answer[0] else 0
        else:
            return 0
        

    def get_correct_answers(self):
        return [self._correct_answer]
    
    
    @staticmethod
    def read_from_dict(q_dict):
        result = SingleChoiceQuestion(q_dict['content'], q_dict['answers'].values(), q_dict['correct_answers'], q_dict['number_of_points'])
        # result.answers = q_dict['answers']
        return result
    
    def to_json(self):
        return json.dumps(self.__dict__(), indent=2, ensure_ascii=False)
    
    def shuffle_answers(self):
        correct_answer = self.answers[string.ascii_uppercase[self._correct_answer]][3:]
        shuffled_answers = [answer[3:] for answer in self.answers.values()]
        random.shuffle(shuffled_answers)
        correct_answer_index = shuffled_answers.index(correct_answer)
        return SingleChoiceQuestion(self.content, shuffled_answers, correct_answer_index, self.number_of_points)

 
















@dataclass
class MultipleChoiceQuestion(Question):

    def __init__(self, content: str, answers : list, correct_answers : list[int], number_of_points : int = 1):
        super().__init__(content, answers, number_of_points)
        if len(answers) < len(correct_answers):
            raise IncorrectAnswersNumberException('Incompatible number of answers!!!')
        if len(correct_answers) < 2: 
            raise IncorrectAnswersNumberException('Not enough correct answers found')
        
        for num in correct_answers:
            if num >= len(answers):
                raise IndexError()


        self._correct_answers = correct_answers

    def __dict__(self):
        return {
            'type': 'MQ',
            "content": self._content,
            'answers': self._answers,
            "correct_answers": self._correct_answers,
            "number_of_points": self._number_of_points
        }

    @staticmethod
    def load_from_string(lines):
        try:
            answers_as_digits = lines[0][2:]
            loaded_correct_answer_indexes = []
            for index, digit in enumerate(answers_as_digits):
                if digit == '1':
                    loaded_correct_answer_indexes.append(index+1)
                    
            if len(loaded_correct_answer_indexes) < 2: raise IncorrectAnswersNumberException('Not enough correct answers found')


            if re.match(r'\S', lines[1].strip()):
                loaded_content = lines[1].strip()
            else:
                raise ValueError('No question found')

            loaded_answers = []

            for line in lines[2:]:   
                if re.match(r'\S', line.strip()):
                    loaded_answers.append(line.strip())
                else:
                    break

            if len(loaded_answers) != len(answers_as_digits):
                raise IncorrectAnswersNumberException('Incompatible number of answers!!!')
            
            
            return MultipleChoiceQuestion(loaded_content, loaded_answers, loaded_correct_answer_indexes)


        except IndexError as ex:
            print(ex)

    def convert_to_file_form(self):
        result = MULTIPLE_CHOICE_QUESTION_HEADER

        for answer_index in range(len(self._answers)):
            digit_to_concat = '0'
            for correct_answer_index in self._correct_answers:
                if correct_answer_index == answer_index:
                    digit_to_concat = '1'
                    break
            result += digit_to_concat

        result += f'\n{self._content}\n'

        for key in self._answers.keys():
            result += f'\t{self._answers[key][3:]}\n'

        return result
    
    def check_answer(self, input_answers):
        if len(input_answers) > len(self._correct_answers):
            return 0
        actual_correct_answers = 0
        for correct_answer in self._correct_answers:
            if correct_answer in input_answers:
                actual_correct_answers += 1
            
        # return actual_correct_answers/max(len(self.correct_answers), len(input_answers)) * self.number_of_points
        return actual_correct_answers/len(self._correct_answers)* self._number_of_points
    

    def get_correct_answers(self):
        return self._correct_answers.copy()

    
    def to_json(self):
        return json.dumps(self.__dict__(), indent=2, ensure_ascii=False)
    
    @staticmethod
    def read_from_dict(q_dict):
        return MultipleChoiceQuestion(q_dict['content'], q_dict['answers'].values(), q_dict['correct_answers'], q_dict['number_of_points'])
    
    def shuffle_answers(self):
        to_shuffle = []
        for index, answer in zip(range(len(self.answers.values())), self._answers.values()):
            if index in self._correct_answers:
                to_shuffle.append((index, answer[3:]))
            else:
                to_shuffle.append((-1, answer[3:]))

        random.shuffle(to_shuffle)

        correct_answers, answers = [], []
        for (old_index, answer), new_index in zip(to_shuffle, range(len(self.answers.values()))):
            if old_index != -1:
                correct_answers.append(new_index)
            answers.append(answer)
        
        return MultipleChoiceQuestion(self.content, answers, correct_answers, self.number_of_points)
    