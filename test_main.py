import unittest
from unittest.mock import patch, mock_open


class TestGame(unittest.TestCase):
    
    @patch('pygame.display.set_mode')
    @patch('pygame.font.SysFont')
    @patch('builtins.open', new_callable=mock_open, read_data='1000')
    def test_game_initialization(self, mock_file, mock_font, mock_display):
        from main import Game
        
        game = Game()
        
        self.assertIsNotNone(game.assets)
        self.assertIsNotNone(game.game_state)
        self.assertIsNotNone(game.player)
        self.assertIsNotNone(game.collision)
        self.assertIsNotNone(game.asteroid_factory)
        self.assertIsNotNone(game.window)
        self.assertIsNotNone(game.clock)
        self.assertIsNotNone(game.font)
    
    @patch('pygame.display.set_mode')
    @patch('pygame.font.SysFont')
    @patch('builtins.open', new_callable=mock_open, read_data='5000')
    def test_load_high_score(self, mock_file, mock_font, mock_display):
        from main import Game
        
        game = Game()
        self.assertEqual(game.game_state.high_score, 5000)
    
    @patch('pygame.display.set_mode')
    @patch('pygame.font.SysFont')
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_high_score_default(self, mock_file, mock_font, mock_display):
        from main import Game
        
        game = Game()
        self.assertEqual(game.game_state.high_score, 0)


if __name__ == '__main__':
    unittest.main()
