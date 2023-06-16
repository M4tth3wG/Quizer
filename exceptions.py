


class NotPreparedQuizException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"NotPreparedQuizException: {self.message}"
    

class BlockedQuizException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'BlockedQuizException: {self.message}'
    

class QuizException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'BlockedQuizException: {self.message}'
    

class EndQuestionException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'EndQuestionException: {self.message}'
    

class IncorrectAnswersNumberException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'IncorrectAnswersNumberException: {self.message}'
    

