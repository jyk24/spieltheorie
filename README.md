# Spieltheorie & Verhandlungstrainer

Ein interaktiver Verhandlungstrainer auf Basis spieltheoretischer Konzepte.
Spiele gegen KI-Gegner und lerne durch wissenschaftlich fundierte Lektionen.

## Features

- **4 Spiele**: Gefangenendilemma, Ultimatumspiel, Vertrauensspiel, Verhandlungssimulation
- **16 Lektionen**: Von Nash-Gleichgewicht bis Taktische Empathie
- **KI-Strategien**: Tit-for-Tat, Grim Trigger, Nash Bargaining und mehr
- **Fortschrittstracking**: Punkte, Statistiken und Lernpfad
- **Wissenschaftliche Basis**: Fisher & Ury, Axelrod, Kahneman, Voss, Schelling

## Installation

```bash
cd E:\User\Documents\Apps\Spieltheorie
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Dann im Browser: http://localhost:8000

## Tech Stack

- **Backend**: FastAPI + Python
- **DB**: SQLAlchemy + SQLite
- **Frontend**: Jinja2 + Tailwind CSS + HTMX + Chart.js

## Wissenschaftliche Quellen

| Konzept | Quelle |
|---|---|
| Nash-Gleichgewicht | Nash (1951), Dixit & Nalebuff (1991) |
| Tit-for-Tat | Axelrod (1984) |
| Prospect Theory | Kahneman & Tversky (1979) |
| Ultimatumspiel | Güth et al. (1982) |
| Rubinstein Bargaining | Rubinstein (1982) |
| BATNA / Harvard-Konzept | Fisher & Ury (1981) |
| Taktische Empathie | Voss (2016) |
| Signaling | Schelling (1960), Spence (1973) |
