from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    subscription_tier: Mapped[str] = mapped_column(String(20), default="free")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
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
    __table_args__ = (
        UniqueConstraint("game_type", "user_id", name="uq_progress_game_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    game_type: Mapped[str] = mapped_column(String(50), nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, default=0)
    total_score: Mapped[int] = mapped_column(Integer, default=0)
    best_score: Mapped[int] = mapped_column(Integer, default=0)
    lessons_viewed_json: Mapped[str] = mapped_column(Text, default="[]")
    last_played: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class UserAchievement(Base):
    __tablename__ = "user_achievements"
    __table_args__ = (
        UniqueConstraint("slug", "user_id", name="uq_achievement_slug_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    slug: Mapped[str] = mapped_column(String(50), nullable=False)
    unlocked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class GedaechtnisScore(Base):
    __tablename__ = "gedaechtnis_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    game_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    player_name: Mapped[str] = mapped_column(String(50), default="Anonym")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
