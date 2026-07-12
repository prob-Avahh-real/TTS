import unittest
import numpy as np
from go_game.core.config import GameConfig
from go_game.core.board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.config = GameConfig()
        self.board = Board(self.config)

    def test_board_initialization(self):
        self.assertEqual(self.board.size, 9)
        self.assertTrue(np.all(self.board.board == 0))

    def test_get_neighbors(self):
        neighbors = self.board.get_neighbors(3, 3)
        expected = [(2, 3), (4, 3), (3, 2), (3, 4)]
        self.assertEqual(sorted(neighbors), sorted(expected))

if __name__ == '__main__':
    unittest.main()