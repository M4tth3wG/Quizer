from sqlalchemy import String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Score(Base):

    __tablename__ = 'scores'

    id: Mapped[int] = mapped_column(primary_key=True)
    scored_points: Mapped[float] = mapped_column(Float())
    max_points: Mapped[float] = mapped_column(Float())
    date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))

    quiz: Mapped["QuizDB"] = relationship(back_populates='score', foreign_keys=[quiz_id])

    def __init__(self, scored_points, max_points, quiz):
        self.scored_points=scored_points
        self.max_points=max_points
        self.quiz=quiz

    def __repr__(self) -> str:
        return f'Score(scored_points={self.scored_points}, max_points={self.max_points}, date={self.date})' 




class QuizDB(Base):

    __tablename__ = 'quizzes'

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_name: Mapped[str] = mapped_column(String(100), unique=True)

    score: Mapped[List["Score"]] = relationship(back_populates='quiz', foreign_keys="Score.quiz_id")



