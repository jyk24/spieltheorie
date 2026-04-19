"""Rätsel & Paradoxe – einmalige spieltheoretische Denkexperimente."""
import random as _random

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/raetsel")
templates = Jinja2Templates(directory="app/templates")

RAETSEL_META = [
    {
        "id": "monty-hall",
        "name": "Monty Hall Problem",
        "icon": "🚪",
        "beschreibung": "Du wählst eine von drei Türen. Der Moderator öffnet eine falsche. Wechselst du? Die Antwort überrascht fast jeden.",
        "typ": "Wahrscheinlichkeits-Paradox",
        "schwierigkeit": "Einsteiger",
        "dauer": "3 min",
    },
    {
        "id": "allais",
        "name": "Allais-Paradoxon",
        "icon": "🎰",
        "beschreibung": "Zwei Lotterie-Entscheidungen, kein Feedback dazwischen. Am Ende zeigt sich: deine Wahl widerspricht sich selbst – wie bei fast allen.",
        "typ": "Entscheidungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
    },
    {
        "id": "piraten",
        "name": "Das Piratenspiel",
        "icon": "🏴‍☠️",
        "beschreibung": "5 Piraten teilen 100 Goldstücke. Wie viel bekommt der Anführer laut Rückwärtsinduktion? Die Antwort schockiert fast jeden.",
        "typ": "Logik-Puzzle",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
    },
    {
        "id": "st-petersburg",
        "name": "St. Petersburger Paradoxon",
        "icon": "🎰",
        "beschreibung": "Ein Spiel mit theoretisch unendlichem Erwartungswert – und doch würde kaum jemand mehr als 30€ dafür zahlen. Warum?",
        "typ": "Entscheidungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
    },
    {
        "id": "reisenden-dilemma",
        "name": "Reisenden-Dilemma",
        "icon": "🧳",
        "beschreibung": "Wähle eine Zahl von 2–100. Nash-Gleichgewicht sagt: 2. Aber fast alle Menschen spielen 95+ und verdienen mehr.",
        "typ": "Strategieparadox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
    },
    {
        "id": "condorcet",
        "name": "Condorcet-Paradoxon",
        "icon": "🗳️",
        "beschreibung": "Drei Wähler, drei Optionen – und die Mehrheitswahl dreht im Kreis. Das Fundament der Social-Choice-Theorie.",
        "typ": "Abstimmungsparadox",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
    },
    {
        "id": "newcomb",
        "name": "Newcomb-Paradoxon",
        "icon": "📦",
        "beschreibung": "Eine Box oder zwei? Ein nahezu unfehlbarer Vorhersager hat bereits entschieden – und beide Entscheidungen lassen sich rational begründen.",
        "typ": "Entscheidungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
    },
    {
        "id": "simpson",
        "name": "Simpson-Paradoxon",
        "icon": "📊",
        "beschreibung": "Medikament A ist in jeder Untergruppe besser – trotzdem gewinnt Medikament B in der Gesamtstatistik. Warum?",
        "typ": "Statistik-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
    },
    {
        "id": "geburtstag",
        "name": "Geburtstagsparadoxon",
        "icon": "🎂",
        "beschreibung": "Wie viele Menschen braucht es, damit die Wahrscheinlichkeit eines gemeinsamen Geburtstags über 50 % liegt? Weit weniger als du denkst.",
        "typ": "Wahrscheinlichkeits-Paradox",
        "schwierigkeit": "Einsteiger",
        "dauer": "3 min",
    },
    {
        "id": "zwei-umschlag",
        "name": "Zwei-Umschlag-Problem",
        "icon": "✉️",
        "beschreibung": "Du hast einen Umschlag mit Geld. Der andere enthält doppelt oder halb so viel. Tauschen? Das Argument sagt immer ja – aber das kann nicht stimmen.",
        "typ": "Entscheidungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
    },
    {
        "id": "sekretaerin",
        "name": "Sekretärinnen-Problem",
        "icon": "📋",
        "beschreibung": "Du bewertest Kandidaten nacheinander, ohne zurückgehen zu können. Wann hörst du auf zu suchen? Die optimale Strategie basiert auf der Zahl e.",
        "typ": "Optimierungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
    },
    {
        "id": "braess",
        "name": "Braess-Paradoxon",
        "icon": "🛣️",
        "beschreibung": "Eine neue Straße hinzufügen kann den Verkehr für alle verlangsamen. Das Nash-Gleichgewicht ist nicht das gesellschaftliche Optimum.",
        "typ": "Spieltheorie-Paradox",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
    },
]


