import sys
sys.path.append("..")
import unittest
from field import Field

class testFieldMethods(unittest.TestCase):

    def test_mine(self):
        f = Field()
        f.set_mine()
        self.assertEqual("*", f.value)
        self.assertEqual(True, f.is_mined)

    def test_flag(self):
        f = Field()
        # Tests that flag is false by default
        self.assertEqual(False, f.flag)
        # Test that we can set flag to true
        f.set_flag(True)
        self.assertEqual(True, f.flag)
        # Test that we can set flag to false
        f.set_flag(False)
        self.assertEqual(False, f.flag)

    def test_increment(self):
        f = Field()

        # Try adding one
        f.increment()
        self.assertEqual(1, f.value)
        # Try adding another
        f.increment()
        self.assertEqual(2, f.value)
        # Mines should override values
        f.set_mine()
        f.increment()
        self.assertEqual("*", f.value)
        # Flagging should not affect value
        f.set_flag(True)
        f.increment()
        self.assertEqual("*", f.value)

    def test_reveal(self):
        f = Field()

        # Check that a Field is not revealed by default
        self.assertEqual(False, f.revealed)

        # Try revealing
        f.reveal()
        self.assertEqual(True, f.revealed)



if __name__ == "__main__":
    unittest.main()