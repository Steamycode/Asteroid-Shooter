import pygame
from scripts.assets import AssetManager
from scripts.game_object import GameObject


class Bullet(GameObject):
    
    def __init__(self, x, y, cos, sin):
        self._x = x
        self._y = y
        self._width = 4
        self._height = 4
        self._cos = cos
        self._sin = sin
        self._x_velocity = self.cos * 10
        self._y_velocity = self.sin * 10
        self._assets = AssetManager()

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def cos(self):
        return self._cos
    
    @property
    def sin(self):
        return self._sin
    
    @property
    def x_velocity(self):
        return self._x_velocity
    
    @property
    def y_velocity(self):
        return self._y_velocity
    
    @property
    def assets(self):
        return self._assets
    

    def move(self):
        self.x += self.x_velocity
        self.y -= self.y_velocity

    def draw(self, win):
        super().draw(win)
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.width, self.height])

    def check_off_screen(self):
        if (self.x < -50 or self.x > self.assets.screen_width or 
            self.y > self.assets.screen_height or self.y < -50):
            return True
        return False
