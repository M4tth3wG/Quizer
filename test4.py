

from QuizBuilder import QuizBuilder
from questions import SingleChoiceQuestion, MultipleChoiceQuestion

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



qb = QuizBuilder()

qb.add_question(x1)
print(qb.current_question)
qb.drop_current_question()
print(qb.current_question)


qb.add_question(x1)
qb.add_question(x2)
print(qb.current_question)
print(qb.prev())
print(qb.current_question)
qb.drop_current_question()
print(qb.current_question)
qb.drop_current_question()
print(qb.current_question)