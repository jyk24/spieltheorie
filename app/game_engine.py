"""
Spiellogik für alle 4 Verhandlungsspiele.
Jede Funktion verarbeitet einen Spielzug und gibt das Ergebnis zurück.
"""
import random
from dataclasses import dataclass, field
from typing import Literal


# ---------------------------------------------------------------------------
# Gefangenendilemma
# ---------------------------------------------------------------------------

GD_PAYOFF = {
    ("C", "C"): (3, 3),
    ("C", "D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (1, 1),
}


def gd_ai_move(strategy: str, history: list[dict]) -> str:
    """Berechnet den nächsten Zug der KI für das Gefangenendilemma."""
    if strategy == "tit_for_tat":
        if not history:
            return "C"
        return history[-1]["player"]
    elif strategy == "always_cooperate":
        return "C"
    elif strategy == "always_defect":
        return "D"
    elif strategy == "grim_trigger":
        if any(r["player"] == "D" for r in history):
            return "D"
        return "C"
    elif strategy == "random":
        return random.choice(["C", "D"])
    return "C"


def gd_play_round(player_move: str, strategy: str, history: list[dict]) -> dict:
    """Verarbeitet eine Runde des Gefangenendilemmas."""
    ai_move = gd_ai_move(strategy, history)
    player_score, ai_score = GD_PAYOFF[(player_move, ai_move)]
    labels = {"C": "Kooperieren", "D": "Verraten"}
    return {
        "round": len(history) + 1,
        "player": player_move,
        "ai": ai_move,
        "player_label": labels[player_move],
        "ai_label": labels[ai_move],
        "player_score": player_score,
        "ai_score": ai_score,
    }


def gd_final_result(history: list[dict]) -> dict:
    """Berechnet das Gesamtergebnis des Gefangenendilemmas."""
    total_player = sum(r["player_score"] for r in history)
    total_ai = sum(r["ai_score"] for r in history)
    if total_player > total_ai:
        result = "win"
    elif total_player < total_ai:
        result = "loss"
    else:
        result = "draw"
    coop_rate = sum(1 for r in history if r["player"] == "C") / len(history) * 100
    return {
        "result": result,
        "player_total": total_player,
        "ai_total": total_ai,
        "cooperation_rate": round(coop_rate),
    }


# ---------------------------------------------------------------------------
# Ultimatumspiel
# ---------------------------------------------------------------------------

def ultimatum_ai_response(offer_percent: int, strategy: str, round_num: int) -> dict:
    """KI entscheidet ob sie ein Angebot akzeptiert (Spieler ist Proposer)."""
    if strategy == "fair":
        accepts = offer_percent >= 40
    elif strategy == "strict":
        accepts = offer_percent >= 50
    elif strategy == "strategic":
        # Lernende Strategie: akzeptiert niedrigere Angebote in späteren Runden
        threshold = max(30, 50 - round_num * 2)
        accepts = offer_percent >= threshold
    else:
        accepts = offer_percent >= 40

    reason = ""
    if accepts:
        if offer_percent >= 50:
            reason = "Das Angebot ist fair oder großzügig."
        elif offer_percent >= 40:
            reason = "Das Angebot ist knapp, aber akzeptabel."
        else:
            reason = "Ich akzeptiere, obwohl es wenig ist."
    else:
        if offer_percent < 20:
            reason = "Das Angebot ist eine Beleidigung. Ich lehne ab, auch wenn ich nichts bekomme."
        elif offer_percent < 30:
            reason = "Zu unfair. Ich lehne ab."
        else:
            reason = "Das Angebot liegt unter meiner Akzeptanzgrenze."

    return {"accepts": accepts, "reason": reason}


def ultimatum_ai_offer(strategy: str, round_num: int) -> int:
    """KI macht ein Angebot (KI ist Proposer, Spieler ist Responder)."""
    if strategy == "fair":
        return random.randint(45, 55)
    elif strategy == "strict":
        return random.randint(30, 45)
    elif strategy == "strategic":
        # Beginnt knapp, verbessert sich wenn abgelehnt wurde
        base = max(25, 45 - round_num * 3)
        return random.randint(base, base + 10)
    return random.randint(35, 50)


def ultimatum_score(offer_percent: int, accepted: bool, is_proposer: bool) -> tuple[int, int]:
    """Berechnet Punkte für Proposer und Responder."""
    if not accepted:
        return (0, 0)
    if is_proposer:
        return (100 - offer_percent, offer_percent)
    else:
        return (offer_percent, 100 - offer_percent)


# ---------------------------------------------------------------------------
# Vertrauensspiel
# ---------------------------------------------------------------------------

def trust_ai_return(invested: int, strategy: str) -> dict:
    """KI entscheidet, wie viel sie zurückgibt (tripled amount)."""
    pot = invested * 3
    if strategy == "reciprocal":
        # Gibt proportional zurück: ~50-60% des Topfes
        return_amount = round(pot * random.uniform(0.45, 0.60))
        reason = "Ich gebe fair zurück – Vertrauen wird belohnt."
    elif strategy == "selfish":
        # Gibt wenig oder nichts zurück
        return_amount = round(pot * random.uniform(0.0, 0.20))
        reason = "Ich behalte den Großteil für mich." if return_amount < pot * 0.15 else "Ich gebe einen kleinen Teil zurück."
    elif strategy == "cooperative":
        # Gibt großzügig zurück: 55-70%
        return_amount = round(pot * random.uniform(0.55, 0.70))
        reason = "Ich gebe mehr zurück – langfristige Kooperation lohnt sich."
    else:
        return_amount = round(pot * 0.5)
        reason = "Ich teile fair auf."

    player_net = return_amount - invested
    ai_net = pot - return_amount
    return {
        "invested": invested,
        "pot": pot,
        "returned": return_amount,
        "player_net": player_net,
        "ai_net": ai_net,
        "reason": reason,
    }


def trust_final_result(history: list[dict]) -> dict:
    """Gesamtergebnis des Vertrauensspiels."""
    total_invested = sum(r["invested"] for r in history)
    total_returned = sum(r["returned"] for r in history)
    total_player = sum(r["player_net"] for r in history)
    total_ai = sum(r["ai_net"] for r in history)
    avg_trust_rate = (total_returned / (total_invested * 3)) * 100 if total_invested > 0 else 0
    return {
        "total_invested": total_invested,
        "total_returned": total_returned,
        "player_net": total_player,
        "ai_net": total_ai,
        "trust_rate": round(avg_trust_rate),
        "result": "win" if total_player > 0 else ("draw" if total_player == 0 else "loss"),
    }


# ---------------------------------------------------------------------------
# Verhandlungssimulation (Rubinstein Bargaining)
# ---------------------------------------------------------------------------

SCENARIOS = {
    "gehalt": {
        "name": "Gehaltsverhandlung",
        "beschreibung": "Du verhandelst dein Jahresgehalt mit deinem zukünftigen Arbeitgeber.",
        "min_value": 50_000,
        "max_value": 90_000,
        "unit": "€",
        "player_label": "Dein Wunschgehalt",
        "ai_label": "Angebot des Arbeitgebers",
        "ai_batna": 55_000,
        "player_batna": 60_000,
        "decay_per_round": 0.05,
        "max_rounds": 6,
    },
    "auto": {
        "name": "Autokauf",
        "beschreibung": "Du kaufst ein Gebrauchtfahrzeug vom Händler.",
        "min_value": 15_000,
        "max_value": 25_000,
        "unit": "€",
        "player_label": "Dein Maximalgebot",
        "ai_label": "Händlerpreis",
        "ai_batna": 17_000,
        "player_batna": 22_000,
        "decay_per_round": 0.04,
        "max_rounds": 5,
    },
    "projekt": {
        "name": "Projektauftrag",
        "beschreibung": "Du verhandelst das Budget für einen Freelance-Auftrag mit einem Kunden.",
        "min_value": 8_000,
        "max_value": 20_000,
        "unit": "€",
        "player_label": "Dein Angebot",
        "ai_label": "Kundenbudget",
        "ai_batna": 9_000,
        "player_batna": 15_000,
        "decay_per_round": 0.06,
        "max_rounds": 5,
    },
}


def verhandlung_ai_offer(scenario: dict, round_num: int, last_player_offer: int | None) -> dict:
    """KI berechnet ihr Angebot basierend auf Nash Bargaining Solution und Zeitdruck."""
    min_v = scenario["min_value"]
    max_v = scenario["max_value"]
    ai_batna = scenario["ai_batna"]
    decay = scenario["decay_per_round"]
    max_rounds = scenario["max_rounds"]

    # Nash Bargaining Solution: geometrischer Mittelpunkt der Überschüsse
    nash_point = (ai_batna + max_v) / 2

    # Zeitdruck-Faktor: KI macht mehr Zugeständnisse je später die Runde
    pressure_factor = 1 - (round_num / max_rounds) * 0.4
    current_effective_max = max_v * (1 - decay * round_num)

    # KI-Strategie: beginnt hoch, konvergiert gegen Nash-Punkt
    if last_player_offer is None:
        ai_offer = round(current_effective_max * 0.85)
    else:
        # Trifft den Gegner auf halbem Weg, aber gewichtet nach Zeitdruck
        midpoint = (last_player_offer + current_effective_max * 0.85) / 2
        ai_offer = round(midpoint * pressure_factor + nash_point * (1 - pressure_factor))

    ai_offer = max(min_v, min(int(current_effective_max), ai_offer))

    # Einigung prüfen
    if last_player_offer and abs(last_player_offer - ai_offer) / max_v < 0.05:
        return {"offer": ai_offer, "deal": True, "final_price": round((last_player_offer + ai_offer) / 2)}

    return {"offer": ai_offer, "deal": False, "final_price": None}


def verhandlung_score(scenario: dict, final_price: int, round_num: int) -> dict:
    """Berechnet Score und Feedback nach Einigung."""
    player_batna = scenario["player_batna"]
    ai_batna = scenario["ai_batna"]
    max_v = scenario["max_value"]
    nash_point = (ai_batna + max_v) / 2
    decay = scenario["decay_per_round"]

    # Verbleibender Wert nach Zeitverlust
    effective_value = max_v * (1 - decay * round_num)

    # Score: wie nah ist das Ergebnis an deinem BATNA?
    player_surplus = final_price - player_batna
    score = max(0, round((player_surplus / (max_v - player_batna)) * 100))

    if final_price >= nash_point:
        feedback = "Exzellent! Du hast mehr als den Nash-Punkt erreicht."
        grade = "A"
    elif final_price >= (player_batna + nash_point) / 2:
        feedback = "Gut – du hast über deiner BATNA abgeschlossen."
        grade = "B"
    elif final_price >= player_batna:
        feedback = "Akzeptabel, aber unter dem Nash-Gleichgewicht. Raum für Verbesserung."
        grade = "C"
    else:
        feedback = "Deal unter deiner BATNA – hättest du besser abgebrochen?"
        grade = "D"

    return {
        "final_price": final_price,
        "player_batna": player_batna,
        "ai_batna": ai_batna,
        "nash_point": round(nash_point),
        "effective_value": round(effective_value),
        "player_surplus": player_surplus,
        "score": score,
        "feedback": feedback,
        "grade": grade,
    }
