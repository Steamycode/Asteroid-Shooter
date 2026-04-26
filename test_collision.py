import unittest
from scripts.collision import Collision
from scripts.asteroids import AsteroidFactory
from scripts.player import Player
from scripts.game_state import GameState
from scripts.bullet import Bullet


class TestCollision(unittest.TestCase):
    
    def setUp(self):
        self.collision = Collision()
        self.factory = AsteroidFactory()
        self.player = Player()
        self.game_state = GameState()
    
    # Player collision tests
    def test_check_player_collision_true(self):
        asteroid = self.factory.create_asteroid(3)
        asteroid.x = self.player.x
        asteroid.y = self.player.y
        self.assertTrue(self.collision.check_player_collision(asteroid, self.player))
    
    def test_check_player_collision_false(self):
        asteroid = self.factory.create_asteroid(3)
        asteroid.x = 0
        asteroid.y = 0
        self.player.x = 1000
        self.player.y = 1000
        self.assertFalse(self.collision.check_player_collision(asteroid, self.player))
    
    # Bullet collision tests
    def test_check_bullet_collision_hit(self):
        asteroid = self.factory.create_asteroid(3)
        bullet = Bullet(asteroid.x, asteroid.y, 1, 0)
        self.player.fire(bullet)
        
        result = self.collision.check_bullet_collision(asteroid, self.player)
        self.assertIsNotNone(result)
    
    def test_check_bullet_collision_checks_all_bullets(self):
        asteroid = self.factory.create_asteroid(3)
        
        # Fire bullets that don't hit
        bullet1 = Bullet(-100, -100, 1, 0)
        self.player.fire(bullet1)
        
        bullet2 = Bullet(-200, -200, 1, 0)
        self.player.fire(bullet2)
        
        # Fire a bullet that hits
        bullet3 = Bullet(asteroid.x, asteroid.y, 1, 0)
        self.player.fire(bullet3)
        
        # Should find the colliding bullet
        result = self.collision.check_bullet_collision(asteroid, self.player)
        self.assertIsNotNone(result)
        self.assertEqual(result, bullet3)
    
    # Asteroid collision handling tests
    def test_handle_bullet_asteroid_collision_big_asteroid(self):
        asteroid = self.factory.create_asteroid(3)
        asteroids = [asteroid]
        bullet = Bullet(asteroid.x, asteroid.y, 1, 0)
        self.player.fire(bullet)
        
        initial_asteroids = len(asteroids)
        initial_score = self.game_state.score
        
        self.collision.handle_bullet_asteroid_collision(self.player, bullet, asteroid, asteroids, self.game_state)
        
        self.assertEqual(len(asteroids), initial_asteroids + 1)  # 1 removed, 2 added
        self.assertEqual(self.game_state.score, initial_score + 10)
        self.assertEqual(len(self.player.bullets), 0)  # Bullet removed


if __name__ == '__main__':
    unittest.main()
