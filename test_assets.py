import unittest
from scripts.assets import AssetManager


class TestAssetManager(unittest.TestCase):
    
    def test_singleton_instance(self):
        manager1 = AssetManager()
        manager2 = AssetManager()
        self.assertIs(manager1, manager2)
    
    def test_bg_img_loaded(self):
        manager = AssetManager()
        self.assertIsNotNone(manager.bg_img)
    
    def test_ship_img_loaded(self):
        manager = AssetManager()
        self.assertIsNotNone(manager.ship_img)
    
    def test_asteroid_images_loaded(self):
        manager = AssetManager()
        self.assertIsNotNone(manager.big_asteroid_img)
        self.assertIsNotNone(manager.medium_asteroid_img)
        self.assertIsNotNone(manager.small_asteroid_img)
    
    def test_sounds_loaded(self):
        manager = AssetManager()
        self.assertIsNotNone(manager.shoot_sound)
        self.assertIsNotNone(manager.explosion_sound)


if __name__ == '__main__':
    unittest.main()
