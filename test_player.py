import unittest
from scripts.player import Player
from scripts.assets import AssetManager
from scripts.bullet import Bullet


class TestPlayer(unittest.TestCase):
    
    def setUp(self):
        self.assets = AssetManager()
        self.player = Player()
    
    def test_turn_left(self):
        initial_angle = self.player.angle
        self.player.turn_left()
        self.assertEqual(self.player.angle, initial_angle + 5)
    
    def test_turn_right(self):
        initial_angle = self.player.angle
        self.player.turn_right()
        self.assertEqual(self.player.angle, initial_angle - 5)
    
    def test_fire(self):
        initial_bullet_count = len(self.player.bullets)
        bullet = Bullet(self.player._x, self.player._y, 1, 0)
        self.player.fire(bullet)
        self.assertEqual(len(self.player.bullets), initial_bullet_count + 1)
    
    def test_move(self):
        initial_y = self.player.y
        self.player.move()
        self.assertLess(self.player.y, initial_y)

    def test_update_rotation(self):
        initial_angle = self.player.angle
        self.player.update_rotation(10)
        self.assertEqual(self.player.angle, initial_angle + 10)
    
    def test_check_off_screen_wrap_right(self):
        self.player.x = self.assets.screen_width + 100
        self.player.check_off_screen(self.assets.screen_width, self.assets.screen_height)
        self.assertEqual(self.player.x, 0)
    
    def test_check_off_screen_wrap_left(self):
        self.player.x = -100
        self.player.check_off_screen(self.assets.screen_width, self.assets.screen_height)
        self.assertEqual(self.player.x, self.assets.screen_width)
    
    def test_check_off_screen_wrap_bottom(self):
        self.player.y = self.assets.screen_height + 100
        self.player.check_off_screen(self.assets.screen_width, self.assets.screen_height)
        self.assertEqual(self.player.y, 0)
    
    def test_check_off_screen_wrap_top(self):
        self.player.y = -100
        self.player.check_off_screen(self.assets.screen_width, self.assets.screen_height)
        self.assertEqual(self.player.y, self.assets.screen_height)


if __name__ == '__main__':
    unittest.main()
