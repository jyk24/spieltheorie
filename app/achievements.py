"""Achievements – Definitionen und Check-Logik."""
from __future__ import annotations

from collections import Counter
from datetime import datetime

from sqlalchemy.orm import Session

from .models import UserAchievement, UserProgress

# Spiegelwert aus game_engine (vermeidet zirkulären Import)
_DOLLAR_PRIZE = 100

ACHIEVEMENTS: list[dict] = [
    # ── Einstieg ──────────────────────────────────────────────────────────────
    {"slug": "erster_schritt",    "icon": "👣",  "title": "Erster Schritt",      "desc": "Dein erstes Spiel gespielt"},
    {"slug": "neugierig",         "icon": "🔍",  "title": "Neugierig",            "desc": "5 verschiedene Spiele ausprobiert"},
    {"slug": "entdecker",         "icon": "🗺️",  "title": "Entdecker",            "desc": "Alle 15 Spiele mindestens einmal gespielt"},
    # ── Lernpfad ──────────────────────────────────────────────────────────────
    {"slug": "level1",            "icon": "⭐",   "title": "Grundlagen",          "desc": "Level 1 abgeschlossen: Gefangenendilemma, Ultimatum, Vertrauen"},
    {"slug": "level2",            "icon": "⭐⭐",  "title": "Konflikt-Kenner",     "desc": "Level 2 abgeschlossen: Chicken, Hirschjagd, Koordination, RPS"},
    {"slug": "pfad_meister",      "icon": "🏆",  "title": "Pfad-Meister",         "desc": "Alle 5 Levelstufen des Lernpfads abgeschlossen"},
    # ── Verhalten ─────────────────────────────────────────────────────────────
    {"slug": "kooperator",        "icon": "🤝",  "title": "Kooperator",           "desc": "Gefangenendilemma: ≥ 80 % Kooperation in einer Partie"},
    {"slug": "vertrauensperson",  "icon": "💎",  "title": "Vertrauensperson",     "desc": "Vertrauensspiel: Geld investiert und netto gewonnen"},
    {"slug": "optimaler_bieter",  "icon": "🎯",  "title": "Optimaler Bieter",     "desc": "Vickrey-Auktion: In 3+ Runden den wahren Wert geboten"},
    {"slug": "schoenheitskoenig", "icon": "👑",  "title": "Schönheitskönig",      "desc": "Schönheitswettbewerb: 4 von 6 Runden gewonnen"},
    {"slug": "unbestechlich",     "icon": "🐛",  "title": "Unbestechlich",        "desc": "Centipede: Bis Knoten 5 oder weiter gewartet"},
    {"slug": "top_negotiator",    "icon": "💼",  "title": "Top-Verhandler",       "desc": "Verhandlung: Sehr gutes Ergebnis erzielt (Score ≥ 80/100)"},
    {"slug": "fair_dealer",       "icon": "⚖️",  "title": "Faire Einigung",       "desc": "Ultimatum: ≥ 60 % Effizienz (Score ≥ 300 von 500)"},
    {"slug": "antiherding",       "icon": "🔢",  "title": "Gegen den Strom",      "desc": "Minderheitsspiel: 6 von 8 Runden in der Minderheit"},
    {"slug": "kein_sunk_cost",    "icon": "🚪",  "title": "Sunk-Cost-Frei",       "desc": "Dollarauktion: Aufgegeben bevor der Verlust den Preiswert übersteigt"},
    {"slug": "diktator_fair",     "icon": "🌟",  "title": "Gerechter Herrscher",  "desc": "Diktatorspiel: Als Diktator im Schnitt ≥ 40 % abgegeben"},
    {"slug": "nash_spieler",      "icon": "🧮",  "title": "Nash-Spieler",         "desc": "Schere-Stein-Papier: Keine dominante Strategie (jeder Zug < 60 %)"},
]

ACHIEVEMENT_BY_SLUG: dict[str, dict] = {a["slug"]: a for a in ACHIEVEMENTS}


