from QuizBuilder import QuizBuilder
from questions import SingleChoiceQuestion, MultipleChoiceQuestion



qb = QuizBuilder()

q1 = SingleChoiceQuestion("Czy to jest kot?", ['Tak', 'Nie'], 1, 1)
q2 = SingleChoiceQuestion("Wybierz liczbę pierwszą", ['1', '2', '3'], 2, 1)
q3 = SingleChoiceQuestion("Wybierz liczbę parzystą", ['1', '2', '3'], 1, 1)

print(qb.current_index)
qb.current_question = q1
print(qb.current_index)
print(qb.current_question)
qb.add_question(q2)
print(qb.current_index)
print(qb.current_question)
print(qb.has_previous())
print(qb.has_next())
print(qb.prev())
print(qb.has_previous())
print(qb.has_next())
print(qb.next())
print(qb.has_previous())
print(qb.has_next())
qb.add_question(q3)
print(qb.current_index)
print(qb.current_question)
print(qb.has_previous())
print(qb.has_next())
print(qb.prev())
print(qb.has_previous())
print(qb.has_next())
print(qb.current_index)
print(qb.current_question)
qb.drop_current_question()
print(qb.current_index)
print(qb.current_question)
qb.drop_current_question()
print(qb.current_index)
print(qb.current_question)
qb.drop_current_question()
# print(qb.current_index)
# print(qb.current_question)



print(q1.answers)
print(q1.get_plain_answers())
