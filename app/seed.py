"""Lädt Lektions- und Bibliotheksdaten aus JSON-Dateien in die Datenbank."""
import json
from pathlib import Path

from sqlalchemy.orm import Session

from .models import Lesson, UserProgress

DATA_DIR = Path(__file__).parent.parent / "data"

GAME_TYPES = ["gefangenendilemma", "ultimatum", "vertrauen", "verhandlung", "chicken", "public_goods", "beauty_contest", "stag_hunt", "centipede", "rps", "koordination", "auktion", "diktator", "dollarauktion", "minderheit", "habicht-taube", "geschlechter-kampf", "freiwilligen-dilemma", "gleiche-muenzen", "gewinner-fluch", "hollaendische-auktion", "englische-auktion"]


def seed_lessons(db: Session) -> None:
    """Lektionen aus lektionen.json laden – fehlende Einträge werden ergänzt."""
    with open(DATA_DIR / "lektionen.json", encoding="utf-8") as f:
        lessons = json.load(f)

    existing = {l.slug: l for l in db.query(Lesson).all()}
    changed = 0
    for item in lessons:
        sources_json = json.dumps(item["sources"], ensure_ascii=False)
        lesson = existing.get(item["slug"])
        if lesson is None:
            db.add(Lesson(
                slug=item["slug"],
                title=item["title"],
                category=item["category"],
                difficulty=item["difficulty"],
                content_md=item["content_md"],
                sources_json=sources_json,
                related_game=item.get("related_game"),
                order_index=item["order_index"],
            ))
            changed += 1
            continue
        # Re-sync source-of-truth fields from JSON so content updates reach existing DBs.
        fields = {
            "title": item["title"],
            "category": item["category"],
            "difficulty": item["difficulty"],
            "content_md": item["content_md"],
            "sources_json": sources_json,
            "related_game": item.get("related_game"),
            "order_index": item["order_index"],
        }
        for attr, value in fields.items():
            if getattr(lesson, attr) != value:
                setattr(lesson, attr, value)
                changed += 1

    if changed:
        db.commit()


def seed_progress(db: Session) -> None:
    """Initialer UserProgress-Eintrag pro Spieltyp."""
    for game_type in GAME_TYPES:
        existing = db.query(UserProgress).filter_by(game_type=game_type).first()
        if not existing:
            db.add(UserProgress(game_type=game_type))
    db.commit()
