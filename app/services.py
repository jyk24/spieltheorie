"""Service-Funktionen: Fortschritts-Updates, Score-Berechnung, Statistiken."""
import json
from datetime import datetime

from sqlalchemy.orm import Session

from .models import GameSession, Lesson, UserProgress
from .achievements import check_achievements


def save_game_session(
    db: Session,
    game_type: str,
    ai_strategy: str,
    moves: list[dict],
    result: str,
    score: int,
    ai_score: int,
    scenario: str | None = None,
) -> tuple[GameSession, list[dict]]:
    session = GameSession(
        game_type=game_type,
        ai_strategy=ai_strategy,
        moves_json=json.dumps(moves, ensure_ascii=False),
        result=result,
        score=score,
        ai_score=ai_score,
        scenario=scenario,
        created_at=datetime.utcnow(),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    _update_progress(db, game_type, score)
    new_achievements = check_achievements(db, game_type, moves, result, score, ai_score)
    return session, new_achievements


def _update_progress(db: Session, game_type: str, score: int) -> None:
    prog = db.query(UserProgress).filter_by(game_type=game_type).first()
    if not prog:
        prog = UserProgress(game_type=game_type)
        db.add(prog)
    prog.games_played += 1
    prog.total_score += score
    if score > prog.best_score:
        prog.best_score = score
    prog.last_played = datetime.utcnow()
    db.commit()


def mark_lesson_viewed(db: Session, slug: str) -> None:
    """Markiert eine Lektion als gelesen (in allen Progress-Einträgen)."""
    progs = db.query(UserProgress).all()
    for prog in progs:
        viewed = json.loads(prog.lessons_viewed_json or "[]")
        if slug not in viewed:
            viewed.append(slug)
            prog.lessons_viewed_json = json.dumps(viewed)
    db.commit()


def get_all_progress(db: Session) -> dict:
    """Gibt Gesamtstatistiken zurück."""
    progs = db.query(UserProgress).all()
    total_games = sum(p.games_played for p in progs)
    total_score = sum(p.total_score for p in progs)

    # Gelernte Lektionen (unique slugs über alle Progress-Einträge)
    viewed_slugs: set[str] = set()
    for p in progs:
        viewed_slugs.update(json.loads(p.lessons_viewed_json or "[]"))

    total_lessons = db.query(Lesson).count()
    recent_sessions = (
        db.query(GameSession)
        .order_by(GameSession.created_at.desc())
        .limit(5)
        .all()
    )

    per_game = {
        p.game_type: {
            "games_played": p.games_played,
            "total_score": p.total_score,
            "best_score": p.best_score,
            "last_played": p.last_played,
        }
        for p in progs
    }

    return {
        "total_games": total_games,
        "total_score": total_score,
        "lessons_viewed": len(viewed_slugs),
        "total_lessons": total_lessons,
        "per_game": per_game,
        "recent_sessions": recent_sessions,
    }


def get_game_history(db: Session, game_type: str, limit: int = 10) -> list[GameSession]:
    return (
        db.query(GameSession)
        .filter_by(game_type=game_type)
        .order_by(GameSession.created_at.desc())
        .limit(limit)
        .all()
    )
