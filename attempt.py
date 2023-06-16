from questions import *

class Attempt:


    def __init__(self):
        self.questions = []
        self.given_answers = []
        self.score = 0
        self.index = 0

    def add_question_attempt(self, question, answers):
        if len(question.get_correct_answers()) < answers:
            raise ValueError('There are more answers than there are in the question!!!')
        index = min(len(self.questions, len(self.given_answers)))
        self.questions.insert(index, question)
        self.given_answers.insert(index, answers)
        self.score += question.check_answer(answers)

    def get_total_score(self):
        score = 0
        for question, given_answer in zip(self.questions, self.given_answers):
            score += question.check_answer(given_answer)

        self.score = score
        return score
    
    def get_max_points(self):
        points = 0
        for question in self.questions:
            points += question.number_of_points
        return points
    
    def add_question_list(self, questions):
        self.questions = questions
        self.given_answers = []
        self.score = 0
        self.index = 0

    def add_answer(self, given_answer):
        print(len(self.questions))
        if len(self.questions) > len(self.given_answers):
            self.score += self.questions[len(self.given_answers)].check_answer(given_answer)
            self.given_answers.append(given_answer)

        else:
            raise ValueError('There are more answers than there are in the question!!!')
        
    def pop_next_question(self):
        self.index += 1
        return self.questions[self.index - 1]
    
    def peek_next_question(self):
        return self.questions[self.index]

