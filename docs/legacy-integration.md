# Legacy review and adapter contracts

The local workspace was empty before this checkout. The referenced chat returned
no attachments. No newer Statcast or updater files were available in the inspected
repository. These are integration contracts, not a claim those scripts were ported.

| Reviewed file | Finding | Migration |
| --- | --- | --- |
| baseball.py | Import-time CSV/network work, fixed weights, full-game win odds, mutates CSV logs | Keep as historical reference; new pure F5 training/inference entry points |
| lineups.py | Equal lineup means discard order; fixed six-inning starter; one away starter split uses home field | Port the projection/shrinkage idea, not fixed weights or workload assumptions |
| find_posted_lineups.py | Python 2 urllib2, fetches HTML at import, dated selectors, team-pair IDs | Fixture-tested parser plus explicit fetch function; game_pk and timestamps |
| starting_lineups.py | Embedded credentials, shared XML file, expected lineups treated as starters, old DH logic | Environment credentials, independent capture files, ordered IDs and explicit confirmation |
| merge_data.py | Name/team joins and inner game merge risk silent losses | MLB/provider ID crosswalk with unknown/ambiguous IDs quarantined and coverage reported |
| readme.md | Records original feeds and known name matching limitations | Retained historical documentation below new research entry point |

Hardcoded credential literals in starting_lineups.py were replaced with environment
variable access in this branch. This does not repair the legacy script or erase
credentials from Git history. Rotate the exposed provider credentials; do not run
this script as part of the new pipeline.

## Statcast script contract (pending actual file)

Input: explicit inclusive date range and output location, no wall-clock defaults.
Output: original response bytes/file plus manifest with retrieval time, source,
query, content hash and parser version. Normalize game_pk, at_bat_number,
pitch_number, pitcher and batter IDs; preserve nulls and revisions. Check expected
games and response completeness. Retry bounded date partitions and reconcile a
recent configurable window without deleting prior versions. Test overlapping
updates, empty dates, duplicate rows, schema additions and interrupted writes.
Never infer historical publication timestamps from game_date.

## Lineup scraper contract

Separate fetch from parse. parse(bytes, capture_metadata) returns game/team IDs,
ordered nine-player lineup, projected vs confirmed status, starter ID/status and
source publication time if provided. Unknown names must resolve via a reviewed
crosswalk or quarantine. A page showing nine names does not prove confirmation.
Persist scratches and replacements as new snapshots. Prefer structured sources
where permitted; retain HTML only as an authorized fallback with captured fixtures.

## Updater contract (pending actual file)

update(start, end, as_of, checkpoint) emits immutable captures and validated
partitions, then atomically publishes a manifest. Idempotency keys include source,
request window and content hash; a repeated identical response is a no-op, a changed
response is a revision. Advance the checkpoint only after validation and commit.
Timeouts, rate limits and partial fetches must not yield a success checkpoint.
Keep historical backfill and live capture modes explicit; neither may fabricate
past availability. No downstream training starts with partial inputs.

Bring the missing scripts into a follow-up branch for detailed review, credential
removal, fixture capture and adapter implementation. No placeholder live client
has been installed in their place.
