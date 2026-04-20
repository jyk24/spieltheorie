"""Konzepte – Tiefe Spieltheorie-Konzepte mit interaktiven Visualisierungen."""
import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

NOBELPREIS_TIMELINE = [
    {"jahr": 1994, "person": "John Nash, John Harsanyi, Reinhard Selten", "beitrag": "Nash-Gleichgewicht, Bayesianische Spiele, Teilspielperfektes Gleichgewicht"},
    {"jahr": 1996, "person": "James Mirrlees, William Vickrey", "beitrag": "Asymmetrische Information, Anreize, Auktionstheorie"},
    {"jahr": 2001, "person": "George Akerlof, Michael Spence, Joseph Stiglitz", "beitrag": "Märkte mit asymmetrischer Information, Adverse Selektion, Signaling"},
    {"jahr": 2005, "person": "Robert Aumann, Thomas Schelling", "beitrag": "Konflikt & Kooperation, Focal Points, Commitment"},
    {"jahr": 2007, "person": "Leonid Hurwicz, Eric Maskin, Roger Myerson", "beitrag": "Mechanismus-Design, Implementierungstheorie"},
    {"jahr": 2009, "person": "Elinor Ostrom, Oliver Williamson", "beitrag": "Kollektive Ressourcen, Transaktionskosten"},
    {"jahr": 2012, "person": "Alvin Roth, Lloyd Shapley", "beitrag": "Matching-Theorie, Shapley-Wert, Marktdesign"},
    {"jahr": 2014, "person": "Jean Tirole", "beitrag": "Marktmacht, Regulierung, Plattformökonomie"},
    {"jahr": 2016, "person": "Oliver Hart, Bengt Holmström", "beitrag": "Vertragstheorie, Unvollständige Verträge, Anreize"},
    {"jahr": 2020, "person": "Paul Milgrom, Robert Wilson", "beitrag": "Auktionstheorie, Auktionsdesign"},
]

SPIELTYPEN = [
    {
        "name": "Nullsummenspiele",
        "icon": "⚖️",
        "beschreibung": "Was einer gewinnt, verliert der andere. Kein gemeinsamer Gewinn möglich.",
        "beispiele": ["Schere-Stein-Papier", "Gleiche Münzen", "Poker"],
        "loesung": "Minimax / Gemischte Strategien",
        "farbe": "red",
    },
    {
        "name": "Koordinationsspiele",
        "icon": "🎯",
        "beschreibung": "Beide wollen koordinieren, aber welche Option wählen? Mehrere Nash-Gleichgewichte.",
        "beispiele": ["Fahren rechts/links", "Battle of the Sexes", "Stag Hunt"],
        "loesung": "Focal Points, Kommunikation",
        "farbe": "blue",
    },
    {
        "name": "Soziale Dilemmata",
        "icon": "🔒",
        "beschreibung": "Individuelle Rationalität führt zu kollektivem Versagen.",
        "beispiele": ["Gefangenendilemma", "Öffentliche Güter", "Freiwilligen-Dilemma"],
        "loesung": "Wiederholung, Reputation, Institutionen",
        "farbe": "amber",
    },
    {
        "name": "Verhandlungsspiele",
        "icon": "💼",
        "beschreibung": "Aufteilung eines gemeinsamen Überschusses. Wer erhält welchen Anteil?",
        "beispiele": ["Ultimatumspiel", "Rubinstein-Bargaining", "Nash-Bargaining"],
        "loesung": "Drohpunkte, Zeitdiskontierung, Fairness",
        "farbe": "emerald",
    },
    {
        "name": "Evolutionäre Spiele",
        "icon": "🧬",
        "beschreibung": "Strategien breiten sich durch natürliche Selektion aus. Rationalität nicht vorausgesetzt.",
        "beispiele": ["Habicht-Taube", "Hawk-Dove-Blot", "Replicator Dynamics"],
        "loesung": "Evolutionär Stabile Strategien (ESS)",
        "farbe": "violet",
    },
    {
        "name": "Bayesianische Spiele",
        "icon": "🎲",
        "beschreibung": "Spieler haben private Information über ihren 'Typ'. Updates nach Beobachtungen.",
        "beispiele": ["Auktionen", "Arbeitsmarkt-Signaling", "Kreditvergabe"],
        "loesung": "Bayes-Nash-Gleichgewicht, Screening, Signaling",
        "farbe": "indigo",
    },
]

NASH_MATRIX_EXAMPLES = [
    {
        "name": "Gefangenendilemma",
        "rows": ["Kooperieren", "Verraten"],
        "cols": ["Kooperieren", "Verraten"],
        "payoffs": [[[3,3],[0,5]],[[5,0],[1,1]]],
        "nash": [[1,1]],
        "pareto_optimal": [[0,0],[0,1],[1,0]],
        "info": "Einziges Nash-GG ist (Verraten, Verraten) – obwohl (Kooperieren, Kooperieren) besser für beide wäre.",
    },
    {
        "name": "Battle of the Sexes",
        "rows": ["Option A", "Option B"],
        "cols": ["Option A", "Option B"],
        "payoffs": [[[3,1],[0,0]],[[0,0],[1,3]]],
        "nash": [[0,0],[1,1]],
        "pareto_optimal": [[0,0],[1,1]],
        "info": "Zwei reine Nash-GGs: (A,A) und (B,B). Jeder bevorzugt ein anderes. Plus gemischtes GG.",
    },
    {
        "name": "Hirschjagd (Stag Hunt)",
        "rows": ["Hirsch", "Hase"],
        "cols": ["Hirsch", "Hase"],
        "payoffs": [[[4,4],[0,2]],[[2,0],[2,2]]],
        "nash": [[0,0],[1,1]],
        "pareto_optimal": [[0,0]],
        "info": "Zwei Nash-GGs: (Hirsch,Hirsch) und (Hase,Hase). Hirsch ist Pareto-optimal, Hase ist risikodomiant.",
    },
]


@router.get("/konzepte", response_class=HTMLResponse)
def konzepte_page(request: Request):
    return templates.TemplateResponse(
        request,
        "konzepte.html",
        {
            "active_page": "konzepte",
            "nobelpreis": NOBELPREIS_TIMELINE,
            "spieltypen": SPIELTYPEN,
            "nash_examples": NASH_MATRIX_EXAMPLES,
            "nash_examples_json": json.dumps(NASH_MATRIX_EXAMPLES),
        },
    )
