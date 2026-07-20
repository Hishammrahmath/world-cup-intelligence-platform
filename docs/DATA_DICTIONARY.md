# Data Dictionary

This document describes the first four raw CSV files used by the World Cup
Intelligence Platform.

Raw files live in:

```text
data/raw/
```

Phase 1 and Phase 2 use only these files:

```text
teams.csv
matches.csv
match_events.csv
match_team_stats.csv
```

Do not edit files in `data/raw/` directly. Treat them as source data.

## Dataset Summary

| File | Rows | Purpose |
| --- | ---: | --- |
| `teams.csv` | 48 | Lists all tournament teams. |
| `matches.csv` | 104 | Lists all World Cup 2026 matches. |
| `match_events.csv` | 824 | Lists important in-match events. |
| `match_team_stats.csv` | 206 | Lists match-level team statistics. |

## Main Relationships

These IDs connect the files:

| ID | Meaning | Used In |
| --- | --- | --- |
| `team_id` | Unique team identifier. | `teams.csv`, `matches.csv`, `match_events.csv`, `match_team_stats.csv` |
| `match_id` | Unique match identifier. | `matches.csv`, `match_events.csv`, `match_team_stats.csv` |
| `player_id` | Unique player identifier. | `match_events.csv`, `matches.csv` |
| `venue_id` | Unique venue identifier. | `matches.csv` |
| `referee_id` | Unique referee identifier. | `matches.csv` |
| `stage_id` | Tournament stage identifier. | `matches.csv` |

Important joins:

| From | To | Meaning |
| --- | --- | --- |
| `matches.home_team_id` | `teams.team_id` | Finds the home team. |
| `matches.away_team_id` | `teams.team_id` | Finds the away team. |
| `match_events.match_id` | `matches.match_id` | Finds events for one match. |
| `match_events.team_id` | `teams.team_id` | Finds which team performed an event. |
| `match_team_stats.match_id` | `matches.match_id` | Finds team stats for one match. |
| `match_team_stats.team_id` | `teams.team_id` | Finds which team the stats belong to. |

## `teams.csv`

One row represents one national team.

| Column | Meaning | Empty Values |
| --- | --- | ---: |
| `team_id` | Unique ID for the team. | 0 |
| `team_name` | Full team name. | 0 |
| `fifa_code` | Three-letter FIFA code. | 0 |
| `group_letter` | Group stage group. | 0 |
| `confederation` | Football confederation, such as UEFA or CONCACAF. | 0 |
| `fifa_ranking_pre_tournament` | FIFA ranking before the tournament. | 0 |
| `elo_rating` | Elo rating before or during the dataset snapshot. | 0 |
| `manager_name` | Team manager name. | 0 |

## `matches.csv`

One row represents one match.

| Column | Meaning | Empty Values |
| --- | --- | ---: |
| `match_id` | Unique ID for the match. | 0 |
| `date` | Match date. | 0 |
| `kickoff_time_utc` | Kickoff time in UTC. | 0 |
| `stage_id` | ID for the tournament stage. | 0 |
| `venue_id` | ID for the stadium or venue. | 0 |
| `home_team_id` | Team ID for the home team. | 0 |
| `away_team_id` | Team ID for the away team. | 0 |
| `home_score` | Home team goals. | 0 |
| `away_score` | Away team goals. | 0 |
| `home_penalty_score` | Home team penalty shootout score, when needed. | 100 |
| `away_penalty_score` | Away team penalty shootout score, when needed. | 100 |
| `status` | Match status, such as Completed or Scheduled. | 0 |
| `result_type` | How the match ended, such as Regular, AET, or Penalties. | 1 |
| `home_xg` | Home team expected goals. | 0 |
| `away_xg` | Away team expected goals. | 0 |
| `referee_id` | ID for the referee. | 0 |
| `player_of_the_match_id` | Player ID for player of the match. | 0 |

Notes:

- `matches.csv` contains 104 matches.
- `home_penalty_score` and `away_penalty_score` are empty for most matches because most matches do not go to penalties.
- Match `104` is currently `Scheduled`, so related events and team stats are not present yet.
- `result_type` is empty for the scheduled match.

Current `result_type` counts:

| Result Type | Count |
| --- | ---: |
| `Regular` | 95 |
| `AET` | 4 |
| `Penalties` | 4 |
| Empty | 1 |

Current `status` counts:

| Status | Count |
| --- | ---: |
| `Completed` | 103 |
| `Scheduled` | 1 |

## `match_events.csv`

One row represents one event during a match.

| Column | Meaning | Empty Values |
| --- | --- | ---: |
| `event_id` | Unique ID for the event. | 0 |
| `match_id` | Match where the event happened. | 0 |
| `minute` | Match minute when the event happened. | 0 |
| `event_type` | Type of event. | 0 |
| `team_id` | Team connected to the event. | 0 |
| `player_id` | Player connected to the event. | 0 |

Current event types:

| Event Type | Count |
| --- | ---: |
| `Assist` | 202 |
| `Goal` | 307 |
| `Penalty Shootout Goal` | 25 |
| `Penalty Shootout Miss` | 15 |
| `Red Card` | 13 |
| `VAR Review` | 15 |
| `Yellow Card` | 247 |

Notes:

- Events connect to matches using `match_id`.
- Events connect to teams using `team_id`.
- Events connect to players using `player_id`, but player details are not part of Phase 1 or Phase 2 yet.
- Match `104` currently has no event rows because it is scheduled.

## `match_team_stats.csv`

One row represents one team's statistics in one match.

Usually, a completed match should have two rows: one for each team.

| Column | Meaning | Empty Values |
| --- | --- | ---: |
| `match_id` | Match connected to these stats. | 0 |
| `team_id` | Team connected to these stats. | 0 |
| `possession_pct` | Team possession percentage. | 0 |
| `total_shots` | Total shots by the team. | 0 |
| `shots_on_target` | Shots on target by the team. | 0 |
| `corners` | Corners won by the team. | 0 |
| `fouls` | Fouls committed by the team. | 0 |
| `offsides` | Offsides by the team. | 0 |
| `saves` | Saves made by the team. | 0 |
| `player_of_the_match` | Player of the match name, if listed on that row. | 103 |
| `data_source` | Source used for this stat row. | 0 |
| `last_updated` | Date when this row was last updated. | 0 |

Notes:

- This file has 206 rows, covering 103 matches with two teams each.
- Match `104` is scheduled and has no team stat rows yet.
- `player_of_the_match` is empty on many rows. This is expected because the value appears only on one row for many matches.

## Known Data Gaps

These are not bugs in our code, but they affect how we should write future code:

- Scheduled matches may not have events yet.
- Scheduled matches may not have team stats yet.
- Penalty shootout scores are empty unless the match went to penalties.
- `player_of_the_match` can be empty in `match_team_stats.csv`.
- Player, venue, referee, and stage details require extra CSV files that are not part of the current phase.

## Rules For Future Code

- Do not assume every match has events.
- Do not assume every match has team stats.
- Do not treat empty penalty scores as errors.
- Do not claim an event caused a momentum shift unless the data proves it.
- Keep joins explicit: use `match_id` for match data and `team_id` for team data.
