# rice_score.py

Deterministic RICE calculator for the `rice-prioritization` skill. The model
decides the scale values (judgment); this script does the arithmetic, ranking,
tie-flagging, and sensitivity (mechanics). Stdlib only, no venv.

## Run

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/rice_score.py candidates.json
python3 ${CLAUDE_SKILL_DIR}/scripts/rice_score.py --format table candidates.json
cat candidates.json | python3 ${CLAUDE_SKILL_DIR}/scripts/rice_score.py -
python3 ${CLAUDE_SKILL_DIR}/scripts/rice_score.py --tolerance 0.15 candidates.json
```

## Input

A JSON list. Each candidate:

| Key | Meaning | Rules |
|---|---|---|
| `name` | Candidate label | Required, unique across the list |
| `reach` | Absolute count in the round's one fixed time window | Required, >= 0 |
| `impact` | Canonical RICE multiplier | Required, one of `3, 2, 1, 0.5, 0.25` |
| `confidence` | Certainty in the estimates | Required, `0-1` fraction or `1-100` percentage (auto-normalized); `> 0`, `<= 100` |
| `effort` | Person-months across ALL disciplines | Required, `> 0` |

Extra keys (`notes`, `reach_source`, `evidence`, `needs_human`, etc.) pass
through to the output untouched, so the skill can carry provenance alongside
the numbers.

Bad input fails loudly with a non-zero exit (impact off the canonical scale,
effort <= 0, confidence > 100, duplicate names, malformed JSON). The script
never guesses a fix.

## Output

`--format json` (default) returns:

```json
{
  "tolerance": 0.15,
  "results": [ { ...candidate, "rice_score": 53.33, "rank": 1, "tie_group": null }, ... ],
  "ties":   [ { "tie_group": 1, "members": ["A", "B"] } ],
  "sensitivity": [
    {
      "pair": ["A", "B"],
      "score_gap": 100.0,
      "lower_item_confidence_to_overtake": 0.538,
      "current_lower_confidence": 0.5,
      "flippable_by_confidence_alone": true
    }
  ]
}
```

- `rice_score` = `(reach x impact x confidence) / effort`, rounded to 2 dp. Ranking uses full precision.
- `tie_group` marks candidates within `--tolerance` (default 15%) of an adjacent score. Same id = too close to call given RICE's estimation noise; do not rank them against each other on score alone.
- `sensitivity` walks adjacent pairs and reports the confidence the lower item would need to overtake the higher. `flippable_by_confidence_alone: true` means the order is fragile and worth validating before committing.

`--format table` prints a compact ranked table plus the tie summary for quick reading.

## Verified examples

These match published worked examples and are the script's regression anchors:

- Savio MRR set -> Permissions & Roles `53.33` > Zapier `42.50` > Streak `12.50`.
- Whatfix single case `(1500 x 2 x 0.5) / 2` -> `750`.

See `../references/rice-methodology.md` for the full worked examples and sources.
