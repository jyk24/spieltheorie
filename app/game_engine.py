"""
Spiellogik für alle Verhandlungsspiele.
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
    elif strategy == "adaptive_exploiter":
        if len(history) < 3:
            return "C"  # erst beobachten
        recent = history[-3:]
        recent_coop = sum(1 for r in recent if r["player"] == "C") / 3
        if recent_coop >= 0.67:
            return "D"  # kooperativen Spieler ausnutzen
        elif recent_coop == 0.0:
            return "C" if random.random() < 0.25 else "D"  # defensiven Spieler testen
        else:
            return history[-1]["player"]  # gemischter Spieler → Tit-for-Tat
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


# ---------------------------------------------------------------------------
# Feiglingsspiel (Chicken Game)
# ---------------------------------------------------------------------------

CHICKEN_PAYOFF = {
    ("H", "H"): (-8, -8),   # Crash – beide verlieren stark
    ("H", "S"): (5, -3),    # Du hältst, KI weicht aus – du gewinnst
    ("S", "H"): (-3, 5),    # Du weichst aus, KI hält – KI gewinnt
    ("S", "S"): (1, 1),     # Beide weichen aus – kleiner Ausgleich
}


def chicken_ai_move(strategy: str, history: list[dict]) -> str:
    """Berechnet den KI-Zug für das Feiglingsspiel."""
    if strategy == "aggressive":
        return "H"
    elif strategy == "dove":
        return "S"
    elif strategy == "adaptive":
        if not history:
            return "H"
        # Wenn Spieler oft ausgewichen ist, bleibt KI aggressiv; sonst weicht KI aus
        player_swerves = sum(1 for r in history if r["player"] == "S")
        swerve_rate = player_swerves / len(history)
        if swerve_rate > 0.5:
            return "H"
        else:
            return "S"
    elif strategy == "mixed":
        # Nash-Gleichgewicht des Chicken-Spiels: gemischte Strategie ~60% S
        return random.choices(["H", "S"], weights=[40, 60])[0]
    return "H"


def chicken_play_round(player_move: str, strategy: str, history: list[dict]) -> dict:
    """Verarbeitet eine Runde des Feiglingsspiels."""
    ai_move = chicken_ai_move(strategy, history)
    player_score, ai_score = CHICKEN_PAYOFF[(player_move, ai_move)]
    labels = {"H": "Halten", "S": "Ausweichen"}
    return {
        "round": len(history) + 1,
        "player": player_move,
        "ai": ai_move,
        "player_label": labels[player_move],
        "ai_label": labels[ai_move],
        "player_score": player_score,
        "ai_score": ai_score,
    }


def chicken_final_result(history: list[dict]) -> dict:
    """Berechnet das Gesamtergebnis des Feiglingsspiels."""
    total_player = sum(r["player_score"] for r in history)
    total_ai = sum(r["ai_score"] for r in history)
    crashes = sum(1 for r in history if r["player"] == "H" and r["ai"] == "H")
    held_rate = sum(1 for r in history if r["player"] == "H") / len(history) * 100
    if total_player > total_ai:
        result = "win"
    elif total_player < total_ai:
        result = "loss"
    else:
        result = "draw"
    return {
        "result": result,
        "player_total": total_player,
        "ai_total": total_ai,
        "crashes": crashes,
        "held_rate": round(held_rate),
    }


# ---------------------------------------------------------------------------
# Öffentliche-Güter-Spiel (Public Goods Game)
# ---------------------------------------------------------------------------

TOKENS_PER_ROUND = 10
MULTIPLIER = 1.6


def public_goods_ai_contribution(strategy: str, round_num: int, history: list[dict]) -> int:
    """Berechnet den Beitrag der KI zum öffentlichen Gut."""
    if strategy == "cooperative":
        return random.randint(7, 9)
    elif strategy == "free_rider":
        return random.randint(0, 2)
    elif strategy == "conditional":
        if not history:
            return 5
        last_player = history[-1]["player_contribution"]
        # Spiegelt den Spieler mit leichtem Rauschen
        noise = random.randint(-1, 1)
        return max(0, min(TOKENS_PER_ROUND, last_player + noise))
    elif strategy == "punisher":
        if not history:
            return 7
        # Bestraft Trittbrettfahrer: gibt viel wenn Spieler gibt, gibt nichts wenn nicht
        last_player = history[-1]["player_contribution"]
        return 8 if last_player >= 5 else 0
    return 5


def public_goods_play_round(player_contribution: int, strategy: str, history: list[dict]) -> dict:
    """Verarbeitet eine Runde des Öffentliche-Güter-Spiels."""
    player_contribution = max(0, min(TOKENS_PER_ROUND, player_contribution))
    ai_contribution = public_goods_ai_contribution(strategy, len(history), history)
    total_pool = (player_contribution + ai_contribution) * MULTIPLIER
    each_share = total_pool / 2
    player_net = TOKENS_PER_ROUND - player_contribution + each_share
    ai_net = TOKENS_PER_ROUND - ai_contribution + each_share
    return {
        "round": len(history) + 1,
        "player_contribution": player_contribution,
        "ai_contribution": ai_contribution,
        "total_pool": round(total_pool, 1),
        "each_share": round(each_share, 1),
        "player_net": round(player_net, 1),
        "ai_net": round(ai_net, 1),
    }


def public_goods_final_result(history: list[dict]) -> dict:
    """Gesamtergebnis des Öffentliche-Güter-Spiels."""
    total_player = round(sum(r["player_net"] for r in history), 1)
    total_ai = round(sum(r["ai_net"] for r in history), 1)
    avg_player_contrib = round(
        sum(r["player_contribution"] for r in history) / len(history), 1
    )
    avg_ai_contrib = round(
        sum(r["ai_contribution"] for r in history) / len(history), 1
    )
    if total_player > total_ai:
        result = "win"
    elif total_player < total_ai:
        result = "loss"
    else:
        result = "draw"
    return {
        "result": result,
        "player_total": total_player,
        "ai_total": total_ai,
        "avg_player_contrib": avg_player_contrib,
        "avg_ai_contrib": avg_ai_contrib,
        "max_possible": TOKENS_PER_ROUND * len(history) * MULTIPLIER / 2,
    }


# ---------------------------------------------------------------------------
# Schönheitswettbewerb (Keynesian Beauty Contest) – K-Level Thinking
# ---------------------------------------------------------------------------

def beauty_contest_ai_guesses(strategy: str, round_num: int, history: list[dict]) -> list[int]:
    """Liefert 3 KI-Einsätze für den Schönheitswettbewerb (0–100)."""
    def _clamp(v: int) -> int:
        return max(0, min(100, v))

    if strategy == "level_0":
        # Alle drei spielen zufällig – Level-0 Denker
        return [_clamp(random.randint(0, 100)) for _ in range(3)]

    elif strategy == "level_1":
        # Alle drei gehen von Level-0 (Durchschnitt ≈ 50) aus → 2/3 * 50 ≈ 33
        return [_clamp(33 + random.randint(-4, 4)) for _ in range(3)]

    elif strategy == "level_2":
        # Alle drei gehen von Level-1 (≈ 33) aus → 2/3 * 33 ≈ 22
        return [_clamp(22 + random.randint(-3, 3)) for _ in range(3)]

    elif strategy == "adaptive":
        # Lernt aus vergangenen Gewinnzahlen
        if not history:
            return [_clamp(33 + random.randint(-5, 5)) for _ in range(3)]
        past_targets = [r["target"] for r in history]
        avg_target = sum(past_targets) / len(past_targets)
        # Konvergiert gegen tatsächliches Gleichgewicht
        base = round(avg_target * 0.85)
        return [_clamp(base + random.randint(-3, 3)) for _ in range(3)]

    return [_clamp(random.randint(0, 100)) for _ in range(3)]


def beauty_contest_play_round(player_guess: int, strategy: str, round_num: int, history: list[dict]) -> dict:
    """Verarbeitet eine Runde des Schönheitswettbewerbs."""
    player_guess = max(0, min(100, player_guess))
    ai_guesses = beauty_contest_ai_guesses(strategy, round_num, history)
    all_guesses = [player_guess] + ai_guesses
    average = sum(all_guesses) / len(all_guesses)
    target = round(average * 2 / 3, 1)

    # Abstände zum Ziel
    distances = [abs(g - target) for g in all_guesses]
    min_dist = min(distances)
    player_dist = distances[0]
    player_wins = player_dist == min_dist and all(distances[i] >= min_dist for i in range(1, len(distances)))

    return {
        "round": round_num + 1,
        "player_guess": player_guess,
        "ai_guesses": ai_guesses,
        "all_guesses": all_guesses,
        "average": round(average, 1),
        "target": target,
        "player_distance": round(player_dist, 1),
        "player_wins_round": player_wins,
    }


def beauty_contest_final_result(history: list[dict]) -> dict:
    """Gesamtergebnis des Schönheitswettbewerbs."""
    player_round_wins = sum(1 for r in history if r["player_wins_round"])
    total_rounds = len(history)
    avg_player_guess = round(sum(r["player_guess"] for r in history) / total_rounds, 1)
    avg_target = round(sum(r["target"] for r in history) / total_rounds, 1)
    avg_distance = round(sum(r["player_distance"] for r in history) / total_rounds, 1)
    result = "win" if player_round_wins > total_rounds / 2 else ("draw" if player_round_wins == total_rounds / 2 else "loss")
    return {
        "result": result,
        "player_round_wins": player_round_wins,
        "total_rounds": total_rounds,
        "avg_player_guess": avg_player_guess,
        "avg_target": avg_target,
        "avg_distance": avg_distance,
    }


# ---------------------------------------------------------------------------
# Hirschjagd (Stag Hunt) – Koordinationsspiel
# ---------------------------------------------------------------------------

STAG_PAYOFF = {
    ("S", "S"): (8, 8),   # Beide jagen Hirsch – kooperatives Optimum
    ("S", "H"): (0, 3),   # Du jagst Hirsch, KI jagt Hase – du gehst leer aus
    ("H", "S"): (3, 0),   # Du jagst Hase, KI jagt Hirsch – KI geht leer aus
    ("H", "H"): (3, 3),   # Beide jagen Hase – sicheres aber suboptimales Ergebnis
}


def stag_ai_move(strategy: str, history: list[dict]) -> str:
    """Berechnet den KI-Zug für die Hirschjagd."""
    if strategy == "risk_averse":
        # Spielt immer sicher: Hase
        return "H"
    elif strategy == "optimist":
        # Vertraut immer auf Koordination: Hirsch
        return "S"
    elif strategy == "coordinator":
        # Tit-for-Tat für Koordination: spiegelt letzten Spielerzug
        if not history:
            return "S"  # optimistischer Start
        return history[-1]["player"]
    elif strategy == "cautious_learner":
        # Beginnt vorsichtig, kooperiert bei konsistenter Zusammenarbeit
        if not history:
            return "H"
        stag_rate = sum(1 for r in history if r["player"] == "S") / len(history)
        if stag_rate >= 0.7:
            return "S"
        elif stag_rate >= 0.4 and len(history) >= 3:
            return random.choices(["S", "H"], weights=[int(stag_rate * 10), 10 - int(stag_rate * 10)])[0]
        return "H"
    return "H"


def stag_play_round(player_move: str, strategy: str, history: list[dict]) -> dict:
    """Verarbeitet eine Runde der Hirschjagd."""
    ai_move = stag_ai_move(strategy, history)
    player_score, ai_score = STAG_PAYOFF[(player_move, ai_move)]
    labels = {"S": "Hirsch jagen", "H": "Hase jagen"}
    return {
        "round": len(history) + 1,
        "player": player_move,
        "ai": ai_move,
        "player_label": labels[player_move],
        "ai_label": labels[ai_move],
        "player_score": player_score,
        "ai_score": ai_score,
    }


def stag_final_result(history: list[dict]) -> dict:
    """Gesamtergebnis der Hirschjagd."""
    total_player = sum(r["player_score"] for r in history)
    total_ai = sum(r["ai_score"] for r in history)
    stag_rate = sum(1 for r in history if r["player"] == "S") / len(history) * 100
    coord_rate = sum(1 for r in history if r["player"] == r["ai"]) / len(history) * 100
    if total_player > total_ai:
        result = "win"
    elif total_player < total_ai:
        result = "loss"
    else:
        result = "draw"
    return {
        "result": result,
        "player_total": total_player,
        "ai_total": total_ai,
        "stag_rate": round(stag_rate),
        "coord_rate": round(coord_rate),
    }


# ---------------------------------------------------------------------------
# Centipede-Spiel – Rückwärtsinduktion
# ---------------------------------------------------------------------------

# Jeder Knoten: wer entscheidet, und was passiert bei "Nehmen"
CENTIPEDE_NODES = [
    {"node": 1, "actor": "player", "take_player": 4,  "take_ai": 1},
    {"node": 2, "actor": "ai",     "take_player": 2,  "take_ai": 8},
    {"node": 3, "actor": "player", "take_player": 8,  "take_ai": 4},
    {"node": 4, "actor": "ai",     "take_player": 4,  "take_ai": 16},
    {"node": 5, "actor": "player", "take_player": 16, "take_ai": 8},
    {"node": 6, "actor": "ai",     "take_player": 8,  "take_ai": 32},
    {"node": 7, "actor": "player", "take_player": 32, "take_ai": 16},
    {"node": 8, "actor": "ai",     "take_player": 16, "take_ai": 64},
]
CENTIPEDE_END = {"take_player": 64, "take_ai": 32}  # wenn alle passen


def centipede_ai_decision(strategy: str, node_idx: int, history: list[dict]) -> str:
    """KI entscheidet ob sie 'nimmt' oder 'weitergibt' (nur für KI-Knoten)."""
    node = CENTIPEDE_NODES[node_idx]

    if strategy == "backward_induction":
        # Rückwärtsinduktion: immer nehmen (subgame-perfektes Gleichgewicht)
        return "take"

    elif strategy == "cooperative":
        # Kooperiert bis zum letzten KI-Knoten
        if node_idx == 7:  # Knoten 8 (letzter)
            return "take"
        return "pass"

    elif strategy == "opportunist":
        # Lässt erstmal wachsen, greift dann zu (ab Knoten 4)
        if node_idx >= 3:  # ab Knoten 4
            return "take"
        return "pass"

    elif strategy == "mirror":
        # Spiegelt Spielerverhalten: Wenn Spieler öfter genommen hat → nehmen
        player_takes = sum(1 for r in history if r.get("actor") == "player" and r.get("action") == "take")
        player_passes = sum(1 for r in history if r.get("actor") == "player" and r.get("action") == "pass")
        if player_takes > player_passes:
            return "take"
        return "pass"

    return "take"


def centipede_process_turn(player_action: str, strategy: str, node_idx: int, history: list[dict]) -> dict:
    """
    Verarbeitet den Spieler-Zug bei node_idx (muss ein Spieler-Knoten sein).
    Wenn Spieler weitergibt, entscheidet danach die KI am nächsten Knoten.
    Gibt dict zurück mit allen Events dieser Runde.
    """
    node = CENTIPEDE_NODES[node_idx]
    events = []
    game_over = False
    final_player = None
    final_ai = None

    # Spieler-Aktion
    events.append({
        "node": node_idx + 1,
        "actor": "player",
        "action": player_action,
        "take_player": node["take_player"],
        "take_ai": node["take_ai"],
    })

    if player_action == "take":
        final_player = node["take_player"]
        final_ai = node["take_ai"]
        game_over = True
    else:
        # Nächster Knoten: KI-Entscheidung
        next_idx = node_idx + 1
        if next_idx >= len(CENTIPEDE_NODES):
            # Alle Knoten durchlaufen
            final_player = CENTIPEDE_END["take_player"]
            final_ai = CENTIPEDE_END["take_ai"]
            game_over = True
            events.append({
                "node": next_idx + 1,
                "actor": "end",
                "action": "end",
                "take_player": final_player,
                "take_ai": final_ai,
            })
        else:
            ai_action = centipede_ai_decision(strategy, next_idx, history + events)
            ai_node = CENTIPEDE_NODES[next_idx]
            events.append({
                "node": next_idx + 1,
                "actor": "ai",
                "action": ai_action,
                "take_player": ai_node["take_player"],
                "take_ai": ai_node["take_ai"],
            })
            if ai_action == "take":
                final_player = ai_node["take_player"]
                final_ai = ai_node["take_ai"]
                game_over = True

    # Nächster Spieler-Knoten
    next_player_node_idx = node_idx + 2 if not game_over else None

    return {
        "events": events,
        "game_over": game_over,
        "final_player": final_player,
        "final_ai": final_ai,
        "next_node_idx": next_player_node_idx,
    }


def centipede_final_result(history_events: list[dict], final_player: int, final_ai: int) -> dict:
    """Gesamtergebnis des Centipede-Spiels."""
    total_nodes = len(CENTIPEDE_NODES)
    reached_node = history_events[-1]["node"] if history_events else 1
    if final_player > final_ai:
        result = "win"
    elif final_player < final_ai:
        result = "loss"
    else:
        result = "draw"
    return {
        "result": result,
        "player_score": final_player,
        "ai_score": final_ai,
        "reached_node": reached_node,
        "total_nodes": total_nodes,
        "cooperation_depth": round(reached_node / total_nodes * 100),
    }


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


# ---------------------------------------------------------------------------
# Schere-Stein-Papier (Rock-Paper-Scissors)
# ---------------------------------------------------------------------------

# S=Schere beats P=Papier, T=Stein beats S=Schere, P=Papier beats T=Stein
RPS_BEATS = {"S": "P", "T": "S", "P": "T"}
RPS_NAMES = {"S": "Schere", "T": "Stein", "P": "Papier"}
RPS_ICONS = {"S": "✂️", "T": "🪨", "P": "📄"}


def rps_ai_move(strategy: str, history: list[dict]) -> str:
    moves = ["S", "T", "P"]
    if strategy == "nash_mixed":
        return random.choice(moves)
    elif strategy == "pattern_detector":
        if len(history) < 3:
            return random.choice(moves)
        last3 = [r["player"] for r in history[-3:]]
        freq = {m: last3.count(m) for m in moves}
        predicted = max(freq, key=freq.get)
        return next(m for m, beats in RPS_BEATS.items() if beats == predicted)
    elif strategy == "win_stay_lose_shift":
        if not history:
            return random.choice(moves)
        last = history[-1]
        if last["outcome"] == "ai_win":
            return last["ai"]
        return next(m for m, beats in RPS_BEATS.items() if beats == last["player"])
    elif strategy == "frequency_analyzer":
        if len(history) < 4:
            return random.choice(moves)
        freq = {m: sum(1 for r in history if r["player"] == m) for m in moves}
        predicted = max(freq, key=freq.get)
        return next(m for m, beats in RPS_BEATS.items() if beats == predicted)
    return random.choice(moves)


def rps_play_round(player_move: str, strategy: str, history: list[dict]) -> dict:
    ai_move = rps_ai_move(strategy, history)
    if RPS_BEATS[player_move] == ai_move:
        outcome = "player_win"
        pd, ad = 1, -1
    elif RPS_BEATS[ai_move] == player_move:
        outcome = "ai_win"
        pd, ad = -1, 1
    else:
        outcome = "draw"
        pd, ad = 0, 0
    prev_ps = sum(r.get("player_delta", 0) for r in history)
    prev_as = sum(r.get("ai_delta", 0) for r in history)
    return {
        "round": len(history) + 1,
        "player": player_move,
        "ai": ai_move,
        "player_name": RPS_NAMES[player_move],
        "ai_name": RPS_NAMES[ai_move],
        "outcome": outcome,
        "player_delta": pd,
        "ai_delta": ad,
        "player_score": prev_ps + pd,
        "ai_score": prev_as + ad,
    }


def rps_final_result(history: list[dict]) -> dict:
    player_wins = sum(1 for r in history if r["outcome"] == "player_win")
    ai_wins = sum(1 for r in history if r["outcome"] == "ai_win")
    draws = sum(1 for r in history if r["outcome"] == "draw")
    player_score = history[-1]["player_score"] if history else 0
    ai_score = history[-1]["ai_score"] if history else 0
    moves = ["S", "T", "P"]
    freq = {m: sum(1 for r in history if r["player"] == m) for m in moves}
    most_played = max(freq, key=freq.get)
    max_f = max(freq.values()) if freq else 1
    min_f = min(freq.values()) if freq else 1
    randomness = round(min_f / max_f * 100) if max_f else 100
    if player_score > ai_score:
        result = "win"
    elif player_score < ai_score:
        result = "loss"
    else:
        result = "draw"
    return {
        "result": result,
        "player_wins": player_wins,
        "ai_wins": ai_wins,
        "draws": draws,
        "player_score": player_score,
        "ai_score": ai_score,
        "total_rounds": len(history),
        "move_freq": freq,
        "most_played": most_played,
        "most_played_name": RPS_NAMES[most_played],
        "randomness": randomness,
    }


# ---------------------------------------------------------------------------
# Koordinationsspiel (Battle of the Sexes)
# ---------------------------------------------------------------------------

COORD_PAYOFF = {
    ("A", "A"): (3, 2),
    ("B", "B"): (2, 3),
    ("A", "B"): (0, 0),
    ("B", "A"): (0, 0),
}


def coord_ai_move(strategy: str, history: list[dict]) -> str:
    if strategy == "stubborn":
        return "B"
    elif strategy == "flexible":
        if not history:
            return "A"
        return history[-1]["player"]
    elif strategy == "alternating":
        return "A" if len(history) % 2 == 0 else "B"
    elif strategy == "learner":
        if len(history) < 2:
            return "B"
        a_count = sum(1 for r in history if r["player"] == "A")
        return "A" if a_count > len(history) / 2 else "B"
    return "B"


def coord_play_round(player_move: str, strategy: str, history: list[dict]) -> dict:
    ai_move = coord_ai_move(strategy, history)
    ps, as_ = COORD_PAYOFF[(player_move, ai_move)]
    prev_p = sum(r["player_score_round"] for r in history)
    prev_a = sum(r["ai_score_round"] for r in history)
    return {
        "round": len(history) + 1,
        "player": player_move,
        "ai": ai_move,
        "player_score_round": ps,
        "ai_score_round": as_,
        "player_total": prev_p + ps,
        "ai_total": prev_a + as_,
        "coordinated": player_move == ai_move,
    }


def coord_final_result(history: list[dict]) -> dict:
    coord_rounds = sum(1 for r in history if r["coordinated"])
    total = len(history)
    player_total = history[-1]["player_total"] if history else 0
    ai_total = history[-1]["ai_total"] if history else 0
    max_possible = total * 3
    efficiency = round(player_total / max_possible * 100) if max_possible else 0
    coord_rate = round(coord_rounds / total * 100) if total else 0
    if efficiency >= 65:
        result = "win"
    elif efficiency >= 35:
        result = "draw"
    else:
        result = "loss"
    return {
        "result": result,
        "player_total": player_total,
        "ai_total": ai_total,
        "coord_rounds": coord_rounds,
        "total_rounds": total,
        "coord_rate": coord_rate,
        "efficiency": efficiency,
    }


# ---------------------------------------------------------------------------
# Auktion (Vickrey Second-Price Auction)
# ---------------------------------------------------------------------------


def auction_ai_bids(strategy: str) -> list[int]:
    """3 KI-Bieter für diese Runde."""
    ai_values = [random.randint(20, 100) for _ in range(3)]
    if strategy == "truthful":
        return ai_values
    elif strategy == "aggressive":
        return [min(180, int(v * random.uniform(1.15, 1.45))) for v in ai_values]
    elif strategy == "conservative":
        return [max(2, int(v * random.uniform(0.5, 0.8))) for v in ai_values]
    elif strategy == "random":
        return [random.randint(2, 160) for _ in range(3)]
    return ai_values


def auction_play_round(player_bid: int, player_value: int, strategy: str, round_num: int) -> dict:
    ai_bids = auction_ai_bids(strategy)
    all_bids = sorted([player_bid] + ai_bids, reverse=True)
    max_bid = all_bids[0]
    second_price = all_bids[1]
    player_wins = player_bid >= max_bid
    if player_wins:
        price_paid = second_price
        profit = player_value - price_paid
    else:
        price_paid = None
        profit = 0
    return {
        "round": round_num,
        "player_bid": player_bid,
        "player_value": player_value,
        "ai_bids": ai_bids,
        "max_bid": max_bid,
        "second_price": second_price,
        "player_wins": player_wins,
        "price_paid": price_paid,
        "profit": profit,
        "bid_deviation": abs(player_bid - player_value),
    }


def auction_final_result(history: list[dict]) -> dict:
    total_profit = sum(r["profit"] for r in history)
    wins = sum(1 for r in history if r["player_wins"])
    avg_dev = round(sum(r["bid_deviation"] for r in history) / len(history)) if history else 0
    near_truthful = sum(1 for r in history if r["bid_deviation"] <= 10)
    truthful_rate = round(near_truthful / len(history) * 100) if history else 0
    if total_profit >= 40:
        result = "win"
    elif total_profit >= -10:
        result = "draw"
    else:
        result = "loss"
    return {
        "result": result,
        "total_profit": total_profit,
        "wins": wins,
        "total_rounds": len(history),
        "avg_deviation": avg_dev,
        "truthful_rate": truthful_rate,
    }


# ---------------------------------------------------------------------------
# Diktatorspiel
# ---------------------------------------------------------------------------

def diktator_ai_offer(strategy: str, player_rounds: list[dict]) -> int:
    """Bestimmt das Angebot der KI als Diktator (0–100)."""
    if strategy == "selfish":
        return 10
    elif strategy == "fair":
        return 50
    elif strategy == "altruistic":
        return 65
    elif strategy == "reciprocal":
        if not player_rounds:
            return 40
        avg = sum(r["player_offer"] for r in player_rounds) / len(player_rounds)
        return max(5, round(avg * 0.9))
    return 30


def diktator_play_round(player_offer: int, strategy: str, round_num: int, history: list[dict]) -> dict:
    """Runden 1–4: Spieler ist Diktator. Runden 5–8: KI ist Diktator."""
    is_player_dictator = round_num <= 4
    if is_player_dictator:
        ps, as_ = 100 - player_offer, player_offer
        ai_offer = None
    else:
        player_rounds = [r for r in history if r["player_is_dictator"]]
        ai_offer = diktator_ai_offer(strategy, player_rounds)
        ps, as_ = ai_offer, 100 - ai_offer
    prev_p = sum(r["player_score"] for r in history)
    prev_a = sum(r["ai_score"] for r in history)
    return {
        "round": round_num,
        "player_is_dictator": is_player_dictator,
        "player_offer": player_offer if is_player_dictator else None,
        "ai_offer": ai_offer,
        "player_score": ps,
        "ai_score": as_,
        "player_total": prev_p + ps,
        "ai_total": prev_a + as_,
    }


def diktator_final_result(history: list[dict]) -> dict:
    player_total = history[-1]["player_total"] if history else 0
    ai_total = history[-1]["ai_total"] if history else 0
    dictator_rounds = [r for r in history if r["player_is_dictator"]]
    avg_offer = round(sum(r["player_offer"] for r in dictator_rounds) / len(dictator_rounds)) if dictator_rounds else 0
    if avg_offer >= 45:
        generosity = "sehr_großzügig"
    elif avg_offer >= 30:
        generosity = "fair"
    elif avg_offer >= 15:
        generosity = "leicht_egoistisch"
    else:
        generosity = "egoistisch"
    result = "win" if player_total > ai_total else ("loss" if player_total < ai_total else "draw")
    return {
        "result": result,
        "player_total": player_total,
        "ai_total": ai_total,
        "avg_offer": avg_offer,
        "generosity": generosity,
        "total_rounds": len(history),
    }


# ---------------------------------------------------------------------------
# Dollarauktion
# ---------------------------------------------------------------------------

DOLLAR_PRIZE = 100


def dollar_ai_response(player_bid: int, strategy: str, round_num: int) -> dict:
    """KI entscheidet: weiterbieten oder aufgeben?"""
    next_bid = player_bid + 10
    if strategy == "escalator":
        return {"bids": next_bid <= 150, "amount": next_bid}
    elif strategy == "rational_stopper":
        return {"bids": next_bid <= DOLLAR_PRIZE, "amount": next_bid}
    elif strategy == "aggressive":
        return {"bids": next_bid <= 210, "amount": next_bid}
    elif strategy == "random_quitter":
        import random as _r
        stop_prob = max(0, (player_bid - 60) / 150)
        bids = _r.random() > stop_prob and next_bid <= 180
        return {"bids": bids, "amount": next_bid if bids else None}
    return {"bids": next_bid <= DOLLAR_PRIZE, "amount": next_bid}


def dollar_process_turn(player_bid: int, player_quit: bool, strategy: str, ai_last_bid: int, round_num: int) -> dict:
    """Verarbeitet einen Spielzug der Dollarauktion."""
    if player_quit:
        # Spieler gibt auf: KI gewinnt Preis, zahlt ihren letzten Einsatz
        player_payoff = -player_bid
        ai_payoff = DOLLAR_PRIZE - ai_last_bid
        return {
            "game_over": True,
            "winner": "ai",
            "player_bid": player_bid,
            "ai_bid": ai_last_bid,
            "player_payoff": player_payoff,
            "ai_payoff": ai_payoff,
            "next_player_bid": player_bid,
            "next_ai_bid": ai_last_bid,
        }
    # Spieler bietet: dann reagiert KI
    ai_resp = dollar_ai_response(player_bid, strategy, round_num)
    if not ai_resp["bids"]:
        # KI gibt auf: Spieler gewinnt Preis
        player_payoff = DOLLAR_PRIZE - player_bid
        ai_payoff = -ai_last_bid
        return {
            "game_over": True,
            "winner": "player",
            "player_bid": player_bid,
            "ai_bid": ai_last_bid,
            "player_payoff": player_payoff,
            "ai_payoff": ai_payoff,
            "next_player_bid": player_bid,
            "next_ai_bid": ai_last_bid,
        }
    return {
        "game_over": False,
        "winner": None,
        "player_bid": player_bid,
        "ai_bid": ai_resp["amount"],
        "player_payoff": None,
        "ai_payoff": None,
        "next_player_bid": player_bid,
        "next_ai_bid": ai_resp["amount"],
    }


# ---------------------------------------------------------------------------
# Minderheitsspiel (El Farol / Minority Game)
# ---------------------------------------------------------------------------

def minority_ai_choices(strategy: str, history: list[dict], n_bots: int = 6) -> list[int]:
    """Erzeugt Entscheidungen der 6 KI-Bots (0 = Gruppe A, 1 = Gruppe B)."""
    if strategy == "random":
        return [random.randint(0, 1) for _ in range(n_bots)]
    elif strategy == "herding":
        if not history:
            return [0] * n_bots
        last_maj = 0 if history[-1]["count_0"] > history[-1]["count_1"] else 1
        return [last_maj] * n_bots
    elif strategy == "contrarian":
        if not history:
            return [1] * n_bots
        last_maj = 0 if history[-1]["count_0"] > history[-1]["count_1"] else 1
        return [1 - last_maj] * n_bots
    elif strategy == "nash_mixed":
        return [random.randint(0, 1) for _ in range(n_bots)]
    return [random.randint(0, 1) for _ in range(n_bots)]


def minority_play_round(player_choice: int, strategy: str, history: list[dict]) -> dict:
    """player_choice: 0 = Gruppe A, 1 = Gruppe B. Minderheit gewinnt 3 Punkte."""
    ai_ch = minority_ai_choices(strategy, history)
    all_ch = [player_choice] + ai_ch
    count_0 = sum(1 for c in all_ch if c == 0)
    count_1 = 7 - count_0
    player_count = count_0 if player_choice == 0 else count_1
    other_count = 7 - player_count
    in_minority = player_count < other_count
    in_tie = count_0 == count_1
    player_score = 3 if in_minority else (1 if in_tie else 0)
    prev_p = sum(r["player_score"] for r in history)
    return {
        "round": len(history) + 1,
        "player": player_choice,
        "ai_choices": ai_ch,
        "count_0": count_0,
        "count_1": count_1,
        "in_minority": in_minority,
        "in_tie": in_tie,
        "player_score": player_score,
        "player_total": prev_p + player_score,
    }


def minority_final_result(history: list[dict]) -> dict:
    player_total = history[-1]["player_total"] if history else 0
    total_rounds = len(history)
    minority_wins = sum(1 for r in history if r["in_minority"])
    max_possible = total_rounds * 3
    efficiency = round(player_total / max_possible * 100) if max_possible else 0
    result = "win" if efficiency >= 55 else ("draw" if efficiency >= 33 else "loss")
    return {
        "result": result,
        "player_total": player_total,
        "total_rounds": total_rounds,
        "minority_wins": minority_wins,
        "efficiency": efficiency,
    }
