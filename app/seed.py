"""Lädt Lektions- und Bibliotheksdaten aus JSON-Dateien in die Datenbank."""
import json
from pathlib import Path

from sqlalchemy.orm import Session

from .models import Lesson, UserProgress

DATA_DIR = Path(__file__).parent.parent / "data"

GAME_TYPES = ["gefangenendilemma", "ultimatum", "vertrauen", "verhandlung", "chicken", "public_goods", "beauty_contest", "stag_hunt", "centipede", "rps", "koordination", "auktion", "diktator", "dollarauktion", "minderheit", "habicht-taube", "geschlechter-kampf", "freiwilligen-dilemma", "gleiche-muenzen", "gewinner-fluch", "hollaendische-auktion", "englische-auktion"]


def seed_lessons(db: Session) -> None:
    """Lektionen aus lektionen.json laden – fehlende Einträge werden ergänzt.
    Für bereits vorhandene Lektionen wird `related_game` mit der JSON abgeglichen,
    damit URL-Kürzel wie ``stag_hunt``→``stag-hunt`` auch nach dem ersten Seed noch
    korrigiert werden können."""
    with open(DATA_DIR / "lektionen.json", encoding="utf-8") as f:
        lessons = json.load(f)

    existing = {l.slug: l for l in db.query(Lesson).all()}
    added = 0
    updated = 0
    for item in lessons:
        current = existing.get(item["slug"])
        if current is None:
            lesson = Lesson(
                slug=item["slug"],
                title=item["title"],
                category=item["category"],
                difficulty=item["difficulty"],
                content_md=item["content_md"],
                sources_json=json.dumps(item["sources"], ensure_ascii=False),
                related_game=item.get("related_game"),
                order_index=item["order_index"],
            )
            db.add(lesson)
            added += 1
        else:
            new_related = item.get("related_game")
            if current.related_game != new_related:
                current.related_game = new_related
                updated += 1

    if added or updated:
        db.commit()


def seed_progress(db: Session) -> None:
    """Initialer UserProgress-Eintrag pro Spieltyp."""
    for game_type in GAME_TYPES:
        existing = db.query(UserProgress).filter_by(game_type=game_type).first()
        if not existing:
            db.add(UserProgress(game_type=game_type))
    db.commit()
