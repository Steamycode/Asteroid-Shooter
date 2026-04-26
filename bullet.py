import pygame
from assets import AssetManager
from game_object import GameObject


class Bullet(GameObject):
    
    def __init__(self, x, y, cos, sin):
        self._x = x
        self._y = y
        self._width = 4
        self._height = 4
        self._cos = cos
        self._sin = sin
        self._x_velocity = self._cos * 10
        self._y_velocity = self._sin * 10
        self._assets = AssetManager()

    def move(self):
        self._x += self._x_velocity
        self._y -= self._y_velocity

    def draw(self, win):
        super().draw(win)
        pygame.draw.rect(win, (255, 255, 255), [self._x, self._y, self._width, self._height])

    def check_off_screen(self):
        if (self._x < -50 or self._x > self._assets._screen_width or 
            self._y > self._assets._screen_height or self._y < -50):
            return True
        return False
