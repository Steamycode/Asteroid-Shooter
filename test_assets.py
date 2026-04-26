import unittest
from scripts.game_state import GameState


class TestGameState(unittest.TestCase):
    
    def setUp(self):
        self.game_state = GameState()
    
    def test_gamestate_add_score(self):
        initial_score = self.game_state.score
        self.game_state.add_score(10)
        self.assertEqual(self.game_state.score, initial_score + 10)
    
    def test_gamestate_lose_life(self):
        initial_lives = self.game_state.lives
        self.game_state.lose_life()
        self.assertEqual(self.game_state.lives, initial_lives - 1)
    
    def test_gamestate_lose_all_lives_triggers_gameover(self):
        self.game_state.lose_life()
        self.game_state.lose_life()
        self.game_state.lose_life()
        self.assertTrue(self.game_state.gameover)
    
    def test_gamestate_toggle_sound(self):
        initial_state = self.game_state.sound_on
        self.game_state.toggle_sound()
        self.assertNotEqual(self.game_state.sound_on, initial_state)
        self.game_state.toggle_sound()
        self.assertEqual(self.game_state.sound_on, initial_state)



if __name__ == '__main__':
    unittest.main()
