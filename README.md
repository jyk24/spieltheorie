# Redesign-Skin (Beta) — Integration

Dieser Patch fügt eine **zusätzliche Designoption** hinzu, ohne das bestehende Tailwind-Design zu verändern.

## Dateien

```
app/static/redesign/        ← CSS + React/JSX-Komponenten der neuen Skin
app/templates/redesign.html ← Jinja-Einstieg (lädt die SPA)
app/routers/redesign.py     ← FastAPI-Router, mountet /redesign
```

## Schritt 1 — Dateien committen

Kopiere den Inhalt von `repo-patch/` in den Repo-Root, sodass die Pfade
exakt `app/static/redesign/...`, `app/templates/redesign.html` und
`app/routers/redesign.py` sind.

## Schritt 2 — Router in `app/main.py` registrieren

In `app/main.py` zwei kleine Änderungen:

```python
# alte Zeile:
from .routers import dashboard, lektionen, spiele, fortschritt, raetsel, grundlagen, spielpfad, konzepte, lernpfade, skills

# neue Zeile (ergänze 'redesign'):
from .routers import dashboard, lektionen, spiele, fortschritt, raetsel, grundlagen, spielpfad, konzepte, lernpfade, skills, redesign
```

Und ganz unten:

```python
app.include_router(redesign.router)
```

## Schritt 3 — Optional: Link in `base.html` Navigation

In `app/templates/base.html` kannst du im Nav-Block einen Link einfügen:

```html
<a href="/redesign" class="text-indigo-200 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">✨ Editorial (Beta)</a>
```

## Schritt 4 — Lokal testen

```bash
uvicorn app.main:app --reload
# http://localhost:8000/redesign
```

## Schritt 5 — Push

```bash
git checkout -b redesign-skin
git add app/static/redesign app/templates/redesign.html app/routers/redesign.py app/main.py
git commit -m "feat: add editorial redesign skin (beta) at /redesign"
git push origin redesign-skin
```

## Hinweise

- Die SPA ist **rein clientseitig** (React via CDN + Babel-in-browser). Sie zeigt Mock-Daten; keine DB-Anbindung.
- Light/Dark und DE/EN sind in der Topbar umschaltbar.
- Wenn du das Design später produktiv willst, müssen die Komponenten an die Jinja-Routes angebunden und (für Performance) serverseitig vorgerendert oder vorab transpiliert werden.
