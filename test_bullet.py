import unittest
from scripts.bullet import Bullet


class TestBullet(unittest.TestCase):
    
    def setUp(self):
        self.bullet = Bullet(100, 100, cos=1, sin=0)
    
    def test_bullet_move(self):
        initial_x = self.bullet.x
        self.bullet.move()
        self.assertGreater(self.bullet.x, initial_x)
    
    def test_bullet_off_screen(self):
        self.bullet.x = 100
        self.bullet.y = 560
        self.assertFalse(self.bullet.check_off_screen(1280, 720))
        self.assertTrue(self.bullet.check_off_screen(10, 337))


if __name__ == '__main__':
    unittest.main()