# ---------------------------------------------------------------------------
# Übersicht
# ---------------------------------------------------------------------------

@router.get("", response_class=HTMLResponse)
def raetsel_overview(request: Request):
    return templates.TemplateResponse(
        request, "raetsel.html", {"active_page": "raetsel", "raetsel": RAETSEL_META}
    )


# ---------------------------------------------------------------------------
# Monty Hall Problem
# ---------------------------------------------------------------------------

@router.get("/monty-hall", response_class=HTMLResponse)
def monty_hall_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/monty_hall.html", {"active_page": "raetsel"}
    )


@router.post("/monty-hall/reveal", response_class=HTMLResponse)
def monty_hall_reveal(request: Request, chosen: int = Form(...)):
    """Spieler hat Tür gewählt – Moderator öffnet eine Ziegentür."""
    winning = _random.randint(1, 3)
    options = [d for d in [1, 2, 3] if d != chosen and d != winning]
    revealed = _random.choice(options)
    switch_door = next(d for d in [1, 2, 3] if d != chosen and d != revealed)
    return templates.TemplateResponse(
        request,
        "partials/monty_reveal.html",
        {
            "chosen": chosen,
            "winning": winning,
            "revealed": revealed,
            "switch_door": switch_door,
        },
    )


@router.post("/monty-hall/result", response_class=HTMLResponse)
def monty_hall_result(
    request: Request,
    chosen: int = Form(...),
    winning: int = Form(...),
    decision: str = Form(...),
    switch_door: int = Form(...),
):
    final_door = chosen if decision == "stay" else switch_door
    won = final_door == winning
    # Deterministische Simulation (analytisch exakt)
    sim_n = 10000
    sim_stay_wins = round(sim_n / 3)
    sim_switch_wins = sim_n - sim_stay_wins
    return templates.TemplateResponse(
        request,
        "partials/monty_result.html",
        {
            "chosen": chosen,
            "winning": winning,
            "final_door": final_door,
            "decision": decision,
            "switch_door": switch_door,
            "won": won,
            "sim_n": sim_n,
            "sim_stay_wins": sim_stay_wins,
            "sim_switch_wins": sim_switch_wins,
            "sim_stay_rate": round(sim_stay_wins / sim_n * 100),
            "sim_switch_rate": round(sim_switch_wins / sim_n * 100),
        },
    )


# ---------------------------------------------------------------------------
# Allais-Paradoxon
# ---------------------------------------------------------------------------

@router.get("/allais", response_class=HTMLResponse)
def allais_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/allais.html", {"active_page": "raetsel"}
    )


@router.post("/allais/phase2", response_class=HTMLResponse)
def allais_phase2(request: Request, choice1: str = Form(...)):
    return templates.TemplateResponse(
        request, "partials/allais_phase2.html", {"choice1": choice1}
    )


@router.post("/allais/result", response_class=HTMLResponse)
def allais_result(
    request: Request,
    choice1: str = Form(...),
    choice2: str = Form(...),
):
    # A + D  oder  B + C  sind inkonsistent (verletzen Unabhängigkeitsaxiom)
    # A + C  oder  B + D  sind konsistent
    inconsistent = (choice1 == "A" and choice2 == "D") or (choice1 == "B" and choice2 == "C")
    # Beschreibungen für die Auflösung
    choice1_label = "A (sichere Million)" if choice1 == "A" else "B (Risiko mit höherem Erwartungswert)"
    choice2_label = "D (höherer Erwartungswert)" if choice2 == "D" else "C (kleinere sichere Chance)"
    return templates.TemplateResponse(
        request,
        "partials/allais_result.html",
        {
            "choice1": choice1,
            "choice2": choice2,
            "choice1_label": choice1_label,
            "choice2_label": choice2_label,
            "inconsistent": inconsistent,
        },
    )


