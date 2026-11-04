"""F5 reference distribution and paper settlement; never submits orders."""
from math import exp, isfinite


def poisson_probabilities(mean: float, line: float) -> dict[str, float]:
    """Exact CDF at the line; over retains all remaining tail mass."""
    if not isfinite(mean) or not 0 <= mean <= 100:
        raise ValueError("mean outside supported [0,100] range")
    if not isfinite(line) or not 0 <= line <= 100 or line * 2 != int(line * 2):
        raise ValueError("line must be a nonnegative integer or half integer <=100")
    mass = exp(-mean)
    under = push = 0.0
    for runs in range(int(line) + 1):
        if runs < line:
            under += mass
        elif runs == line:
            push = mass
        mass *= mean / (runs + 1)
    return {"under": under, "push": push, "over": max(0.0, 1 - under - push)}


def paper_profit(runs: int | None, line: float, side: str, decimal_odds: float,
                 *, complete_five: bool, rules_supported: bool) -> float | None:
    """Unit-stake return; None means void/unsupported, distinct from a push."""
    if side not in {"over", "under"}:
        raise ValueError("unknown side")
    if not isfinite(decimal_odds) or decimal_odds <= 1:
        raise ValueError("decimal odds must exceed one")
    if not isfinite(line) or line < 0 or line * 2 != int(line * 2):
        raise ValueError("invalid total line")
    if not complete_five or not rules_supported or runs is None:
        return None
    if isinstance(runs, bool) or not isinstance(runs, int) or runs < 0:
        raise ValueError("runs must be a nonnegative integer")
    if runs == line:
        return 0.0
    win = runs > line if side == "over" else runs < line
    return decimal_odds - 1 if win else -1.0
