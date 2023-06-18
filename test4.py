

from QuizBuilder import QuizBuilder
from questions import SingleChoiceQuestion

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

qb = QuizBuilder()

qb.add_question(x1)