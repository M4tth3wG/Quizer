
from sqlalchemy import create_engine
from database import Base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import sys, os
from database import QuizDB, Score
from datetime import datetime, date


ALL_QUIZZES_FILE_PATH = r'quizzes\all_quizes.txt'

def create_empty_db(path, db_name):

    engine = create_engine(f'sqlite:///{path}{os.sep}{db_name}')
    Base.metadata.create_all(bind=engine)


def check_quiz(input_quiz_name, session) -> QuizDB:
    quiz = session.query(QuizDB).filter_by(quiz_name=input_quiz_name).first()
    if not quiz:
        quiz = QuizDB(quiz_name=input_quiz_name)
        session.add(quiz)
        session.commit()

    try:
        with open(ALL_QUIZZES_FILE_PATH, "r+", encoding='utf-8') as file:
                lines = file.readlines()
                found = any(input_quiz_name in line for line in lines)

                if not found:
                    file.write(input_quiz_name + '\n')
    except FileNotFoundError:
        sys.stderr.write(f'File not found (Path: {ALL_QUIZZES_FILE_PATH})\n')
    return quiz




def load_score_to_base(quiz_name, input_scored_points, input_max_points, db_path):
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)


    with Session(engine, autoflush=False) as session:
                  
        try:
            quiz = check_quiz(quiz_name, session)
            new_score = Score(
                                scored_points=input_scored_points,
                                max_points=input_max_points,
                                quiz=quiz
                            )
            session.add(new_score)
            session.commit()
        except IntegrityError:
            sys.stderr(f'This object has already existed in database: {new_score}')
        except Exception:
            raise
        session.commit()

def find_all_scores_for_quiz(quiz_name, db_path):
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)

    with Session(engine, autoflush=False) as session:
        return session.query(Score).join(Score.quiz).filter(QuizDB.quiz_name == quiz_name).all()