# ---------------------------------------------------------------------------
# Piratenspiel
# ---------------------------------------------------------------------------

# Rückwärtsinduktions-Schritte (für die Erklärung)
PIRATE_STEPS = [
    {
        "n": 2,
        "pirates": "P4 + P5",
        "proposal": [None, None, None, 100, 0],
        "votes": "P4 stimmt ja (50% = Mehrheit mit Tie-Breaking). Angenommen.",
        "reasoning": "P4 braucht nur die eigene Stimme.",
    },
    {
        "n": 3,
        "pirates": "P3 + P4 + P5",
        "proposal": [None, None, 99, 0, 1],
        "votes": "P3 + P5 stimmen ja (2/3).",
        "reasoning": "P4 würde bei 2 Piraten 100 bekommen → nicht zu bestechen. P5 würde 0 bekommen → 1 Münze reicht.",
    },
    {
        "n": 4,
        "pirates": "P2 + P3 + P4 + P5",
        "proposal": [None, 99, 0, 1, 0],
        "votes": "P2 + P4 stimmen ja (2/4 = 50%).",
        "reasoning": "P3 würde 99 bekommen → zu teuer. P4 würde 0 bekommen → 1 Münze reicht. P5 würde 1 bekommen → bräuchte 2 Münzen → teurer.",
    },
    {
        "n": 5,
        "pirates": "P1 + P2 + P3 + P4 + P5",
        "proposal": [98, 0, 1, 0, 1],
        "votes": "P1 + P3 + P5 stimmen ja (3/5).",
        "reasoning": "P2 würde 99 bekommen → nicht zu bestechen. P3 würde 0 bekommen → 1 Münze reicht. P4 würde 1 bekommen → bräuchte 2 Münzen. P5 würde 0 bekommen → 1 Münze reicht. Günstigste Option: P3 + P5 je 1 Münze.",
    },
]

PIRATE_SOLUTION = [98, 0, 1, 0, 1]


@router.get("/piraten", response_class=HTMLResponse)
def piraten_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/piraten.html", {"active_page": "raetsel"}
    )


@router.post("/piraten/result", response_class=HTMLResponse)
def piraten_result(
    request: Request,
    p1: int = Form(...),
    p2: int = Form(...),
    p3: int = Form(...),
    p4: int = Form(...),
    p5: int = Form(...),
):
    player_guess = [p1, p2, p3, p4, p5]
    total = sum(player_guess)
    diff = sum(abs(player_guess[i] - PIRATE_SOLUTION[i]) for i in range(5))
    exact = player_guess == PIRATE_SOLUTION
    close = diff <= 15 and not exact
    return templates.TemplateResponse(
        request,
        "partials/piraten_result.html",
        {
            "player_guess": player_guess,
            "solution": PIRATE_SOLUTION,
            "total": total,
            "exact": exact,
            "close": close,
            "diff": diff,
            "steps": PIRATE_STEPS,
        },
    )


# ---------------------------------------------------------------------------
# St. Petersburger Paradoxon
# ---------------------------------------------------------------------------

@router.get("/st-petersburg", response_class=HTMLResponse)
def st_petersburg_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/st_petersburg.html", {"active_page": "raetsel"}
    )


