import json
import random as _random

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..game_engine import (
    CENTIPEDE_NODES,
    DOLLAR_PRIZE,
    SCENARIOS,
    auction_final_result,
    auction_play_round,
    beauty_contest_final_result,
    beauty_contest_play_round,
    bots_final_result,
    bots_play_round,
    centipede_final_result,
    centipede_process_turn,
    chicken_final_result,
    chicken_play_round,
    coord_final_result,
    coord_play_round,
    diktator_final_result,
    diktator_play_round,
    dollar_process_turn,
    gd_final_result,
    gd_play_round,
    hd_final_result,
    hd_play_round,
    minority_final_result,
    minority_play_round,
    mp_final_result,
    mp_play_round,
    public_goods_final_result,
    public_goods_play_round,
    rps_final_result,
    rps_play_round,
    stag_final_result,
    stag_play_round,
    trust_ai_return,
    trust_final_result,
    ultimatum_ai_offer,
    ultimatum_ai_response,
    ultimatum_score,
    vd_final_result,
    vd_play_round,
    verhandlung_ai_offer,
    verhandlung_score,
    wc_final_result,
    wc_generate_item,
    wc_play_round,
)
from ..services import save_game_session

router = APIRouter(prefix="/spiele")
templates = Jinja2Templates(directory="app/templates")

# ---------------------------------------------------------------------------
# Strategy-Infos für Debrief (nach dem Spiel aufgedeckt)
# ---------------------------------------------------------------------------

GD_STRATEGY_POOL = ["tit_for_tat", "always_defect", "always_cooperate", "grim_trigger", "random", "adaptive_exploiter"]
GD_STRATEGY_WEIGHTS = [20, 10, 10, 20, 10, 30]

