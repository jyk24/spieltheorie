from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_type: Mapped[str] = mapped_column(String(50), nullable=False)
    ai_strategy: Mapped[str] = mapped_column(String(50), nullable=False)
    moves_json: Mapped[str] = mapped_column(Text, default="[]")
    result: Mapped[str | None] = mapped_column(String(20), nullable=True)  # "win", "loss", "draw"
    score: Mapped[int] = mapped_column(Integer, default=0)
    ai_score: Mapped[int] = mapped_column(Integer, default=0)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    scenario: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), default="mittel")
    content_md: Mapped[str] = mapped_column(Text, nullable=False)
    sources_json: Mapped[str] = mapped_column(Text, default="[]")
    related_game: Mapped[str | None] = mapped_column(String(50), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_type: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, default=0)
    total_score: Mapped[int] = mapped_column(Integer, default=0)
    best_score: Mapped[int] = mapped_column(Integer, default=0)
    lessons_viewed_json: Mapped[str] = mapped_column(Text, default="[]")
    last_played: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    unlocked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class GedaechtnisScore(Base):
    __tablename__ = "gedaechtnis_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    player_name: Mapped[str] = mapped_column(String(50), default="Anonym")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