@router.post("/st-petersburg/result", response_class=HTMLResponse)
def st_petersburg_result(
    request: Request,
    wtp: int = Form(...),
):
    # Expected value after N flips = sum of 2^n * (1/2)^n = sum of 1 → infinite
    # Bernoulli's log utility: U = log2(wtp) → fair price ≈ log2(wealth)
    # Typical WTP in studies: 10-30€
    import math
    ev_10 = sum(2**n * (0.5**n) for n in range(1, 11))  # truncated at 10 flips
    ev_20 = sum(2**n * (0.5**n) for n in range(1, 21))
    log_utility_price = round(math.log2(max(wtp, 1)) * 2)

    if wtp <= 10:
        reaction = "sehr_niedrig"
    elif wtp <= 30:
        reaction = "typisch"
    elif wtp <= 100:
        reaction = "hoch"
    else:
        reaction = "sehr_hoch"

    return templates.TemplateResponse(
        request,
        "partials/st_petersburg_result.html",
        {
            "wtp": wtp,
            "ev_10": round(ev_10, 1),
            "ev_20": round(ev_20, 1),
            "log_utility_price": log_utility_price,
            "reaction": reaction,
        },
    )


# ---------------------------------------------------------------------------
# Reisenden-Dilemma
# ---------------------------------------------------------------------------

@router.get("/reisenden-dilemma", response_class=HTMLResponse)
def reisenden_dilemma_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/reisenden_dilemma.html", {"active_page": "raetsel"}
    )


@router.post("/reisenden-dilemma/result", response_class=HTMLResponse)
def reisenden_dilemma_result(
    request: Request,
    claim: int = Form(...),
):
    # Nash equilibrium: claim = 2 (iterated dominance argument)
    # Against Nash player: if you claim X, Nash player claims 2
    # You get max(2, claim) - 2 = 0 if claim >= 3, or 4 if claim = 2
    # Wait - let's recalculate:
    # Rules: lower claimant gets their value + 2, higher gets lower value - 2
    # If claim=100, Nash=2: you get 2-2=0, Nash gets 2+2=4 → Nash wins
    # If claim=2, Nash=2: both get 2 → tie
    # Against high human players (avg ~90): claim=97 → you get 97+2=99, they get 97-2=95 → you win!
    nash_claim = 2
    if claim == nash_claim:
        your_payoff = claim
        nash_payoff = nash_claim
    elif claim < nash_claim:
        your_payoff = claim + 2
        nash_payoff = claim - 2
    else:  # claim > nash_claim
        your_payoff = nash_claim - 2
        nash_payoff = nash_claim + 2

    # Against a typical human (claim ~90)
    human_avg = 90
    if claim == human_avg:
        vs_human_you = claim
        vs_human_other = human_avg
    elif claim < human_avg:
        vs_human_you = claim + 2
        vs_human_other = claim - 2
    else:
        vs_human_you = human_avg - 2
        vs_human_other = human_avg + 2

    # Nash iteration explanation
    dominance_steps = [
        {"from": 100, "to": 99, "reason": "Wenn du 100 bietest und der andere auch – wechsle zu 99: du bekommst 99+2=101 statt 100"},
        {"from": 99, "to": 98, "reason": "Wenn du 99 bietest und der andere auch – wechsle zu 98: 98+2=100 > 99"},
        {"from": 98, "to": "...", "reason": "Dieses Argument wiederholt sich... bis zum Boden"},
        {"from": 3, "to": 2, "reason": "Der letzte Schritt: von 3 zu 2. Nash-Gleichgewicht = 2"},
    ]

    return templates.TemplateResponse(
        request,
        "partials/reisenden_dilemma_result.html",
        {
            "claim": claim,
            "your_payoff_vs_nash": your_payoff,
            "nash_payoff": nash_payoff,
            "vs_human_you": vs_human_you,
            "vs_human_other": vs_human_other,
            "human_avg": human_avg,
            "dominance_steps": dominance_steps,
        },
    )


# ---------------------------------------------------------------------------
# Condorcet-Paradoxon
# ---------------------------------------------------------------------------

CONDORCET_VOTERS = [
    {"name": "Wähler 1", "icon": "👤", "prefs": ["A", "B", "C"], "label": "A > B > C"},
    {"name": "Wähler 2", "icon": "👥", "prefs": ["B", "C", "A"], "label": "B > C > A"},
    {"name": "Wähler 3", "icon": "🧑", "prefs": ["C", "A", "B"], "label": "C > A > B"},
]

