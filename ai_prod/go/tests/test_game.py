import unittest
from go_game.core.config import GameConfig
from go_game.core.game import GoGame

class TestGame(unittest.TestCase):
    def setUp(self):
        self.config = GameConfig()
        self.game = GoGame(self.config)

    def test_game_initialization(self):
        state = self.game.get_state()
        self.assertEqual(state.current_player, 1)
        self.assertEqual(state.black_captures, 0)
        self.assertEqual(state.white_captures, 0)

    def test_valid_moves(self):
        moves = self.game.get_valid_moves()
        self.assertIn((3, 3), moves)  # Center moves should be valid
        self.assertIn((-1, -1), moves)  # Pass should be valid

if __name__ == '__main__':
    unittest.main()