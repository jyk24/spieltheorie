import json

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..game_engine import (
    SCENARIOS,
    gd_final_result,
    gd_play_round,
    trust_ai_return,
    trust_final_result,
    ultimatum_ai_offer,
    ultimatum_ai_response,
    ultimatum_score,
    verhandlung_ai_offer,
    verhandlung_score,
)
from ..services import save_game_session

router = APIRouter(prefix="/spiele")
templates = Jinja2Templates(directory="app/templates")

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
]


@router.get("", response_class=HTMLResponse)
def spiele_overview(request: Request):
    return templates.TemplateResponse(
        "spiele.html",
        {"request": request, "active_page": "spiele", "games": GAME_META},
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
    return templates.TemplateResponse(
        "games/gefangenendilemma.html",
        {
            "request": request,
            "active_page": "spiele",
            "strategies": GD_STRATEGIES,
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

    if is_final and final:
        save_game_session(
            db,
            game_type="gefangenendilemma",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=final["player_total"],
            ai_score=final["ai_total"],
        )

    return templates.TemplateResponse(
        "partials/gd_result.html",
        {
            "request": request,
            "round_result": round_result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "strategies": GD_STRATEGIES,
            "max_rounds": 10,
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
    return templates.TemplateResponse(
        "games/ultimatum.html",
        {
            "request": request,
            "active_page": "spiele",
            "strategies": ULTIMATUM_STRATEGIES,
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

    if is_final:
        total_player = sum(r["player_score"] for r in history)
        total_ai = sum(r["ai_score"] for r in history)
        result = "win" if total_player > total_ai else ("draw" if total_player == total_ai else "loss")
        save_game_session(
            db,
            game_type="ultimatum",
            ai_strategy=strategy,
            moves=history,
            result=result,
            score=total_player,
            ai_score=total_ai,
        )
    else:
        result = None
        total_player = total_ai = 0

    next_is_proposer = len(history) < 5

    return templates.TemplateResponse(
        "partials/ultimatum_result.html",
        {
            "request": request,
            "entry": entry,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "result": result,
            "total_player": sum(r["player_score"] for r in history),
            "total_ai": sum(r["ai_score"] for r in history),
            "next_is_proposer": next_is_proposer,
            "next_ai_offer": ultimatum_ai_offer(strategy, len(history)) if not next_is_proposer else None,
            "strategies": ULTIMATUM_STRATEGIES,
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
    return templates.TemplateResponse(
        "games/vertrauen.html",
        {
            "request": request,
            "active_page": "spiele",
            "strategies": TRUST_STRATEGIES,
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

    if is_final and final:
        save_game_session(
            db,
            game_type="vertrauen",
            ai_strategy=strategy,
            moves=history,
            result=final["result"],
            score=max(0, final["player_net"]),
            ai_score=max(0, final["ai_net"]),
        )

    return templates.TemplateResponse(
        "partials/trust_result.html",
        {
            "request": request,
            "round_result": result,
            "history": history,
            "history_json": json.dumps(history),
            "strategy": strategy,
            "is_final": is_final,
            "final": final,
            "strategies": TRUST_STRATEGIES,
            "cumulative_player": sum(r["player_net"] for r in history),
            "cumulative_ai": sum(r["ai_net"] for r in history),
        },
    )


# ---------------------------------------------------------------------------
# Verhandlungssimulation
# ---------------------------------------------------------------------------


@router.get("/verhandlung", response_class=HTMLResponse)
def verhandlung_page(request: Request):
    return templates.TemplateResponse(
        "games/verhandlung.html",
        {
            "request": request,
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

    if is_final:
        final_price = ai_result["final_price"] or round((player_offer + ai_result["offer"]) / 2)
        score_data = verhandlung_score(scenario, final_price, round_num)
        save_game_session(
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
        "partials/verhandlung_result.html",
        {
            "request": request,
            "entry": entry,
            "history": history,
            "history_json": json.dumps(history),
            "scenario_key": scenario_key,
            "scenario": scenario,
            "is_final": is_final,
            "score_data": score_data,
        },
    )