# Pairwise results
CONDORCET_DUELS = [
    {
        "match": "A vs. B",
        "winner": "A",
        "votes": {"A": 2, "B": 1},
        "voters_for_A": ["Wähler 1 (A>B)", "Wähler 3 (A>B)"],
        "voters_for_B": ["Wähler 2 (B>A)"],
    },
    {
        "match": "B vs. C",
        "winner": "B",
        "votes": {"B": 2, "C": 1},
        "voters_for_A": ["Wähler 1 (B>C)", "Wähler 2 (B>C)"],
        "voters_for_B": ["Wähler 3 (C>B)"],
    },
    {
        "match": "C vs. A",
        "winner": "C",
        "votes": {"C": 2, "A": 1},
        "voters_for_A": ["Wähler 2 (C>A)", "Wähler 3 (C>A)"],
        "voters_for_B": ["Wähler 1 (A>C)"],
    },
]


@router.get("/condorcet", response_class=HTMLResponse)
def condorcet_page(request: Request):
    return templates.TemplateResponse(
        request,
        "raetsel/condorcet.html",
        {"active_page": "raetsel", "voters": CONDORCET_VOTERS},
    )


@router.post("/condorcet/result", response_class=HTMLResponse)
def condorcet_result(request: Request):
    return templates.TemplateResponse(
        request,
        "partials/condorcet_result.html",
        {
            "voters": CONDORCET_VOTERS,
            "duels": CONDORCET_DUELS,
        },
    )


# ---------------------------------------------------------------------------
# Newcomb-Paradoxon
# ---------------------------------------------------------------------------

@router.get("/newcomb", response_class=HTMLResponse)
def newcomb_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/newcomb.html", {"active_page": "raetsel"}
    )


@router.post("/newcomb/result", response_class=HTMLResponse)
def newcomb_result(
    request: Request,
    choice: str = Form(...),   # "b_only" or "both"
):
    # Expected value calculation
    accuracy = 0.95
    ev_b_only = round(accuracy * 1_000_000)          # 950.000
    ev_both   = round(1_000 + (1 - accuracy) * 1_000_000)  # 51.000
    return templates.TemplateResponse(
        request,
        "partials/newcomb_result.html",
        {
            "choice": choice,
            "ev_b_only": ev_b_only,
            "ev_both": ev_both,
            "accuracy": int(accuracy * 100),
        },
    )


# ---------------------------------------------------------------------------
# Simpson-Paradoxon
# ---------------------------------------------------------------------------

# Klassisches Nierenstein-Beispiel (Charig et al. 1986)
SIMPSON_DATA = {
    "overall": {
        "A": {"success": 273, "total": 350, "rate": 78},
        "B": {"success": 289, "total": 350, "rate": 83},
        "winner": "B",
    },
    "small_stones": {
        "label": "Kleine Nierensteine",
        "A": {"success": 81, "total": 87, "rate": 93},
        "B": {"success": 234, "total": 270, "rate": 87},
        "winner": "A",
    },
    "large_stones": {
        "label": "Große Nierensteine",
        "A": {"success": 192, "total": 263, "rate": 73},
        "B": {"success": 55, "total": 80, "rate": 69},
        "winner": "A",
    },
}


@router.get("/simpson", response_class=HTMLResponse)
def simpson_page(request: Request):
    return templates.TemplateResponse(
        request,
        "raetsel/simpson.html",
        {
            "active_page": "raetsel",
            "overall": SIMPSON_DATA["overall"],
        },
    )


@router.post("/simpson/result", response_class=HTMLResponse)
def simpson_result(
    request: Request,
    choice: str = Form(...),  # "A" or "B"
):
    return templates.TemplateResponse(
        request,
        "partials/simpson_result.html",
        {
            "choice": choice,
            "data": SIMPSON_DATA,
        },
    )


