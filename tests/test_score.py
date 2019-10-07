import sys, os
sys.path.append("..")
import unittest
from score import Scores

class testScoreBoard(unittest.TestCase):

    def test_database(self):
        # New Scoreboard object
        # Passes True to create a test database.
        sc = Scores(True)

        # Clear preexisting test scores.
        sc.clear_testscores()

        # Seed some test data
        seeds = (
            ("Ace", 867, "classic", "test"),
            ("Wild One", 745,"classic", "test"),
            ("Jimothy", 1042,"classic", "test"),
            ("Ace", 3377,"classic", "test")
        )

        # Write them to the high scoreslist
        for s in seeds:
            sc.write_highscore(s[0], s[1], s[2], s[3])

        # Save and close the connection
        sc.save()


        # New Scoreboard object
        sc = Scores(True)

        # Get the test scores
        hs = sc.get_highscores("classic", "test")

        actual = []
        for s in hs:
            actual += s

        # Test that the data is the same
        self.assertEqual(['Ace', 3377, 'Jimothy', 1042, 'Ace', 867, 'Wild One', 745], actual)

        # Save and close the connection
        sc.save()

        # Remove test database
        try:
            os.remove("test_scores.sqlite")
        except FileNotFoundError:
            print("")






if __name__ == "__main__":
    unittest.main()