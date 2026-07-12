import os
import shutil

def create_directory_structure():
    # Define the base structure
    structure = {
        'go': {
            'go_game': {
                'core': ['__init__.py', 'config.py', 'board.py', 'game.py'],
                'models': ['__init__.py', 'networks.py'],
                'agents': ['__init__.py', 'base.py', 'q_learning.py', 'deep_learning.py'],
                'ui': ['__init__.py', 'display.py', 'input_handler.py', 'game_messages.py'],
                'utils': ['__init__.py', 'training.py'],
                '__init__.py': ''
            },
            'tests': {
                '__init__.py': '',
                'test_config.py': '',
                'test_board.py': '',
                'test_game.py': '',
                'test_agent.py': '',
                '_test_game.py': ''
            },
            'main.py': '',
            'setup.py': '',
            'requirements.txt': 'numpy\ntorch\npytest\n',
            'README.md': '# Go Game with AI\n\nA Go game implementation with Q-Learning and Deep Learning agents.'
        }
    }

    def create_structure(base_path, structure):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                if isinstance(content, list):
                    os.makedirs(path, exist_ok=True)
                    for file in content:
                        with open(os.path.join(path, file), 'w') as f:
                            f.write('')
                else:
                    with open(path, 'w') as f:
                        f.write(content)

    # Create the structure
    create_structure('.', structure)
    print("Directory structure created successfully!")

def copy_code_to_files():
    # Dictionary mapping file paths to their content
    files = {
        'go/tests/test_config.py': '''
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
''',
        'go/tests/test_board.py': '''
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
''',
        'go/tests/test_game.py': '''
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
''',
        'go/tests/test_agent.py': '''
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
'''
        # Add other files content here...
    }

    for file_path, content in files.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content.strip())

def main():
    try:
        create_directory_structure()
        copy_code_to_files()
        print("Project setup completed successfully!")
        print("\nTo run tests:")
        print("1. Individual test:")
        print("   python -m unittest go/tests/test_game.py")
        print("\n2. All tests:")
        print("   python -m unittest discover go/tests")
        print("\n3. Verbose output:")
        print("   python -m unittest discover -v go/tests")
    except Exception as e:
        print(f"Error during setup: {e}")

if __name__ == "__main__":
    main()