GD_STRATEGY_INFO = {
    "tit_for_tat": {
        "name": "Tit-for-Tat",
        "icon": "🔄",
        "verhalten": "Startete mit Kooperation und spiegelte danach jeden deiner Züge sofort – Verrat wird bestraft, Kooperation wird belohnt.",
        "gegencheck": "Gegen Tit-for-Tat ist permanente Kooperation optimal: beide erzielen 3 Punkte pro Runde statt 1.",
        "lesson_slug": "tit-for-tat",
        "lesson_title": "Tit-for-Tat – Die beste Strategie?",
    },
    "always_cooperate": {
        "name": "Immer Kooperieren",
        "icon": "🕊️",
        "verhalten": "Hat in jeder Runde kooperiert, egal was du gemacht hast. Diese Strategie ist vollständig ausnutzbar.",
        "gegencheck": "Immer Verraten maximiert deinen Score (5 pro Runde). Im echten Leben zerstört das jedoch jede Beziehung.",
        "lesson_slug": "wiederholte-spiele-reputation",
        "lesson_title": "Wiederholte Spiele & Reputation",
    },
    "always_defect": {
        "name": "Immer Verraten",
        "icon": "🗡️",
        "verhalten": "Hat in jeder Runde verraten – dominante Strategie im Einmalspiel. Kein Zug kann sie verbessern.",
        "gegencheck": "Auch verraten – du minimierst deinen Verlust (DD = 1/1 statt CD = 0/5). Besser als kooperieren.",
        "lesson_slug": "dominante-strategien",
        "lesson_title": "Dominante Strategien",
    },
    "grim_trigger": {
        "name": "Grim Trigger",
        "icon": "💣",
        "verhalten": "Kooperierte, bis du das erste Mal verraten hast. Danach: ewige Bestrafung, keine zweite Chance.",
        "gegencheck": "Niemals verraten – ein einziger Fehler ruiniert alle künftigen Runden.",
        "lesson_slug": "signaling-glaubwuerdigkeit",
        "lesson_title": "Signaling & Glaubwürdigkeit",
    },
    "random": {
        "name": "Zufallsstrategie",
        "icon": "🎲",
        "verhalten": "Würfelte jeden Zug – kein Muster, keine Reaktion auf dein Verhalten. Nicht zu lesen, nicht zu beeinflussen.",
        "gegencheck": "Kooperieren hat im Erwartungswert leicht mehr Ertrag. Aber: gegen echten Zufall gibt es keine optimale reine Strategie.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "adaptive_exploiter": {
        "name": "Adaptive KI",
        "icon": "🧠",
        "verhalten": "Beobachtete dein Muster in den ersten Runden und spielte dann die beste Gegenantwort – kooperative Spieler werden ausgenutzt.",
        "gegencheck": "Unberechenbar bleiben: Mische Kooperation und Verrat ohne erkennbares Muster, damit die KI nichts exploitieren kann.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
}

ULTIMATUM_STRATEGY_POOL = ["fair", "strict", "strategic"]

ULTIMATUM_STRATEGY_INFO = {
    "fair": {
        "name": "Faire KI",
        "icon": "⚖️",
        "verhalten": "Akzeptierte Angebote ab 40% und machte als Proposer faire Angebote (45–55%). Orientiert an experimentellen Fairnessnormen.",
        "gegencheck": "Als Proposer: 40–45% anbieten ist oft ausreichend. Als Responder: unter 40% ablehnen war richtig.",
        "lesson_slug": "fairness-effekte",
        "lesson_title": "Fairness-Effekte in Verhandlungen",
    },
    "strict": {
        "name": "Strikte KI",
        "icon": "📏",
        "verhalten": "Akzeptierte nur Angebote ≥50% und bestand als Proposer auf hohen Gegenangeboten (30–45%). Maximale Fairnessforderung.",
        "gegencheck": "Als Proposer: mindestens 50% anbieten. Als Responder: niedrige Angebote ruhig ablehnen – du hast Prinzipien.",
        "lesson_slug": "fairness-effekte",
        "lesson_title": "Fairness-Effekte in Verhandlungen",
    },
    "strategic": {
        "name": "Strategische KI",
        "icon": "📈",
        "verhalten": "Lernte aus den Runden: Akzeptierte mit der Zeit immer niedrigere Angebote. Als Proposer: begann hoch und senkte schrittweise.",
        "gegencheck": "Früh niedrige Angebote testen – die Akzeptanzschwelle sinkt mit der Zeit. Das ist Rubinstein-Zeitdruck in Aktion.",
        "lesson_slug": "rubinstein-bargaining",
        "lesson_title": "Rubinstein Bargaining & Zeitdruck",
    },
}

TRUST_STRATEGY_POOL = ["reciprocal", "selfish", "cooperative"]

TRUST_STRATEGY_INFO = {
    "reciprocal": {
        "name": "Reziproke KI",
        "icon": "🔁",
        "verhalten": "Gab proportional zurück – im Schnitt 50–60% des Topfes. Vertrauen wird fair belohnt, aber nicht üppig.",
        "gegencheck": "Viel investieren lohnt sich: Jeder investierte Punkt bringt ~0,5–0,8 zurück. Hohe Investitionen ergeben positiven Netto-Gewinn.",
        "lesson_slug": "wiederholte-spiele-reputation",
        "lesson_title": "Wiederholte Spiele & Reputation",
    },
    "selfish": {
        "name": "Egoistische KI",
        "icon": "💰",
        "verhalten": "Behielt fast alles – gab nur 0–20% des Topfes zurück. Jede Investition war ein Verlust für dich.",
        "gegencheck": "Gegen eine egoistische KI: minimal investieren (0–1). Du kannst ihr Verhalten nicht ändern – erkenne es früh.",
        "lesson_slug": "informationsasymmetrie-signaling",
        "lesson_title": "Informationsasymmetrie",
    },
    "cooperative": {
        "name": "Kooperative KI",
        "icon": "🤝",
        "verhalten": "Gab großzügig zurück – 55–70% des Topfes. Langfristige Kooperation wurde reich belohnt.",
        "gegencheck": "Maximiere deine Investitionen – jeder investierte Punkt bringt ~0,6–1,1 zurück. Voller Einsatz ist optimal.",
        "lesson_slug": "wiederholte-spiele-reputation",
        "lesson_title": "Wiederholte Spiele & Reputation",
    },
}

CHICKEN_STRATEGY_POOL = ["aggressive", "dove", "adaptive", "mixed"]

CHICKEN_STRATEGY_INFO = {
    "aggressive": {
        "name": "Aggressive KI",
        "icon": "🔥",
        "verhalten": "Hat in jeder Runde gehalten – kompromisslos. Maximaler Druck, maximales Crash-Risiko.",
        "gegencheck": "Gegen immer-Halten: du musst ausweichen um Crashes zu vermeiden. Aber: gegen echte Aggression hat Nachgeben einen Preis.",
        "lesson_slug": "feiglingsspiel-chicken-game",
        "lesson_title": "Feiglingsspiel & Brinkmanship",
    },
    "dove": {
        "name": "Taube KI",
        "icon": "🕊️",
        "verhalten": "Hat immer ausgewichen – vermied jeden Konflikt. Leicht ausnutzbar durch konsequentes Halten.",
        "gegencheck": "Immer halten maximiert deinen Score. Aber: im echten Verhandlungsleben gibt es selten echte 'Tauben'.",
        "lesson_slug": "feiglingsspiel-chicken-game",
        "lesson_title": "Feiglingsspiel & Brinkmanship",
    },
    "adaptive": {
        "name": "Adaptive KI",
        "icon": "🧠",
        "verhalten": "Beobachtete dein Ausweichmuster und hielt dagegen: Je mehr du ausgewichen bist, desto aggressiver wurde sie.",
        "gegencheck": "Unberechenbar spielen – wenn die KI dein Muster kennt, exploitiert sie es. Manchmal halten, manchmal ausweichen.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "mixed": {
        "name": "Nash-Gleichgewicht-KI",
        "icon": "⚖️",
        "verhalten": "Spielte die theoretische Nash-Gleichgewichtsstrategie: ~40% Halten, ~60% Ausweichen – zufällig gemischt.",
        "gegencheck": "Auch du solltest mischen. Das Nash-GGW im Chicken Game ist eine gemischte Strategie – keine reine ist stabil.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
}

PUBLIC_GOODS_STRATEGY_POOL = ["cooperative", "free_rider", "conditional", "punisher"]

PUBLIC_GOODS_STRATEGY_INFO = {
    "cooperative": {
        "name": "Kooperative KI",
        "icon": "🌱",
        "verhalten": "Zahlte konstant viel ein (7–9 Token). Unabhängig von deinem Verhalten – altruistisch oder naiv?",
        "gegencheck": "Gegen eine kooperative KI lohnt sich Trittbrettfahren kurzfristig – aber zerstört langfristig das kollektive Optimum.",
        "lesson_slug": "oeffentliche-gueter-kollektivgut",
        "lesson_title": "Öffentliche Güter & Trittbrettfahrerproblem",
    },
    "free_rider": {
        "name": "Trittbrettfahrer-KI",
        "icon": "🛹",
        "verhalten": "Zahlte fast nichts ein (0–2 Token) und lebte von deinen Beiträgen. Maximale Ausbeutung des Gemeinwohls.",
        "gegencheck": "Wenn du auch wenig einzahlst, kollabiert das System. Optimal: früh wenig beitragen und schauen ob sie reagiert.",
        "lesson_slug": "oeffentliche-gueter-kollektivgut",
        "lesson_title": "Öffentliche Güter & Trittbrettfahrerproblem",
    },
    "conditional": {
        "name": "Konditionale KI",
        "icon": "🔄",
        "verhalten": "Spiegelte deinen letzten Beitrag mit kleinem Rauschen. Fairness wird mit Fairness beantwortet.",
        "gegencheck": "Viel einzahlen triggert hohe Gegenleistung. Das ist das Reziprozitätsprinzip in Aktion.",
        "lesson_slug": "tit-for-tat",
        "lesson_title": "Tit-for-Tat – Die beste Strategie?",
    },
    "punisher": {
        "name": "Bestrafer-KI",
        "icon": "⚡",
        "verhalten": "Zahlte viel ein solange du kooperiert hast – und zog sich sofort zurück wenn du wenig beigetragen hast.",
        "gegencheck": "Konsequent viel einzahlen (≥5) wird belohnt. Trittbrettfahren wird sofort bestraft – Grim Trigger für öffentliche Güter.",
        "lesson_slug": "oeffentliche-gueter-kollektivgut",
        "lesson_title": "Öffentliche Güter & Trittbrettfahrerproblem",
    },
}


def _gd_player_analysis(history: list[dict]) -> dict:
    """Analysiert das Spielerverhalten im Gefangenendilemma für den Debrief."""
    coop_rate = sum(1 for r in history if r["player"] == "C") / len(history)
    first_defect = next((r["round"] for r in history if r["player"] == "D"), None)
    if coop_rate >= 0.9:
        pattern = "Du hast fast immer kooperiert – sehr kooperativ, aber leicht ausnutzbar."
    elif coop_rate >= 0.6:
        pattern = "Du hast überwiegend kooperiert – eine solide, aber vorhersehbare Strategie."
    elif coop_rate >= 0.4:
        pattern = "Du hast gemischt gespielt – schwer zu lesen, aber möglicherweise inkonsistent."
    elif coop_rate >= 0.1:
        pattern = "Du hast überwiegend verraten – kurzfristig profitabel, langfristig reputationsschädlich."
    else:
        pattern = "Du hast fast immer verraten – maximaler kurzfristiger Gewinn, null Kooperation."
    return {
        "coop_rate": round(coop_rate * 100),
        "first_defect": first_defect,
        "pattern": pattern,
    }


def _gd_evaluate_response(strategy: str, history: list[dict]) -> dict:
    """
    Bewertet ob der Spieler optimal auf die KI-Strategie reagiert hat.
    Gibt 'win' wenn die Gegenstrategie korrekt war – unabhängig von den Rohpunkten.
    """
    coop_rate = sum(1 for r in history if r["player"] == "C") / len(history)
    defect_rate = 1 - coop_rate

    if strategy == "always_defect":
        # Dominante Strategie: Gegner muss ebenfalls verraten
        if defect_rate >= 0.70:
            return {
                "result": "win",
                "title": "Optimale Gegenstrategie gespielt!",
                "explanation": "Gegen 'Immer Verraten' ist konsequentes Verraten die einzig rationale Antwort (DD = 1/1). Du hast nicht in die Kooperationsfalle getappt – das ist das spieltheoretisch korrekte Verhalten.",
            }
        elif defect_rate >= 0.45:
            return {
                "result": "draw",
                "title": "Teilweise richtig reagiert",
                "explanation": "Du hast häufig verraten, aber auch zu oft kooperiert. Gegen eine Strategie die niemals kooperiert, bringt deine Kooperation nur 0 Punkte – konsequentes Verraten wäre besser gewesen.",
            }
        else:
            return {
                "result": "loss",
                "title": "Kooperationsfalle: Gegenstrategie nicht erkannt",
                "explanation": "Du hast oft kooperiert – gegen eine KI, die immer verrät. Das Ergebnis: du bekommst 0 statt 1 pro Kooperationsrunde. Die optimale Antwort auf 'Immer Verraten' ist immer zu verraten.",
            }

    elif strategy == "always_cooperate":
        if defect_rate >= 0.65:
            return {
                "result": "win",
                "title": "Strategie erkannt und optimal ausgenutzt!",
                "explanation": "'Immer Kooperieren' ist vollständig ausbeutbar. Du hast die Schwäche erkannt und die spieltheoretisch dominante Antwort gespielt – Verraten bringt 5 statt 3 pro Runde.",
            }
        elif coop_rate >= 0.80:
            return {
                "result": "draw",
                "title": "Gegenseitige Kooperation – fair, aber nicht optimal",
                "explanation": "Beide haben kooperiert (CC = 3/3 je Runde). Sozial fair – aber du hättest durch Verraten mehr herausholen können. Für das Erkennen eines Musters ist das trotzdem gut.",
            }
        else:
            return {
                "result": "loss",
                "title": "Kein klares Muster erkannt",
                "explanation": "Gegen eine immer-kooperierende KI wäre entweder konsequentes Ausnutzen (Verraten, 5/Runde) oder dauerhaftes Kooperieren (3/Runde) die richtige Strategie. Inkonsistenz verschenkt Potenzial.",
            }

    elif strategy == "tit_for_tat":
        if coop_rate >= 0.80:
            return {
                "result": "win",
                "title": "Perfekt! Dauerkooperation gegen Tit-for-Tat",
                "explanation": "Tit-for-Tat belohnt Kooperation sofort und bestraft Verrat sofort. Deine dauerhafteKooperation hat das gemeinsame Optimum herbeigeführt: CC = 3/3 pro Runde, das Maximum was beide erzielen können.",
            }
        elif coop_rate >= 0.55:
            return {
                "result": "draw",
                "title": "Überwiegend gut – Verratrunden haben Punkte gekostet",
                "explanation": "Die kooperativen Phasen waren optimal. Aber jedes Mal wenn du verraten hast, hat TfT sofort gespiegelt – Vergeltungszyklen kosten beide Seiten Punkte. Mehr Kooperation wäre besser gewesen.",
            }
        else:
            return {
                "result": "loss",
                "title": "Vergeltungsspirale: TfT hat dein Verraten gespiegelt",
                "explanation": "Tit-for-Tat spiegelt jeden Zug. Dein häufiges Verraten hat permanente Vergeltung ausgelöst (DD = 1/1). Ein kooperativer Start und konsequente Kooperation hätten CC = 3/3 pro Runde ermöglicht.",
            }

    elif strategy == "grim_trigger":
        player_defected = any(r["player"] == "D" for r in history)
        if not player_defected:
            return {
                "result": "win",
                "title": "Perfekt! Grim Trigger nie ausgelöst",
                "explanation": "Du hast kein einziges Mal verraten – damit hast du das einzig gute Gleichgewicht (CC = 3/3 je Runde) über alle 10 Runden aufrechterhalten. Grim Trigger bestraft jeden Fehler dauerhaft.",
            }
        elif coop_rate >= 0.85:
            return {
                "result": "draw",
                "title": "Fast optimal – ein Ausrutscher hat Grim Trigger ausgelöst",
                "explanation": "Du hast nur einmal verraten – aber das hat Grim Trigger dauerhaft aktiviert. Diese Strategie verzeiht nicht: ein einziger Fehler macht den Unterschied zwischen CC und DD für alle Folgerunden.",
            }
        else:
            return {
                "result": "loss",
                "title": "Grim Trigger ausgelöst – irreversibler Schaden",
                "explanation": "Nach deinem ersten Verrat hat Grim Trigger auf dauerhaftes Verraten umgeschaltet. Es gab keine zweite Chance mehr. Das ist die Drohkraft dieser Strategie – und warum sie so mächtig ist.",
            }

    elif strategy == "random":
        if coop_rate >= 0.40:
            return {
                "result": "win",
                "title": "Gute Reaktion auf eine unlesbare Strategie",
                "explanation": "Gegen echten Zufall gibt es keine perfekte Gegenstrategie. Kooperation hat im Erwartungswert leicht mehr Ertrag. Du hast solide gespielt – mehr lässt sich gegen Unberechenbarkeit nicht tun.",
            }
        else:
            return {
                "result": "draw",
                "title": "Gegen Zufall ist jede Strategie gleich gut",
                "explanation": "Eine Zufalls-KI lässt sich nicht lesen und nicht beeinflussen. Dein Spielmuster ist in Ordnung – kooperativer wäre im Schnitt leicht besser, aber der Unterschied ist gering.",
            }

    elif strategy == "adaptive_exploiter":
        if 0.25 <= coop_rate <= 0.65:
            return {
                "result": "win",
                "title": "Unberechenbar gespielt – Adaptive KI ausgehebelt!",
                "explanation": "Die Adaptive KI liest Verhaltensmuster und exploitiert sie. Dein gemischtes Spiel hat ihr keine stabile Grundlage gegeben. Das ist genau die richtige Gegenstrategie: unberechenbar bleiben.",
            }
        elif coop_rate > 0.75:
            return {
                "result": "loss",
                "title": "Zu berechenbar kooperativ – Adaptive KI hat ausgenutzt",
                "explanation": "Die KI hat erkannt, dass du häufig kooperierst, und hat auf Ausbeuten umgeschaltet. Gegen Adaptive KI ist Unberechenbarkeit (gemischtes Spielen) die einzig wirksame Strategie.",
            }
        else:
            return {
                "result": "draw",
                "title": "Zu defensiv – Potenzial nicht ausgeschöpft",
                "explanation": "Dein überwiegendes Verraten hat die Adaptive KI zwar verwirrt, aber auch dein eigenes Ergebnis gedrückt. Mehr gemischtes Spiel (C und D wechseln) wäre langfristig effizienter.",
            }

    return {"result": "draw", "title": "Spiel beendet", "explanation": ""}


# ---------------------------------------------------------------------------
# Spielübersicht
# ---------------------------------------------------------------------------

GAME_META = [
    {
        "id": "gefangenendilemma",
        "name": "Gefangenendilemma",
        "icon": "🔒",
        "beschreibung": "Kooperieren oder Verraten? Das Kernspiel der Spieltheorie – direkt relevant für jede Verhandlung.",
        "schwierigkeit": "Einsteiger",
        "runden": 10,
        "konzept": "Dominante Strategien, Tit-for-Tat",
    },
    {
        "id": "ultimatum",
        "name": "Ultimatumspiel",
        "icon": "⚖️",
        "beschreibung": "Mache faire Angebote – oder riskiere, dass alles abgelehnt wird. Fairness hat ihren Preis.",
        "schwierigkeit": "Einsteiger",
        "runden": 10,
        "konzept": "Fairness, Ankern, Verlustangst",
    },
    {
        "id": "vertrauen",
        "name": "Vertrauensspiel",
        "icon": "🤝",
        "beschreibung": "Investiere Vertrauen – und sieh, ob es zurückkommt. Die Grundlage jeder Kooperationsverhandlung.",
        "schwierigkeit": "Einsteiger",
        "runden": 8,
        "konzept": "Vertrauen, Reziprozität, Reputation",
    },
    {
        "id": "verhandlung",
        "name": "Verhandlungssimulation",
        "icon": "💼",
        "beschreibung": "Mehrrunden-Verhandlung mit echten Szenarien. Nutze BATNA, ZOPA und Zeitdruck-Strategien.",
        "schwierigkeit": "Fortgeschritten",
        "runden": 6,
        "konzept": "BATNA, ZOPA, Rubinstein Bargaining",
    },
    {
        "id": "chicken",
        "name": "Feiglingsspiel",
        "icon": "🚗",
        "beschreibung": "Halten oder ausweichen? Das Brinkmanship-Spiel zeigt, wie Commitment-Strategien und Drohungen wirken.",
        "schwierigkeit": "Einsteiger",
        "runden": 8,
        "konzept": "Brinkmanship, Commitment, Drohungen",
    },
    {
        "id": "public-goods",
        "name": "Öffentliche-Güter-Spiel",
        "icon": "🏛️",
        "beschreibung": "Wie viel trägst du zum Gemeinwohl bei? Erlebe das Trittbrettfahrerproblem und Gruppenkooperation.",
        "schwierigkeit": "Einsteiger",
        "runden": 8,
        "konzept": "Trittbrettfahrer, Kollektivgut, soziale Normen",
    },
    {
        "id": "beauty-contest",
        "name": "Schönheitswettbewerb",
        "icon": "🎯",
        "beschreibung": "Rate 0–100: Wer ist am nächsten zu 2/3 des Durchschnitts? Das klassische K-Level-Thinking-Experiment.",
        "schwierigkeit": "Fortgeschritten",
        "runden": 6,
        "konzept": "K-Level Thinking, rationale Erwartungen",
    },
    {
        "id": "stag-hunt",
        "name": "Hirschjagd",
        "icon": "🦌",
        "beschreibung": "Jagst du den Hirsch (riskant, hoher Lohn) oder den Hasen (sicher, niedriger Lohn)? Das Koordinationsdilemma.",
        "schwierigkeit": "Einsteiger",
        "runden": 8,
        "konzept": "Koordination, Risikodominanz, Gleichgewichtsauswahl",
    },
    {
        "id": "centipede",
        "name": "Centipede-Spiel",
        "icon": "🐛",
        "beschreibung": "Nehmen oder weitergeben? Rückwärtsinduktion sagt: sofort nehmen. Aber lohnt sich Vertrauen doch?",
        "schwierigkeit": "Fortgeschritten",
        "runden": 4,
        "konzept": "Rückwärtsinduktion, Backward Induction Paradox",
    },
    {
        "id": "rps",
        "name": "Schere-Stein-Papier",
        "icon": "✂️",
        "beschreibung": "Das einfachste Nullsummenspiel – aber warum gewinnt eine rein zufällige Strategie langfristig?",
        "schwierigkeit": "Einsteiger",
        "runden": 7,
        "konzept": "Gemischte Strategien, Nash-Gleichgewicht, Nullsummenspiele",
    },
    {
        "id": "koordination",
        "name": "Koordinationsspiel",
        "icon": "🤝",
        "beschreibung": "Du und die KI möchten sich treffen – aber ihr habt verschiedene Lieblingsoptionen. Wer gibt nach?",
        "schwierigkeit": "Einsteiger",
        "runden": 8,
        "konzept": "Koordinationsdilemma, multiple Nash-Gleichgewichte, Focal Points",
    },
    {
        "id": "auktion",
        "name": "Vickrey-Auktion",
        "icon": "🔨",
        "beschreibung": "Biete auf Objekte mit geheimem Wert. Die spieltheoretische Lösung ist überraschend einfach.",
        "schwierigkeit": "Fortgeschritten",
        "runden": 5,
        "konzept": "Dominante Strategien, Zweitpreisauktion, Wahrheitsaussage",
    },
    {
        "id": "diktator",
        "name": "Diktatorspiel",
        "icon": "👑",
        "beschreibung": "Teile 100 Punkte auf – ohne dass dein Gegenüber ablehnen kann. Bist du großzügig, wenn es keine Konsequenzen gibt?",
        "schwierigkeit": "Einsteiger",
        "runden": 8,
        "konzept": "Fairness, Altruismus, soziale Präferenzen",
    },
    {
        "id": "dollarauktion",
        "name": "Dollarauktion",
        "icon": "💸",
        "beschreibung": "Versteigere 1€ – aber beide Bieter zahlen. Wie weit eskaliert du, bevor du aufgibst?",
        "schwierigkeit": "Fortgeschritten",
        "runden": "variabel",
        "konzept": "Sunk Cost, Eskalation, Commitment Trap",
    },
    {
        "id": "minderheit",
        "name": "Minderheitsspiel",
        "icon": "🔢",
        "beschreibung": "Wähle A oder B. Wer in der Minderheit liegt, gewinnt. 7 Spieler, keine Kommunikation – ein Koordinationsproblem.",
        "schwierigkeit": "Fortgeschritten",
        "runden": 8,
        "konzept": "El Farol Problem, Minderheitskoordination, Emergenz",
    },
    {
        "id": "habicht-taube",
        "name": "Habicht-Taube-Spiel",
        "icon": "🦅",
        "beschreibung": "Sei aggressiv (Habicht) oder nachgebend (Taube)? Das Grundmodell der evolutionären Spieltheorie zeigt, warum Aggressivität nicht immer gewinnt.",
        "schwierigkeit": "Fortgeschritten",
        "runden": 10,
        "konzept": "Evolutionär Stabile Strategie, ESS, Hawk-Dove",
    },
    {
        "id": "geschlechter-kampf",
        "name": "Koordinationsdilemma",
        "icon": "🎭",
        "beschreibung": "Zwei Spieler wollen zusammen sein, bevorzugen aber verschiedene Aktivitäten. Wer gibt nach? Das klassische Battle-of-the-Sexes-Modell.",
        "schwierigkeit": "Einsteiger",
        "runden": 8,
        "konzept": "Multiple Nash-Gleichgewichte, Koordination, gemischte Strategien",
    },
    {
        "id": "freiwilligen-dilemma",
        "name": "Freiwilligen-Dilemma",
        "icon": "🙋",
        "beschreibung": "Jemand muss sich opfern – aber wer? 5 Spieler, eine unangenehme Aufgabe. Das Volunteer's Dilemma zeigt die Logik des Trittbrettfahrens.",
        "schwierigkeit": "Fortgeschritten",
        "runden": 8,
        "konzept": "Freiwilligen-Dilemma, Trittbrettfahrer, Gruppenentscheidung",
    },
    {
        "id": "gleiche-muenzen",
        "name": "Gleiche Münzen",
        "icon": "🪙",
        "beschreibung": "Wähle Kopf oder Zahl. Das reinste Nullsummenspiel der Spieltheorie – kein Nash-Gleichgewicht in reinen Strategien. Nur Zufall gewinnt.",
        "schwierigkeit": "Einsteiger",
        "runden": 10,
        "konzept": "Nullsummenspiel, Gemischte Strategien, Minimax",
    },
    {
        "id": "gewinner-fluch",
        "name": "Der Fluch des Gewinners",
        "icon": "🏆",
        "beschreibung": "Biete auf ein Objekt mit unbekanntem Wert. Wer gewinnt, hat meist zu viel geboten – der Fluch des Gewinners trifft fast jeden.",
        "schwierigkeit": "Fortgeschritten",
        "runden": 5,
        "konzept": "Fluch des Gewinners, Common Value Auction, Bayesianisches Schließen",
    },
]


@router.get("", response_class=HTMLResponse)
def spiele_overview(request: Request):
    return templates.TemplateResponse(
        request,
        "spiele.html",
        {"active_page": "spiele", "games": GAME_META},
    )


# ---------------------------------------------------------------------------
# Gefangenendilemma
# ---------------------------------------------------------------------------

GD_STRATEGIES = [
    {"id": "tit_for_tat", "name": "Tit-for-Tat", "desc": "Kopiert deinen letzten Zug. Die erfolgreichste bekannte Strategie (Axelrod)."},
    {"id": "always_cooperate", "name": "Immer Kooperieren", "desc": "Kooperiert immer – leicht ausnutzbar."},
    {"id": "always_defect", "name": "Immer Verraten", "desc": "Verrät immer – maximiert kurzfristigen Gewinn."},
    {"id": "grim_trigger", "name": "Grim Trigger", "desc": "Kooperiert, bis du einmal verrätst – dann verrät sie für immer."},
    {"id": "random", "name": "Zufällig", "desc": "Spielt zufällig – unvorhersehbar."},
]


@router.get("/gefangenendilemma", response_class=HTMLResponse)
def gefangenendilemma_page(request: Request):
    hidden_strategy = _random.choices(GD_STRATEGY_POOL, weights=GD_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/gefangenendilemma.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "max_rounds": 10,
        },
    )


@router.post("/gefangenendilemma/zug", response_class=HTMLResponse)
def gefangenendilemma_zug(
    request: Request,
    move: str = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = gd_play_round(move, strategy, history)
    history.append(round_result)

    is_final = len(history) >= 10
    final = gd_final_result(history) if is_final else None

    strategy_info = None
    player_analysis = None
    evaluation = None
    new_achievements: list = []
    if is_final and final:
        evaluation = _gd_evaluate_response(strategy, history)
        _, new_achievements = save_game_session(
            db,
            game_type="gefangenendilemma",
            ai_strategy=strategy,
            moves=history,
            result=evaluation["result"],   # strategy-quality result, not raw points
            score=final["player_total"],
            ai_score=final["ai_total"],
        )
        strategy_info = GD_STRATEGY_INFO.get(strategy)
        player_analysis = _gd_player_analysis(history)

    return templates.TemplateResponse(
        request,
        "partials/gd_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 10,
            "strategy_info": strategy_info,
            "player_analysis": player_analysis,
            "evaluation": evaluation,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Ultimatumspiel
# ---------------------------------------------------------------------------

ULTIMATUM_STRATEGIES = [
    {"id": "fair", "name": "Fair", "desc": "Akzeptiert Angebote ≥ 40%. Orientiert an experimentellen Fairness-Normen."},
    {"id": "strict", "name": "Streng", "desc": "Akzeptiert nur Angebote ≥ 50%. Besteht auf Gleichverteilung."},
    {"id": "strategic", "name": "Strategisch", "desc": "Lernt aus Runden – akzeptiert mit der Zeit auch niedrigere Angebote."},
]


@router.get("/ultimatum", response_class=HTMLResponse)
def ultimatum_page(request: Request):
    hidden_strategy = _random.choice(ULTIMATUM_STRATEGY_POOL)
    return templates.TemplateResponse(
        request,
        "games/ultimatum.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "max_rounds": 10,
        },
    )


@router.post("/ultimatum/zug", response_class=HTMLResponse)
def ultimatum_zug(
    request: Request,
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    # Proposer-Modus: Spieler macht Angebot
    player_offer: int | None = Form(default=None),
    # Responder-Modus: KI macht Angebot, Spieler antwortet
    player_response: str | None = Form(default=None),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_num = len(history)
    is_proposer = round_num < 5

    if is_proposer and player_offer is not None:
        response = ultimatum_ai_response(player_offer, strategy, round_num)
        p_score, ai_score = ultimatum_score(player_offer, response["accepts"], is_proposer=True)
        entry = {
            "round": round_num + 1,
            "role": "proposer",
            "offer": player_offer,
            "accepted": response["accepts"],
            "reason": response["reason"],
            "player_score": p_score,
            "ai_score": ai_score,
        }
    else:
        ai_offer = ultimatum_ai_offer(strategy, round_num)
        accepted = player_response == "accept"
        p_score, ai_score = ultimatum_score(ai_offer, accepted, is_proposer=False)
        entry = {
            "round": round_num + 1,
            "role": "responder",
            "offer": ai_offer,
            "accepted": accepted,
            "player_score": p_score,
            "ai_score": ai_score,
        }

    history.append(entry)
    is_final = len(history) >= 10

    total_player = sum(r["player_score"] for r in history)
    total_ai = sum(r["ai_score"] for r in history)

    strategy_info = None
    new_achievements: list = []
    efficiency = 0
    proposer_accepted = proposer_total = responder_accepted = responder_total = 0
    result = None

    if is_final:
        proposer_rounds = [r for r in history if r["role"] == "proposer"]
        responder_rounds = [r for r in history if r["role"] == "responder"]
        proposer_accepted = sum(1 for r in proposer_rounds if r["accepted"])
        proposer_total = len(proposer_rounds)
        responder_accepted = sum(1 for r in responder_rounds if r["accepted"])
        responder_total = len(responder_rounds)
        # Effizienz: Anteil der maximal möglichen Punkte (10 Runden × 50 Punkte pro Runde)
        max_possible = 500
        efficiency = round(total_player / max_possible * 100)
        result = "win" if efficiency >= 55 else ("draw" if efficiency >= 30 else "loss")
        _, new_achievements = save_game_session(
            db,
            game_type="ultimatum",
            ai_strategy=strategy,
            moves=history,
            result=result,
            score=total_player,
            ai_score=total_ai,
        )
        strategy_info = ULTIMATUM_STRATEGY_INFO.get(strategy)

    next_is_proposer = len(history) < 5

    return templates.TemplateResponse(
        request,
        "partials/ultimatum_result.html",
        {
            "entry": entry,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "result": result,
            "total_player": total_player,
            "total_ai": total_ai,
            "efficiency": efficiency,
            "proposer_accepted": proposer_accepted,
            "proposer_total": proposer_total,
            "responder_accepted": responder_accepted,
            "responder_total": responder_total,
            "next_is_proposer": next_is_proposer,
            "next_ai_offer": ultimatum_ai_offer(strategy, len(history)) if not next_is_proposer else None,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Vertrauensspiel
# ---------------------------------------------------------------------------

TRUST_STRATEGIES = [
    {"id": "reciprocal", "name": "Reziprok", "desc": "Gibt proportional zurück – Vertrauen wird belohnt (~50%)."},
    {"id": "selfish", "name": "Egoistisch", "desc": "Behält fast alles – ein realistisches Szenario."},
    {"id": "cooperative", "name": "Kooperativ", "desc": "Gibt großzügig zurück (~60%) – fördert Vertrauen."},
]


@router.get("/vertrauen", response_class=HTMLResponse)
def vertrauen_page(request: Request):
    hidden_strategy = _random.choice(TRUST_STRATEGY_POOL)
    return templates.TemplateResponse(
        request,
        "games/vertrauen.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "max_rounds": 8,
        },
    )


@router.post("/vertrauen/zug", response_class=HTMLResponse)
def vertrauen_zug(
    request: Request,
    invested: int = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    result = trust_ai_return(invested, strategy)
    history.append(result)

    is_final = len(history) >= 8
    final = trust_final_result(history) if is_final else None

    strategy_info = None
    new_achievements: list = []
    if is_final and final:
        _, new_achievements = save_game_session(
            db,
            game_type="vertrauen",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=max(0, final["player_net"]),
            ai_score=max(0, final["ai_net"]),
        )
        strategy_info = TRUST_STRATEGY_INFO.get(strategy)

    return templates.TemplateResponse(
        request,
        "partials/trust_result.html",
        {
            "round_result": result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "cumulative_player": sum(r["player_net"] for r in history),
            "cumulative_ai": sum(r["ai_net"] for r in history),
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Verhandlungssimulation
# ---------------------------------------------------------------------------


@router.get("/verhandlung", response_class=HTMLResponse)
def verhandlung_page(request: Request):
    return templates.TemplateResponse(
        request,
        "games/verhandlung.html",
        {
            "active_page": "spiele",
            "scenarios": SCENARIOS,
        },
    )


@router.post("/verhandlung/zug", response_class=HTMLResponse)
def verhandlung_zug(
    request: Request,
    scenario_key: str = Form(...),
    player_offer: int = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    scenario = SCENARIOS[scenario_key]
    round_num = len(history)

    last_player = history[-1]["player_offer"] if history else None
    ai_result = verhandlung_ai_offer(scenario, round_num, player_offer)

    entry = {
        "round": round_num + 1,
        "player_offer": player_offer,
        "ai_offer": ai_result["offer"],
        "deal": ai_result["deal"],
        "final_price": ai_result["final_price"],
    }
    history.append(entry)

    is_final = ai_result["deal"] or len(history) >= scenario["max_rounds"]
    score_data = None

    new_achievements: list = []
    if is_final:
        final_price = ai_result["final_price"] or round((player_offer + ai_result["offer"]) / 2)
        score_data = verhandlung_score(scenario, final_price, round_num)
        _, new_achievements = save_game_session(
            db,
            game_type="verhandlung",
            ai_strategy="nash_rubinstein",
            moves=history,
            result="win" if score_data["grade"] in ("A", "B") else "loss",
            score=score_data["score"],
            ai_score=100 - score_data["score"],
            scenario=scenario_key,
        )

    return templates.TemplateResponse(
        request,
        "partials/verhandlung_result.html",
        {
            "entry": entry,
            "history": history,
            "history_json": json.dumps(history),
            "scenario_key": scenario_key,
            "scenario": scenario,
            "is_final": is_final,
            "score_data": score_data,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Feiglingsspiel (Chicken Game)
# ---------------------------------------------------------------------------

CHICKEN_STRATEGIES = [
    {"id": "aggressive", "name": "Aggressiv", "desc": "Hält immer durch – maximaler Druck, maximales Risiko."},
    {"id": "dove", "name": "Taube", "desc": "Weicht immer aus – vermeidet Konflikte, leicht ausnutzbar."},
    {"id": "adaptive", "name": "Adaptiv", "desc": "Lernt aus deinem Verhalten – nutzt deine Muster gegen dich."},
    {"id": "mixed", "name": "Nash-Gemischt", "desc": "Spielt die theoretische Nash-Gleichgewichtsstrategie (~60% ausweichen)."},
]


@router.get("/chicken", response_class=HTMLResponse)
def chicken_page(request: Request):
    hidden_strategy = _random.choice(CHICKEN_STRATEGY_POOL)
    return templates.TemplateResponse(
        request,
        "games/chicken.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "max_rounds": 8,
        },
    )


@router.post("/chicken/zug", response_class=HTMLResponse)
def chicken_zug(
    request: Request,
    move: str = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = chicken_play_round(move, strategy, history)
    history.append(round_result)

    is_final = len(history) >= 8
    final = chicken_final_result(history) if is_final else None

    strategy_info = None
    new_achievements: list = []
    if is_final and final:
        _, new_achievements = save_game_session(
            db,
            game_type="chicken",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=max(0, final["player_total"]),
            ai_score=max(0, final["ai_total"]),
        )
        strategy_info = CHICKEN_STRATEGY_INFO.get(strategy)

    return templates.TemplateResponse(
        request,
        "partials/chicken_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 8,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Öffentliche-Güter-Spiel (Public Goods Game)
# ---------------------------------------------------------------------------

PUBLIC_GOODS_STRATEGIES = [
    {"id": "cooperative", "name": "Kooperativ", "desc": "Trägt viel bei (7–9 von 10) – fördert das Gemeinwohl."},
    {"id": "free_rider", "name": "Trittbrettfahrer", "desc": "Trägt kaum bei (0–2) – profitiert von deinen Beiträgen."},
    {"id": "conditional", "name": "Konditional", "desc": "Spiegelt deinen letzten Beitrag – Fairness bedingt Fairness."},
    {"id": "punisher", "name": "Bestrafer", "desc": "Trägt viel bei solange du kooperierst, zieht sich zurück wenn du trittbrettfährst."},
]


@router.get("/public-goods", response_class=HTMLResponse)
def public_goods_page(request: Request):
    hidden_strategy = _random.choice(PUBLIC_GOODS_STRATEGY_POOL)
    return templates.TemplateResponse(
        request,
        "games/public_goods.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "max_rounds": 8,
            "tokens_per_round": 10,
        },
    )


@router.post("/public-goods/zug", response_class=HTMLResponse)
def public_goods_zug(
    request: Request,
    contribution: int = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = public_goods_play_round(contribution, strategy, history)
    history.append(round_result)

    is_final = len(history) >= 8
    final = public_goods_final_result(history) if is_final else None

    strategy_info = None
    new_achievements: list = []
    if is_final and final:
        _, new_achievements = save_game_session(
            db,
            game_type="public_goods",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=int(final["player_total"]),
            ai_score=int(final["ai_total"]),
        )
        strategy_info = PUBLIC_GOODS_STRATEGY_INFO.get(strategy)

    return templates.TemplateResponse(
        request,
        "partials/public_goods_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 8,
            "tokens_per_round": 10,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Schönheitswettbewerb (Beauty Contest / K-Level Thinking)
# ---------------------------------------------------------------------------

BEAUTY_STRATEGY_POOL = ["level_0", "level_1", "level_2", "adaptive"]
BEAUTY_STRATEGY_WEIGHTS = [15, 25, 30, 30]

BEAUTY_STRATEGY_INFO = {
    "level_0": {
        "name": "Level-0 KI",
        "icon": "🎲",
        "verhalten": "Würfelte zufällig (0–100) – kein strategisches Denken. Durchschnitt der Gruppe lag daher nahe 50, Ziel nahe 33.",
        "gegencheck": "Gegen Level-0-Spieler: konsequent 33 raten. Das liegt näher am Ziel als jede andere feste Zahl.",
        "lesson_slug": "k-level-thinking",
        "lesson_title": "K-Level Thinking & rationale Erwartungen",
    },
    "level_1": {
        "name": "Level-1 KI",
        "icon": "🧮",
        "verhalten": "Nahm an, alle spielen zufällig (Schnitt 50), und riet 2/3 davon ≈ 33. Ein Denkschritt voraus.",
        "gegencheck": "Gegen Level-1-Spieler: 22 raten (2/3 von 33). Du brauchst einen Schritt mehr als sie.",
        "lesson_slug": "k-level-thinking",
        "lesson_title": "K-Level Thinking & rationale Erwartungen",
    },
    "level_2": {
        "name": "Level-2 KI",
        "icon": "🧠",
        "verhalten": "Nahm an, alle spielen Level-1 (≈33), und riet 2/3 davon ≈ 22. Zwei Denkschritte voraus.",
        "gegencheck": "Gegen Level-2-Spieler: 15 raten. Das Nash-Gleichgewicht liegt bei 0 – aber niemand spielt wirklich dorthin.",
        "lesson_slug": "k-level-thinking",
        "lesson_title": "K-Level Thinking & rationale Erwartungen",
    },
    "adaptive": {
        "name": "Adaptive KI",
        "icon": "📈",
        "verhalten": "Lernte aus vergangenen Gewinnzahlen und passte ihre Rate schrittweise an. Konvergiert gegen das reale Gleichgewicht.",
        "gegencheck": "Beobachte die tatsächlichen Zielzahlen über Runden. Das Muster zeigt dir das echte Denkniveau der Gegner.",
        "lesson_slug": "k-level-thinking",
        "lesson_title": "K-Level Thinking & rationale Erwartungen",
    },
}


@router.get("/beauty-contest", response_class=HTMLResponse)
def beauty_contest_page(request: Request):
    hidden_strategy = _random.choices(BEAUTY_STRATEGY_POOL, weights=BEAUTY_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/beauty_contest.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "max_rounds": 6,
        },
    )


@router.post("/beauty-contest/zug", response_class=HTMLResponse)
def beauty_contest_zug(
    request: Request,
    guess: int = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_num = len(history)
    round_result = beauty_contest_play_round(guess, strategy, round_num, history)
    history.append(round_result)

    is_final = len(history) >= 6
    final = beauty_contest_final_result(history) if is_final else None

    strategy_info = None
    new_achievements: list = []
    if is_final and final:
        _, new_achievements = save_game_session(
            db,
            game_type="beauty_contest",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_round_wins"],
            ai_score=final["total_rounds"] - final["player_round_wins"],
        )
        strategy_info = BEAUTY_STRATEGY_INFO.get(strategy)

    return templates.TemplateResponse(
        request,
        "partials/beauty_contest_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 6,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Hirschjagd (Stag Hunt) – Koordinationsspiel
# ---------------------------------------------------------------------------

STAG_STRATEGY_POOL = ["risk_averse", "optimist", "coordinator", "cautious_learner"]
STAG_STRATEGY_WEIGHTS = [20, 20, 30, 30]

STAG_STRATEGY_INFO = {
    "risk_averse": {
        "name": "Risikoscheue KI",
        "icon": "🐇",
        "verhalten": "Jagte immer den Hasen – das sichere Ergebnis (3,3). Koordination war unmöglich, egal was du getan hast.",
        "gegencheck": "Gegen eine risikoscheue KI: auch Hase jagen. Hirsch bringt dir 0, Hase bringt 3 – akzeptiere das sichere Gleichgewicht.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele & Gleichgewichtsauswahl",
    },
    "optimist": {
        "name": "Optimistische KI",
        "icon": "🦌",
        "verhalten": "Jagte immer den Hirsch – setzte voll auf Koordination. Bei gegenseitigem Vertrauen: das Pareto-Optimum (8,8).",
        "gegencheck": "Gegen eine immer-Hirsch-KI: auch Hirsch jagen! Du bekommst 8 statt 3 – das ist die Pareto-dominante Strategie.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele & Gleichgewichtsauswahl",
    },
    "coordinator": {
        "name": "Koordinations-KI",
        "icon": "🔄",
        "verhalten": "Spiegelte deinen letzten Zug (Tit-for-Tat für Koordination). Kooperation erzeugt Kooperation.",
        "gegencheck": "Einmal Hirsch jagen bringt die KI auf deine Seite. Danach beide konsequent Hirsch = maximaler gemeinsamer Gewinn.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele & Gleichgewichtsauswahl",
    },
    "cautious_learner": {
        "name": "Lernende KI",
        "icon": "📊",
        "verhalten": "Startete vorsichtig mit Hase, aber erhöhte Hirsch-Rate wenn du oft genug kooperierst (≥70%). Vertrauen muss verdient werden.",
        "gegencheck": "Konsequent Hirsch jagen – die KI beobachtet dich und steigt ein, wenn sie dir vertraut. Geduld wird belohnt.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele & Gleichgewichtsauswahl",
    },
}


@router.get("/stag-hunt", response_class=HTMLResponse)
def stag_hunt_page(request: Request):
    hidden_strategy = _random.choices(STAG_STRATEGY_POOL, weights=STAG_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/stag_hunt.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "max_rounds": 8,
        },
    )


@router.post("/stag-hunt/zug", response_class=HTMLResponse)
def stag_hunt_zug(
    request: Request,
    move: str = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = stag_play_round(move, strategy, history)
    history.append(round_result)

    is_final = len(history) >= 8
    final = stag_final_result(history) if is_final else None

    strategy_info = None
    new_achievements: list = []
    if is_final and final:
        _, new_achievements = save_game_session(
            db,
            game_type="stag_hunt",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_total"],
            ai_score=final["ai_total"],
        )
        strategy_info = STAG_STRATEGY_INFO.get(strategy)

    return templates.TemplateResponse(
        request,
        "partials/stag_hunt_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 8,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Centipede-Spiel – Rückwärtsinduktion
# ---------------------------------------------------------------------------

CENTIPEDE_STRATEGY_POOL = ["backward_induction", "cooperative", "opportunist", "mirror"]
CENTIPEDE_STRATEGY_WEIGHTS = [15, 30, 30, 25]

CENTIPEDE_STRATEGY_INFO = {
    "backward_induction": {
        "name": "Rückwärtsinduktions-KI",
        "icon": "🔢",
        "verhalten": "Nahm bei jedem ihrer Züge sofort – das subgame-perfekte Nash-Gleichgewicht. Rational, aber kollektiv suboptimal.",
        "gegencheck": "Gegen eine immer-nehmende KI: auch du nimmst sofort. Andernfalls gibst du Punkte ab ohne Gegenleistung.",
        "lesson_slug": "rueckwaertsinduktion",
        "lesson_title": "Rückwärtsinduktion",
    },
    "cooperative": {
        "name": "Kooperative KI",
        "icon": "🤝",
        "verhalten": "Gab weiter bis zum letzten Knoten – setzte auf gemeinsames Wachstum. Erreichtes das Pareto-Optimum wenn du mitspieltst.",
        "gegencheck": "Weitergeben bis zum Ende lohnt sich: (64,32) schlägt alle frühzeitigen Abbrecherpunkte für dich.",
        "lesson_slug": "rueckwaertsinduktion",
        "lesson_title": "Rückwärtsinduktion",
    },
    "opportunist": {
        "name": "Opportunistische KI",
        "icon": "🎣",
        "verhalten": "Ließ den Topf wachsen und griff dann ab Knoten 4 zu – maximaler Gewinn mit kalkulierter Geduld.",
        "gegencheck": "Nimm spätestens bei Knoten 5 (deiner letzten großen Chance), bevor die KI bei 6 zugreift.",
        "lesson_slug": "rueckwaertsinduktion",
        "lesson_title": "Rückwärtsinduktion",
    },
    "mirror": {
        "name": "Spiegel-KI",
        "icon": "🪞",
        "verhalten": "Spiegelte dein Verhalten: Wenn du oft genommen hast, nahm sie auch – wenn du kooperierst, kooperiert sie.",
        "gegencheck": "Signalisiere Kooperationsbereitschaft durch Weitergeben – die KI belohnt es. Ein einmaliges Nehmen kann aber alles ändern.",
        "lesson_slug": "rueckwaertsinduktion",
        "lesson_title": "Rückwärtsinduktion",
    },
}


@router.get("/centipede", response_class=HTMLResponse)
def centipede_page(request: Request):
    hidden_strategy = _random.choices(CENTIPEDE_STRATEGY_POOL, weights=CENTIPEDE_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/centipede.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "nodes": CENTIPEDE_NODES,
        },
    )


@router.post("/centipede/zug", response_class=HTMLResponse)
def centipede_zug(
    request: Request,
    action: str = Form(...),
    strategy: str = Form(...),
    node_idx: int = Form(...),
    events_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    events = json.loads(events_json)
    turn_result = centipede_process_turn(action, strategy, node_idx, events)
    events.extend(turn_result["events"])

    is_final = turn_result["game_over"]
    final = None
    strategy_info = None

    new_achievements: list = []
    if is_final:
        final = centipede_final_result(events, turn_result["final_player"], turn_result["final_ai"])
        _, new_achievements = save_game_session(
            db,
            game_type="centipede",
            ai_strategy=strategy,
            moves=events,
            result=final["result"],
            score=final["player_score"],
            ai_score=final["ai_score"],
        )
        strategy_info = CENTIPEDE_STRATEGY_INFO.get(strategy)

    return templates.TemplateResponse(
        request,
        "partials/centipede_result.html",
        {
            "turn_result": turn_result,
            "events": events,
            "events_json": json.dumps(events),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "next_node_idx": turn_result["next_node_idx"],
            "nodes": CENTIPEDE_NODES,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Schere-Stein-Papier
# ---------------------------------------------------------------------------

RPS_STRATEGY_POOL = ["nash_mixed", "pattern_detector", "win_stay_lose_shift", "frequency_analyzer"]
RPS_STRATEGY_WEIGHTS = [2, 3, 3, 2]

RPS_STRATEGY_INFO = {
    "nash_mixed": {
        "icon": "🎲",
        "name": "Zufällig (Nash-Gemischt)",
        "verhalten": "Wählt jede der drei Optionen mit genau 1/3 Wahrscheinlichkeit – das einzige Nash-Gleichgewicht in gemischten Strategien. Mathematisch unschlagbar auf lange Sicht.",
        "gegencheck": "Gegen eine wirklich zufällige Strategie gibt es keine Gegenstrategie – du kannst nur selbst zufällig spielen. Jedes Muster kostet dich im Erwartungswert.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "pattern_detector": {
        "icon": "🔍",
        "name": "Mustererkenner",
        "verhalten": "Analysiert deine letzten 3 Züge und spielt den Zug, der deinen wahrscheinlichsten nächsten Zug schlägt. Menschen wiederholen Muster öfter als sie denken.",
        "gegencheck": "Variiere aktiv: Spiel bewusst gegen deinen eigenen Instinkt. Der Mustererkenner versagt, wenn kein Muster da ist.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "win_stay_lose_shift": {
        "icon": "📌",
        "name": "Win-Stay-Lose-Shift",
        "verhalten": "Behält den Zug bei, wenn er gewonnen hat. Wechselt nach einer Niederlage zum Zug, der den eigenen Zug geschlagen hätte. Eine häufige menschliche Heuristik.",
        "gegencheck": "Nutze die Vorhersagbarkeit: Wenn die KI gerade verloren hat, weißt du, was sie als nächstes spielt. Konter entsprechend.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "frequency_analyzer": {
        "icon": "📊",
        "name": "Frequenzanalyst",
        "verhalten": "Zählt deine Züge über die gesamte Spielzeit und spielt gegen deine häufigste Option. Braucht mindestens 4 Runden zum Einlernen.",
        "gegencheck": "Gleiche deine Häufigkeiten aktiv aus – spiel bewusst mehr von dem, was du zuletzt gemieden hast. Ein exakt gleiches Vorkommen aller drei Optionen neutralisiert ihn.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
}


@router.get("/rps", response_class=HTMLResponse)
def rps_page(request: Request):
    hidden_strategy = _random.choices(RPS_STRATEGY_POOL, weights=RPS_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/rps.html",
        {"active_page": "spiele", "hidden_strategy": hidden_strategy, "max_rounds": 7},
    )


@router.post("/rps/zug", response_class=HTMLResponse)
def rps_zug(
    request: Request,
    move: str = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = rps_play_round(move, strategy, history)
    history.append(round_result)
    is_final = len(history) >= 7
    final = rps_final_result(history) if is_final else None
    strategy_info = None
    new_achievements: list = []
    if is_final:
        _, new_achievements = save_game_session(
            db,
            game_type="rps",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_score"],
            ai_score=final["ai_score"],
        )
        strategy_info = RPS_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/rps_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 7,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Koordinationsspiel (Battle of the Sexes)
# ---------------------------------------------------------------------------

COORD_STRATEGY_POOL = ["stubborn", "flexible", "alternating", "learner"]
COORD_STRATEGY_WEIGHTS = [3, 2, 2, 3]

COORD_STRATEGY_INFO = {
    "stubborn": {
        "icon": "🦏",
        "name": "Sturköpfig",
        "verhalten": "Besteht immer auf Option B (Sportevent). Keine Rücksicht auf deine Präferenz – hofft, dass du nachgibst.",
        "gegencheck": "Wenn du erkennst, dass die KI immer B spielt, ist dein bester Zug ebenfalls B – lieber koordiniert mit kleinerem Gewinn als gar nicht koordiniert.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele",
    },
    "flexible": {
        "icon": "🤸",
        "name": "Anpassungsfähig",
        "verhalten": "Kopiert deinen letzten Zug. Entscheidet sich im ersten Zug für A (deine Präferenz). Will vor allem koordinieren.",
        "gegencheck": "Führe mit einer konsistenten Wahl – die KI folgt dir nach einer Runde. Wer zuerst eine stabile Option setzt, gewinnt die Koordination.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele",
    },
    "alternating": {
        "icon": "🔄",
        "name": "Abwechselnd",
        "verhalten": "Spielt abwechselnd A und B – unabhängig von deinen Zügen. In geraden Runden A, in ungeraden B.",
        "gegencheck": "Erkenne das Muster (es dauert 2-3 Runden) und spiele immer das, was die KI in dieser Runde spielen wird.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele",
    },
    "learner": {
        "icon": "🧠",
        "name": "Lernend",
        "verhalten": "Beobachtet deine Häufigkeiten und passt sich an. Spielt, was du öfter spielst. Braucht 2 Runden zur Kalibrierung.",
        "gegencheck": "Zeige früh klare Präferenz: Spiel die ersten 3 Runden konsequent A. Die KI lernt und folgt – du gewinnst die Koordination auf deinem Terrain.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele",
    },
}


@router.get("/koordination", response_class=HTMLResponse)
def koordination_page(request: Request):
    hidden_strategy = _random.choices(COORD_STRATEGY_POOL, weights=COORD_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/koordination.html",
        {"active_page": "spiele", "hidden_strategy": hidden_strategy, "max_rounds": 8},
    )


@router.post("/koordination/zug", response_class=HTMLResponse)
def koordination_zug(
    request: Request,
    move: str = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = coord_play_round(move, strategy, history)
    history.append(round_result)
    is_final = len(history) >= 8
    final = coord_final_result(history) if is_final else None
    strategy_info = None
    new_achievements: list = []
    if is_final:
        _, new_achievements = save_game_session(
            db,
            game_type="koordination",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_total"],
            ai_score=final["ai_total"],
        )
        strategy_info = COORD_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/koordination_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 8,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Auktion (Vickrey Second-Price)
# ---------------------------------------------------------------------------

AUCTION_STRATEGY_POOL = ["truthful", "aggressive", "conservative", "random"]
AUCTION_STRATEGY_WEIGHTS = [3, 3, 2, 2]

AUCTION_STRATEGY_INFO = {
    "truthful": {
        "icon": "⚖️",
        "name": "Wahrheitsgetreue Bieter",
        "verhalten": "Alle KI-Bieter bieten ihren tatsächlichen Wert – das Nash-Gleichgewicht der Vickrey-Auktion. Kaum Überraschungen.",
        "gegencheck": "Gegen wahrheitsgetreue Bieter ist wahrheitsgetreues Bieten ebenfalls optimal. Über- oder Unterbieten schadet dir nur.",
        "lesson_slug": "spieltheorie-grundlagen",
        "lesson_title": "Spieltheorie Grundlagen",
    },
    "aggressive": {
        "icon": "⚡",
        "name": "Aggressive Überbieter",
        "verhalten": "KI-Bieter bieten 15-45% über ihrem tatsächlichen Wert – oft zahlen sie mehr als das Objekt wert ist. Typisch in echten Auktionen (Winner's Curse).",
        "gegencheck": "Gegen aggressive Bieter: Bleib bei deinem wahren Wert. Du gewinnst weniger Runden, aber wenn du gewinnst, zahlst du einen guten Preis.",
        "lesson_slug": "spieltheorie-grundlagen",
        "lesson_title": "Spieltheorie Grundlagen",
    },
    "conservative": {
        "icon": "🐢",
        "name": "Vorsichtige Unterbieter",
        "verhalten": "KI-Bieter bieten 20-50% unter ihrem tatsächlichen Wert – sehr konservativ. Du gewinnst häufig, aber zu welchem Preis?",
        "gegencheck": "Gegen konservative Bieter könntest du minimal überbieten und trotzdem günstigen Preis zahlen. Aber Vorsicht: das Risiko von Überbieten bleibt.",
        "lesson_slug": "spieltheorie-grundlagen",
        "lesson_title": "Spieltheorie Grundlagen",
    },
    "random": {
        "icon": "🎰",
        "name": "Zufällige Bieter",
        "verhalten": "Völlig zufällige Gebote zwischen 2 und 160. Manchmal irrational hoch, manchmal niedrig – schwer zu lesen.",
        "gegencheck": "Gegen zufällige Bieter ist deine dominante Strategie unveränderlich: biete deinen wahren Wert. Alles andere ist Glücksspiel.",
        "lesson_slug": "spieltheorie-grundlagen",
        "lesson_title": "Spieltheorie Grundlagen",
    },
}


@router.get("/auktion", response_class=HTMLResponse)
def auktion_page(request: Request):
    hidden_strategy = _random.choices(AUCTION_STRATEGY_POOL, weights=AUCTION_STRATEGY_WEIGHTS)[0]
    initial_value = _random.randint(20, 100)
    return templates.TemplateResponse(
        request,
        "games/auktion.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "max_rounds": 5,
            "initial_value": initial_value,
            "round_num": 1,
        },
    )


@router.post("/auktion/zug", response_class=HTMLResponse)
def auktion_zug(
    request: Request,
    player_bid: int = Form(...),
    player_value: int = Form(...),
    strategy: str = Form(...),
    round_num: int = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = auction_play_round(player_bid, player_value, strategy, round_num)
    history.append(round_result)
    is_final = len(history) >= 5
    final = auction_final_result(history) if is_final else None
    strategy_info = None
    new_achievements: list = []
    next_value = _random.randint(20, 100) if not is_final else None
    if is_final:
        _, new_achievements = save_game_session(
            db,
            game_type="auktion",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["total_profit"],
            ai_score=0,
        )
        strategy_info = AUCTION_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/auktion_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 5,
            "next_value": next_value,
            "next_round_num": round_num + 1,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Diktatorspiel
# ---------------------------------------------------------------------------

DIKTATOR_STRATEGY_POOL = ["selfish", "fair", "altruistic", "reciprocal"]
DIKTATOR_STRATEGY_WEIGHTS = [2, 3, 2, 3]

DIKTATOR_STRATEGY_INFO = {
    "selfish": {
        "icon": "💰",
        "name": "Egoistischer Diktator",
        "verhalten": "Bot als Diktator immer nur 10 von 100 – minimale Abgabe. Spiegelt das homo-oeconomicus-Modell: nur der eigene Nutzen zählt.",
        "gegencheck": "Du konntest sein Angebot nicht ablehnen – das ist der Kern des Diktatorexperiments. Trotzdem geben echte Menschen im Schnitt 20–30 %.",
        "lesson_slug": "fairness-effekte",
        "lesson_title": "Fairness-Effekte in Verhandlungen",
    },
    "fair": {
        "icon": "⚖️",
        "name": "Fairer Diktator",
        "verhalten": "Teilte immer genau 50/50. Entspricht dem, was viele Menschen als 'gerecht' empfinden – obwohl sie theoretisch mehr behalten könnten.",
        "gegencheck": "Gleiche Aufteilung ist sozial robust: Diktatorexperimente zeigen, dass ~30 % der Probanden 50/50 teilen, auch ohne Konsequenzen.",
        "lesson_slug": "fairness-effekte",
        "lesson_title": "Fairness-Effekte in Verhandlungen",
    },
    "altruistic": {
        "icon": "🎁",
        "name": "Altruistischer Diktator",
        "verhalten": "Gab 65 von 100 – mehr als die Hälfte, obwohl er das nicht musste. Echte Altruismus-Präferenzen über reinen Eigennutz.",
        "gegencheck": "Altruismus im Experiment: ~5–10 % der Probanden geben tatsächlich mehr als 50 %. Es existiert echte soziale Präferenz.",
        "lesson_slug": "fairness-effekte",
        "lesson_title": "Fairness-Effekte in Verhandlungen",
    },
    "reciprocal": {
        "icon": "🔁",
        "name": "Reziproker Diktator",
        "verhalten": "Orientierte sein Angebot an deiner eigenen Großzügigkeit (ca. 90 % deines Durchschnitts). Reziprozität – du bekommst, was du gibst.",
        "gegencheck": "Deine Großzügigkeit in Runden 1–4 beeinflusste, was du in Runden 5–8 zurückbekamst. Sozialer Austausch funktioniert bidirektional.",
        "lesson_slug": "wiederholte-spiele-reputation",
        "lesson_title": "Wiederholte Spiele & Reputation",
    },
}


@router.get("/diktator", response_class=HTMLResponse)
def diktator_page(request: Request):
    hidden_strategy = _random.choices(DIKTATOR_STRATEGY_POOL, weights=DIKTATOR_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/diktator.html",
        {"active_page": "spiele", "hidden_strategy": hidden_strategy, "max_rounds": 8},
    )


@router.post("/diktator/zug", response_class=HTMLResponse)
def diktator_zug(
    request: Request,
    player_offer: int = Form(default=0),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_num = len(history) + 1
    round_result = diktator_play_round(player_offer, strategy, round_num, history)
    history.append(round_result)
    is_final = len(history) >= 8
    final = diktator_final_result(history) if is_final else None
    strategy_info = None
    new_achievements: list = []
    if is_final:
        _, new_achievements = save_game_session(
            db,
            game_type="diktator",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_total"],
            ai_score=final["ai_total"],
        )
        strategy_info = DIKTATOR_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/diktator_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 8,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Dollarauktion
# ---------------------------------------------------------------------------

DOLLAR_STRATEGY_POOL = ["escalator", "rational_stopper", "aggressive", "random_quitter"]
DOLLAR_STRATEGY_WEIGHTS = [3, 2, 2, 3]

DOLLAR_STRATEGY_INFO = {
    "escalator": {
        "icon": "📈",
        "name": "Eskalierer",
        "verhalten": "Überbietete konsequent bis 150 – weit über den Preiswert von 100. Typisches Verhalten im Sunk-Cost-Modus: jeder neue Einsatz soll den alten rechtfertigen.",
        "gegencheck": "Sobald dein Gebot über 50 steigt und die KI noch aktiv ist, droht ein Nettoverlust. Die rationale Entscheidung: früh aufhören und den Verlust akzeptieren.",
        "lesson_slug": "spieltheorie-grundlagen",
        "lesson_title": "Spieltheorie Grundlagen",
    },
    "rational_stopper": {
        "icon": "🛑",
        "name": "Rationaler Stopper",
        "verhalten": "Hörte auf zu bieten, sobald das nächste Gebot den Preiswert (100) überschreiten würde. Das ist das spieltheoretisch rationale Verhalten.",
        "gegencheck": "Wenn die KI aufhört, hast du gewonnen – aber zu welchem Preis? Gegen einen rationalen Stopper: früh einsteigen und die KI frühzeitig über 100 treiben.",
        "lesson_slug": "spieltheorie-grundlagen",
        "lesson_title": "Spieltheorie Grundlagen",
    },
    "aggressive": {
        "icon": "🔥",
        "name": "Aggressiver Bieter",
        "verhalten": "Steigerte bis 210 – deutlich über Preiswert. Maximale Eskalation, typisch für Commitment-Fallen in echten Auktionen.",
        "gegencheck": "Früh aufhören ist die einzig sichere Strategie. Gegen einen aggressiven Bieter: niemals anfangen zu bieten, wenn du nicht bereit bist, massiv zu verlieren.",
        "lesson_slug": "spieltheorie-grundlagen",
        "lesson_title": "Spieltheorie Grundlagen",
    },
    "random_quitter": {
        "icon": "🎲",
        "name": "Zufälliger Aussteiger",
        "verhalten": "Hörte mit zunehmender Wahrscheinlichkeit auf, je höher die Gebote stiegen. Simuliert unsicheres, irrationales Verhalten in echten Auktionen.",
        "gegencheck": "Schwer vorhersagbar – manchmal steigt die KI früh aus, manchmal sehr spät. Deine beste Strategie: nicht anfangen oder nach dem ersten Gebot aussteigen.",
        "lesson_slug": "spieltheorie-grundlagen",
        "lesson_title": "Spieltheorie Grundlagen",
    },
}


@router.get("/dollarauktion", response_class=HTMLResponse)
def dollarauktion_page(request: Request):
    hidden_strategy = _random.choices(DOLLAR_STRATEGY_POOL, weights=DOLLAR_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/dollarauktion.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "prize": DOLLAR_PRIZE,
        },
    )


@router.post("/dollarauktion/zug", response_class=HTMLResponse)
def dollarauktion_zug(
    request: Request,
    player_bid: int = Form(default=0),
    player_quit: str = Form(default="false"),
    strategy: str = Form(...),
    ai_last_bid: int = Form(default=0),
    round_num: int = Form(default=1),
    db: Session = Depends(get_db),
):
    quit_flag = player_quit.lower() == "true"
    turn = dollar_process_turn(player_bid, quit_flag, strategy, ai_last_bid, round_num)
    is_final = turn["game_over"]
    strategy_info = None
    new_achievements: list = []
    if is_final:
        result = "win" if turn["winner"] == "player" else "loss"
        _, new_achievements = save_game_session(
            db,
            game_type="dollarauktion",
            ai_strategy=strategy,
            moves=[turn],
            result=result,
            score=turn["player_payoff"] if turn["player_payoff"] is not None else 0,
            ai_score=max(0, turn["ai_payoff"] or 0),
        )
        strategy_info = DOLLAR_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/dollarauktion_result.html",
        {
            "turn": turn,
            "strategy": strategy,
            "is_final": is_final,
            "prize": DOLLAR_PRIZE,
            "round_num": round_num,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Minderheitsspiel (El Farol / Minority Game)
# ---------------------------------------------------------------------------

MINORITY_STRATEGY_POOL = ["random", "herding", "contrarian", "nash_mixed"]
MINORITY_STRATEGY_WEIGHTS = [2, 3, 3, 2]

MINORITY_STRATEGY_INFO = {
    "random": {
        "icon": "🎲",
        "name": "Zufällige Bots",
        "verhalten": "Jeder Bot entschied sich zufällig für A oder B – keine Koordination. Das Nash-Gleichgewicht im Minderheitsspiel ist tatsächlich eine gemischte Strategie.",
        "gegencheck": "Gegen rein zufällige Bots: spiel selbst zufällig mit p=0.5. Das ist das einzige Nash-Gleichgewicht – jedes Muster kostet langfristig.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "herding": {
        "icon": "🐑",
        "name": "Herdenverhalten-Bots",
        "verhalten": "Bots liefen der letzten Mehrheit hinterher – wenn Gruppe A zuletzt die Mehrheit hatte, wechselten sie zu A. Das erzeugt systematische Überfüllung.",
        "gegencheck": "Antizyklisch spielen: Wenn zuletzt A die Mehrheit war, die Bots zu A laufen – spiel B, du bist dann in der Minderheit.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele",
    },
    "contrarian": {
        "icon": "🔄",
        "name": "Gegenteil-Bots",
        "verhalten": "Bots spielten immer das Gegenteil der letzten Mehrheit. Das erzeugt systematisches Wechseln und Vorhersagbarkeit.",
        "gegencheck": "Muster erkennen: Wenn zuletzt B die Mehrheit war, wechseln Bots zu A – also spiel B als Gegenreaktion.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "nash_mixed": {
        "icon": "⚖️",
        "name": "Nash-Gemischt-Bots",
        "verhalten": "Bots spielten die theoretisch optimale gemischte Strategie (50/50 zufällig). Das Nash-Gleichgewicht – gegen das du nichts ausrichten kannst.",
        "gegencheck": "Das Nash-Gleichgewicht im Minderheitsspiel ist tatsächlich schwer zu schlagen. Selbst zufällig spielen ist die beste Antwort.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
}


@router.get("/minderheit", response_class=HTMLResponse)
def minderheit_page(request: Request):
    hidden_strategy = _random.choices(MINORITY_STRATEGY_POOL, weights=MINORITY_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/minderheit.html",
        {"active_page": "spiele", "hidden_strategy": hidden_strategy, "max_rounds": 8},
    )


@router.post("/minderheit/zug", response_class=HTMLResponse)
def minderheit_zug(
    request: Request,
    choice: int = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = minority_play_round(choice, strategy, history)
    history.append(round_result)
    is_final = len(history) >= 8
    final = minority_final_result(history) if is_final else None
    strategy_info = None
    new_achievements: list = []
    if is_final:
        _, new_achievements = save_game_session(
            db,
            game_type="minderheit",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_total"],
            ai_score=0,
        )
        strategy_info = MINORITY_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/minderheit_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 8,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Habicht-Taube-Spiel (Hawk-Dove / ESS)
# ---------------------------------------------------------------------------

HD_STRATEGY_POOL = ["ess_mixed", "always_hawk", "always_dove", "adaptive"]
HD_STRATEGY_WEIGHTS = [3, 2, 2, 3]

HD_STRATEGY_INFO = {
    "ess_mixed": {
        "icon": "🧬",
        "name": "ESS-Gemischt-Population",
        "verhalten": "Die KI spielte die evolutionär stabile Strategie: 2/3 Hawk, 1/3 Dove. Gegen diese Mischung kann keine reine Strategie langfristig besser abschneiden.",
        "gegencheck": "Gegen ESS: selbst 2/3 Hawk spielen. Jede Abweichung kostet langfristig.",
        "lesson_slug": "evolutionaere-stabilitaet",
        "lesson_title": "Evolutionär Stabile Strategien",
    },
    "always_hawk": {
        "icon": "🦅",
        "name": "Immer Hawk",
        "verhalten": "Die KI war stets aggressiv. Bei H vs H entstehen hohe Kampfkosten – diese Strategie verliert gegen gemischte Spieler.",
        "gegencheck": "Dove spielen: Du verlierst zwar einzelne Kämpfe (0 statt -1), aber sparst Kampfkosten.",
        "lesson_slug": "evolutionaere-stabilitaet",
        "lesson_title": "Evolutionär Stabile Strategien",
    },
    "always_dove": {
        "icon": "🕊️",
        "name": "Immer Dove",
        "verhalten": "Die KI wich immer zurück. Hawk dominiert Dove vollständig: 4 vs 0 jede Runde.",
        "gegencheck": "Immer Hawk spielen – maximaler Exploit gegen Dove.",
        "lesson_slug": "dominante-strategien",
        "lesson_title": "Dominante Strategien",
    },
    "adaptive": {
        "icon": "🔄",
        "name": "Adaptive KI",
        "verhalten": "Spielte Hawk wenn du Dove warst, Dove wenn du Hawk warst – klassisches Ausweichen.",
        "gegencheck": "Unberechenbar mischen: 2/3 Hawk. Dann profitiert auch die adaptive KI nicht.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
}


@router.get("/habicht-taube", response_class=HTMLResponse)
def habicht_taube_page(request: Request):
    hidden_strategy = _random.choices(HD_STRATEGY_POOL, weights=HD_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/habicht_taube.html",
        {"active_page": "spiele", "hidden_strategy": hidden_strategy, "max_rounds": 10},
    )


@router.post("/habicht-taube/zug", response_class=HTMLResponse)
def habicht_taube_zug(
    request: Request,
    choice: str = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = hd_play_round(choice, strategy, history)
    history.append(round_result)
    is_final = len(history) >= 10
    final = hd_final_result(history) if is_final else None
    strategy_info = None
    new_achievements: list = []
    if is_final:
        _, new_achievements = save_game_session(
            db,
            game_type="habicht-taube",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_total"],
            ai_score=final["ai_total"],
        )
        strategy_info = HD_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/habicht_taube_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 10,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Koordinationsdilemma / Battle of the Sexes
# ---------------------------------------------------------------------------

BOTS_STRATEGY_POOL = ["stubborn_b", "mirror", "nash_mixed", "adaptive"]
BOTS_STRATEGY_WEIGHTS = [3, 2, 3, 2]

BOTS_STRATEGY_INFO = {
    "stubborn_b": {
        "icon": "💪",
        "name": "Sture KI (immer B)",
        "verhalten": "Die KI bestand auf Option B – jede Koordination erforderte, dass du nachgibst.",
        "gegencheck": "Bei sturer KI: manchmal B spielen sichert wenigstens 1 Punkt. Reines A erzeugt nur 0er-Runden.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele",
    },
    "mirror": {
        "icon": "🪞",
        "name": "Spiegel-KI",
        "verhalten": "Kopierte deinen letzten Zug. Einmal koordiniert → immer koordiniert.",
        "gegencheck": "A spielen und darauf beharren – KI folgt nach einer Runde.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele",
    },
    "nash_mixed": {
        "icon": "⚖️",
        "name": "Nash-Gemischt-KI",
        "verhalten": "Spielte die gemischte Nash-Strategie (25% A, 75% B). Gegen diese Mischung gibt es keine bessere reine Antwort.",
        "gegencheck": "Selbst gemischt spielen (75% A, 25% B) – das ist das gemischte Nash-Gleichgewicht.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "adaptive": {
        "icon": "🧠",
        "name": "Adaptive KI",
        "verhalten": "Wiederholte koordinierte Züge, verwarf Miskoordination. Lernende Strategie.",
        "gegencheck": "Früh A als Fokalpunkt etablieren – adaptive KI folgt stabilen Mustern.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele",
    },
}


@router.get("/geschlechter-kampf", response_class=HTMLResponse)
def geschlechter_kampf_page(request: Request):
    hidden_strategy = _random.choices(BOTS_STRATEGY_POOL, weights=BOTS_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/geschlechter_kampf.html",
        {"active_page": "spiele", "hidden_strategy": hidden_strategy, "max_rounds": 8},
    )


@router.post("/geschlechter-kampf/zug", response_class=HTMLResponse)
def geschlechter_kampf_zug(
    request: Request,
    choice: str = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = bots_play_round(choice, strategy, history)
    history.append(round_result)
    is_final = len(history) >= 8
    final = bots_final_result(history) if is_final else None
    strategy_info = None
    new_achievements: list = []
    if is_final:
        _, new_achievements = save_game_session(
            db,
            game_type="geschlechter-kampf",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_total"],
            ai_score=final["ai_total"],
        )
        strategy_info = BOTS_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/geschlechter_kampf_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 8,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Freiwilligen-Dilemma (Volunteer's Dilemma)
# ---------------------------------------------------------------------------

VD_STRATEGY_POOL = ["selfish", "nash_mixed", "threshold", "altruistic"]
VD_STRATEGY_WEIGHTS = [3, 3, 2, 2]

VD_STRATEGY_INFO = {
    "selfish": {
        "icon": "😤",
        "name": "Egoistische Bots",
        "verhalten": "Alle Bots spielten NV – klassisches Trittbrettfahren. Wenn du nicht hilfst, gibt es gar nichts.",
        "gegencheck": "Manchmal helfen lohnt sich: 3 Punkte statt 0 ist besser als riskieren, leer auszugehen.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele",
    },
    "nash_mixed": {
        "icon": "⚖️",
        "name": "Nash-Gemischt-Bots",
        "verhalten": "Bots spielten die Nash-Gleichgewichts-Mischung (~71% NV). Manchmal hilft einer, oft nicht.",
        "gegencheck": "Selbst gemischt spielen – die Nash-Strategie ist robust gegen diese Botmischung.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "threshold": {
        "icon": "🚦",
        "name": "Schwellenwert-Bots",
        "verhalten": "Bots halfen nach zwei NV-Runden in Folge. Kollektive Reaktion auf anhaltende Inaktivität.",
        "gegencheck": "Frühzeitig helfen verhindert Schwellenwert-Eskalation. Erkenne das Muster.",
        "lesson_slug": "wiederholte-spiele-reputation",
        "lesson_title": "Wiederholte Spiele & Reputation",
    },
    "altruistic": {
        "icon": "💚",
        "name": "Altruistische Bots",
        "verhalten": "Bots halfen immer. Als Trittbrettfahrer kannst du jede Runde 5 Punkte kassieren.",
        "gegencheck": "NV spielen und profitieren – zeigt wie Trittbrettfahrertum funktioniert.",
        "lesson_slug": "koordinationsspiele",
        "lesson_title": "Koordinationsspiele",
    },
}


@router.get("/freiwilligen-dilemma", response_class=HTMLResponse)
def freiwilligen_dilemma_page(request: Request):
    hidden_strategy = _random.choices(VD_STRATEGY_POOL, weights=VD_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/freiwilligen_dilemma.html",
        {"active_page": "spiele", "hidden_strategy": hidden_strategy, "max_rounds": 8},
    )


@router.post("/freiwilligen-dilemma/zug", response_class=HTMLResponse)
def freiwilligen_dilemma_zug(
    request: Request,
    choice: str = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = vd_play_round(choice, strategy, history)
    history.append(round_result)
    is_final = len(history) >= 8
    final = vd_final_result(history) if is_final else None
    strategy_info = None
    new_achievements: list = []
    if is_final:
        _, new_achievements = save_game_session(
            db,
            game_type="freiwilligen-dilemma",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_total"],
            ai_score=0,
        )
        strategy_info = VD_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/freiwilligen_dilemma_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 8,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Gleiche Münzen (Matching Pennies)
# ---------------------------------------------------------------------------

MP_STRATEGY_POOL = ["random", "pattern_exploit", "last_winner", "anti_last"]
MP_STRATEGY_WEIGHTS = [2, 3, 3, 2]

MP_STRATEGY_INFO = {
    "random": {
        "icon": "🎲",
        "name": "Zufalls-KI",
        "verhalten": "50/50 zufällig – das einzige Nash-Gleichgewicht im Matching-Pennies-Spiel. Nicht zu schlagen.",
        "gegencheck": "Selbst 50/50 zufällig spielen – das ist die Minimax-Strategie.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "pattern_exploit": {
        "icon": "🔍",
        "name": "Muster-Exploiter",
        "verhalten": "Analysierte deine letzten 3 Züge und spielte die häufigere Seite. Erkannte Muster werden ausgenutzt.",
        "gegencheck": "Kein Muster – echter Zufall (Münze werfen!) ist die einzige sichere Methode.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "last_winner": {
        "icon": "🏆",
        "name": "Gewinner-Wiederholt-KI",
        "verhalten": "Wiederholte gewinnende Züge. Vorhersagbar nach einem Gewinn – dann immer wechseln.",
        "gegencheck": "Nach einer KI-Niederlage: spiel dasselbe wie zuvor. Nach KI-Sieg: wechsel.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
    "anti_last": {
        "icon": "↩️",
        "name": "Anti-Letzter-Zug-KI",
        "verhalten": "Spielte das Gegenteil deines letzten Zuges. Sobald erkannt: spielst du K, kommt Z – spiel dann Z.",
        "gegencheck": "Erkenne das Muster: spiel immer das Gegenteil deines letzten Zuges.",
        "lesson_slug": "gemischte-strategien",
        "lesson_title": "Gemischte Strategien",
    },
}


@router.get("/gleiche-muenzen", response_class=HTMLResponse)
def gleiche_muenzen_page(request: Request):
    hidden_strategy = _random.choices(MP_STRATEGY_POOL, weights=MP_STRATEGY_WEIGHTS)[0]
    return templates.TemplateResponse(
        request,
        "games/gleiche_muenzen.html",
        {"active_page": "spiele", "hidden_strategy": hidden_strategy, "max_rounds": 10},
    )


@router.post("/gleiche-muenzen/zug", response_class=HTMLResponse)
def gleiche_muenzen_zug(
    request: Request,
    choice: str = Form(...),
    strategy: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    history = json.loads(history_json)
    round_result = mp_play_round(choice, strategy, history)
    history.append(round_result)
    is_final = len(history) >= 10
    final = mp_final_result(history) if is_final else None
    strategy_info = None
    new_achievements: list = []
    if is_final:
        _, new_achievements = save_game_session(
            db,
            game_type="gleiche-muenzen",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_total"],
            ai_score=final["ai_total"],
        )
        strategy_info = MP_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/gleiche_muenzen_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 10,
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )


# ---------------------------------------------------------------------------
# Gewinner-Fluch (Winner's Curse / Common Value Auction)
# ---------------------------------------------------------------------------

WC_STRATEGY_POOL = ["naive", "rational", "aggressive"]
WC_STRATEGY_WEIGHTS = [3, 3, 4]

WC_STRATEGY_INFO = {
    "naive": {
        "icon": "😊",
        "name": "Naive Bieter",
        "verhalten": "Boten ungefähr ihr Signal – typisches Verhalten ohne Winner's-Curse-Bewusstsein.",
        "gegencheck": "Biet unter deinem Signal: wahre Wert = Signal × (n-1)/n. Bei 4 Bietern: Signal × 3/4.",
        "lesson_slug": "auktionstheorie",
        "lesson_title": "Auktionstheorie & Winner's Curse",
    },
    "rational": {
        "icon": "🧮",
        "name": "Rationale Bieter",
        "verhalten": "Passten ihr Signal nach unten an, um den Winner's Curse zu vermeiden. Schwerste Konkurrenz.",
        "gegencheck": "Selbst rational bieten: Signal × (n-1)/n als Richtwert.",
        "lesson_slug": "auktionstheorie",
        "lesson_title": "Auktionstheorie & Winner's Curse",
    },
    "aggressive": {
        "icon": "💥",
        "name": "Aggressive Bieter",
        "verhalten": "Boten über ihrem Signal – maximales Risiko für Winner's Curse. Wer gewinnt, zahlt oft zu viel.",
        "gegencheck": "Konservativ bieten – lass die aggressiven Bieter sich selbst schaden.",
        "lesson_slug": "auktionstheorie",
        "lesson_title": "Auktionstheorie & Winner's Curse",
    },
}


@router.get("/gewinner-fluch", response_class=HTMLResponse)
def gewinner_fluch_page(request: Request):
    hidden_strategy = _random.choices(WC_STRATEGY_POOL, weights=WC_STRATEGY_WEIGHTS)[0]
    first_item = wc_generate_item(1)
    return templates.TemplateResponse(
        request,
        "games/gewinner_fluch.html",
        {
            "active_page": "spiele",
            "hidden_strategy": hidden_strategy,
            "max_rounds": 5,
            "item": first_item,
            "item_json": json.dumps(first_item),
        },
    )


@router.post("/gewinner-fluch/zug", response_class=HTMLResponse)
def gewinner_fluch_zug(
    request: Request,
    player_bid: int = Form(...),
    strategy: str = Form(...),
    item_json: str = Form(...),
    history_json: str = Form(default="[]"),
    db: Session = Depends(get_db),
):
    item = json.loads(item_json)
    history = json.loads(history_json)
    round_result = wc_play_round(player_bid, item, strategy)
    history.append(round_result)
    is_final = len(history) >= 5
    final = wc_final_result(history) if is_final else None
    next_item = wc_generate_item(len(history) + 1) if not is_final else None
    strategy_info = None
    new_achievements: list = []
    if is_final:
        _, new_achievements = save_game_session(
            db,
            game_type="gewinner-fluch",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["total_profit"],
            ai_score=0,
        )
        strategy_info = WC_STRATEGY_INFO.get(strategy)
    return templates.TemplateResponse(
        request,
        "partials/gewinner_fluch_result.html",
        {
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "max_rounds": 5,
            "next_item": next_item,
            "next_item_json": json.dumps(next_item) if next_item else "null",
            "strategy_info": strategy_info,
            "new_achievements": new_achievements,
        },
    )
