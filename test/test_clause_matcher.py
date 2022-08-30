import sys
import unittest
sys.path.append('/Users/antoni/code/individual_project/confiscli/confiscomponents/')
from clausematcher import ClauseMatcher


class ClauseMatcherTesting(unittest.TestCase):
    def test_get(self):
        clausematcher = ClauseMatcher()
        matches = [(111, 10, 10) , (111, 100, 100)]
        new_matches = clausematcher.get_matches_with_sub_matches_removed(matches)
        self.assertEqual(matches, new_matches)

        matches_2 = [(111, 10, 10) , (111, 100, 100), (111, 90, 110)]
        new_matches_2_expected = [(111, 10, 10), (111, 90, 110)]
        new_matches_2 = clausematcher.get_matches_with_sub_matches_removed(matches_2)
        self.assertEqual(new_matches_2_expected, new_matches_2)


if __name__ == '__main__':
    unittest.main()