# ---------------------------------------------------------------------------
# Geburtstagsparadoxon
# ---------------------------------------------------------------------------

import math as _math

_birthday_table = []
for _n in range(1, 51):
    _p_no_match = 1.0
    for _k in range(_n):
        _p_no_match *= (365 - _k) / 365
    _birthday_table.append({"n": _n, "prob": round((1 - _p_no_match) * 100, 1)})


@router.get("/geburtstag", response_class=HTMLResponse)
def geburtstag_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/geburtstag.html", {"active_page": "raetsel"}
    )


@router.post("/geburtstag/result", response_class=HTMLResponse)
def geburtstag_result(
    request: Request,
    guess: int = Form(...),   # player's guess for how many people needed for 50%
):
    # Correct answer: 23 people → 50.7%
    correct = 23
    diff = abs(guess - correct)
    if diff == 0:
        reaction = "exakt"
    elif diff <= 5:
        reaction = "nah"
    elif diff <= 15:
        reaction = "mittel"
    else:
        reaction = "weit"

    # Prob for player's guess
    p_no_match = 1.0
    for k in range(min(guess, 365)):
        p_no_match *= (365 - k) / 365
    p_guess = round((1 - p_no_match) * 100, 1)

    # Highlight a few milestones
    milestones = [
        {"n": 10, "prob": 11.7},
        {"n": 23, "prob": 50.7},
        {"n": 30, "prob": 70.6},
        {"n": 50, "prob": 97.0},
        {"n": 70, "prob": 99.9},
    ]
    return templates.TemplateResponse(
        request,
        "partials/geburtstag_result.html",
        {
            "guess": guess,
            "correct": correct,
            "diff": diff,
            "reaction": reaction,
            "p_guess": p_guess,
            "milestones": milestones,
            "table": _birthday_table,
        },
    )


# ---------------------------------------------------------------------------
# Zwei-Umschlag-Problem
# ---------------------------------------------------------------------------

@router.get("/zwei-umschlag", response_class=HTMLResponse)
def zwei_umschlag_page(request: Request):
    amount = _random.choice([10, 20, 50, 100, 200])
    return templates.TemplateResponse(
        request,
        "raetsel/zwei_umschlag.html",
        {"active_page": "raetsel", "amount": amount},
    )


@router.post("/zwei-umschlag/result", response_class=HTMLResponse)
def zwei_umschlag_result(
    request: Request,
    decision: str = Form(...),   # "stay" or "switch"
    amount: int = Form(...),
):
    # If player switches: 50% chance double (2*amount), 50% chance half (amount/2)
    ev_switch = 0.5 * (2 * amount) + 0.5 * (amount / 2)
    ev_stay = amount
    # The paradox: expected value calculation seems to say always switch
    # But this is wrong because the setup constrains the other envelope
    # If amount=X, other is either X/2 or 2X, so either you have the small or large one
    # True EV if amount is the small envelope: switch gives 2X (100% gain)
    # True EV if amount is the large envelope: switch gives X/2 (50% loss)
    # Without knowing which, EV=X always
    return templates.TemplateResponse(
        request,
        "partials/zwei_umschlag_result.html",
        {
            "decision": decision,
            "amount": amount,
            "ev_switch": round(ev_switch, 2),
            "ev_stay": ev_stay,
        },
    )


# ---------------------------------------------------------------------------
# Sekretärinnen-Problem (Optimal Stopping)
# ---------------------------------------------------------------------------

_sekr_candidates = [
    {"id": 1, "quality": 62, "rank_hint": "Gut"},
    {"id": 2, "quality": 85, "rank_hint": "Sehr gut"},
    {"id": 3, "quality": 41, "rank_hint": "Mittel"},
    {"id": 4, "quality": 93, "rank_hint": "Ausgezeichnet"},
    {"id": 5, "quality": 57, "rank_hint": "Gut"},
    {"id": 6, "quality": 78, "rank_hint": "Sehr gut"},
    {"id": 7, "quality": 34, "rank_hint": "Schwach"},
    {"id": 8, "quality": 89, "rank_hint": "Ausgezeichnet"},
    {"id": 9, "quality": 71, "rank_hint": "Sehr gut"},
    {"id": 10, "quality": 48, "rank_hint": "Mittel"},
]


