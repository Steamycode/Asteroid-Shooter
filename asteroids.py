import random
from assets import AssetManager
from game_object import GameObject


class Asteroid(GameObject):
    
    def __init__(self):
        self._rank = 0
        self._image = None
        self._width = 0
        self._height = 0
        self._assets = AssetManager()
        self._random_spawn_location(self._assets._screen_width, self._assets._screen_height)
        self._set_velocity(self._assets._screen_width, self._assets._screen_height)

    def _random_spawn_location(self, width, height):
        self._ran_point = random.choice([(random.randrange(0, width + self._width), 
                                          random.choice([-self._height - 50, height + 5])),
                                          (random.choice([-self._width - 50, width + 5]),
                                           random.randrange(0, height + self._height))])
        self._x, self._y = self._ran_point

    def _set_velocity(self, width, height):      
        if self._x < width // 2:
            self.x_direction = 1
        else:
            self.x_direction = -1
        if self._y < height // 2:
            self.y_direction = 1
        else:
            self.y_direction = -1
        self.x_velocity = self.x_direction * random.randrange(1, 3)
        self.y_velocity = self.y_direction * random.randrange(1, 3)

    def move(self):
        self._x += self.x_velocity
        self._y += self.y_velocity

    def draw(self, win):
        super().draw(win)
        win.blit(self._image, (self._x, self._y))


class BigAsteroid(Asteroid):

    def __init__(self):
        super().__init__()
        self._rank = 3
        self._image = self._assets.big_asteroid_img
        self._width = 150
        self._height = 150


class MediumAsteroid(Asteroid):
    
    def __init__(self):
        super().__init__()
        self._rank = 2
        self._image = self._assets.medium_asteroid_img
        self._width = 100
        self._height = 100


class SmallAsteroid(Asteroid):
    
    def __init__(self):
        super().__init__()
        self._rank = 1
        self._image = self._assets.small_asteroid_img
        self._width = 50
        self._height = 50


class AsteroidFactory:
    
    def create_asteroid(self, rank):
        if rank == 3:
            return BigAsteroid()
        elif rank == 2:
            return MediumAsteroid()
        elif rank == 1:
            return SmallAsteroid()
