from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class QuestionStatistics(Base):
    __tablename__ = 'question_statistics'

    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('questions.id'),
        unique=True,
        nullable=False
    )
    total_answers: Mapped[int] = mapped_column(Integer, default=0)

    # Связи
    question: Mapped["Question"] = relationship(back_populates="statistics")
    option_stats: Mapped[list["OptionStatistics"]] = relationship(
        back_populates="question_stats",
        cascade="all, delete-orphan"
    )


class OptionStatistics(Base):
    __tablename__ = 'option_statistics'

    question_stats_id: Mapped[int] = mapped_column(
        ForeignKey('question_statistics.id'),
        nullable=False
    )
    option_id: Mapped[int] = mapped_column(
        ForeignKey('question_options.id'),
        nullable=False
    )
    answers_count: Mapped[int] = mapped_column(Integer, default=0)
    percentage: Mapped[float] = mapped_column(Float, default=0.0)

    # Связи
    question_stats: Mapped["QuestionStatistics"] = relationship(back_populates="option_stats")
