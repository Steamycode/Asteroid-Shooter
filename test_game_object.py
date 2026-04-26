import unittest
from scripts.game_object import GameObject


class TestGameObject(unittest.TestCase):
    
    def test_gameobject_is_abstract(self):
        with self.assertRaises(TypeError):
            GameObject()
    
    def test_gameobject_requires_all_abstract_methods(self):
        class IncompleteObject(GameObject):
            def draw(self):
                pass
        
        with self.assertRaises(TypeError):
            IncompleteObject()
    
    def test_gameobject_subclass_with_all_methods(self):
        class CompleteObject(GameObject):
            def draw(self):
                pass
            
            def move(self):
                pass
            
            def check_off_screen(self):
                pass
        
        self.assertIsNotNone(CompleteObject())


if __name__ == '__main__':
    unittest.main()
