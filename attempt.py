from questions import *
from exceptions import EndQuestionException

class Attempt:


    def __init__(self):
        self._questions = []
        self._given_answers = []
        self._actual_score = 0
        self._actual_max_points = 0
        self._index = 0

    def __dict__(self):
        return {
            'questions': [question.__dict__() for question in self._questions],
            'given_answers': self._given_answers,
            'actual_score': self._actual_score,
            'actual_max_points': self._actual_max_points,
            'index': self._index
        }

    def add_question_attempt(self, question, answers):
        if len(question.get_correct_answers()) < answers:
            raise ValueError('There are more answers than there are in the question!!!')
        index = min(len(self.questions, len(self.given_answers)))
        self._questions.insert(index, question)
        self._given_answers.insert(index, answers)
        self._actual_score += question.check_answer(answers)
        self._actual_max_points += question.number_of_points

    
    def get_total_score(self):
        actual_score = 0
        for question, given_answer in zip(self._questions, self._given_answers):
            actual_score += question.check_answer(given_answer)

        self._actual_score = actual_score
        return actual_score
    
    def get_max_points(self):
        points = 0
        for question in self._questions:
            points += question._number_of_points
        return points
    
    def add_question_list(self, questions):
        self._questions = questions
        self._given_answers = []
        self._actual_score = 0
        self._index = 0

    def add_answer(self, given_answer):
        if len(self._questions) > len(self._given_answers):
            self._actual_score += self._questions[len(self._given_answers)].check_answer(given_answer)
            self._actual_max_points += self._questions[len(self._given_answers)]._number_of_points
            self._given_answers.append(given_answer)

        else:
            raise ValueError('There are more answers than there are in the question!!!')
        
    def pop_next_question(self):
        if self.is_next_question:
            self._index += 1
            return self._questions[self._index - 1]
        raise EndQuestionException("There is no more questions!!!")
    
    def peek_next_question(self):
        if self.is_next_question:
            return self._questions[self._index]
        raise EndQuestionException("There is no more questions!!!")
        
    
    def get_length_of_questions(self):
        return len(self._questions)
    
    def is_next_question(self):
        return not self._index >= len(self._questions)
    
    def is_previous_question(self):
        return self._index > 0
    
    def to_json(self):
        return json.dumps(self.__dict__(), indent=4, ensure_ascii=False)

    @staticmethod   
    def load_from_json(path):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.loads(file.read())

            questions = data['questions']
            given_answers = data['given_answers']
            actual_score = data['actual_score']
            actual_max_points = data['actual_max_points']
            index = data['index']

            if len(questions) < len(given_answers):
                raise ValueError('There are more answers than there are in the question!!!')
            if actual_score < 0 or actual_max_points < 0 or actual_score > actual_max_points:
                raise ValueError('Incorrect value of score')
            if index > min(len(questions), len(given_answers)) or index < 0:
                raise ValueError("Incorrect value of index")

            return_attempt = Attempt()

            return_attempt._questions = questions
            return_attempt._given_answers = given_answers
            return_attempt._actual_score = actual_score
            return_attempt._actual_max_points = actual_max_points
            return_attempt._index = index

            return return_attempt
        

    def save_attempt_to_json(self, path):
        try:
            with open(path, 'w+', encoding='utf-8') as file:
                file.write(self.to_json() + '\n')
            return True
        except FileNotFoundError:
            sys.err.write(f'Attempt not written to file: {path}')
            return False

        