def check_achievements(
    db: Session,
    game_type: str,
    moves: list[dict],
    result: str,
    score: int,
    ai_score: int,
) -> list[dict]:
    """Prüft alle Achievements und gibt neu freigeschaltete zurück."""
    already = {a.slug for a in db.query(UserAchievement).all()}
    all_progress: dict[str, int] = {
        p.game_type: p.games_played for p in db.query(UserProgress).all()
    }

    newly: list[dict] = []
    for ach in ACHIEVEMENTS:
        slug = ach["slug"]
        if slug in already:
            continue
        if _check_condition(slug, game_type, moves, result, score, ai_score, all_progress):
            db.add(UserAchievement(slug=slug, unlocked_at=datetime.utcnow()))
            newly.append(ach)

    if newly:
        db.commit()
    return newly


def _check_condition(
    slug: str,
    game_type: str,
    moves: list[dict],
    result: str,
    score: int,
    ai_score: int,
    all_progress: dict[str, int],
) -> bool:
    total_played = sum(all_progress.values())
    games_with_play = {g for g, n in all_progress.items() if n >= 1}

    match slug:
        # ── Einstieg ──────────────────────────────────────────────────────
        case "erster_schritt":
            return total_played == 1

        case "neugierig":
            return len(games_with_play) >= 5

        case "entdecker":
            return len(games_with_play) >= 15

        # ── Lernpfad ──────────────────────────────────────────────────────
        case "level1":
            return {"gefangenendilemma", "ultimatum", "vertrauen"}.issubset(games_with_play)

        case "level2":
            return {"chicken", "stag_hunt", "koordination", "rps"}.issubset(games_with_play)

        case "pfad_meister":
            all_15 = {
                "gefangenendilemma", "ultimatum", "vertrauen",
                "chicken", "stag_hunt", "koordination", "rps",
                "public_goods", "diktator", "auktion",
                "beauty_contest", "centipede", "dollarauktion", "verhandlung",
                "minderheit",
            }
            return all_15.issubset(games_with_play)

        # ── Verhalten ─────────────────────────────────────────────────────
        case "kooperator":
            if game_type != "gefangenendilemma" or not moves:
                return False
            coop = sum(1 for m in moves if m.get("player") == 0)
            return coop / len(moves) >= 0.8

        case "vertrauensperson":
            if game_type != "vertrauen" or not moves:
                return False
            invested_any = any(m.get("invested", 0) > 0 for m in moves)
            net_positive = sum(m.get("player_net", 0) for m in moves) > 0
            return invested_any and net_positive

        case "optimaler_bieter":
            if game_type != "auktion" or not moves:
                return False
            on_target = sum(1 for m in moves if m.get("bid_deviation", 99) == 0)
            return on_target >= 3

        case "schoenheitskoenig":
            if game_type != "beauty_contest" or not moves:
                return False
            wins = sum(1 for m in moves if m.get("player_wins_round"))
            return wins >= 4

        case "unbestechlich":
            if game_type != "centipede" or not moves:
                return False
            passed = [
                e["node"]
                for e in moves
                if e.get("actor") == "player" and e.get("action") == "pass"
            ]
            return bool(passed) and max(passed) >= 5

        case "top_negotiator":
            return game_type == "verhandlung" and result == "win" and score >= 80

        case "fair_dealer":
            return game_type == "ultimatum" and score >= 300

        case "antiherding":
            if game_type != "minderheit" or not moves:
                return False
            minority_rounds = sum(1 for m in moves if m.get("in_minority"))
            return minority_rounds >= 6

        case "kein_sunk_cost":
            return (
                game_type == "dollarauktion"
                and result == "loss"
                and score > -_DOLLAR_PRIZE
            )

        case "diktator_fair":
            if game_type != "diktator" or not moves:
                return False
            dictator_moves = [m for m in moves if m.get("player_is_dictator")]
            if not dictator_moves:
                return False
            avg_offer = sum(m.get("ai_score", 0) for m in dictator_moves) / len(dictator_moves)
            return avg_offer >= 40

        case "nash_spieler":
            if game_type != "rps" or not moves:
                return False
            counts = Counter(m.get("player", -1) for m in moves)
            total = len(moves)
            return total > 0 and all(c / total < 0.6 for c in counts.values())

    return False
