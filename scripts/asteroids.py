import random
from scripts.assets import AssetManager
from scripts.game_object import GameObject


class Asteroid(GameObject):
    
    def __init__(self):
        self._rank = 0
        self._image = None
        self._width = 0
        self._height = 0
        self._assets = AssetManager()
        self.random_spawn_location(self.assets.screen_width, self.assets.screen_height)
        self.set_velocity(self.assets.screen_width, self.assets.screen_height)

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
    
    @property
    def x_direction(self):
        return self._x_direction
    
    @property
    def x_velocity(self):
        return self._x_velocity
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value

    @property
    def y_velocity(self):
        return self._y_velocity
    
    @property
    def y_direction(self):
        return self._y_direction

    @property
    def rank(self):
        return self._rank
    
    @property
    def image(self):
        return self._image
    
    @property
    def ran_point(self):
        return self._ran_point

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def assets(self):
        return self._assets


    def random_spawn_location(self, width, height):
        self._ran_point = random.choice([(random.randrange(0, width + self.width), 
                                          random.choice([-self.height - 50, height + 5])),
                                          (random.choice([-self.width - 50, width + 5]),
                                           random.randrange(0, height + self.height))])
        self._x, self._y = self.ran_point

    def set_velocity(self, width, height):      
        if self.x < width // 2:
            self._x_direction = 1
        else:
            self._x_direction = -1
        if self.y < height // 2:
            self._y_direction = 1
        else:
            self._y_direction = -1
        self._x_velocity = self.x_direction * random.randrange(1, 3)
        self._y_velocity = self.y_direction * random.randrange(1, 3)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def draw(self, win):
        super().draw(win)
        win.blit(self.image, (self.x, self.y))

    def check_off_screen(self, width, height):
        if (self.x < -50 or self.x > width or 
            self.y > height or self.y < -50):
            return True
        return False


class BigAsteroid(Asteroid):

    def __init__(self):
        super().__init__()
        self._rank = 3
        self._image = self.assets.big_asteroid_img
        self._width = 150
        self._height = 150


class MediumAsteroid(Asteroid):
    
    def __init__(self):
        super().__init__()
        self._rank = 2
        self._image = self.assets.medium_asteroid_img
        self._width = 100
        self._height = 100


class SmallAsteroid(Asteroid):
    
    def __init__(self):
        super().__init__()
        self._rank = 1
        self._image = self.assets.small_asteroid_img
        self._width = 50
        self._height = 50


class AsteroidFactory:
    
    @staticmethod
    def create_asteroid(rank):
        if rank == 3:
            return BigAsteroid()
        elif rank == 2:
            return MediumAsteroid()
        elif rank == 1:
            return SmallAsteroid()