@router.get("/sekretaerin", response_class=HTMLResponse)
def sekretaerin_page(request: Request):
    candidates = _sekr_candidates.copy()
    _random.shuffle(candidates)
    # Only show relative rank info (better/worse than seen so far), not absolute quality
    return templates.TemplateResponse(
        request,
        "raetsel/sekretaerin.html",
        {"active_page": "raetsel", "total": len(candidates)},
    )


@router.post("/sekretaerin/result", response_class=HTMLResponse)
def sekretaerin_result(
    request: Request,
    chosen_at: int = Form(...),    # which position player stopped at (1-10)
    chosen_quality: int = Form(...),  # quality of chosen candidate
    best_quality: int = Form(default=93),  # best available
):
    import math as _m
    n = 10
    # Optimal cutoff: stop after first 1/e ≈ 37% → round(10/e) = 4
    optimal_cutoff = round(n / _m.e)
    # Probability of success with optimal strategy ~= 1/e ≈ 36.8%
    optimal_prob = round(100 / _m.e, 1)

    got_best = chosen_quality == best_quality
    rank_fraction = round(chosen_quality / best_quality * 100)

    if got_best:
        outcome = "optimal"
    elif chosen_quality >= 85:
        outcome = "gut"
    elif chosen_quality >= 70:
        outcome = "mittel"
    else:
        outcome = "schlecht"

    return templates.TemplateResponse(
        request,
        "partials/sekretaerin_result.html",
        {
            "chosen_at": chosen_at,
            "chosen_quality": chosen_quality,
            "best_quality": best_quality,
            "got_best": got_best,
            "rank_fraction": rank_fraction,
            "outcome": outcome,
            "optimal_cutoff": optimal_cutoff,
            "optimal_prob": optimal_prob,
            "n": n,
        },
    )


# ---------------------------------------------------------------------------
# Braess-Paradoxon
# ---------------------------------------------------------------------------

# Network scenarios: without new road vs. with new road
BRAESS_NETWORK = {
    "without_road": {
        "label": "Ohne neue Straße",
        "routes": [
            {"name": "Oben (A→X→B)", "cost_formula": "t/100 + 45", "desc": "Variable Fahrtzeit + feste 45 min"},
            {"name": "Unten (A→Y→B)", "cost_formula": "45 + t/100", "desc": "Feste 45 min + variable Fahrtzeit"},
        ],
        "nash_time": 65,
        "optimal_time": 65,
        "is_paradox": False,
    },
    "with_road": {
        "label": "Mit neuer Straße A→Y und X→B direkt",
        "routes": [
            {"name": "Oben (A→X→B)", "cost_formula": "t/100 + 45", "desc": "Variable + 45 min"},
            {"name": "Unten (A→Y→B)", "cost_formula": "45 + t/100", "desc": "45 min + Variable"},
            {"name": "Neue Route (A→X→Y→B)", "cost_formula": "t/100 + 0 + t/100", "desc": "Nur variable Kosten – verlockend!"},
        ],
        "nash_time": 80,
        "optimal_time": 65,
        "is_paradox": True,
    },
}


@router.get("/braess", response_class=HTMLResponse)
def braess_page(request: Request):
    return templates.TemplateResponse(
        request,
        "raetsel/braess.html",
        {"active_page": "raetsel", "network": BRAESS_NETWORK},
    )


@router.post("/braess/result", response_class=HTMLResponse)
def braess_result(
    request: Request,
    choice: str = Form(...),   # "yes_new_road" or "no_new_road"
):
    return templates.TemplateResponse(
        request,
        "partials/braess_result.html",
        {
            "choice": choice,
            "network": BRAESS_NETWORK,
        },
    )
