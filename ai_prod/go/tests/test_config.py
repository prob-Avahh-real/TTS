import unittest
from go_game.core.config import GameConfig, AgentConfig

class TestConfig(unittest.TestCase):
    def test_game_config(self):
        config = GameConfig()
        self.assertEqual(config.board_size, 9)
        self.assertEqual(config.win_condition, 5)
        self.assertEqual(config.komi, 6.5)

    def test_agent_config(self):
        config = AgentConfig()
        self.assertEqual(config.learning_rate, 0.001)
        self.assertEqual(config.epsilon, 0.1)

if __name__ == '__main__':
    unittest.main()