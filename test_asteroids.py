import unittest
from scripts.asteroids import BigAsteroid, MediumAsteroid, SmallAsteroid, AsteroidFactory


class TestAsteroidLogic(unittest.TestCase):

    def test_check_off_screen(self):
        asteroid = BigAsteroid()
        asteroid.x = -51
        self.assertTrue(asteroid.check_off_screen(1280, 720))
        asteroid.y = 721
        self.assertTrue(asteroid.check_off_screen(1280, 720))
        asteroid.x = 400
        asteroid.y = 300
        self.assertFalse(asteroid.check_off_screen(1280, 720))

    def test_set_velocity(self):
        asteroid = BigAsteroid()
        asteroid.x = 100
        asteroid.y = 100
        asteroid.set_velocity(1280, 720)
        self.assertGreater(asteroid.x_velocity, 0)
        self.assertGreater(asteroid.y_velocity, 0)

        asteroid.x = 700
        asteroid.y = 500
        asteroid.set_velocity(1280, 720)
        self.assertLess(asteroid.x_velocity, 0)
        self.assertLess(asteroid.y_velocity, 0)

    def test_random_spawn_location(self):
        factory = AsteroidFactory()
        for _ in range(100):
            asteroid = factory.create_asteroid(3)
            self.assertTrue(asteroid.x < 0 or asteroid.x > 1280 or asteroid.y < 0 or asteroid.y > 720)

class TestAsteroidFactory(unittest.TestCase):
    
    def setUp(self):
        self.factory = AsteroidFactory()
    
    def test_create_big_asteroid(self):
        asteroid = self.factory.create_asteroid(3)
        self.assertIsInstance(asteroid, BigAsteroid)
        self.assertEqual(asteroid.rank, 3)
    
    def test_create_medium_asteroid(self):
        asteroid = self.factory.create_asteroid(2)
        self.assertIsInstance(asteroid, MediumAsteroid)
        self.assertEqual(asteroid.rank, 2)
    
    def test_create_small_asteroid(self):
        asteroid = self.factory.create_asteroid(1)
        self.assertIsInstance(asteroid, SmallAsteroid)
        self.assertEqual(asteroid.rank, 1)
    
    def test_invalid_rank_returns_none(self):
        asteroid = self.factory.create_asteroid(99)
        self.assertIsNone(asteroid)


if __name__ == '__main__':
    unittest.main()
