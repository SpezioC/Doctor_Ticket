import unittest

from definition.scores_rules import score, score_problem, score_critical
from definition.models import problem_dict


class TestScoreFunctions(unittest.TestCase):

    def test_score_basic_combination(self):
        s = score(score_alert=10, score_problem=50, score_negative=5)
        self.assertEqual(s, 47)

    def test_score_critical_no_problems(self):
        prio = score_critical(score=0, problem_count={})
        self.assertEqual(prio, "problem don't found")

    def test_score_critical_single_heavy_problem(self):
        heavy_key = None
        for k, v in problem_dict.items():
            if v >= 130:
                heavy_key = k
                break
        self.assertIsNotNone(heavy_key, "serve almeno un problema con peso >=130")

        prio = score_critical(score=10, problem_count={heavy_key: 1})
        self.assertEqual(prio, "critical")

    def test_score_critical_multiple_problems(self):
        words = ["payment error", "pipe leak", "production stopped"]
        score_value, problem_count = score_problem(words)
        prio = score_critical(score_value, problem_count)
        assert prio == "critical"

    def test_score_critical_thresholds(self):
        low = score_critical(score=10, problem_count={"payment error": 1})
        medium = score_critical(score=60, problem_count={"payment error": 1})
        high = score_critical(score=120, problem_count={"payment error": 1})
        self.assertEqual(low, "low")
        self.assertEqual(medium, "medium")
        self.assertEqual(high, "high")


if __name__ == "__main__":
    unittest.main()
