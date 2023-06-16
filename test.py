from questions import SingleChoiceQuestion, MultipleChoiceQuestion, Question
from quiz import Quiz
from pathlib import Path
import os


SPLIT_LINE = '---------------------------'

def main():

    x1 = SingleChoiceQuestion(
        'Jaki jest cel komunikatów ICMP?',
        [
            'Zapewniają poprawne dostarczanie pakietu IP do odbiorcy',
            'Dostarczają informacji zwrotnych o transmisjach pakietów IP',
            'Monitorują proces zamiany adresów domenowych na adresy IP',
            'Informują routery o zmianach topologii sieci'
        ],
        2
    )

    x2 = MultipleChoiceQuestion(
       'Określ dwa powody, dla których administrator powinien podzielić większą sieć na podsieci.',
       [
           	'W celu uproszczenia topologii sieci',
	        'W celu redukcji liczby potrzebnych routerów',
	        'W celu ułatwienia wdrażania polityki bezpieczeństwa w przedsiębiorstwie',  
        	'W celu poprawy wydajności sieci',
	        'W celu redukcji liczby potrzebnych przełączników'
       ],
       [3,4]
    )

    x3 = Question.load_from_string(
        """SQ0100
           Jaki jest cel komunikatów ICMP
            Zapewniają poprawne dostarczanie pakietu IP do odbiorcy
            Dostarczają informacji zwrotnych o transmisjach pakietów IP
            Monitorują proces zamiany adresów domenowych na adresy IP
            Informują routery o zmianach topologii sieci
        """
    )

    x4 = Question.load_from_string(
        """MQ00110
           Określ dwa powody, dla których administrator powinien podzielić większą sieć na podsieci
	        W celu uproszczenia topologii sieci
	        W celu redukcji liczby potrzebnych routerów
	        W celu ułatwienia wdrażania polityki bezpieczeństwa w przedsiębiorstwie
	        W celu poprawy wydajności sieci
	        W celu redukcji liczby potrzebnych przełączników
        """
    )


    print(x1.convert_to_file_form())
    print(x2.convert_to_file_form())
    print(x3)
    print(x4)

    # x1.show_answers()
    # x2.show_answers()
    # x3.show_answers()
    # x4.show_answers()

    quiz = Quiz('my_first_quiz', [x1,x2,x3,x4])
    quiz.prepare_quiz()

    correct_answers = [[2], [1,2,3], [2], [3,4]]

    print(SPLIT_LINE)
    for answer in correct_answers:
        print(quiz.get_question()) 
        print(quiz.check_answer(answer))
        print(SPLIT_LINE)

    print('Score:', quiz.get_score())

    print(x3.answers)
    print(x3.save_question_into_file(Path(f'./questions_txt'), 'test001.txt'))
    print(x4.save_question_into_file(Path(f'./questions_txt'), 'test002.txt'))
    print(x4.save_question_into_file(Path(f'./questions2_txt'), 'test002.txt'))

    print(Question.read_question_from_file(Path(r'C:\Users\trine\OneDrive\Pulpit\Quizer\questions_txt\test001.txt')))
    print(Question.read_question_from_file(Path(r'C:\Users\trine\OneDrive\Pulpit\Quizer\questions_txt\test002.txt')))

    quiz.save_scores()
    quiz.read_scores()


    quiz2 = Quiz('my_second_quiz', [x1,x2,x3,x4])
    quiz2.save_scores()
    # quiz2.read_scores()







if __name__ == '__main__':
    main()
