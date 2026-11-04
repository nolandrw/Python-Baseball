import unittest
from datetime import datetime, timedelta, timezone
from mlb_f5.temporal import Observation, as_of
from mlb_f5.markets import paper_profit, poisson_probabilities


class TemporalTests(unittest.TestCase):
    def setUp(self):
        self.cutoff = datetime(2025, 6, 1, 19, tzinfo=timezone.utc)

    def row(self, value=1, revision=0, delay=-1):
        return Observation("123", "velocity", self.cutoff - timedelta(days=2),
                           self.cutoff + timedelta(hours=delay),
                           self.cutoff + timedelta(hours=delay), revision, value)

    def test_correction_cannot_rewrite_past(self):
        original, correction = self.row(), self.row(99, 1, 1)
        self.assertEqual(as_of([original, correction], "123", "velocity", self.cutoff), original)

    def test_late_ingestion_excluded(self):
        row = self.row()
        late = Observation(row.entity_id, row.feature, row.event_at, row.available_at,
                           self.cutoff + timedelta(seconds=1), 1, 5)
        self.assertIsNone(as_of([late], "123", "velocity", self.cutoff))

    def test_no_cross_entity_or_missing_fallback(self):
        self.assertIsNone(as_of([self.row()], "other", "velocity", self.cutoff))

    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):
            as_of([], "123", "velocity", datetime(2025, 1, 1))

    def test_ambiguous_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            as_of([self.row(), self.row()], "123", "velocity", self.cutoff)


class MarketTests(unittest.TestCase):
    def test_distribution_mass_and_push(self):
        p = poisson_probabilities(4.5, 4)
        self.assertAlmostEqual(sum(p.values()), 1)
        self.assertGreater(p["push"], 0)
        self.assertEqual(poisson_probabilities(4.5, 4.5)["push"], 0)

    def test_zero_runs_and_tail(self):
        self.assertEqual(poisson_probabilities(0, 0), {"under": 0, "push": 1, "over": 0})
        self.assertGreater(poisson_probabilities(30, 5)["over"], .999)

    def test_push_void_win_loss_distinct(self):
        def settle(runs, complete=True):
            return paper_profit(runs, 4, "over", 1.91,
                                complete_five=complete, rules_supported=True)
        self.assertEqual(settle(4), 0)
        self.assertIsNone(settle(4, False))
        self.assertAlmostEqual(settle(5), .91)
        self.assertEqual(settle(3), -1)

    def test_invalid_inputs_fail_closed(self):
        for mean, line in [(float("nan"), 4), (-1, 4), (4, 4.2)]:
            with self.assertRaises(ValueError):
                poisson_probabilities(mean, line)


if __name__ == "__main__":
    unittest.main()
