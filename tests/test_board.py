import sys
sys.path.append("..")
import unittest
from board import Board

class testFieldMethods(unittest.TestCase):

    def compare_board(self, board, expected):
        actual = board.get_board()
        self.assertEqual(actual, expected)

    def test_board(self):
        b = Board("test")
        gui = b.get_board()
        len_board = range(len(b.get_board()))

        # Test that it generates a blank board.
        expected_board = [False for i in len_board]
        self.compare_board(b, expected_board)

        # Test that we can look up a Field
        b.get_field((0, 0)).set_mine()
        b.reveal((0,0))
        expected_board = ["*", False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        self.compare_board(b, expected_board)

        # Test that it graphed properly
        expected = {(0, 0): [(0, 1), (1, 0), (1, 1)], (0, 1): [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)], (0, 2): [(0, 1), (0, 3), (1, 1), (1, 2), (1, 3)], (0, 3): [(0, 2), (1, 2), (1, 3)], (1, 0): [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)], (1, 1): [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)], (1, 2): [(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3)], (1, 3): [(0, 2), (0, 3), (1, 2), (2, 2), (2, 3)], (2, 0): [(1, 0), (1, 1), (2, 1), (3, 0), (3, 1)], (2, 1): [(1, 0), (1, 1), (1, 2), (2, 0), (2, 2), (3, 0), (3, 1), (3, 2)], (2, 2): [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)], (2, 3): [(1, 2), (1, 3), (2, 2), (3, 2), (3, 3)], (3, 0): [(2, 0), (2, 1), (3, 1)], (3, 1): [(2, 0), (2, 1), (2, 2), (3, 0), (3, 2)], (3, 2): [(2, 1), (2, 2), (2, 3), (3, 1), (3, 3)], (3, 3): [(2, 2), (2, 3), (3, 2)]}
        actual = b.graph
        self.assertEqual(expected, actual)

        # Test that we can count the mines
        b.count_mines()
        expected_board = ["*", 1, 0, False, 1, 1, False, False, False, False, False, False, False, False, False, False]
        b.reveal((0, 1))
        b.reveal((0, 2))
        b.reveal((1, 0))
        b.reveal((1, 1))
        self.compare_board(b, expected_board)

        # Test that recursive reveal worked
        expected_board = ["*", 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        b.reveal((3, 3))
        self.compare_board(b, expected_board)

        # Test that we can flag fields
        b.get_field((0, 0)).set_flag(True)
        self.assertTrue(b.get_field((0, 0)).flag)

        # Test that we can unflag fields
        b.get_field((0, 0)).set_flag(False)
        self.assertFalse(b.get_field((0, 0)).flag)

        # Test that we can get the total number of mines
        self.assertEqual(0, b.get_total_number_of_mines())

        # Test that we can lay a mine using the random lay_mines method
        b.lay_mines(3)
        actual = b.get_board()
        # We test for four, because we already layed one down
        self.assertEqual(4, actual.count("*"))









if __name__ == "__main__":
    unittest.main()