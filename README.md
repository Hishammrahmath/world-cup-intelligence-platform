# MatchIQ

**Explainable momentum analytics for all 104 FIFA World Cup 2026 matches.**

Live demo: _coming soon_

Box scores show who had the ball. MatchIQ shows *when* a match swung. It turns
raw match events into a minute-by-minute momentum score for each team, detects
the turning points where momentum changed most, and explains each match using
only facts it can calculate.

## What it does

- **Momentum model.** Each event gets a weight (goal +5, shot on target +2,
  corner +1, red card −4, and so on). Momentum is the rolling sum over a
  5-minute window, per team, per minute. See [docs/MOMENTUM_MODEL.md](docs/MOMENTUM_MODEL.md).
- **Turning-point detection.** Flags any 5-minute stretch where a team's
  momentum rises by 5 or more, links the match events within 2 minutes of it,
  and removes overlapping detections.
- **Fact-only explanations.** Fan, player, and coach views summarize each match
  without inventing causes: momentum shifted *near* an event, not *because of* it.
- **Dashboard.** Interactive Plotly momentum chart, team stats, turning points,
  and an event timeline for every match.

## Stack

| Layer | Tools |
| --- | --- |
| Data and modeling | Python, pandas |
| API | FastAPI, tested with pytest |
| Frontend | Next.js, React, TypeScript, Plotly |
| Hosting | Vercel (static data export) |

## Data

Four related CSV files from the [FIFA World Cup 2026 Dataset](https://github.com/mominullptr/FIFA-World-Cup-2026-Dataset) (CC0): `teams.csv` (48
teams), `matches.csv` (104 matches), `match_events.csv`, and
`match_team_stats.csv`. Column definitions are in
[docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md). Raw CSVs go in `data/raw/`
and are not committed.

## Run it locally

Backend API:

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload    # docs at http://127.0.0.1:8000/docs
python -m pytest tests
```

Frontend (reads the exported JSON in `frontend/public/data/`):

```bash
cd frontend
npm install
npm run dev                                # http://localhost:3000
```

To point the frontend at the live API instead, set
`NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`.

## Refresh the hosted data

The hosted site needs no backend. After changing the model, regenerate the
static JSON and commit it:

```bash
cd backend
python -m scripts.export_static
```

## Explanation rule

The explanation layer only uses facts calculated by the app. It never invents
events, players, statistics, tactics, or causes.

```text
Correct: Momentum shifted near an event.
Avoid:   Momentum shifted because of an event.
```
