import unittest
from backgammon.core.dice import Dice

class TestDice(unittest.TestCase):

    def setUp(self):
        self.dice = Dice()

    def test_initial_values(self):
        """Al iniciar debe estar en (0,0)."""
        self.assertEqual(self.dice.get_values(), (0,0))

    def test_roll_returns_two_values(self):
        """roll debe devolver dos valores entre 1-6."""
        d1, d2 = self.dice.roll()
        self.assertTrue(1 <= d1 <= 6)
        self.assertTrue(1 <= d2 <= 6)

    def test_last_roll_updates(self):
        """get_values debe devolver la última tirada."""
        roll = self.dice.roll()
        self.assertEqual(self.dice.get_values(), roll)

    def test_roll_double_forces_equal_values(self):
        """roll_double debe devolver un doble."""
        d1, d2 = self.dice.roll_double()
        self.assertEqual(d1, d2)
        self.assertTrue(1 <= d1 <= 6)

    def test_roll_double_updates_last_roll(self):
        """roll_double debe actualizar last_roll."""
        roll = self.dice.roll_double()
        self.assertEqual(self.dice.get_values(), roll)

if __name__ == "__main__":
    unittest.main()
