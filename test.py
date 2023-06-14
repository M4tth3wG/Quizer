from questions import SingleChoiceQuestion, MultipleChoiceQuestion
from quiz import Quiz


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

    # print(x1.convert_to_file_form())
    # print(x2.convert_to_file_form())
    # x1.show_answers()
    # x2.show_answers()

    quiz = Quiz([x1,x2])
    quiz.prepare_quiz()

    correct_answers = [[1], [3,4]]

    print(SPLIT_LINE)
    for answer in correct_answers:
        print(quiz.get_question(), quiz.check_answer(answer))
        print(SPLIT_LINE)

    print('Score:', quiz.score)


if __name__ == '__main__':
    main()
