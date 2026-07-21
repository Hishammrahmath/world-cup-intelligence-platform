# Momentum Model

This document explains the first version of the match momentum model.

The goal is to create an explainable score by minute for each team. This is not
a prediction model and it does not prove that one event caused another.

## Inputs

The model uses events from:

```text
data/raw/match_events.csv
```

Each event should have:

```text
match_id
minute
event_type
team_id
player_id
```

## Event Weights

Each event type receives a simple point value.

| Event Type | Weight | Meaning |
| --- | ---: | --- |
| `Goal` | 5 | Major positive event. |
| `Assist` | 2 | Positive attacking event connected to a goal. |
| `Shot on Target` | 2 | Medium attacking pressure. |
| `Shot` | 1 | Small attacking pressure. |
| `Corner` | 1 | Small attacking pressure. |
| `VAR Review` | 1 | Notable match event. |
| `Penalty Shootout Goal` | 3 | Positive penalty shootout event. |
| `Penalty Shootout Miss` | -3 | Negative penalty shootout event. |
| `Yellow Card` | -1 | Small negative disciplinary event. |
| `Red Card` | -4 | Major negative disciplinary event. |

Unknown event types receive `0`.

## Formula

For each team and each minute:

```text
event_score = sum of event weights for that team in that minute
momentum_score = sum of recent event_score values inside the rolling window
```

The first version uses a five-minute rolling window.

Stoppage-time values are converted into normal minute numbers. For example, `90+6` becomes `96`.

Example:

```text
Minute 10: Goal (+5) and Assist (+2)
Event score: 7
Momentum score: sum of recent event scores in the five-minute window
```

## Output

The model returns rows with:

```text
minute
team_id
event_score
momentum_score
```

This shape is useful for a future frontend chart or animated momentum bar.

## Important Limits

- The model is explainable, not predictive.
- The model does not prove cause and effect.
- A future popup should say "momentum shifted near an event", not "because of an event".
- Scheduled matches can return zero momentum because they may not have event data yet.

## Future Improvements

Later versions can add:

- Better event weights after reviewing real match examples.
- Separate first-half, second-half, extra-time, and penalty shootout handling.
- Nearby event labels for frontend popups.
- Turning-point detection that looks for sustained momentum changes.


