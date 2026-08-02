# World Cup Intelligence Platform

A web application for explainable World Cup 2026 match intelligence.

The platform helps fans, players, and coaches review matches using:

- match details and scores
- team statistics
- event timelines
- momentum graphs
- turning point detection
- factual match explanations

## Current Status

Completed phases:

- Phase 1: Data Loader
- Phase 2: Data Dictionary
- Phase 3: Match Service
- Phase 4: Momentum Engine
- Phase 5: Turning Points
- Phase 6: FastAPI Backend
- Phase 7: Frontend Match Page
- Phase 8: Fan, Player, and Coach Views
- Phase 9: Factual Explanation Layer

## Backend

From the project root:

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend docs:

```text
http://127.0.0.1:8000/docs
```

Run backend tests:

```powershell
cd backend
python -m pytest tests
```

## Frontend

Open a second terminal from the project root:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Frontend app:

```text
http://127.0.0.1:3000
```

PowerShell may block plain `npm`, so use `npm.cmd` on this machine.

## Data

Raw CSV files should be placed in:

```text
data/raw/
```

Required files:

```text
teams.csv
matches.csv
match_events.csv
match_team_stats.csv
```

Raw CSV files are ignored by Git. The folder structure is kept with `.gitkeep` files.

## Explanation Rule

The explanation layer only uses facts calculated by the app. It should not invent events, players, statistics, tactics, or causes.

Correct wording:

```text
Momentum shifted near an event.
```

Avoid:

```text
Momentum shifted because of an event.
```
