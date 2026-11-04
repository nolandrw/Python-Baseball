# Delivery sequence and acceptance checks

1. **Integrate actual inputs.** Obtain missing Statcast/updater files, inventory
   dependencies and access rights, rotate legacy credentials, choose a permitted
   quote source. Record schema-versioned fixtures, including malformed payloads.
2. **Canonical data and labels.** Implement storage and ingestion; prove update
   idempotency, correction history and atomic recovery. Test doubleheaders,
   postponed/resumed games, absent innings, ten-half-inning totals against known
   linescores, PA deduplication and missing player mappings.
3. **Temporal features.** Implement identical training/inference snapshot builder.
   Test delayed Statcast, scratched starters, revised lineups/weather, as-of player
   mappings, missing projections and current-game exclusion. Add schema constraints,
   join coverage reports and fixed golden snapshots. Naive timestamps fail.
4. **Fit and evaluate.** Fit baselines then candidate models. Tests assert all game
   horizons share a fold, labels precede fitting cutoffs, transforms fit only train,
   calibration is disjoint and later than tuning, and the untouched test stays
   sealed. Repeated runs from the same manifest/seed reproduce predictions.
5. **Paper replay.** Test stale/suspended odds, F5/full-game mismatches, integer
   pushes, half lines, starter replacements, early games and book-specific voids.
   Test no-vig and expected return arithmetic; bootstrap by date, never quote.
6. **Shadow operation.** Persist pregame forecasts and source manifests locally
   without overwrite. Report predictive quality and coverage first. Add quote-based
   results only when timestamps and settlement rules support them. Human reviews
   model promotion; no automatic promotion or wager execution.
7. **Pitcher props.** Implement workload and K/outs distributions with independent
   labels, settlement fixtures, calibration and out-of-sample evaluation.

Current acceptance: offline availability and probability/settlement invariants
only. Full model and pipeline acceptance is pending stages 1-6. Model promotion
requires completed leakage/data audit, reproducibility, improvement on preregistered
out-of-sample metrics with uncertainty, acceptable subgroup behavior, and shadow
evidence. Set numeric tolerances before opening the holdout; no profitability claim
or specific sample-size guarantee is made now.

CI uses only standard-library tests, no network calls in tests, provider credentials,
datasets, artifacts or paid runners. It does not train or scrape on a schedule.
