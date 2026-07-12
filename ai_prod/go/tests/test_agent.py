import unittest
from go_game.core.config import GameConfig, AgentConfig
from go_game.agents.q_learning import QLearningAgent
from go_game.core.game import GoGame

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.game_config = GameConfig()
        self.agent_config = AgentConfig()
        self.agent = QLearningAgent(self.game_config, self.agent_config)
        self.game = GoGame(self.game_config)

    def test_agent_initialization(self):
        self.assertEqual(self.agent.epsilon, self.agent_config.epsilon)
        self.assertEqual(self.agent.lr, self.agent_config.learning_rate)

    def test_agent_action(self):
        state = self.game.get_state()
        valid_moves = self.game.get_valid_moves()
        action = self.agent.get_action(state, valid_moves)
        self.assertIn(action, valid_moves)

if __name__ == '__main__':
    unittest.main()