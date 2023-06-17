
from questions import SingleChoiceQuestion, MultipleChoiceQuestion, Question
from quiz import Quiz
from pathlib import Path
import os, json


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

# print(x1.to_json())
# print(x2.to_json())



quiz = Quiz("test23", [x1,x2], shuffle=True)

i = 1
for q in quiz.questions_bank:
    with open(f'test_json{i}.json', 'w+', encoding='utf-8') as file:
        file.write(q.to_json() + '\n')
    i += 1

with open('quiz_json.json', 'w+', encoding='utf-8') as file:
    file.write(quiz.to_json())


load_quiz = Quiz.load_from_json(r'D:\test_quiz.json')

print(load_quiz.questions_bank[1])