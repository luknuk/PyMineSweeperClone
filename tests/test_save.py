import sys, os
sys.path.append("..")
import unittest
import save_state

class TestLoadAndSave(unittest.TestCase):

    def test_saveAndLoad(self):
        expected = {
            "obj1": 1,
            "obj2": (1, 2)
        }
        save_state.save(expected)

        actual = save_state.load()
        self.assertEqual(expected, actual)

    def test_delete(self):
        save_state.destroy()
        # Assert that file does no longer exist.
        self.assertFalse(os.path.isfile(".save"))


if __name__ == "__main__":
    unittest.main()