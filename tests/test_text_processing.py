import unittest

from core.ticket import new_body, find_problem_score, find_negative_score
from definition.models import value_dict, problem_dict, negative_dict


class TestTextProcessing(unittest.TestCase):

    def test_new_body_corrections(self):
        text = "There is a payent eror and the sistem is broken"
        fixed = new_body(text.lower(), value_dict)
        self.assertIn("payment error", fixed)
        self.assertIn("system", fixed)
        self.assertNotIn("payent", fixed)
        self.assertNotIn("sistem", fixed)
 

    def test_find_problem_score_simple(self):
        text = "we have a payment error and then another payment error"
        text = new_body(text.lower(), value_dict)
        score, counts = find_problem_score(text, problem_dict)
        self.assertIn("payment error", counts)
        self.assertEqual(score, 100)

    def test_find_negative_score(self):
        text = "the situation is bad and very annoying"
        score = find_negative_score(text.lower(), negative_dict)
        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main()
